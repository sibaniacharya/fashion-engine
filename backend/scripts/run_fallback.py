import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import SessionLocal
from models import NormalizedFeedback, ExtractedSignal
from ai.batch_processor import BatchProcessor


def run_fallback():
    db = SessionLocal()
    bp = BatchProcessor()

    valid_records = (
        db.query(NormalizedFeedback).filter(NormalizedFeedback.is_valid == True).all()
    )
    all_signals = db.query(ExtractedSignal).all()
    processed_ids = set()
    for s in all_signals:
        status = s.signals.get("status", s.signals.get("analysis_status", "ANALYZED"))
        if status in ["ANALYZED", "ANALYZED_FALLBACK"]:
            processed_ids.add(s.raw_id)
        else:
            db.delete(s)
    db.commit()

    records_to_process = [r for r in valid_records if r.raw_id not in processed_ids]

    unique_records = []
    seen = set()
    for r in records_to_process:
        if r.raw_id not in seen:
            unique_records.append(r)
            seen.add(r.raw_id)

    print(f"Running fallback for {len(unique_records)} records...")

    count = 0
    for r in unique_records:
        analysis = bp._fallback_analysis(r.normalized_text)
        extracted = ExtractedSignal(
            raw_id=r.raw_id, signals=analysis, processed_at=datetime.utcnow()
        )
        db.add(extracted)
        count += 1

    db.commit()
    db.close()
    print(f"Fallback complete. Processed {count} records.")


if __name__ == "__main__":
    run_fallback()
