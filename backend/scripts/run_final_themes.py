import os
import sys
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.cluster import ThemeClusterer
from ai.theme_generator import ThemeSynthesizer


def run_final_themes():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    canonical_path = os.path.join(base_dir, "output", "analysis_records.json")

    if not os.path.exists(canonical_path):
        print(f"Error: Could not find canonical records at {canonical_path}")
        return

    with open(canonical_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    valid_records = [
        r
        for r in records
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
    ]
    total_analyzed = len(valid_records)
    print(f"Loaded {total_analyzed} successfully analyzed records.")

    if total_analyzed == 0:
        return

    # 1. Cluster Records
    clusterer = ThemeClusterer()
    clusters = clusterer.cluster_records(valid_records)
    print(f"Generated {len(clusters)} clusters.")

    # 2. Synthesize Themes
    synthesizer = ThemeSynthesizer()
    final_themes_data = []

    # Dictionary to keep track of record_id -> assigned_theme_name
    record_theme_map = {}

    for i, cluster in enumerate(clusters):
        print(
            f"Synthesizing Theme {i+1}/{len(clusters)} (Cluster Size: {len(cluster)})"
        )
        try:
            # The ThemeSynthesizer returns dictionary with theme_name, description, etc.
            theme_info = synthesizer.synthesize_cluster(cluster)
            theme_name = theme_info.get("theme_name", "INSUFFICIENT_EVIDENCE")

            # Map every record in this cluster to the synthesized theme name
            for r in cluster:
                record_theme_map[r["record_id"]] = theme_name

            if theme_name != "INSUFFICIENT_EVIDENCE":
                final_themes_data.append(
                    {
                        "theme_name": theme_name,
                        "description": theme_info.get("description", ""),
                        "records": cluster,
                    }
                )

            time.sleep(15)  # Rate limit protection for Gemini API
        except Exception as e:
            print(f"Failed to synthesize theme for cluster {i+1}: {e}")
            for r in cluster:
                record_theme_map[r["record_id"]] = "INSUFFICIENT_EVIDENCE"

    # 3. Merge semantically duplicate themes (exact string match after synthesis)
    merged_themes = {}

    for td in final_themes_data:
        t_name = td["theme_name"]
        if t_name not in merged_themes:
            merged_themes[t_name] = {
                "theme_name": t_name,
                "description": td["description"],
                "records": [],
            }
        # Consolidate records
        merged_themes[t_name]["records"].extend(td["records"])

    final_calculated_themes = []

    # 4. Calculate rigorous metrics for each merged theme
    for t_name, data in merged_themes.items():
        records_in_theme = data["records"]

        # Deduplicate records by record_id just in case
        unique_records = {}
        for r in records_in_theme:
            unique_records[r["record_id"]] = r
        unique_records = list(unique_records.values())

        unique_record_count = len(unique_records)

        if unique_record_count < 2:
            # Ensure sufficient evidence
            for r in unique_records:
                record_theme_map[r["record_id"]] = "INSUFFICIENT_EVIDENCE"
            continue

        percentage = (
            round((unique_record_count / total_analyzed) * 100, 1)
            if total_analyzed > 0
            else 0.0
        )

        google_play_count = sum(
            1 for r in unique_records if r.get("source") == "GOOGLE_PLAY"
        )
        youtube_count = sum(1 for r in unique_records if r.get("source") == "YOUTUBE")

        sources_present = set(
            r.get("source") for r in unique_records if r.get("source")
        )
        source_coverage = len(sources_present)

        if unique_record_count > 10:
            conf = "strong"
        elif unique_record_count > 5:
            conf = "moderate"
        else:
            conf = "weak"

        representative_quotes = []
        for r in unique_records[:5]:  # Take up to 5 quotes
            quote = r.get("text", r.get("normalized_text", ""))
            if quote:
                representative_quotes.append(
                    {
                        "quote": quote,
                        "source": r.get("source", "UNKNOWN"),
                        "trace_id": r.get("record_id", "Unknown"),
                        "date": r.get("date", "Unknown"),
                    }
                )

        # Remap for the frontend
        source_distribution = {}
        if google_play_count > 0:
            source_distribution["GOOGLE_PLAY"] = google_play_count
        if youtube_count > 0:
            source_distribution["YOUTUBE"] = youtube_count

        final_calculated_themes.append(
            {
                "theme_name": t_name,
                "description": data["description"],
                "unique_record_count": unique_record_count,
                "frequency": unique_record_count,  # Alias for backwards compatibility
                "percentage_of_analyzed_records": percentage,
                "google_play_count": google_play_count,
                "youtube_count": youtube_count,
                "source_coverage": source_coverage,
                "source_distribution": source_distribution,
                "evidence_confidence": conf,
                "representative_quotes": representative_quotes,
                "supporting_evidence": representative_quotes,  # Alias for backward compatibility
            }
        )

    # Sort by frequency
    final_calculated_themes.sort(key=lambda x: x["unique_record_count"], reverse=True)

    # 5. Update analysis_records.json with the new fully traced themes
    for r in records:
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]:
            # Default to original if somehow missed
            new_theme = record_theme_map.get(r["record_id"], "INSUFFICIENT_EVIDENCE")
            r["theme"] = new_theme

    with open(canonical_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Updated {canonical_path} with final theme assignments.")

    # 6. Save deterministic themes output
    output_themes_path = os.path.join(base_dir, "output", "themes.json")
    with open(output_themes_path, "w", encoding="utf-8") as f:
        json.dump(final_calculated_themes, f, indent=2, ensure_ascii=False)
    print(
        f"Saved {len(final_calculated_themes)} final deterministic themes to {output_themes_path}."
    )


if __name__ == "__main__":
    run_final_themes()
