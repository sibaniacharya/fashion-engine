import json
import os
import sys

# Validate Data
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
records_file = os.path.join(base_dir, "output", "analysis_records.json")
metadata_file = os.path.join(base_dir, "output", "pipeline_metadata.json")
themes_file = os.path.join(base_dir, "output", "themes.json")
barriers_file = os.path.join(base_dir, "output", "barriers.json")
segments_file = os.path.join(base_dir, "output", "behavioral_segments.json")
opps_file = os.path.join(base_dir, "output", "opportunities.json")

records = json.load(open(records_file, "r", encoding="utf-8"))
metadata = json.load(open(metadata_file, "r", encoding="utf-8"))
themes = json.load(open(themes_file, "r", encoding="utf-8"))
barriers = json.load(open(barriers_file, "r", encoding="utf-8"))
segments = json.load(open(segments_file, "r", encoding="utf-8"))
opps = json.load(open(opps_file, "r", encoding="utf-8"))

# Pipeline
analyzed = [r for r in records if r.get("analysis_status") == "ANALYZED"]
fallback = [r for r in records if r.get("analysis_status") == "ANALYZED_FALLBACK"]
failed = [r for r in records if r.get("analysis_status") == "FAILED"]
deferred_quota = [r for r in records if r.get("analysis_status") == "DEFERRED_QUOTA"]
deferred_rate = [
    r for r in records if r.get("analysis_status") == "DEFERRED_RATE_LIMIT"
]

print(f"ELIGIBLE (meta): {metadata.get('eligible_records')}")
print(f"LLM ANALYZED: {len(analyzed)}")
print(f"FALLBACK ANALYZED: {len(fallback)}")
print(f"FAILED: {len(failed)}")
print(f"DEFERRED QUOTA: {len(deferred_quota)}")
print(f"DEFERRED RATE: {len(deferred_rate)}")

total_eligible_calc = (
    len(analyzed)
    + len(fallback)
    + len(failed)
    + len(deferred_quota)
    + len(deferred_rate)
)
print(f"CALCULATED ELIGIBLE: {total_eligible_calc}")

# Sources
gp = [r for r in records if r.get("source") == "GOOGLE_PLAY"]
yt = [r for r in records if r.get("source") == "YOUTUBE"]

print(
    f"GOOGLE PLAY - analyzed: {len([r for r in gp if r.get('analysis_status') in ['ANALYZED', 'ANALYZED_FALLBACK']])}"
)
print(
    f"YOUTUBE - analyzed: {len([r for r in yt if r.get('analysis_status') in ['ANALYZED', 'ANALYZED_FALLBACK']])}"
)
print(
    f"Synthetic records: {len([r for r in records if r.get('source') == 'SYNTHETIC'])}"
)

# Check themes
print(f"Themes: {len(themes)}")
# Check opportunities
print(f"Opps: {len(opps)}")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ai.analyzer import BehaviorAnalyzer

a = BehaviorAnalyzer(
    [
        r
        for r in records
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
    ]
)
w = a.analyze_wishlist_behavior()
print(json.dumps(w["bookmarking_vs_intent"], indent=2))
r = a.analyze_external_research()
print(json.dumps(r["research_types"], indent=2))
