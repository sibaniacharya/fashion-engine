import os
import uuid
from typing import List, Dict, Any
from datetime import datetime
from googleapiclient.discovery import build
from ingestion.base import IngestionAdapter


class YouTubeAdapter(IngestionAdapter):
    """Fetches YouTube comments from specific fashion review videos by searching keywords."""

    def __init__(
        self,
        queries: List[str] = None,
        max_videos_per_query: int = 2,
        max_comments_per_video: int = 50,
    ):
        self.max_videos_per_query = max_videos_per_query
        self.max_comments_per_video = max_comments_per_video

        if queries is None:
            self.queries = [
                "Myntra review",
                "Myntra shopping experience",
                "Myntra fashion haul",
                "Myntra product review",
                "Myntra fit review",
                "online fashion shopping India",
            ]
        else:
            self.queries = queries

        self.metrics = {
            "videos_searched": 0,
            "comments_collected": 0,
            "relevant_comments": 0,
            "invalid_records_removed": 0,
            "final_valid_comments": 0,
            "failed_requests": 0,
        }

        # We load dotenv locally so if a .env file exists, it's used
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            pass

        self.api_key = os.getenv("YOUTUBE_API_KEY")

        if self.api_key:
            self.youtube = build("youtube", "v3", developerKey=self.api_key)
        else:
            self.youtube = None

    def is_relevant(self, text: str) -> bool:
        """Filters comments for shopping relevance."""
        keywords = [
            "fashion",
            "shopping",
            "buy",
            "bought",
            "purchase",
            "quality",
            "fit",
            "size",
            "styling",
            "price",
            "value",
            "comparison",
            "hesitate",
            "wishlist",
            "save",
            "review",
            "worth",
            "return",
            "delivery",
            "fabric",
            "material",
            "tight",
            "loose",
            "myntra",
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)

    def search_videos(self) -> List[Dict[str, str]]:
        """Search for videos relevant to fashion shopping."""
        videos = []
        for query in self.queries:
            try:
                request = self.youtube.search().list(
                    part="id,snippet",
                    q=query,
                    type="video",
                    maxResults=self.max_videos_per_query,
                    relevanceLanguage="en",
                )
                response = request.execute()
                for item in response.get("items", []):
                    videos.append(
                        {
                            "videoId": item["id"]["videoId"],
                            "search_query": query,
                            "video_title": item["snippet"]["title"],
                        }
                    )
            except Exception as e:
                print(f"Error searching YouTube videos for query '{query}': {e}")
                self.metrics["failed_requests"] += 1

        self.metrics["videos_searched"] = len(videos)
        return videos

    def fetch_data(self) -> List[Dict[str, Any]]:
        if not self.youtube:
            print("YOUTUBE\nStatus: NOT CONFIGURED\nReason: YOUTUBE_API_KEY missing")
            return []

        videos = self.search_videos()
        if not videos:
            return []

        records = []
        seen_comments = set()

        for video in videos:
            video_id = video["videoId"]
            try:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=self.max_comments_per_video,
                    textFormat="plainText",
                )
                response = request.execute()

                for item in response.get("items", []):
                    self.metrics["comments_collected"] += 1
                    snippet = item["snippet"]["topLevelComment"]["snippet"]
                    text = snippet["textDisplay"]

                    if not self.is_relevant(text):
                        self.metrics["invalid_records_removed"] += 1
                        continue

                    self.metrics["relevant_comments"] += 1

                    # Basic in-batch deduplication
                    if text.lower() in seen_comments:
                        self.metrics["invalid_records_removed"] += 1
                        continue
                    seen_comments.add(text.lower())

                    record_date = datetime.strptime(
                        snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                    )

                    records.append(
                        {
                            "internal_id": str(uuid.uuid4()),
                            "source": "YOUTUBE",
                            "source_id": item["id"],
                            "date": record_date,
                            "title": None,
                            "text": text,
                            "rating": None,
                            "url": f"https://www.youtube.com/watch?v={video_id}&lc={item['id']}",
                            "category": "YouTube Comment",
                            "metadata_": {
                                "videoId": video_id,
                                "search_query": video["search_query"],
                                "video_title": video["video_title"],
                                "likeCount": snippet["likeCount"],
                            },
                        }
                    )
                    self.metrics["final_valid_comments"] += 1

            except Exception as e:
                # Videos might have comments disabled
                print(f"Error fetching from YouTube video {video_id}: {e}")
                self.metrics["failed_requests"] += 1

        return records
