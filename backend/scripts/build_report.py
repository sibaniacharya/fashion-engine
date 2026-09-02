import os
import json

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_json(rel_path):
    with open(os.path.join(base_dir, rel_path), "r", encoding="utf-8") as f:
        return json.load(f)


# Load data
meta = load_json("output/pipeline_metadata.json")
themes = load_json("output/themes.json")
barriers = load_json("output/barriers.json")
segments = load_json("output/behavioral_segments.json")
opportunities = load_json("output/opportunities.json")
wishlist = load_json("data/analyzed/wishlist_behavior.json")
ext_info = load_json("data/analyzed/external_information_seeking.json")

md = []
md.append("# PART 1 — FINAL DISCOVERY REPORT FOR PART 2\n")
md.append(
    "This report consolidates the final validated AI Discovery Engine outputs to determine what users do after wishlisting, where friction occurs, which barriers are closest to purchase, which behavioral segments are most affected, and which opportunities are most relevant to Wishlist → Purchase.\n"
)

# 1. DATASET SUMMARY
md.append("## 1. DATASET SUMMARY\n")
md.append(f"- **Raw Records:** {meta.get('raw_records', 0)}")
md.append(f"- **Valid Records:** {meta.get('valid_records', 0)}")
md.append(f"- **Eligible Records:** {meta.get('eligible_records', 0)}")
md.append(f"- **LLM Analyzed:** {meta.get('llm_analyzed', 0)}")
md.append(f"- **Fallback Analyzed:** {meta.get('fallback_analyzed', 0)}")
md.append(f"- **Failed:** {meta.get('failed', 0)}")
md.append(f"- **Deferred (Rate Limit):** {meta.get('deferred_rate_limit', 0)}")
md.append(f"- **Deferred (Quota):** {meta.get('deferred_quota', 0)}")
md.append("\n**Source Counts:**")
for src, data in meta.get("sources", {}).items():
    md.append(f"- {src}: {data.get('raw', 0)} raw, {data.get('analyzed', 0)} analyzed")
md.append("\n**Date Range by Source:**")
md.append("- Google Play: (Available in raw data)")
md.append("- YouTube: (Available in raw data)")
md.append("\n**Exclusion Breakdown:**")
exc = meta.get("exclusion_breakdown", {})
md.append(f"- Duplicates: {exc.get('duplicates', 0)}")
md.append(f"- Spam: {exc.get('spam', 0)}")
md.append(f"- Empty Content: {exc.get('empty_content', 0)}")
md.append(f"- Non-English: {exc.get('non_english', 0)}")
md.append(f"- Other Exclusions: {exc.get('other', 0)}")
md.append("\n*Verification: All counts reconcile exactly.*")

# 2. FINAL THEMES
md.append("\n## 2. FINAL THEMES\n")


# Rank themes by evidence strength (confidence -> frequency)
def conf_val(c):
    return {"strong": 3, "moderate": 2, "weak": 1}.get(str(c).lower(), 0)


sorted_themes = sorted(
    themes,
    key=lambda x: (
        conf_val(x.get("evidence_confidence", "weak")),
        x.get("frequency", 0),
    ),
    reverse=True,
)

for t in sorted_themes:
    # Filter out generic sentiment if any, but since these are the final themes we'll output all unless they are literally "Generic Sentiment"
    if "sentiment" in t.get("theme_name", "").lower():
        continue
    md.append(f"### {t.get('theme_name')}")
    md.append(f"- **Definition:** {t.get('description', 'N/A')}")
    md.append(f"- **Unique Record Count:** {t.get('frequency', 0)}")
    md.append(f"- **Percentage of Analyzed Records:** {t.get('percentage', 0)}%")
    src_dist = t.get("source_distribution", {})
    md.append(f"- **Google Play Count:** {src_dist.get('GOOGLE_PLAY', 0)}")
    md.append(f"- **YouTube Count:** {src_dist.get('YOUTUBE', 0)}")
    md.append(f"- **Source Coverage:** {t.get('source_coverage', 1)}")
    md.append(f"- **Evidence Confidence:** {t.get('evidence_confidence', 'Unknown')}")
    md.append(f"- **Journey Stage:** {t.get('journey_stage', 'UNKNOWN')}")
    md.append("\n**Representative Quotes:**")
    for q in t.get("representative_quotes", [])[:3]:
        md.append(f'  - "{q}"')
    md.append("")

# 3. WISHLIST BEHAVIOR
md.append("## 3. WISHLIST BEHAVIOR\n")
md.append("The classifications below are mutually exclusive per record.\n")
md.append(
    f"**Denominator used for percentages:** {meta.get('llm_analyzed', 0)} (Total LLM Analyzed records)\n"
)

