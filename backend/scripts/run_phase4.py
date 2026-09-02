import os
import sys
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.cluster import ThemeClusterer
from ai.theme_generator import ThemeSynthesizer


def run_phase4():
    # Load Canonical Analysis Records
    input_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "output", "analysis_records.json"
        )
    )

    if not os.path.exists(input_path):
        print(f"Error: Could not find canonical records at {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not records:
        print("Error: analysis_records file is empty.")
        return

    valid_records = [
        r
        for r in records
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
    ]

    print(f"Loaded {len(records)} records for Theme Discovery.")

    # 1. Cluster Records
    clusterer = ThemeClusterer()
    clusters = clusterer.cluster_records(valid_records)
    print(f"Generated {len(clusters)} clusters.")

    # 2. Synthesize Themes
    synthesizer = ThemeSynthesizer()
    final_themes = []

    for i, cluster in enumerate(clusters):
        print(
            f"Synthesizing Theme {i+1}/{len(clusters)} (Cluster Size: {len(cluster)})"
        )
        try:
            theme = synthesizer.synthesize_cluster(cluster)
            final_themes.append(theme)
            time.sleep(15)  # Respect rate limits (15s for 5 RPM limit)
        except Exception as e:
            print(f"Failed to synthesize theme for cluster {i+1}: {e}")

    # Consolidate duplicate themes
    consolidated = {}
    for t in final_themes:
        name = t["theme_name"]
        if name == "INSUFFICIENT_EVIDENCE":
            continue

        if name not in consolidated:
            consolidated[name] = t
        else:
            # Merge
            consolidated[name]["frequency"] += t["frequency"]
            consolidated[name]["unique_records"] += t["unique_records"]

            for src, count in t["source_distribution"].items():
                consolidated[name]["source_distribution"][src] = (
                    consolidated[name]["source_distribution"].get(src, 0) + count
                )

            consolidated[name]["supporting_evidence"].extend(t["supporting_evidence"])

            # Recalculate confidence
            unique = consolidated[name]["unique_records"]
            if unique > 10:
                conf = "strong"
            elif unique > 5:
                conf = "moderate"
            elif unique > 2:
                conf = "weak"
            else:
                conf = "unknown"
            consolidated[name]["evidence_confidence"] = conf

    final_merged = list(consolidated.values())
    final_merged.sort(key=lambda x: x["frequency"], reverse=True)

    # Max 8 themes
    final_merged = final_merged[:8]

    # 3. Export
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "analyzed")
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "themes.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_merged, f, indent=2, ensure_ascii=False)

    print(f"\n--- Phase 4 Complete ---")
    print(f"Discovered {len(final_merged)} canonical themes.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    run_phase4()
