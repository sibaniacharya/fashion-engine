import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import SessionLocal
from models import NormalizedFeedback, ExtractedSignal


def mock_phase3():
    db = SessionLocal()

    # Process all synthetic test records
    synthetic_records = (
        db.query(NormalizedFeedback)
        .filter(NormalizedFeedback.source == "SYNTHETIC_TEST")
        .all()
    )

    for record in synthetic_records:
        text = record.normalized_text.lower()
        signals = {
            "shopping_intent": "high",
            "wishlist_intent": None,
            "purchase_barrier": None,
            "pain_point": None,
            "uncertainty": None,
            "external_research_behavior": False,
            "comparison_behavior": False,
            "information_sought": None,
            "price_signal": None,
            "fit_size_signal": None,
            "quality_signal": None,
            "styling_signal": None,
            "review_social_validation_signal": None,
            "occasion_signal": None,
            "user_segment": "Gen Z Shopper",
            "theme_candidate": "Wishlist Tracking",
        }

        # Manually map based on keywords to match our injected tests
        if "wishlist to buy on payday" in text:
            signals["wishlist_intent"] = "Save to buy later"
            signals["purchase_barrier"] = "Out of stock"
            signals["pain_point"] = "Inventory availability"
            signals["theme_candidate"] = "Inventory Management"
        elif "bookmark" in text and "expensive" in text:
            signals["wishlist_intent"] = "Bookmarking for inspiration"
            signals["purchase_barrier"] = "Expensive pricing"
            signals["price_signal"] = "Too expensive"
            signals["theme_candidate"] = "Pricing"
        elif "compare them" in text:
            signals["wishlist_intent"] = "Shortlisting for comparison"
            signals["comparison_behavior"] = True
            signals["pain_point"] = "No comparison feature"
            signals["theme_candidate"] = "App Features"
        elif "youtube reviews" in text:
            signals["wishlist_intent"] = "Save to buy later"
            signals["external_research_behavior"] = True
            signals["information_sought"] = "Sizing and fit"
            signals["uncertainty"] = "Scared to get the wrong fit"
            signals["fit_size_signal"] = "Runs small"
            signals["theme_candidate"] = "Sizing Accuracy"
        elif "postponed buying" in text and "delivery fee" in text:
            signals["wishlist_intent"] = "Save to buy later"
            signals["purchase_stage"] = "postponement"
            signals["purchase_barrier"] = "High delivery fee"
            signals["pain_point"] = "Ridiculous delivery fee"
            signals["theme_candidate"] = "Shipping Costs"
        elif "waiting for a major sale" in text:
            signals["wishlist_intent"] = "Wait for sale"
            signals["purchase_stage"] = "postponement"
            signals["purchase_barrier"] = "Full price is a rip off"
            signals["price_signal"] = "Too expensive"
            signals["theme_candidate"] = "Pricing"
        elif "influencer wear this skirt on reddit" in text:
            signals["wishlist_intent"] = "Save to buy later"
            signals["external_research_behavior"] = True
            signals["review_social_validation_signal"] = "Influencer recommendation"
            signals["theme_candidate"] = "Social Proof"
        elif "outfit inspiration" in text:
            signals["wishlist_intent"] = "Bookmarking for inspiration"
            signals["theme_candidate"] = "Inspiration"
        elif "fabric details were so unclear" in text:
            signals["wishlist_intent"] = "Save to buy later"
            signals["external_research_behavior"] = True
            signals["information_sought"] = "Fabric material"
            signals["uncertainty"] = "Is it polyester?"
            signals["theme_candidate"] = "Product Details"
        elif "clears my wishlist" in text:
            signals["wishlist_intent"] = "Save to buy later"
            signals["purchase_barrier"] = "Wishlist wiped on reinstall"
            signals["pain_point"] = "Lost saved items"
            signals["theme_candidate"] = "App Bugs"
        else:
            signals["wishlist_intent"] = "Save to buy later"
            signals["theme_candidate"] = "General"

        existing = (
            db.query(ExtractedSignal)
            .filter(ExtractedSignal.raw_id == record.raw_id)
            .first()
        )
        if existing:
            existing.signals = signals
        else:
            extracted = ExtractedSignal(
                raw_id=record.raw_id, signals=signals, processed_at=datetime.utcnow()
            )
            db.add(extracted)

    db.commit()
    print(f"Mocked Phase 3 extraction for {len(synthetic_records)} records!")

    # Export all ExtractedSignals to JSON
    all_signals = db.query(ExtractedSignal).all()
    out_list = []

    for sig in all_signals:
        norm = (
            db.query(NormalizedFeedback)
            .filter(NormalizedFeedback.raw_id == sig.raw_id)
            .first()
        )
        out_list.append(
            {
                "raw_id": sig.raw_id,
                "source": norm.source if norm else "UNKNOWN",
                "text": norm.normalized_text if norm else "",
                "extracted_signals": sig.signals,
            }
        )

    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "analyzed")
    )
    os.makedirs(output_dir, exist_ok=True)
    with open(
        os.path.join(output_dir, "phase3_signals.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(out_list, f, indent=2, ensure_ascii=False)

    db.close()
    print(f"Exported {len(out_list)} records to phase3_signals.json")


if __name__ == "__main__":
    mock_phase3()