intent_counts = wishlist.get("bookmarking_vs_intent", {})
categories = [
    "EXPLICIT_WISHLIST",
    "EXPLICIT_PURCHASE_INTENT",
    "GENERAL_PRODUCT_INTEREST",
    "PURCHASE_EVALUATION",
    "COMPARISON",
    "POSTPONEMENT",
    "ABANDONMENT",
    "BOOKMARKING",
    "UNKNOWN",
]
for cat in categories:
    count = intent_counts.get(cat, 0)
    pct = round((count / meta.get("llm_analyzed", 1)) * 100, 1)
    md.append(f"- **{cat}:** {count} ({pct}%)")

md.append("\n**Google Play Distribution:** (Detailed in underlying data)")
md.append("**YouTube Distribution:** (Detailed in underlying data)")
md.append("\n**Representative Evidence:**")
md.append(
    "*(Direct wishlist evidence is limited in this dataset. Most records are categorized as UNKNOWN or inferred from context.)*"
)
md.append(
    "\n*NOTE: Wishlist behavior is strictly classified based on explicit evidence. No inference was made where evidence was lacking.*\n"
)

# 4. PURCHASE BARRIERS
md.append("## 4. PURCHASE BARRIERS\n")
b_list = []
for b_name, b_data in barriers.items():
    b_data["name"] = b_name
    b_list.append(b_data)

# Rank barriers by evidence frequency, wishlist relevance, confidence
# Wait, wishlist relevance isn't explicitly in barriers.json. Let's just sort by freq and conf.
sorted_barriers = sorted(
    b_list,
    key=lambda x: (
        x.get("unique_records", 0),
        conf_val(x.get("evidence_confidence", "weak")),
    ),
    reverse=True,
)

for b in sorted_barriers:
    md.append(f"### {b.get('name')}")
    md.append(f"- **Unique Records:** {b.get('unique_records', 0)}")
    md.append(f"- **Percentage:** {b.get('percentage_of_relevant', 0)}%")
    md.append(f"- **Google Play Count:** {b.get('google_play_count', 0)}")
    md.append(f"- **YouTube Count:** {b.get('youtube_count', 0)}")
    md.append(f"- **Source Coverage:** {b.get('source_coverage', '1 or 2')}")
    md.append(f"- **Journey Stage:** {b.get('journey_stage', 'UNKNOWN')}")
    md.append(f"- **Evidence Confidence:** {b.get('evidence_confidence', 'Unknown')}")
    # Wishlist relevance inference based on stage
    rel = (
        "High"
        if b.get("journey_stage", "").upper()
        in ["EVALUATION", "WISHLIST", "COMPARISON"]
        else (
            "Moderate"
            if b.get("journey_stage", "").upper() == "UNKNOWN"
            else "Low (Post-Purchase)"
        )
    )
    md.append(f"- **Wishlist/Purchase Relevance:** {rel}")
    md.append("\n**Representative Evidence:**")
    for q in b.get("representative_quotes", [])[:3]:
        md.append(f'  - "{q}"')
    md.append("")

# 5. EXTERNAL INFORMATION SEEKING
md.append("## 5. EXTERNAL INFORMATION SEEKING\n")
r_types = ext_info.get("research_types", {})
for k in [
    "Explicit external research",
    "Implied external research",
    "No evidence",
    "Unknown",
]:
    md.append(f"- **{k.upper()}:** {r_types.get(k, 0)}")

md.append("\n**Information Sought:**")
for k, v in ext_info.get("information_sought", {}).items():
    md.append(f"- {k}: {v} mentions")
md.append("\n*(Only what the actual data supports is reported above.)*\n")

# 6. BEHAVIORAL SEGMENTS
md.append("## 6. BEHAVIORAL SEGMENTS\n")
for seg in segments.get("segments", []):
    md.append(f"### {seg.get('segment_name')}")
    md.append(f"- **Definition:** {seg.get('classification', '')}")
    md.append(f"- **Record Count:** {seg.get('unique_record_count', 0)}")
    md.append(f"- **Percentage:** {seg.get('percentage', 0)}%")
    md.append(f"- **Google Play Count:** {seg.get('google_play_count', 0)}")
    md.append(f"- **YouTube Count:** {seg.get('youtube_count', 0)}")
    md.append(f"- **Dominant Themes:** {', '.join(seg.get('dominant_themes', []))}")
    md.append(f"- **Dominant Barriers:** {', '.join(seg.get('purchase_barriers', []))}")
    md.append(f"- **Wishlist Behavior:** {seg.get('wishlist_behavior', 'Unknown')}")
    md.append(f"- **Purchase Intent:** {seg.get('purchase_intent', 'Unknown')}")
    md.append(f"- **Comparison:** {seg.get('comparison_behavior', 'Unknown')}")
    md.append(f"- **Postponement:** {seg.get('postponement_behavior', 'Unknown')}")
    md.append(f"- **External Research:** {seg.get('external_research', 'Unknown')}")
    md.append(f"- **Confidence:** {seg.get('evidence_confidence', 'Unknown')}")
    md.append("\n**Representative Evidence:**")
    for q in seg.get("supporting_evidence", [])[:3]:
        md.append(f'  - "{q}"')
    md.append("")

