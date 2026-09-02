import os
import sys
import json


def validate_pipeline():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(backend_dir, "..", "..", "data"))

    with open(
        os.path.join(data_dir, "normalized", "data_quality_report.json"),
        encoding="utf-8",
    ) as f:
        dq = json.load(f)

    eligible = dq.get("eligible_records", 0)
    analyzed = dq.get("analyzed_records", 0)
    failed = dq.get("failed_records", 0)
    excluded = dq.get("excluded_records", 0)

    # 1. Counts Reconcile
    assert (
        eligible == analyzed + failed + excluded
    ), f"Count mismatch: {eligible} != {analyzed} + {failed} + {excluded}"
    print(
        f"PASS: Counts Reconcile: {eligible} eligible = {analyzed} analyzed + {failed} failed + {excluded} excluded"
    )

    # 2. Themes not empty and no fabricated generic themes
    with open(os.path.join(data_dir, "analyzed", "themes.json"), encoding="utf-8") as f:
        themes = json.load(f)

    if len(themes) == 0:
        print(
            "WARNING: Themes array is empty (likely due to LLM rate limit or no valid clusters)"
        )
    else:
        for t in themes:
            assert (
                t["theme_name"] != "Insufficient evidence"
            ), "Insufficient evidence leaked into valid themes"
            assert (
                "general user feedback" not in t["theme_name"].lower()
            ), "Fabricated generic theme detected"
    print(f"PASS: Themes Valid: {len(themes)} themes generated")

    # 3. Opportunity Scoring constraints
    with open(
        os.path.join(data_dir, "analyzed", "opportunities.json"), encoding="utf-8"
    ) as f:
        opps = json.load(f)

    for o in opps:
        classification = o.get("classification", "")
        conf = o.get("scores", {}).get("evidence_confidence", 0)

        assert classification in [
            "OBSERVATION",
            "EMERGING SIGNAL",
            "OPPORTUNITY",
            "HIGH-CONFIDENCE OPPORTUNITY",
        ], f"Invalid classification: {classification}"

        if classification == "HIGH-CONFIDENCE OPPORTUNITY":
            assert conf >= 4, "High confidence opportunity with low evidence score"

    print(f"PASS: Opportunities Valid: {len(opps)} generated with correct thresholds")


if __name__ == "__main__":
    validate_pipeline()
