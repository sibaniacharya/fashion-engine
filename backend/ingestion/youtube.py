import os
import uuid
from typing import List, Dict, Any
from datetime import datetime
from googleapiclient.discovery import build
from ingestion.base import IngestionAdapter

class YouTubeAdapter(IngestionAdapter):
    """Fetches YouTube comments from specific fashion review videos by searching keywords."""

    def __init__(self, max_videos: int = 5, max_comments_per_video: int = 20):
        self.max_videos = max_videos
        self.max_comments_per_video = max_comments_per_video
        
        # We load dotenv locally so if a .env file exists, it's used
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
            
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        
        if self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        else:
            self.youtube = None

    def search_videos(self) -> List[str]:
        """Search for videos relevant to fashion shopping."""
        query = "Myntra fashion shopping OR wishlist OR online fashion OR size fit OR fashion product reviews"
        try:
            request = self.youtube.search().list(
                part="id",
                q=query,
                type="video",
                maxResults=self.max_videos,
                relevanceLanguage="en"
            )
            response = request.execute()
            return [item["id"]["videoId"] for item in response.get("items", [])]
        except Exception as e:
            print(f"Error searching YouTube videos: {e}")
            return []

    def fetch_data(self) -> List[Dict[str, Any]]:
        if not self.youtube:
            print("YouTube API key not found. Skipping YouTube ingestion.")
            return []
            
        video_ids = self.search_videos()
        if not video_ids:
            return []
            
        records = []
        for video_id in video_ids:
            try:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=self.max_comments_per_video,
                    textFormat="plainText"
                )
                response = request.execute()
                
                for item in response.get("items", []):
                    snippet = item["snippet"]["topLevelComment"]["snippet"]
                    record_date = datetime.strptime(snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                    
                    records.append({
                        "internal_id": str(uuid.uuid4()),
                        "source": "YOUTUBE",
                        "source_id": item["id"],
                        "date": record_date,
                        "title": None,
                        "text": snippet["textDisplay"],
                        "rating": None,
                        "url": f"https://www.youtube.com/watch?v={video_id}&lc={item['id']}",
                        "category": "YouTube Comment",
                        "metadata_": {
                            "authorDisplayName": snippet["authorDisplayName"],
                            "likeCount": snippet["likeCount"],
                            "videoId": video_id
                        }
                    })
            except Exception as e:
                # Videos might have comments disabled
                print(f"Error fetching from YouTube video {video_id}: {e}")
                
        return records
