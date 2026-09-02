import json
import os
import uuid


def patch_json():
    filepath = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "analyzed",
            "phase3_signals.json",
        )
    )

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    fake_reviews = [
        (
            "I added this dress to my wishlist to buy on payday, but when I checked today it was out of stock. So frustrating, I really wanted it!",
            "Save to buy later",
            "Out of stock",
            "Inventory availability",
            "Inventory Management",
            False,
            None,
        ),
        (
            "Saved these jeans to my wishlist just as a bookmark because I like the style, but they are way too expensive to actually purchase right now.",
            "Bookmarking for inspiration",
            "Expensive pricing",
            None,
            "Pricing",
            False,
            None,
        ),
        (
            "I have 5 different pairs of sneakers in my wishlist. I'm trying to compare them to find the best one before buying, but the app doesn't have a good comparison feature.",
            "Shortlisting for comparison",
            None,
            "No comparison feature",
            "App Features",
            True,
            None,
        ),
        (
            "I want to buy this jacket I saved in my wishlist, but I checked YouTube reviews and people say the sizing runs very small. I am scared to buy it and get the wrong fit.",
            "Save to buy later",
            None,
            None,
            "Sizing Accuracy",
            False,
            True,
        ),
        (
            "Put this watch in my cart but postponed buying because the delivery fee is ridiculous. I'll just wait until I have a larger order.",
            "Save to buy later",
            "High delivery fee",
            "Ridiculous delivery fee",
            "Shipping Costs",
            False,
            None,
        ),
        (
            "I wishlisted this top but I'm waiting for a major sale before I pull the trigger. Full price is a rip off for this quality.",
            "Wait for sale",
            "Full price is a rip off",
            None,
            "Pricing",
            False,
            None,
        ),
        (
            "I saw an influencer wear this skirt on Reddit so I saved it to my wishlist. Will definitely buy it for my upcoming vacation!",
            "Save to buy later",
            None,
            None,
            "Social Proof",
            False,
            True,
        ),
        (
            "I use the wishlist strictly for outfit inspiration. I rarely ever buy anything from it.",
            "Bookmarking for inspiration",
            None,
            None,
            "Inspiration",
            False,
            None,
        ),
        (
            "Added to wishlist because I intend to purchase, but the fabric details were so unclear I had to go to the brand's main website to verify it wasn't polyester.",
            "Save to buy later",
            None,
            None,
            "Product Details",
            False,
            True,
        ),
        (
            "Why does it clear my wishlist when I reinstall the app? I had all my future purchases saved there and now I can't find them!",
            "Save to buy later",
            "Wishlist wiped on reinstall",
            "Lost saved items",
            "App Bugs",
            False,
            None,
        ),
    ]

    for text, w_intent, barrier, pain, theme, comp, ext_research in fake_reviews:
        data.append(
            {
                "raw_id": str(uuid.uuid4()),
                "source": "SYNTHETIC_TEST",
                "text": text.lower(),
                "extracted_signals": {
                    "shopping_intent": "high",
                    "wishlist_intent": w_intent,
                    "purchase_barrier": barrier,
                    "pain_point": pain,
                    "uncertainty": "Scared to get the wrong fit"
                    if "youtube" in text
                    else None,
                    "external_research_behavior": bool(ext_research),
                    "comparison_behavior": bool(comp),
                    "information_sought": "Sizing and fit"
                    if "youtube" in text
                    else None,
                    "price_signal": "Too expensive"
                    if "expensive" in text or "sale" in text
                    else None,
                    "fit_size_signal": "Runs small" if "youtube" in text else None,
                    "quality_signal": None,
                    "styling_signal": None,
                    "review_social_validation_signal": "Influencer recommendation"
                    if "reddit" in text
                    else None,
                    "occasion_signal": None,
                    "user_segment": "Gen Z Shopper",
                    "theme_candidate": theme,
                    "purchase_stage": "postponement"
                    if "postponed" in text or "waiting" in text
                    else "evaluation",
                },
            }
        )

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Patched JSON! Now contains {len(data)} records.")


if __name__ == "__main__":
    patch_json()
