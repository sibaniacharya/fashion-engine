import os
import json
from collections import defaultdict
import sys


def fix_pipeline():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    signals_path = os.path.join(base_dir, "data", "analyzed", "phase3_signals.json")

    with open(signals_path, "r", encoding="utf-8") as f:
        signals = json.load(f)

    canonical_list = []

    for r in signals:
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
        canonical_list.append(canonical_record)

    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    canonical_path1 = os.path.join(output_dir, "analysis_records.json")
    canonical_path2 = os.path.join(
        base_dir, "data", "analyzed", "analysis_records.json"
    )

    with open(canonical_path1, "w", encoding="utf-8") as f:
        json.dump(canonical_list, f, indent=2, ensure_ascii=False)

    with open(canonical_path2, "w", encoding="utf-8") as f:
        json.dump(canonical_list, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(canonical_list)} records to {canonical_path1}")

    # Generate Themes
    theme_groups = defaultdict(
        lambda: {"count": 0, "sources": defaultdict(int), "evidence": []}
    )

    generic_terms = [
        "general",
        "feedback",
        "positive",
        "satisfaction",
        "experience",
        "praise",
        "appreciation",
        "great",
        "good",
        "awesome",
        "nice",
        "best",
        "unknown",
        "dissatisfaction",
    ]

    for c in canonical_list:
        if c.get("analysis_status") not in ["ANALYZED", "ANALYZED_FALLBACK"]:
            continue

        t = c.get("theme", "")
        if not t:
            continue

        if any(term in t.lower() for term in generic_terms):
            continue

        if t.upper() == "UNKNOWN" or t == "INSUFFICIENT_EVIDENCE":
            continue

        theme_groups[t]["count"] += 1
        theme_groups[t]["sources"][c.get("source", "UNKNOWN")] += 1

        # Collect evidence up to 5
        if len(theme_groups[t]["evidence"]) < 5:
            theme_groups[t]["evidence"].append(
                {
                    "quote": c.get("text", ""),
                    "source": c.get("source", "UNKNOWN"),
                    "trace_id": c.get("record_id", "Unknown"),
                    "date": c.get("date", "Unknown"),
                }
            )

    final_themes = []
    for t_name, data in theme_groups.items():
        # Minimum evidence threshold if needed, but per requirements we just list what we have
        final_themes.append(
            {
                "theme_name": t_name,
                "description": f"User feedback related to {t_name}",
                "frequency": data["count"],
                "source_distribution": dict(data["sources"]),
                "supporting_evidence": data["evidence"],
            }
        )

    final_themes.sort(key=lambda x: x["frequency"], reverse=True)

    themes_path = os.path.join(base_dir, "data", "analyzed", "themes.json")
    with open(themes_path, "w", encoding="utf-8") as f:
        json.dump(final_themes, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(final_themes)} themes to {themes_path}")

    # Trigger deterministic downstream generation for Journey & Opportunities
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from scripts.run_phase5 import run_phase5
    from scripts.run_phase6 import run_phase6

    print("\n--- Running Deterministic Aggregation for Journey Analytics ---")
    run_phase5()

    print("\n--- Running Deterministic Aggregation for Opportunities ---")
    run_phase6()


if __name__ == "__main__":
    fix_pipeline()
