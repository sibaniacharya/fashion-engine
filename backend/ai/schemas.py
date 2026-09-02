from pydantic import BaseModel, Field
from typing import Literal


class AISignalSchema(BaseModel):
    user_segment: Literal[
        "COMPARISON_SHOPPER",
        "FIT_CONSCIOUS",
        "QUALITY_CONSCIOUS",
        "VALUE_CONSCIOUS",
        "FREQUENT_SHOPPER",
        "UNKNOWN",
    ] = Field(
        description="Behavioral segment of the user. Only use if explicit evidence exists, otherwise use 'UNKNOWN'. Do NOT infer demographics."
    )

    shopping_intent: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Does this text explicitly state why they are shopping (e.g., gifting, browsing)?"
    )
    wishlist_intent: Literal[
        "EXPLICIT_WISHLIST",
        "EXPLICIT_PURCHASE_INTENT",
        "GENERAL_PRODUCT_INTEREST",
        "PURCHASE_EVALUATION",
        "COMPARISON",
        "POSTPONEMENT",
        "ABANDONMENT",
        "BOOKMARKING",
        "UNKNOWN",
    ] = Field(
        description="Why they added to wishlist. Use 'UNKNOWN' if not explicitly stated."
    )
    purchase_stage: Literal[
        "DISCOVERY", "EVALUATION", "POSTPONEMENT", "POST_PURCHASE", "UNKNOWN"
    ] = Field(description="Current stage in the funnel.")

    pain_point: str = Field(
        description="Any specific frustration or pain point mentioned. Use 'UNKNOWN' if no evidence."
    )
    uncertainty: str = Field(
        description="Doubt or confusion holding them back (e.g., size fit, color accuracy). Use 'UNKNOWN' if no evidence."
    )
    purchase_barrier: str = Field(
        description="A strict blocker preventing purchase (e.g., expensive pricing, delivery fee). Use 'UNKNOWN' if no evidence."
    )
    information_sought: str = Field(
        description="Information they are explicitly looking for. Use 'UNKNOWN' if no evidence."
    )
    comparison_behavior: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Mention of comparing with other brands or products."
    )

    fit_size_signal: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Specific feedback about fit or sizing."
    )
    styling_signal: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Feedback about how to style or wear the item."
    )
    price_signal: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Feedback regarding pricing, discounts, or value for money."
    )
    quality_signal: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Feedback regarding fabric, stitching, or material quality."
    )
    social_validation_signal: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Mentions of relying on reviews, ratings, or influencers."
    )
    occasion_signal: Literal["YES", "NO", "UNKNOWN"] = Field(
        description="Specific event or occasion they are shopping for."
    )
    external_research_behavior: Literal[
        "EXPLICIT_RESEARCH", "IMPLIED_RESEARCH", "NO_EVIDENCE", "UNKNOWN"
    ] = Field(description="Searching elsewhere like YouTube or Reddit before buying.")

    theme_candidate: str = Field(
        description="A 1-3 word high level theme categorizing this review. Use 'UNKNOWN' if no evidence."
    )
    evidence_strength: Literal["STRONG", "MODERATE", "WEAK", "UNKNOWN"] = Field(
        description="Strength of the signal."
    )
