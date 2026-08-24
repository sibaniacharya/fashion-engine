import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SessionLocal, engine, Base
from models import ExtractedSignal, NormalizedFeedback
from ai.batch_processor import BatchProcessor

def run_phase3():
    Base.metadata.create_all(bind=engine)
    
    processor = BatchProcessor()
    metrics = processor.process_all(batch_size=1)
    
    db = SessionLocal()
    signals = db.query(ExtractedSignal).all()
    
    output_list = []
    for s in signals:
        norm = db.query(NormalizedFeedback).filter(NormalizedFeedback.raw_id == s.raw_id).first()
        
        output_list.append({
            "signal_id": s.id,
            "raw_id": s.raw_id,
            "source": norm.source if norm else None,
            "source_id": norm.source_id if norm else None,
            "date": norm.date.isoformat() if norm and norm.date else None,
            "normalized_text": norm.normalized_text if norm else None,
            "extracted_signals": s.signals,
            "processed_at": s.processed_at.isoformat() if s.processed_at else None
        })
        
    db.close()
    
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'analyzed'))
    os.makedirs(output_dir, exist_ok=True)
    
    export_path = os.path.join(output_dir, "phase3_signals.json")
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(output_list, f, indent=2, ensure_ascii=False)
        
    print(f"\n--- Phase 3 Execution Report ---")
    print(f"Total Records Analyzed/Saved: {len(output_list)}")
    print(f"Failed Records: {metrics['failed']}")
    print(f"Retry Count: {metrics['retry_count']}")
    print(f"Rate-limit Events: {metrics['rate_limit_events']}")
    print(f"Output saved to: {export_path}")

if __name__ == "__main__":
    run_phase3()
