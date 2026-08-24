from ingestion.youtube import YouTubeAdapter

def run_test():
    adapter = YouTubeAdapter(max_videos=2, max_comments_per_video=3)
    records = adapter.fetch_data()
    
    print(f"Total YouTube records fetched: {len(records)}")
    for r in records:
        print("-" * 40)
        print(f"Video ID: {r['metadata_']['videoId']}")
        print(f"Author: {r['metadata_']['authorDisplayName']}")
        print(f"Comment: {r['text'][:150]}...")

if __name__ == "__main__":
    run_test()
