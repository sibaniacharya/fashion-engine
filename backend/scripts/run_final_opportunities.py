import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ai.opportunity_scorer import OpportunityScorer


def run_final_opportunities():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # Load canonical deterministic files
    themes_path = os.path.join(base_dir, "output", "themes.json")
    barriers_path = os.path.join(base_dir, "output", "barriers.json")
    segments_path = os.path.join(base_dir, "output", "behavioral_segments.json")

    themes = []
    if os.path.exists(themes_path):
        with open(themes_path, "r", encoding="utf-8") as f:
            themes = json.load(f)

    barriers = {}
    if os.path.exists(barriers_path):
        with open(barriers_path, "r", encoding="utf-8") as f:
            barriers = json.load(f)

    segments = {}
    if os.path.exists(segments_path):
        with open(segments_path, "r", encoding="utf-8") as f:
            segments = json.load(f)

    scorer = OpportunityScorer(themes, barriers, segments)
    opportunities = scorer.generate_opportunities()

    output_path = os.path.join(base_dir, "output", "opportunities.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(opportunities, f, indent=2, ensure_ascii=False)

    print(
        f"Successfully generated {len(opportunities)} opportunities and saved to {output_path}."
    )

    # Quick Summary Report
    high = sum(
        1 for o in opportunities if o["classification"] == "HIGH_CONFIDENCE_OPPORTUNITY"
    )
    opps = sum(1 for o in opportunities if o["classification"] == "OPPORTUNITY")
    emerge = sum(1 for o in opportunities if o["classification"] == "EMERGING_SIGNAL")
    signals = sum(1 for o in opportunities if o["classification"] == "SIGNAL")

    cross = sum(1 for o in opportunities if o.get("source_coverage", 1) > 1)
    single = sum(1 for o in opportunities if o.get("source_coverage", 1) == 1)

    print(f"\nHIGH CONFIDENCE: {high}")
    print(f"OPPORTUNITIES: {opps}")
    print(f"EMERGING SIGNALS: {emerge}")
    print(f"SIGNALS: {signals}")
    print(f"\nCross-source: {cross}")
    print(f"Single-source: {single}")


if __name__ == "__main__":
    run_final_opportunities()
