import time
import json
from datetime import datetime
from database import SessionLocal
from models import NormalizedFeedback, ExtractedSignal
from ai.extractor import SignalExtractor, LLMParseError
from pydantic import ValidationError
from tenacity import RetryError


class BatchProcessor:
    def __init__(self):
        self.extractor = SignalExtractor()

    def _fallback_analysis(self, text: str) -> dict:
        text_lower = text.lower()

        # Deterministic rules
        barrier = "UNKNOWN"
        if any(w in text_lower for w in ["expensive", "price", "cost", "money"]):
            barrier = "Price / Value"
        elif any(
            w in text_lower for w in ["login", "sign in", "account", "password", "otp"]
        ):
            barrier = "Login / Account"
        elif any(
            w in text_lower for w in ["app", "crash", "slow", "bug", "glitch", "load"]
        ):
            barrier = "App Performance"

        wishlist = "UNKNOWN"
        if any(w in text_lower for w in ["wishlist", "saved", "later"]):
            wishlist = "EXPLICIT_WISHLIST"

        segment = "UNKNOWN"
        if barrier == "Price / Value":
            segment = "VALUE_CONSCIOUS"

        return {
            "status": "ANALYZED_FALLBACK",
            "model_used": "FALLBACK",
            "user_segment": segment,
            "shopping_intent": "UNKNOWN",
            "wishlist_intent": wishlist,
            "purchase_stage": "UNKNOWN",
            "pain_point": barrier if barrier != "UNKNOWN" else "UNKNOWN",
            "uncertainty": "UNKNOWN",
            "purchase_barrier": barrier,
            "information_sought": "UNKNOWN",
            "comparison_behavior": "UNKNOWN",
            "fit_size_signal": "UNKNOWN",
            "styling_signal": "UNKNOWN",
            "price_signal": "YES" if barrier == "Price / Value" else "UNKNOWN",
            "quality_signal": "UNKNOWN",
            "social_validation_signal": "UNKNOWN",
            "occasion_signal": "UNKNOWN",
            "external_research_behavior": "UNKNOWN",
            "theme_candidate": "UNKNOWN",
            "evidence_strength": "UNKNOWN",
        }

    def process_all(self, batch_limit: int = 400):
        db = SessionLocal()

        valid_records = (
            db.query(NormalizedFeedback)
            .filter(NormalizedFeedback.is_valid == True)
            .all()
        )

        # Checkpoint: Do not reprocess records that are already successfully analyzed (LLM or FALLBACK)
        all_signals = db.query(ExtractedSignal).all()
        processed_ids = set()
        for s in all_signals:
            status = s.signals.get(
                "status", s.signals.get("analysis_status", "ANALYZED")
            )
            failure_reason = s.signals.get("failure_reason", "")

            if status in ["ANALYZED", "ANALYZED_FALLBACK"]:
                processed_ids.add(s.raw_id)
            elif status == "FAILED" and failure_reason not in [
                "LLM_PARSE_ERROR",
                "SCHEMA_VALIDATION_ERROR",
            ]:
                error_msg = s.signals.get("error", "").lower()
                if failure_reason == "UNKNOWN_ERROR" and (
                    "429" in error_msg or "rate limit" in error_msg
                ):
                    db.delete(s)
                else:
                    processed_ids.add(s.raw_id)
            else:
                db.delete(s)
        db.commit()

        records_to_process = [r for r in valid_records if r.raw_id not in processed_ids]

        # Deduplicate
        unique_records = []
        seen = set()
        for r in records_to_process:
            if r.raw_id not in seen:
                unique_records.append(r)
                seen.add(r.raw_id)

        # Limit
        records_to_process = unique_records[:batch_limit]

        print(f"Total valid records: {len(valid_records)}")
        print(f"Already processed (success): {len(processed_ids)}")
        print(f"Remaining to process in this run: {len(records_to_process)}")

        count = 0
        failed_count = 0

        # Smaller chunks (4) and longer sleep (16s) to respect 8K TPM / 1K RPM limits
        chunk_size = 4
        chunks = [
            records_to_process[i : i + chunk_size]
            for i in range(0, len(records_to_process), chunk_size)
        ]

        for chunk_idx, chunk in enumerate(chunks):
            batch_payload = []
            for r in chunk:
                batch_payload.append(
                    {
                        "record_id": r.raw_id,
                        "source": r.source,
                        "text": r.normalized_text,
                    }
                )

            try:
                # LLM extraction
                results_map = self.extractor.extract_signals_batch(batch_payload)

                # Check for missing records and process
                for r in chunk:
                    if r.raw_id in results_map:
                        analysis = results_map[r.raw_id]
                        analysis["status"] = "ANALYZED"
                        analysis["model_used"] = self.extractor.model
                        extracted = ExtractedSignal(
                            raw_id=r.raw_id,
                            signals=analysis,
                            processed_at=datetime.utcnow(),
                        )
                        db.add(extracted)
                        count += 1
                    else:
                        print(
                            f"Warning: {r.raw_id} missing from LLM response. Retrying individually..."
                        )
                        # Retry individually with LLM
                        try:
                            single_map = self.extractor.extract_signals_batch(
                                [
                                    {
                                        "record_id": r.raw_id,
                                        "source": r.source,
                                        "text": r.normalized_text,
                                    }
                                ]
                            )
                            if r.raw_id in single_map:
                                analysis = single_map[r.raw_id]
                                analysis["status"] = "ANALYZED"
                                analysis["model_used"] = self.extractor.model
                                db.add(
                                    ExtractedSignal(
                                        raw_id=r.raw_id,
                                        signals=analysis,
                                        processed_at=datetime.utcnow(),
                                    )
                                )
                                count += 1
                            else:
                                raise ValueError("Missing again")
                        except Exception as retry_e:
                            if (
                                "429" in str(retry_e)
                                or "rate limit" in str(retry_e).lower()
                            ):
                                raise retry_e
                            print(
                                f"Individual retry failed for {r.raw_id}. Marking as FAILED."
                            )
                            failure_reason = "UNKNOWN_ERROR"
                            if isinstance(retry_e, LLMParseError):
                                failure_reason = "LLM_PARSE_ERROR"
                            elif isinstance(retry_e, ValidationError):
                                failure_reason = "SCHEMA_VALIDATION_ERROR"
                            db.add(
                                ExtractedSignal(
                                    raw_id=r.raw_id,
                                    signals={
                                        "status": "FAILED",
                                        "failure_reason": failure_reason,
                                        "error": str(retry_e),
                                    },
                                    processed_at=datetime.utcnow(),
                                )
                            )
                            failed_count += 1
                db.commit()

                # Token-aware sleep: ~16s per chunk of 4 ensures we don't exceed 8k TPM
                time.sleep(16.0)

            except RetryError as re:
                print(f"Batch {chunk_idx + 1} failed after retries.")
                db.rollback()
                e = re.last_attempt.exception() if re.last_attempt else re
                if "429" in str(e) or "rate limit" in str(e).lower():
                    # Handle rate limit
                    is_daily = "tokens per day" in str(e).lower()
                    status = "DEFERRED_QUOTA" if is_daily else "DEFERRED_RATE_LIMIT"
                    print(f"Rate limit exhausted ({status}). Stopping execution.")

                    # Mark current and remaining records as DEFERRED
                    remaining = sum(
                        [chunks[i] for i in range(chunk_idx, len(chunks))], []
                    )
                    for rem_r in remaining:
                        db.add(
                            ExtractedSignal(
                                raw_id=rem_r.raw_id,
                                signals={"status": status, "error": str(e)},
                                processed_at=datetime.utcnow(),
                            )
                        )
                    db.commit()
                    break
                else:
                    failure_reason = "UNKNOWN_ERROR"
                    if isinstance(e, LLMParseError):
                        failure_reason = "LLM_PARSE_ERROR"
                    elif isinstance(e, ValidationError):
                        failure_reason = "SCHEMA_VALIDATION_ERROR"
                    for r in chunk:
                        db.add(
                            ExtractedSignal(
                                raw_id=r.raw_id,
                                signals={
                                    "status": "FAILED",
                                    "failure_reason": failure_reason,
                                    "error": str(e),
                                },
                                processed_at=datetime.utcnow(),
                            )
                        )
                        failed_count += 1
                    db.commit()
            except Exception as e:
                print(f"Batch {chunk_idx + 1} failed: {e}")
                db.rollback()

                if "429" in str(e) or "rate limit" in str(e).lower():
                    is_daily = "tokens per day" in str(e).lower()
                    status = "DEFERRED_QUOTA" if is_daily else "DEFERRED_RATE_LIMIT"
                    print(f"Rate limit exhausted ({status}). Stopping execution.")
                    remaining = sum(
                        [chunks[i] for i in range(chunk_idx, len(chunks))], []
                    )
                    for rem_r in remaining:
                        db.add(
                            ExtractedSignal(
                                raw_id=rem_r.raw_id,
                                signals={"status": status, "error": str(e)},
                                processed_at=datetime.utcnow(),
                            )
                        )
                    db.commit()
                    break
                else:
                    failure_reason = "UNKNOWN_ERROR"
                    if isinstance(e, LLMParseError):
                        failure_reason = "LLM_PARSE_ERROR"
                    elif isinstance(e, ValidationError):
                        failure_reason = "SCHEMA_VALIDATION_ERROR"
                    for r in chunk:
                        db.add(
                            ExtractedSignal(
                                raw_id=r.raw_id,
                                signals={
                                    "status": "FAILED",
                                    "failure_reason": failure_reason,
                                    "error": str(e),
                                },
                                processed_at=datetime.utcnow(),
                            )
                        )
                        failed_count += 1
                    db.commit()

        db.close()
        print(f"Run complete. LLM: {count}, Failed: {failed_count}.")
        return {
            "processed": count,
            "failed": failed_count,
            "retry_count": self.extractor.retry_count,
            "rate_limit_events": self.extractor.rate_limit_events,
        }
