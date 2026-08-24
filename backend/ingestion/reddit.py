import os
import uuid
import praw
from typing import List, Dict, Any
from datetime import datetime
from ingestion.base import IngestionAdapter

class RedditAdapter(IngestionAdapter):
    """Fetches Reddit posts and comments from specific fashion subreddits."""

    def __init__(self, subreddit_name: str = 'IndianFashionAddicts', limit: int = 50):
        self.subreddit_name = subreddit_name
        self.limit = limit
        
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'python:discovery_engine:v1')
        
        if self.client_id and self.client_secret:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
        else:
            self.reddit = None

    def fetch_data(self) -> List[Dict[str, Any]]:
        if not self.reddit:
            print("Reddit credentials not found. Skipping Reddit ingestion.")
            return []
            
        records = []
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
            for submission in subreddit.hot(limit=self.limit):
                record_date = datetime.fromtimestamp(submission.created_utc)
                records.append({
                    "internal_id": str(uuid.uuid4()),
                    "source": "REDDIT",
                    "source_id": submission.id,
                    "date": record_date,
                    "title": submission.title,
                    "text": submission.selftext if submission.selftext else "(No text body)",
                    "rating": None,
                    "url": submission.url,
                    "category": "Reddit Post",
                    "metadata_": {
                        "score": submission.score,
                        "num_comments": submission.num_comments,
                        "subreddit": self.subreddit_name
                    }
                })
        except Exception as e:
            print(f"Error fetching from Reddit: {e}")
            
        return records