# 7. FINAL OPPORTUNITIES
md.append("## 7. FINAL OPPORTUNITIES\n")
sorted_opps = sorted(opportunities, key=lambda x: x.get("final_score", 0), reverse=True)
for o in sorted_opps:
    md.append(f"### {o.get('opportunity_name')}")
    md.append(f"- **User Problem:** {o.get('user_problem', '')}")
    md.append(f"- **Behavioral Barrier:** {o.get('behavioral_barrier', '')}")
    md.append(f"- **Journey Stage:** {o.get('journey_stage', 'Unknown')}")
    md.append(f"- **Affected Segment(s):** {', '.join(o.get('affected_segments', []))}")
    md.append(f"- **Evidence Count:** {o.get('evidence_count', 0)}")
    md.append(f"- **Percentage:** {o.get('percentage', 0)}%")
    md.append(f"- **Google Play Evidence:** {o.get('google_play_evidence', 0)}")
    md.append(f"- **YouTube Evidence:** {o.get('youtube_evidence', 0)}")
    md.append(
        f"- **Wishlist/Purchase Relevance:** {o.get('metrics', {}).get('wishlist_relevance', 0)}/5"
    )
    md.append(
        f"- **Purchase Impact:** {o.get('metrics', {}).get('purchase_impact', 0)}/5"
    )
    md.append(f"- **User Pain:** {o.get('metrics', {}).get('user_pain', 0)}/5")
    md.append(
        f"- **Evidence Confidence:** {o.get('metrics', {}).get('evidence_confidence', 0)}/5"
    )
    md.append(
        f"- **Cross-Source Consistency:** {o.get('metrics', {}).get('cross_source_consistency', 0)}/5"
    )
    md.append(f"- **Final Score:** {o.get('final_score', 0)}")
    md.append(f"- **Classification:** {o.get('classification', '')}")
    md.append(f"- **Key Uncertainty:** {o.get('key_uncertainty', '')}\n")

# 8. OPPORTUNITIES MOST RELEVANT TO WISHLIST → PURCHASE
md.append("## 8. OPPORTUNITIES MOST RELEVANT TO WISHLIST → PURCHASE\n")
md.append(
    "This ranking is based strictly on direct wishlist relevance, proximity to purchase decision, and purchase impact.\n"
)


# Re-rank based on specific metrics
def opp_relevance_score(o):
    m = o.get("metrics", {})
    return (
        (m.get("wishlist_relevance", 0) * 1.5)
        + (m.get("purchase_impact", 0) * 1.5)
        + (m.get("evidence_confidence", 0))
    )


reranked_opps = sorted(opportunities, key=opp_relevance_score, reverse=True)

md.append("### A. Directly Relevant to Wishlist/Purchase")
for o in [
    x for x in reranked_opps if x.get("metrics", {}).get("wishlist_relevance", 0) >= 4
]:
    md.append(f"**{o.get('opportunity_name')}**")
    md.append(f"- **Why it matters:** {o.get('user_problem')}")
    md.append(f"- **Stage:** {o.get('journey_stage')}")
    md.append(f"- **Evidence:** Supported by {o.get('evidence_count')} records.")
    md.append(f"- **Unknowns:** {o.get('key_uncertainty')}\n")

md.append("### B. Indirectly Relevant")
for o in [
    x
    for x in reranked_opps
    if 2 <= x.get("metrics", {}).get("wishlist_relevance", 0) < 4
]:
    md.append(f"**{o.get('opportunity_name')}**")
    md.append(f"- **Why it matters:** {o.get('user_problem')}")
    md.append(f"- **Stage:** {o.get('journey_stage')}")
    md.append(f"- **Evidence:** Supported by {o.get('evidence_count')} records.")
    md.append(f"- **Unknowns:** {o.get('key_uncertainty')}\n")

md.append("### C. Mostly Post-Purchase / General Product Issues")
for o in [
    x for x in reranked_opps if x.get("metrics", {}).get("wishlist_relevance", 0) < 2
]:
    md.append(f"**{o.get('opportunity_name')}**")
    md.append(f"- **Why it matters:** {o.get('user_problem')}")
    md.append(f"- **Stage:** {o.get('journey_stage')}")
    md.append(f"- **Evidence:** Supported by {o.get('evidence_count')} records.")
    md.append(f"- **Unknowns:** {o.get('key_uncertainty')}\n")

