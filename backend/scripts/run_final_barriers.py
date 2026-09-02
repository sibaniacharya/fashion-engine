import os
import sys
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.cluster import ThemeClusterer
from google import genai
from google.genai import types
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential


class BarrierSchema(BaseModel):
    barrier_name: str


class BarrierSynthesizer:
    def __init__(self):
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"

    @retry(
        stop=stop_after_attempt(1), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def synthesize_cluster(self, records: list[dict]) -> dict:
        sample_size = min(20, len(records))
        samples = []
        for r in records[:sample_size]:
            text = r.get("text", "")
            barrier_cand = r.get("purchase_barrier", "")
            samples.append(f"Feedback: {text}\nCandidate Barrier: {barrier_cand}")

        joined_samples = "\n\n".join(samples)

        prompt = f"""
You are an expert e-commerce analyst. I have clustered user feedback that describes reasons why users postpone or abandon a purchase (Purchase Barriers).

Please review the following sample feedback and synthesize a single, clear, professional category name for this purchase barrier (e.g., "Return Policy Friction", "Price/Value Uncertainty", "App Usability Issues", "Quality Concerns", "Fit and Sizing Uncertainty").

If the feedback does not clearly indicate a purchase barrier (e.g., it is just general praise or unrelated), return "NO_BARRIER".

Samples:
{joined_samples}
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=BarrierSchema,
                temperature=0.1,
            ),
        )
        return json.loads(response.text)


def run_final_barriers():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    canonical_path = os.path.join(base_dir, "output", "analysis_records.json")

    if not os.path.exists(canonical_path):
        print(f"Error: Could not find canonical records at {canonical_path}")
        return

    with open(canonical_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    total_analyzed = len(
        [
            r
            for r in records
            if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
        ]
    )
    print(f"Loaded {total_analyzed} successfully analyzed records.")

    if total_analyzed == 0:
        return

    # Filter records that have a barrier
    barrier_records = []
    for r in records:
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]:
            b = r.get("purchase_barrier", "")
            if b and str(b).upper() not in ["UNKNOWN", "NO", "NONE", ""]:
                barrier_records.append(r)

    print(f"Found {len(barrier_records)} records with potential purchase barriers.")

    if len(barrier_records) == 0:
        print("No barrier records to cluster.")
        return

    # 1. Cluster Records
    clusterer = ThemeClusterer()
    # Temporarily map "theme" logic to "purchase_barrier" for the clusterer implicitly
    # The ThemeClusterer uses theme_cand = r.get("theme") or "" and pain = r.get("purchase_barrier") or "".
    # Since purchase_barrier is heavily populated here, the clusterer will group them properly!
    clusters = clusterer.cluster_records(barrier_records)
    print(f"Generated {len(clusters)} clusters.")

    # 2. Synthesize Barriers
    synthesizer = BarrierSynthesizer()
    final_barrier_data = []

    record_barrier_map = {}

    for i, cluster in enumerate(clusters):
        print(
            f"Synthesizing Barrier {i+1}/{len(clusters)} (Cluster Size: {len(cluster)})"
        )
        try:
            barrier_info = synthesizer.synthesize_cluster(cluster)
            barrier_name = barrier_info.get("barrier_name", "NO_BARRIER")

            for r in cluster:
                record_barrier_map[r["record_id"]] = barrier_name

            if barrier_name != "NO_BARRIER":
                final_barrier_data.append(
                    {"barrier_name": barrier_name, "records": cluster}
                )

            time.sleep(15)  # Rate limit protection for Gemini API
        except Exception as e:
            print(f"Failed to synthesize barrier for cluster {i+1}: {e}")
            for r in cluster:
                record_barrier_map[r["record_id"]] = "UNKNOWN"

    # 3. Merge semantically duplicate barriers
    merged_barriers = {}
    for bd in final_barrier_data:
        b_name = bd["barrier_name"]
        if b_name not in merged_barriers:
            merged_barriers[b_name] = {"barrier_name": b_name, "records": []}
        merged_barriers[b_name]["records"].extend(bd["records"])

    final_calculated_barriers = {}

    # 4. Calculate rigorous metrics for each merged barrier
    for b_name, data in merged_barriers.items():
        records_in_barrier = data["records"]

        unique_records = {}
        for r in records_in_barrier:
            unique_records[r["record_id"]] = r
        unique_records = list(unique_records.values())

        unique_record_count = len(unique_records)

        percentage = (
            round((unique_record_count / total_analyzed) * 100, 1)
            if total_analyzed > 0
            else 0.0
        )

        google_play_count = sum(
            1 for r in unique_records if r.get("source") == "GOOGLE_PLAY"
        )
        youtube_count = sum(1 for r in unique_records if r.get("source") == "YOUTUBE")

        # Determine primary journey stage
        stages = {}
        for r in unique_records:
            stg = r.get("purchase_stage", "Unknown")
            stages[stg] = stages.get(stg, 0) + 1
        journey_stage = max(stages, key=stages.get) if stages else "Unknown"

        if unique_record_count > 10:
            conf = "strong"
        elif unique_record_count > 5:
            conf = "moderate"
        else:
            conf = "weak"

        representative_quotes = []
        for r in unique_records[:3]:  # Take up to 3 quotes
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

        final_calculated_barriers[b_name] = {
            "total_mentions": unique_record_count,
            "unique_records": unique_record_count,
            "percentage_of_relevant": percentage,
            "google_play_count": google_play_count,
            "youtube_count": youtube_count,
            "journey_stage": journey_stage,
            "evidence_confidence": conf,
            "unique_supporting_records": unique_record_count,
            "representative_quotes": [q["quote"] for q in representative_quotes],
            "quotes_detail": representative_quotes,
        }

    # 5. Update analysis_records.json with the new fully traced barriers
    for r in records:
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]:
            # Default to NO_BARRIER if not in map, but if it wasn't in barrier_records, keep its old value
            b = r.get("purchase_barrier", "")
            if b and str(b).upper() not in ["UNKNOWN", "NO", "NONE", ""]:
                new_barrier = record_barrier_map.get(r["record_id"], "UNKNOWN")
                if new_barrier == "NO_BARRIER":
                    r["purchase_barrier"] = "UNKNOWN"
                else:
                    r["purchase_barrier"] = new_barrier

    with open(canonical_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Updated {canonical_path} with final purchase barriers.")

    # 6. Save deterministic barriers output
    output_barriers_path = os.path.join(base_dir, "output", "barriers.json")
    with open(output_barriers_path, "w", encoding="utf-8") as f:
        json.dump(final_calculated_barriers, f, indent=2, ensure_ascii=False)
    print(
        f"Saved {len(final_calculated_barriers)} final deterministic barriers to {output_barriers_path}."
    )


if __name__ == "__main__":
    run_final_barriers()
