from pydantic import BaseModel, Field
from typing import Optional

class AISignalSchema(BaseModel):
    user_segment: Optional[str] = Field(None, description="The segment of the user (e.g., deal seeker, fashion enthusiast). Null if unknown.")
    shopping_intent: Optional[str] = Field(None, description="Why they are shopping (e.g., browsing, searching for specific item, gifting). Null if unknown.")
    wishlist_intent: Optional[str] = Field(None, description="Why they wishlisted an item (e.g., waiting for price drop, comparing). Null if unknown.")
    purchase_stage: Optional[str] = Field(None, description="Stage in funnel (e.g., awareness, consideration, decision). Null if unknown.")
    pain_point: Optional[str] = Field(None, description="Any specific frustration or pain point mentioned. Null if unknown.")
    uncertainty: Optional[str] = Field(None, description="Doubt or confusion holding them back (e.g., size fit, color accuracy). Null if unknown.")
    purchase_barrier: Optional[str] = Field(None, description="A strict blocker preventing purchase (e.g., out of stock, shipping cost, no return policy). Null if unknown.")
    information_sought: Optional[str] = Field(None, description="Information they are explicitly looking for. Null if unknown.")
    comparison_behavior: Optional[str] = Field(None, description="Mention of comparing with other brands or products. Null if unknown.")
    fit_size_signal: Optional[str] = Field(None, description="Specific feedback about fit or sizing. Null if unknown.")
    styling_signal: Optional[str] = Field(None, description="Feedback about how to style or wear the item. Null if unknown.")
    price_signal: Optional[str] = Field(None, description="Feedback regarding pricing, discounts, or value for money. Null if unknown.")
    quality_signal: Optional[str] = Field(None, description="Feedback regarding fabric, stitching, or material quality. Null if unknown.")
    review_social_validation_signal: Optional[str] = Field(None, description="Mentions of relying on reviews, ratings, or influencers. Null if unknown.")
    occasion_signal: Optional[str] = Field(None, description="Specific event or occasion they are shopping for. Null if unknown.")
    external_research_behavior: Optional[str] = Field(None, description="Searching elsewhere like YouTube or Reddit before buying. Null if unknown.")
    theme_candidate: Optional[str] = Field(None, description="A 1-3 word high level theme categorizing this review. Null if unknown.")
    evidence_strength: Optional[str] = Field(None, description="Strength of the signal: 'strong', 'moderate', or 'weak'. Null if unknown.")
