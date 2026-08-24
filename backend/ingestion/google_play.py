import uuid
from typing import List, Dict, Any
from google_play_scraper import reviews, Sort
from datetime import datetime
from ingestion.base import IngestionAdapter

class GooglePlayAdapter(IngestionAdapter):
    """Fetches app reviews from Google Play Store."""

    def __init__(self, app_id: str = 'com.myntra.android', count: int = 100):
        self.app_id = app_id
        self.count = count

    def fetch_data(self) -> List[Dict[str, Any]]:
        try:
            result, continuation_token = reviews(
                self.app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=self.count
            )
            
            records = []
            for item in result:
                # google_play_scraper returns a naive datetime object.
                record_date = item.get('at')
                
                records.append({
                    "internal_id": str(uuid.uuid4()),
                    "source": "GOOGLE_PLAY",
                    "source_id": item.get("reviewId", ""),
                    "date": record_date,
                    "title": None,
                    "text": item.get("content", ""),
                    "rating": float(item.get("score", 0)),
                    "url": None,
                    "category": "App Review",
                    "metadata_": {
                        "userName": item.get("userName"),
                        "thumbsUpCount": item.get("thumbsUpCount"),
                        "reviewCreatedVersion": item.get("reviewCreatedVersion")
                    }
                })
            return records
        except Exception as e:
            print(f"Error fetching from Google Play: {e}")
            return []
