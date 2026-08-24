from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DashboardMetrics(BaseModel):
    total_records_processed: int
    top_opportunities: List[Dict[str, Any]]
    top_themes: List[Dict[str, Any]]

class ThemeSchema(BaseModel):
    theme_name: str
    description: str
    frequency: int
    source_distribution: Dict[str, int]
    supporting_evidence: List[str]

class PaginatedThemes(BaseModel):
    data: List[ThemeSchema]
    total: int
    page: int
    size: int

class OpportunityScore(BaseModel):
    frequency: int
    wishlist_relevance: int
    purchase_impact: int
    user_pain: int
    cross_source_consistency: int
    evidence_confidence: int

class OpportunitySchema(BaseModel):
    opportunity_name: str
    problem: str
    affected_segment: str
    journey_stage: str
    scores: OpportunityScore
    opportunity_score: float
    supporting_evidence: List[str]
    key_uncertainty: str

class WishlistBehaviorSchema(BaseModel):
    total_wishlist_mentions: int
    bookmarking_vs_intent: Dict[str, int]
    postponement_reasons: Dict[str, int]
    by_source: Dict[str, Any]
    by_segment: Dict[str, Any]
    by_theme: Dict[str, Any]

class PurchaseBarrierSchema(BaseModel):
    total_barriers_identified: int
    top_barriers: Dict[str, int]
    top_uncertainties: Dict[str, int]
    by_source: Dict[str, Any]
    by_segment: Dict[str, Any]
    by_theme: Dict[str, Any]
    correlation_with_comparison: int

class ExternalResearchSchema(BaseModel):
    total_external_research_events: int
    information_sought: Dict[str, int]
    alternatives_considered: List[str]
    by_source: Dict[str, Any]
    by_segment: Dict[str, Any]
    by_theme: Dict[str, Any]

class PaginatedEvidence(BaseModel):
    data: List[Dict[str, Any]]
    total: int
    page: int
    size: int
