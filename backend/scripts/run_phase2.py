import os
import sys
import json
from collections import defaultdict

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SessionLocal, engine, Base
from models import RawFeedback, NormalizedFeedback
from processing.cleaner import DataCleaner

def run_phase2():
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    cleaner = DataCleaner()
    
    raw_records = db.query(RawFeedback).all()
    
    stats = {
        "total_processed": len(raw_records),
        "total_valid": 0,
        "dropped_by_reason": defaultdict(int),
        "language_breakdown": defaultdict(int),
        "duplicates_dropped": 0
    }
    
    normalized_list = []
    seen_texts = set()
    
    print(f"Processing {len(raw_records)} raw records...")
    
    for raw in raw_records:
        clean_result = cleaner.clean_record(raw.text)
        
        # Deduplication (using normalized text)
        if clean_result["is_valid"]:
            norm_text_lower = clean_result["normalized_text"].lower()
            if norm_text_lower in seen_texts:
                clean_result["is_valid"] = False
                clean_result["rejection_reason"] = "Duplicate content"
                stats["duplicates_dropped"] += 1
            else:
                seen_texts.add(norm_text_lower)
        
        if not clean_result["is_valid"]:
            stats["dropped_by_reason"][clean_result["rejection_reason"]] += 1
        else:
            stats["total_valid"] += 1
            stats["language_breakdown"][clean_result["language"]] += 1
            
            # Save to database
            norm_record = NormalizedFeedback(
                raw_id=raw.internal_id,
                source=raw.source,
                source_id=raw.source_id,
                date=raw.date,
                rating=raw.rating,
                original_text=raw.text,
                normalized_text=clean_result["normalized_text"],
                language=clean_result["language"],
                is_valid=True
            )
            db.add(norm_record)
            
            # Prepare for JSON export
            normalized_list.append({
                "id": norm_record.id,
                "raw_id": norm_record.raw_id,
                "source": norm_record.source,
                "source_id": norm_record.source_id,
                "date": norm_record.date.isoformat() if norm_record.date else None,
                "rating": norm_record.rating,
                "original_text": norm_record.original_text,
                "normalized_text": norm_record.normalized_text,
                "language": norm_record.language
            })
            
    db.commit()
    db.close()
    
    # Export JSONs
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'normalized'))
    os.makedirs(output_dir, exist_ok=True)
    
    reviews_path = os.path.join(output_dir, "normalized_reviews.json")
    with open(reviews_path, "w", encoding="utf-8") as f:
        json.dump(normalized_list, f, indent=2, ensure_ascii=False)
        
    report_path = os.path.join(output_dir, "data_quality_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
        
    print(f"Phase 2 complete! {stats['total_valid']} records normalized and saved.")
    print(f"Data saved to {output_dir}")

if __name__ == "__main__":
    run_phase2()
