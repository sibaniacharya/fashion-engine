from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from ingestion.google_play import GooglePlayAdapter
from ingestion.reddit import RedditAdapter
from ingestion.youtube import YouTubeAdapter
from models import RawFeedback
import traceback
import os


class IngestionManager:
    def __init__(self, db: Session):
        self.db = db
        self.adapters = [
            GooglePlayAdapter(count=200),
            RedditAdapter(limit=20),
            YouTubeAdapter(),
        ]
        self.is_postgres = os.getenv("DATABASE_URL", "").startswith("postgres")

    def run_ingestion(self) -> dict:
        results = {}
        for adapter in self.adapters:
            source_name = adapter.__class__.__name__
            try:
                print(f"Running ingestion for {source_name}...")
                records = adapter.fetch_data()
                saved_count = 0

                if not records:
                    results[source_name] = {
                        "fetched": 0,
                        "saved": 0,
                        "status": "Skipped or no data",
                    }
                    continue

                for record_dict in records:
                    if self.is_postgres:
                        stmt = pg_insert(RawFeedback).values(**record_dict)
                        stmt = stmt.on_conflict_do_nothing(index_elements=["source_id"])
                    else:
                        stmt = sqlite_insert(RawFeedback).values(**record_dict)
                        stmt = stmt.on_conflict_do_nothing(index_elements=["source_id"])

                    result = self.db.execute(stmt)
                    if result.rowcount > 0:
                        saved_count += 1

                self.db.commit()
                metrics = getattr(adapter, "metrics", {})

                results[source_name] = {
                    "fetched": len(records),
                    "saved": saved_count,
                    "status": "Success",
                    "metrics": metrics,
                }
                print(
                    f"Saved {saved_count}/{len(records)} new records from {source_name}"
                )

            except Exception as e:
                self.db.rollback()
                print(f"Failed ingestion for {source_name}: {e}")
                traceback.print_exc()
                results[source_name] = {
                    "fetched": 0,
                    "saved": 0,
                    "status": f"Error: {str(e)}",
                }

        return results
