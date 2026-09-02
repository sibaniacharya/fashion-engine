import os
import json


def test():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    records_path = os.path.join(base_dir, "output", "analysis_records.json")
    barriers_path = os.path.join(base_dir, "output", "barriers.json")

    with open(records_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    with open(barriers_path, "r", encoding="utf-8") as f:
        barriers = json.load(f)

    records_by_barrier = {}
    for r in records:
        b = r.get("purchase_barrier")
        if b and b != "UNKNOWN":
            if b not in records_by_barrier:
                records_by_barrier[b] = []
            records_by_barrier[b].append(r)

    errors = []

    for b_name, b_data in barriers.items():
        if b_name not in records_by_barrier:
            errors.append(
                f"Barrier '{b_name}' is in barriers.json but not in analysis_records.json"
            )
            continue

        valid_trace_ids = {r["record_id"] for r in records_by_barrier[b_name]}

        quotes_detail = b_data.get("quotes_detail", [])
        for q in quotes_detail:
            if q["trace_id"] not in valid_trace_ids:
                errors.append(
                    f"Quote '{q['trace_id']}' mapped to '{b_name}' in barriers.json but has a different barrier in analysis_records.json"
                )

    for b_name in records_by_barrier.keys():
        if b_name not in barriers:
            errors.append(
                f"Barrier '{b_name}' is in analysis_records.json but missing from barriers.json"
            )

    if errors:
        print("FAIL: Mismatches found:")
        for e in errors:
            print(f" - {e}")
    else:
        print("PASS: All barriers and quotes match perfectly!")


if __name__ == "__main__":
    test()
