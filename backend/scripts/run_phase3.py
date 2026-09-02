import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import SessionLocal, engine, Base
from models import ExtractedSignal, NormalizedFeedback
from ai.batch_processor import BatchProcessor


def run_phase3():
    Base.metadata.create_all(bind=engine)

    processor = BatchProcessor()
    metrics = processor.process_all(batch_limit=400)

    db = SessionLocal()
    signals = db.query(ExtractedSignal).all()
    valid_records = (
        db.query(NormalizedFeedback).filter(NormalizedFeedback.is_valid == True).all()
    )
    unique_valid_records = {r.raw_id: r for r in valid_records}.values()
    eligible_count = len(unique_valid_records)

    processed_raw_ids = set()
    output_list = []

    for s in signals:
        processed_raw_ids.add(s.raw_id)
        norm = (
            db.query(NormalizedFeedback)
            .filter(NormalizedFeedback.raw_id == s.raw_id)
            .first()
        )

        status = s.signals.get("status", "SUCCESS")

        analysis_status = status
        if status not in [
            "FAILED",
            "DEFERRED_QUOTA",
            "DEFERRED_RATE_LIMIT",
            "ANALYZED_FALLBACK",
        ]:
            analysis_status = "ANALYZED"

        output_list.append(
            {
                "signal_id": s.id,
                "raw_id": s.raw_id,
                "source": norm.source if norm else None,
                "source_id": norm.source_id if norm else None,
                "date": norm.date.isoformat() if norm and norm.date else None,
                "normalized_text": norm.normalized_text if norm else None,
                "extracted_signals": s.signals,
                "processed_at": s.processed_at.isoformat() if s.processed_at else None,
                "analysis_status": analysis_status,
                "model_used": "gemini"
                if analysis_status == "ANALYZED"
                else (
                    s.signals.get("model_used")
                    if analysis_status == "ANALYZED_FALLBACK"
                    else None
                ),
            }
        )

    # Actually, unprocessed records are now caught in batch_processor and tagged DEFERRED.
    # But just in case any fell through the cracks (e.g. killed process), tag them DEFERRED_RATE_LIMIT
    for norm in unique_valid_records:
        if norm.raw_id not in processed_raw_ids:
            output_list.append(
                {
                    "signal_id": f"unprocessed-{norm.raw_id}",
                    "raw_id": norm.raw_id,
                    "source": norm.source,
                    "source_id": norm.source_id,
                    "date": norm.date.isoformat() if norm.date else None,
                    "normalized_text": norm.normalized_text,
                    "extracted_signals": {
                        "status": "DEFERRED_RATE_LIMIT",
                        "error": "Unprocessed due to process crash or early exit",
                    },
                    "processed_at": None,
                    "analysis_status": "DEFERRED_RATE_LIMIT",
                    "model_used": None,
                }
            )

    db.close()

    output_dir_canonical = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "output")
    )
    os.makedirs(output_dir_canonical, exist_ok=True)

    # Export canonical
    canonical_list = []
    failed_count = 0
    fallback_count = 0
    llm_count = 0

    deferred_rate_limit = 0
    deferred_quota = 0

    for r in output_list:
        status = r.get("analysis_status")
        ext = r.get("extracted_signals", {})

        canonical_record = {
            "record_id": r.get("raw_id"),
            "source": r.get("source"),
            "text": r.get("normalized_text"),
            "date": r.get("date"),
            "analysis_status": status,
            "model_used": ext.get("model_used", r.get("model_used")),
            "theme": ext.get("theme_candidate", "UNKNOWN"),
            "wishlist_intent": ext.get("wishlist_intent", "Unknown"),
            "purchase_intent": ext.get("shopping_intent", "UNKNOWN"),
            "purchase_stage": ext.get("purchase_stage", "Unknown"),
            "purchase_barrier": ext.get("purchase_barrier", "UNKNOWN"),
            "information_seeking": ext.get("external_research_behavior", "Unknown"),
            "user_segment": ext.get("user_segment", "Segment unknown"),
            "evidence_strength": ext.get("evidence_strength", "unknown"),
        }

        if status == "ANALYZED_FALLBACK":
            fallback_count += 1
        elif status == "FAILED":
            failed_count += 1
        elif status == "DEFERRED_RATE_LIMIT":
            deferred_rate_limit += 1
        elif status == "DEFERRED_QUOTA":
            deferred_quota += 1
        else:
            llm_count += 1

        canonical_list.append(canonical_record)

    canonical_path = os.path.join(output_dir_canonical, "analysis_records.json")
    with open(canonical_path, "w", encoding="utf-8") as f:
        json.dump(canonical_list, f, indent=2, ensure_ascii=False)

    def source_stats(source_name):
        src_valid = [r for r in unique_valid_records if r.source == source_name]
        src_raw_ids = {r.raw_id for r in src_valid}
        src_recs = [r for r in output_list if r.get("raw_id") in src_raw_ids]

        return {
            "raw": len(
                src_valid
            ),  # assuming raw roughly equals valid here for simplicity, or we can just use valid count
            "eligible": len(src_valid),
            "analyzed": len(
                [
                    r
                    for r in src_recs
                    if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
                ]
            ),
            "failed": len(
                [r for r in src_recs if r.get("analysis_status") == "FAILED"]
            ),
            "deferred": len(
                [
                    r
                    for r in src_recs
                    if r.get("analysis_status")
                    in ["DEFERRED_RATE_LIMIT", "DEFERRED_QUOTA"]
                ]
            ),
        }

    # Query true raw records if available, otherwise fallback to len of signals + unanalyzed?
    # Actually, we can get raw records from NormalizedFeedback if we don't filter by is_valid.
    total_raw = db.query(NormalizedFeedback).count()
    total_valid = len(unique_valid_records)

    data_quality_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "normalized",
            "data_quality_report.json",
        )
    )
    exclusions = {"duplicates": 0, "spam": 0, "other": 0}
    if os.path.exists(data_quality_path):
        with open(data_quality_path, "r", encoding="utf-8") as f:
            try:
                dq = json.load(f)
                exclusions["duplicates"] = dq.get("duplicates_dropped", 0)
                exclusions["spam"] = dq.get("dropped_by_reason", {}).get(
                    "Meaningless content", 0
                )
                # raw_records inside data_quality_report is total_processed
                raw = dq.get("total_processed", total_raw)
                exclusions["other"] = (
                    raw - total_valid - exclusions["duplicates"] - exclusions["spam"]
                )
            except Exception:
                pass

    pipeline_metadata = {
        "raw_records": total_raw,
        "valid_records": total_valid,
        "eligible_records": eligible_count,
        "llm_analyzed": llm_count,
        "fallback_analyzed": fallback_count,
        "failed": failed_count,
        "deferred_rate_limit": deferred_rate_limit,
        "deferred_quota": deferred_quota,
        "exclusion_breakdown": exclusions,
        "sources": {
            "GOOGLE_PLAY": source_stats("GOOGLE_PLAY"),
            "YOUTUBE": source_stats("YOUTUBE"),
        },
    }

    metadata_path = os.path.join(output_dir_canonical, "pipeline_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(pipeline_metadata, f, indent=2, ensure_ascii=False)

    # Generate failure-reason report
    failures = [r for r in output_list if r.get("analysis_status") == "FAILED"]
    failure_reasons = []
    for f_rec in failures:
        failure_reasons.append(
            {
                "record_id": f_rec.get("raw_id"),
                "source": f_rec.get("source"),
                "error": f_rec.get("extracted_signals", {}).get(
                    "error", "Unknown processing failure"
                ),
            }
        )
    with open(
        os.path.join(output_dir_canonical, "failed_reasons.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(failure_reasons, f, indent=2, ensure_ascii=False)

    # Automated Assertions
    assert (
        eligible_count
        == llm_count
        + fallback_count
        + failed_count
        + deferred_rate_limit
        + deferred_quota
    ), f"Counts do not reconcile! Eligible: {eligible_count}, LLM: {llm_count}, Fallback: {fallback_count}, Failed: {failed_count}, Deferred RL: {deferred_rate_limit}, Deferred Quota: {deferred_quota}"

    for r in canonical_list:
        assert r.get("record_id"), "Missing record_id"
        assert r.get("source"), "Missing source"
        assert r.get("analysis_status"), "Missing analysis_status"
        if r.get("analysis_status") == "ANALYZED":
            assert r.get("theme"), "Missing theme in analyzed record"
            assert r.get(
                "wishlist_intent"
            ), "Missing wishlist_intent in analyzed record"
            assert r.get("purchase_stage"), "Missing purchase_stage in analyzed record"

    print(f"\n--- Phase 3 Execution Report ---")
    print(f"Total Eligible Input: {eligible_count}")
    print(f"Total Output Records: {len(canonical_list)}")
    print(f"LLM Analyzed: {llm_count}")
    print(f"Fallback Analyzed: {fallback_count}")
    print(f"Failed: {failed_count}")
    print(f"Deferred (Rate Limit): {deferred_rate_limit}")
    print(f"Deferred (Quota): {deferred_quota}")
    print(f"Failed in this batch: {metrics['failed']}")
    print(f"Retry Count: {metrics['retry_count']}")
    print(f"Rate-limit Events: {metrics['rate_limit_events']}")
    print(f"Canonical Analysis saved to: {canonical_path}")


if __name__ == "__main__":
    run_phase3()
