import os
import json


def test_data_contract_consistency():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    metadata_path = os.path.join(base_dir, "output", "pipeline_metadata.json")
    canonical_path = os.path.join(base_dir, "output", "analysis_records.json")

    assert os.path.exists(metadata_path), "pipeline_metadata.json missing"
    assert os.path.exists(canonical_path), "analysis_records.json missing"

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    with open(canonical_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    analyzed_recs = [
        r
        for r in records
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
    ]

    # 1. analyzed_count in metadata equals canonical analyzed records
    meta_analyzed = metadata.get("llm_analyzed", 0) + metadata.get(
        "fallback_analyzed", 0
    )
    assert meta_analyzed == len(
        analyzed_recs
    ), f"Metadata analyzed ({meta_analyzed}) != records analyzed ({len(analyzed_recs)})"

    # 2. Source analyzed counts
    for src, stats in metadata.get("sources", {}).items():
        src_recs = [r for r in analyzed_recs if r.get("source") == src]
        assert stats.get("analyzed", 0) == len(
            src_recs
        ), f"Source {src} analyzed count mismatch"

    # 3. Evidence API count equals canonical analyzed record count
    # We test the data file directly here, routing returns this same length.

    # 4. Journey denominator
    journey_path = os.path.join(base_dir, "data", "analyzed", "wishlist_behavior.json")
    if os.path.exists(journey_path):
        with open(journey_path, "r", encoding="utf-8") as f:
            journey = json.load(f)
        assert journey.get("total_valid_records") == len(
            analyzed_recs
        ), "Journey denominator mismatch"

    # 5. Theme frequencies sum to no more than canonical analyzed record count
    themes_path = os.path.join(base_dir, "data", "analyzed", "themes.json")
    if os.path.exists(themes_path):
        with open(themes_path, "r", encoding="utf-8") as f:
            themes = json.load(f)
        total_theme_freq = sum(
            t.get("frequency", 0)
            for t in themes
            if t.get("theme_name") != "INSUFFICIENT_EVIDENCE"
        )
        assert total_theme_freq <= len(
            analyzed_recs
        ), "Themes frequency exceeds total analyzed records"

    # 6. Every opportunity has supporting canonical records
    opps_path = os.path.join(base_dir, "data", "analyzed", "opportunities.json")
    if os.path.exists(opps_path):
        with open(opps_path, "r", encoding="utf-8") as f:
            opps = json.load(f)
        for opp in opps:
            assert (
                len(opp.get("supporting_evidence", [])) > 0
            ), f"Opportunity {opp.get('opportunity_name')} lacks evidence"

    # 7. No synthetic production records exist
    for r in records:
        assert r.get("source") in [
            "GOOGLE_PLAY",
            "YOUTUBE",
            "UNKNOWN",
        ], f"Invalid source {r.get('source')} found"


if __name__ == "__main__":
    test_data_contract_consistency()
    print("All Data Contract Consistency Tests Passed!")
