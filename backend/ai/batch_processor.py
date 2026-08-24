import time
from datetime import datetime
from database import SessionLocal
from models import NormalizedFeedback, ExtractedSignal
from ai.extractor import SignalExtractor

class BatchProcessor:
    def __init__(self):
        self.extractor = SignalExtractor()

    def process_all(self, batch_size: int = 5):
        db = SessionLocal()
        
        valid_records = db.query(NormalizedFeedback).filter(NormalizedFeedback.is_valid == True).all()
        processed_ids = {r.raw_id for r in db.query(ExtractedSignal.raw_id).all()}
        records_to_process = [r for r in valid_records if r.raw_id not in processed_ids]
        
        print(f"Total valid records: {len(valid_records)}")
        print(f"Already processed: {len(processed_ids)}")
        print(f"Remaining to process: {len(records_to_process)}")
        
        count = 0
        failed_count = 0
        for record in records_to_process:
            try:
                signals_dict = self.extractor.extract_signals(record.normalized_text)
                extracted = ExtractedSignal(
                    raw_id=record.raw_id,
                    signals=signals_dict,
                    processed_at=datetime.utcnow()
                )
                db.add(extracted)
                db.commit()
                count += 1
                
                # Dynamic delay to avoid 5 RPM limit on free tier. 
                # (We will sleep for 12 seconds per request)
                time.sleep(12)
                    
            except Exception as e:
                print(f"Failed to process record {record.raw_id}: {e}")
                db.rollback()
                failed_count += 1
                # If we hit fatal limits we stop, but for the sake of the report let's 
                # allow 3 failed records before aborting the whole run.
                if failed_count >= 3:
                    print("Stopping batch processor due to repeated errors.")
                    break
                else:
                    time.sleep(30) # Cool down
                
        db.close()
        print(f"Batch processing complete. Processed {count} new records.")
        return {
            "processed": count,
            "failed": failed_count,
            "retry_count": self.extractor.retry_count,
            "rate_limit_events": self.extractor.rate_limit_events
        }
