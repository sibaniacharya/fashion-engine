import os
import sys
import uuid
from datetime import datetime

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import SessionLocal
from models import RawFeedback


def inject_data():
    db = SessionLocal()

    test_reviews = [
        "I added this dress to my wishlist to buy on payday, but when I checked today it was out of stock. So frustrating, I really wanted it!",
        "Saved these jeans to my wishlist just as a bookmark because I like the style, but they are way too expensive to actually purchase right now.",
        "I have 5 different pairs of sneakers in my wishlist. I'm trying to compare them to find the best one before buying, but the app doesn't have a good comparison feature.",
        "I want to buy this jacket I saved in my wishlist, but I checked YouTube reviews and people say the sizing runs very small. I am scared to buy it and get the wrong fit.",
        "Put this watch in my cart but postponed buying because the delivery fee is ridiculous. I'll just wait until I have a larger order.",
        "I wishlisted this top but I'm waiting for a major sale before I pull the trigger. Full price is a rip off for this quality.",
        "I saw an influencer wear this skirt on Reddit so I saved it to my wishlist. Will definitely buy it for my upcoming vacation!",
        "I use the wishlist strictly for outfit inspiration. I rarely ever buy anything from it.",
        "Added to wishlist because I intend to purchase, but the fabric details were so unclear I had to go to the brand's main website to verify it wasn't polyester.",
        "Why does it clear my wishlist when I reinstall the app? I had all my future purchases saved there and now I can't find them!",
    ]

    for text in test_reviews:
        record = RawFeedback(
            internal_id=str(uuid.uuid4()),
            source="SYNTHETIC_TEST",
            source_id=str(uuid.uuid4()),
            date=datetime.utcnow(),
            text=text,
            rating=3.0,
            category="Test Review",
        )
        db.add(record)

    db.commit()
    db.close()
    print("Successfully injected 10 highly detailed test reviews into the database!")


if __name__ == "__main__":
    inject_data()
