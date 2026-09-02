import os
import json
from collections import defaultdict
import sys


def aggregate_all():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    canonical_path = os.path.join(base_dir, "output", "analysis_records.json")

    if not os.path.exists(canonical_path):
        print(f"Error: Could not find canonical records at {canonical_path}")
        return

    with open(canonical_path, "r", encoding="utf-8") as f:
        canonical_list = json.load(f)

    print(f"Loaded {len(canonical_list)} canonical records.")

    # 1. Deterministic Theme Aggregation (no LLM, purely by exact match after filtering)
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
        # As per rules, if it survives the filter, it is a valid theme.
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

    output_dir = os.path.join(base_dir, "data", "analyzed")
    os.makedirs(output_dir, exist_ok=True)

    themes_path = os.path.join(output_dir, "themes.json")
    with open(themes_path, "w", encoding="utf-8") as f:
        json.dump(final_themes, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(final_themes)} themes to {themes_path}")

    # 2. Trigger downstream analytics (Journey: Wishlist, Barriers, External Research, Segments, Opportunities)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from scripts.run_phase5 import run_phase5
    from scripts.run_phase6 import run_phase6

    print("\n--- Running Deterministic Aggregation for Journey Analytics ---")
    run_phase5()

    print("\n--- Running Deterministic Aggregation for Opportunities ---")
    run_phase6()


if __name__ == "__main__":
    aggregate_all()