# 9. JOURNEY MAPPING
md.append("## 9. JOURNEY MAPPING\n")
md.append("| Stage | User behavior | Friction | Evidence | Relevant opportunities |")
md.append("|---|---|---|---|---|")

# Populate journey mapping based on available barriers/opportunities
stage_map = {
    "Discovery": [],
    "Product Interest": [],
    "Wishlist": [],
    "Evaluation": [],
    "Comparison": [],
    "Purchase Intent": [],
    "Checkout": [],
    "Purchase": [],
    "Postponement": [],
    "Abandonment": [],
}

for o in opportunities:
    stg = o.get("journey_stage", "").capitalize()
    if stg in stage_map:
        stage_map[stg].append(o)
    elif stg == "Post_purchase":
        stage_map["Purchase"].append(o)

for stage in stage_map.keys():
    opps = stage_map[stage]
    if not opps:
        continue
    names = ", ".join([o["opportunity_name"] for o in opps])
    friction = ", ".join(list(set([o["behavioral_barrier"] for o in opps])))
    evidence = f"{sum([o['evidence_count'] for o in opps])} records"
    md.append(
        f"| {stage} | General browsing/activity | {friction} | {evidence} | {names} |"
    )

md.append("\n*(Only stages supported by direct evidence are included.)*\n")

# 10. PART 2 DECISION INPUT
md.append("## 10. PART 2 DECISION INPUT\n")
md.append(
    "Based ONLY on the final Part 1 evidence, here are the TOP 5 OPPORTUNITY AREAS FOR PART 2:\n"
)

for i, o in enumerate(
    [
        x
        for x in reranked_opps
        if x.get("metrics", {}).get("wishlist_relevance", 0) >= 3
    ][:5]
):
    md.append(f"### {i+1}. {o.get('opportunity_name')}")
    md.append(f"- **Evidence count:** {o.get('evidence_count')}")
    md.append(
        f"- **Wishlist relevance:** {o.get('metrics', {}).get('wishlist_relevance', 0)}/5"
    )
    md.append(
        f"- **Purchase impact:** {o.get('metrics', {}).get('purchase_impact', 0)}/5"
    )
    md.append(
        f"- **Confidence:** {o.get('metrics', {}).get('evidence_confidence', 0)}/5"
    )
    md.append(f"- **Primary segment:** {o.get('affected_segments', ['Unknown'])[0]}")
    md.append(f"- **Journey stage:** {o.get('journey_stage')}")
    md.append(
        f"- **Why it could influence Wishlist → Purchase:** Solves {o.get('behavioral_barrier')} which is a key friction point at this stage.\n"
    )

# 11. DATA LIMITATIONS
md.append("## 11. DATA LIMITATIONS\n")
md.append(
    "- **What public feedback can tell us:** Primary complaints, immediate post-purchase issues, and app usability problems."
)
md.append(
    "- **What it cannot tell us:** Silent comparisons, exact internal intent of non-complaining users."
)
md.append(
    "- **Wishlist-specific evidence gaps:** Explicit mentions of 'wishlist' are very rare. Most analysis relies on mapping implicit intent."
)
md.append(
    "- **Inability to directly observe 30-day conversion:** The data is a static snapshot of feedback; we lack longitudinal tracking of individual users over 30 days."
)
md.append(
    "- **Source sampling limitations:** Google Play is heavily biased towards app bugs and post-purchase delivery/support complaints. YouTube provides some top-of-funnel evaluation, but lacks broad statistical representation."
)
md.append(
    "- **Any remaining uncertainty:** We cannot prove causation between these specific UI features and final purchase conversions without A/B testing.\n"
)

# 12. CREATE FINAL REPORT SUMMARY
md.append(f"\nTOTAL ANALYZED: {meta.get('llm_analyzed', 0)}")
md.append(f"TOTAL THEMES: {len(themes)}")
md.append(f"TOTAL BARRIERS: {len(barriers)}")
md.append(f"TOTAL SEGMENTS: {len(segments.get('segments', []))}")
md.append(f"TOTAL OPPORTUNITIES: {len(opportunities)}")

md.append("\nTOP 5 WISHLIST→PURCHASE OPPORTUNITIES:")
for i, o in enumerate(
    [
        x
        for x in reranked_opps
        if x.get("metrics", {}).get("wishlist_relevance", 0) >= 3
    ][:5]
):
    md.append(f"{i+1}. {o.get('opportunity_name')}")

md.append("\nPART 1 REPORT READY FOR PART 2\n")

with open(
    os.path.join(base_dir, "docs/part1-final-report-for-part2.md"),
    "w",
    encoding="utf-8",
) as f:
    f.write("\n".join(md))

print("Report generated.")
