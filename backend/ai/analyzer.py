import json
from collections import defaultdict

BARRIER_SEMANTIC_MAP = {
    "expensive pricing": "Price / Value Uncertainty",
    "full price is a rip off": "Price / Value Uncertainty",
    "too expensive": "Price / Value Uncertainty",
    "expensive": "Price / Value Uncertainty",
    "rip off": "Price / Value Uncertainty",
    "too much": "Price / Value Uncertainty",
    "high price": "Price / Value Uncertainty",
    "pricey": "Price / Value Uncertainty",
    "delivery": "Shipping Cost Blockers",
    "shipping": "Shipping Cost Blockers",
    "fee": "Shipping Cost Blockers",
    "bug": "App Performance / UX Issues",
    "crash": "App Performance / UX Issues",
    "slow": "App Performance / UX Issues",
    "size": "Fit / Size Uncertainty",
    "fit": "Fit / Size Uncertainty",
}


def map_barrier(b: str) -> str:
    if not b:
        return "Unknown"
    b_lower = b.lower()
    for key, val in BARRIER_SEMANTIC_MAP.items():
        if key in b_lower:
            return val
    # If no map, capitalize first letter
    return b.capitalize()


class BehaviorAnalyzer:
    def __init__(self, signals: list[dict]):
        self.raw_signals = signals
        self.signals = [s for s in signals if s.get("analysis_status") != "FAILED"]

    def _extract_base_metrics(self, record: dict) -> dict:
        return {
            "source": record.get("source", "UNKNOWN"),
            "segment": record.get("user_segment")
            if record.get("user_segment")
            and record.get("user_segment").upper() not in ["UNKNOWN", ""]
            else "Segment unknown",
            "theme": record.get("theme")
            if record.get("theme")
            and record.get("theme").upper() not in ["UNKNOWN", ""]
            else "UNKNOWN",
        }

    def analyze_wishlist_behavior(self) -> dict:
        analysis = {
            "total_valid_records": len(self.signals),
            "total_wishlist_mentions": 0,
            "bookmarking_vs_intent": {
                "EXPLICIT_WISHLIST": 0,
                "EXPLICIT_PURCHASE_INTENT": 0,
                "GENERAL_PRODUCT_INTEREST": 0,
                "PURCHASE_EVALUATION": 0,
                "COMPARISON": 0,
                "POSTPONEMENT": 0,
                "ABANDONMENT": 0,
                "BOOKMARKING": 0,
                "UNKNOWN": 0,
            },
            "postponement_reasons": defaultdict(int),
            "by_source": defaultdict(lambda: {"total": 0, "intents": []}),
            "by_segment": defaultdict(lambda: {"total": 0, "intents": []}),
            "by_theme": defaultdict(lambda: {"total": 0, "intents": []}),
        }

        for r in self.signals:
            wish_intent = r.get("wishlist_intent", "UNKNOWN")

            # Post-process to prevent LLM from forcing intents on generic feedback/complaints
            if wish_intent and wish_intent.upper() in [
                "ABANDONMENT",
                "GENERAL_PRODUCT_INTEREST",
            ]:
                theme = r.get("theme", "")
                text_lower = r.get("text", "").lower()
                complaint_themes = [
                    "Return and Refund Friction",
                    "App Performance / UX Issues",
                    "Delivery / Shipping Friction",
                    "Returns / Exchange Friction",
                    "INSUFFICIENT_EVIDENCE",
                ]
                intent_keywords = [
                    "wishlist",
                    "cart",
                    "buy",
                    "purchas",
                    "order",
                    "save",
                    "later",
                    "compar",
                    "decid",
                    "look",
                    "want",
                ]

                if theme in complaint_themes and not any(
                    kw in text_lower for kw in intent_keywords
                ):
                    wish_intent = "UNKNOWN"

            if wish_intent and wish_intent.upper() not in ["NO", "", "UNKNOWN", "NONE"]:
                cat = "UNKNOWN"
                w_upper = wish_intent.upper()
                if "WISHLIST" in w_upper:
                    cat = "EXPLICIT_WISHLIST"
                elif "PURCHASE" in w_upper and "INTENT" in w_upper:
                    cat = "EXPLICIT_PURCHASE_INTENT"
                elif "GENERAL" in w_upper:
                    cat = "GENERAL_PRODUCT_INTEREST"
                elif "EVALUATION" in w_upper:
                    cat = "PURCHASE_EVALUATION"
                elif "COMPARISON" in w_upper:
                    cat = "COMPARISON"
                elif "POSTPONEMENT" in w_upper:
                    cat = "POSTPONEMENT"
                elif "ABANDONMENT" in w_upper:
                    cat = "ABANDONMENT"
                elif "BOOKMARKING" in w_upper:
                    cat = "BOOKMARKING"
                else:
                    for key in analysis["bookmarking_vs_intent"].keys():
                        if key.upper() == w_upper:
                            cat = key
                            break

                analysis["bookmarking_vs_intent"][cat] += 1
                if cat != "UNKNOWN":
                    analysis["total_wishlist_mentions"] += 1
            else:
                analysis["bookmarking_vs_intent"]["UNKNOWN"] += 1

                base = self._extract_base_metrics(r)

                # Postponement
                if (
                    r.get("purchase_stage") == "Postponement"
                    and r.get("purchase_barrier")
                    and r.get("purchase_barrier") != "UNKNOWN"
                ):
                    analysis["postponement_reasons"][r.get("purchase_barrier")] += 1

                # Distribute
                analysis["by_source"][base["source"]]["total"] += 1
                analysis["by_source"][base["source"]]["intents"].append(wish_intent)

                analysis["by_segment"][base["segment"]]["total"] += 1
                analysis["by_theme"][base["theme"]]["total"] += 1

        return analysis

    def analyze_purchase_barriers(self) -> dict:
        import os

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        barriers_path = os.path.join(base_dir, "output", "barriers.json")

        analysis = {
            "total_barriers_identified": 0,
            "top_barriers": {},
            "top_uncertainties": defaultdict(int),
            "by_source": defaultdict(lambda: {"total": 0, "barriers": []}),
            "by_segment": defaultdict(lambda: {"total": 0, "barriers": []}),
            "by_theme": defaultdict(lambda: {"total": 0, "barriers": []}),
            "correlation_with_comparison": 0,
        }

        if os.path.exists(barriers_path):
            with open(barriers_path, "r", encoding="utf-8") as f:
                analysis["top_barriers"] = json.load(f)
                analysis["total_barriers_identified"] = len(analysis["top_barriers"])

        # Populate the rest of the metadata based on the static barrier records if needed,
        # but the top_barriers already contains the exhaustive metrics required by the dashboard.
        for r in self.signals:
            base = self._extract_base_metrics(r)
            mapped_barrier = r.get("purchase_barrier", "UNKNOWN")

            if mapped_barrier and mapped_barrier.upper() not in [
                "UNKNOWN",
                "NO",
                "NONE",
            ]:
                analysis["by_source"][base["source"]]["total"] += 1
                analysis["by_source"][base["source"]]["barriers"].append(mapped_barrier)

                analysis["by_segment"][base["segment"]]["total"] += 1
                analysis["by_theme"][base["theme"]]["total"] += 1

        return analysis

    def analyze_external_research(self) -> dict:
        analysis = {
            "total_external_research_events": 0,
            "research_types": {
                "Explicit external research": 0,
                "Implied external research": 0,
                "No evidence": 0,
                "Unknown": 0,
            },
            "information_sought": defaultdict(int),
            "alternatives_considered": [],
            "by_source": defaultdict(int),
            "by_segment": defaultdict(int),
            "by_theme": defaultdict(int),
        }

        for r in self.signals:
            research = r.get("information_seeking", "Unknown")
            info = "UNKNOWN"
            comp = "NO"

            cat = "Unknown"
            if research:
                r_upper = research.upper()
                if "EXPLICIT" in r_upper:
                    cat = "Explicit external research"
                elif "IMPLIED" in r_upper:
                    cat = "Implied external research"
                elif "NO_EVIDENCE" in r_upper or "NO EVIDENCE" in r_upper:
                    cat = "No evidence"
                else:
                    for key in analysis["research_types"].keys():
                        if key.lower() == research.lower():
                            cat = key
                            break

            analysis["research_types"][cat] += 1

            if (
                cat in ["Explicit external research", "Implied external research"]
                or (info and info.upper() != "UNKNOWN")
                or comp == "YES"
            ):
                analysis["total_external_research_events"] += 1

                if info and info.upper() != "UNKNOWN":
                    analysis["information_sought"][info] += 1
                if comp == "YES":
                    analysis["alternatives_considered"].append("Alternative Product")

                base = self._extract_base_metrics(r)
                analysis["by_source"][base["source"]] += 1
                analysis["by_segment"][base["segment"]] += 1
                analysis["by_theme"][base["theme"]] += 1

        return analysis

    def analyze_user_segments(self) -> dict:
        import os

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        segments_path = os.path.join(base_dir, "output", "behavioral_segments.json")

        if os.path.exists(segments_path):
            with open(segments_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Reformat to match the expected legacy dictionary schema for backwards compatibility,
            # while passing through the rich data.
            analysis = {
                "total_records_classified": data.get("total_records_classified", 0),
                "segments": {},
            }

            for seg in data.get("segments", []):
                analysis["segments"][seg["segment_name"]] = {
                    "count": seg["unique_record_count"],
                    "source_distribution": {
                        "GOOGLE_PLAY": seg["google_play_count"],
                        "YOUTUBE": seg["youtube_count"],
                    },
                    "top_themes": seg["dominant_themes"],
                    "top_barriers": seg["purchase_barriers"],
                    "evidence_confidence": seg["evidence_confidence"],
                    "classification": seg["classification"],
                    "percentage": seg["percentage"],
                    "wishlist_behavior": seg["wishlist_behavior"],
                    "postponement_behavior": seg["postponement_behavior"],
                    "external_research": seg["external_research"],
                    "supporting_evidence": seg["supporting_evidence"],
                }

            return analysis

        return {"total_records_classified": 0, "segments": {}}
