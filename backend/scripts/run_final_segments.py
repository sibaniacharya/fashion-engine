import os
import sys
import json
from collections import defaultdict


def normalize_segment(raw_segment: str) -> str:
    if not raw_segment:
        return "UNKNOWN"

    seg = raw_segment.upper().strip().replace("-", "_").replace(" ", "_")
    if "SHOPPER" in seg:
        seg = seg.replace("_SHOPPER", "")

    if seg in ["UNKNOWN", "SEGMENT_UNKNOWN", "NONE", ""]:
        return "UNKNOWN"

    return seg


def generate_definition(seg: str) -> str:
    definitions = {
        "QUALITY_CONSCIOUS": "Users primarily motivated by the durability, material, and overall quality of products.",
        "VALUE_CONSCIOUS": "Shoppers highly sensitive to pricing, discounts, and the perceived value of purchases.",
        "FIT_CONSCIOUS": "Users whose primary concern is sizing accuracy and how products fit their body type.",
        "COMPARISON": "Shoppers who heavily research and compare options across multiple platforms before purchasing.",
        "BRAND_LOYAL": "Users demonstrating strong preference and trust toward specific brands or the platform itself.",
        "FREQUENT": "Highly active shoppers who make regular purchases and engage deeply with the platform.",
    }
    return definitions.get(
        seg, f"Users exhibiting behaviors aligned with {seg.replace('_', ' ').title()}."
    )


def run_final_segments():
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

    # Group records by normalized segment
    segment_groups = defaultdict(
        lambda: {
            "records": [],
            "themes": defaultdict(int),
            "barriers": defaultdict(int),
            "wishlist": defaultdict(int),
            "postponement": defaultdict(int),
            "comparison": 0,
            "research": defaultdict(int),
        }
    )

    for r in valid_records:
        raw_seg = r.get("user_segment", "UNKNOWN")
        norm_seg = normalize_segment(raw_seg)

        # Don't try to force unknown records into segments.
        # UNKNOWN means insufficient behavioral evidence.

        sg = segment_groups[norm_seg]
        sg["records"].append(r)

        theme = r.get("theme", "UNKNOWN")
        if theme and theme.upper() not in ["UNKNOWN", "INSUFFICIENT_EVIDENCE"]:
            sg["themes"][theme] += 1

        barrier = r.get("purchase_barrier", "UNKNOWN")
        if barrier and barrier.upper() not in ["UNKNOWN", "NO", "NONE"]:
            sg["barriers"][barrier] += 1

        wish = r.get("wishlist_intent", "UNKNOWN")
        if wish and wish.upper() not in ["UNKNOWN", "NO", "NONE"]:
            sg["wishlist"][wish.upper()] += 1

        if wish and wish.upper() == "COMPARISON":
            sg["comparison"] += 1

        if wish and wish.upper() == "POSTPONEMENT":
            sg["postponement"][barrier] += 1

        research = r.get("information_seeking", "UNKNOWN")
        if research and research.upper() not in ["UNKNOWN", "NO_EVIDENCE"]:
            sg["research"][research.upper()] += 1

    final_segments = []
    unknown_count = len(segment_groups["UNKNOWN"]["records"])

    for seg_name, data in segment_groups.items():
        if seg_name == "UNKNOWN":
            continue

        count = len(data["records"])

        # Classification Thresholds
        if count >= 10:
            cls = "HIGH_CONFIDENCE_SEGMENT"
        elif count >= 5:
            cls = "SUPPORTED_SEGMENT"
        elif count >= 2:
            cls = "EMERGING_SEGMENT"
        else:
            cls = "SIGNAL"

        if count > 10:
            conf = "strong"
        elif count > 4:
            conf = "moderate"
        else:
            conf = "weak"

        gp_count = sum(1 for r in data["records"] if r.get("source") == "GOOGLE_PLAY")
        yt_count = sum(1 for r in data["records"] if r.get("source") == "YOUTUBE")

        top_themes = [
            k
            for k, v in sorted(
                data["themes"].items(), key=lambda i: i[1], reverse=True
            )[:3]
        ]
        top_barriers = [
            k
            for k, v in sorted(
                data["barriers"].items(), key=lambda i: i[1], reverse=True
            )[:3]
        ]

        quotes = []
        for r in data["records"][:3]:
            q = r.get("text")
            if q:
                quotes.append(
                    {
                        "quote": q,
                        "source": r.get("source"),
                        "trace_id": r.get("record_id"),
                        "date": r.get("date"),
                    }
                )

        final_segments.append(
            {
                "segment_name": seg_name,
                "behavioral_definition": generate_definition(seg_name),
                "unique_record_count": count,
                "percentage": round((count / total_analyzed) * 100, 1),
                "google_play_count": gp_count,
                "youtube_count": yt_count,
                "source_coverage": sum(1 for x in [gp_count, yt_count] if x > 0),
                "dominant_themes": top_themes,
                "purchase_barriers": top_barriers,
                "wishlist_behavior": dict(data["wishlist"]),
                "purchase_intent": dict(data["wishlist"]),  # Aliased for simplicity
                "comparison_behavior": data["comparison"],
                "postponement_behavior": dict(data["postponement"]),
                "external_research": dict(data["research"]),
                "evidence_confidence": conf,
                "classification": cls,
                "supporting_evidence": quotes,
            }
        )

    final_segments.sort(key=lambda x: x["unique_record_count"], reverse=True)

    output = {
        "total_records_classified": total_analyzed - unknown_count,
        "unknown_segment_count": unknown_count,
        "segments": final_segments,
    }

    out_path = os.path.join(base_dir, "output", "behavioral_segments.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(final_segments)} segments to {out_path}.")
    print(
        f"Total classified: {output['total_records_classified']}, Unknown: {unknown_count}"
    )


if __name__ == "__main__":
    run_final_segments()
