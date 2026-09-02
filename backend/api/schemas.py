from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class DashboardMetrics(BaseModel):
    total_records_processed: int
    top_opportunities: List[Dict[str, Any]]
    top_themes: List[Dict[str, Any]]


class ThemeSchema(BaseModel):
    theme_name: str
    description: str
    unique_record_count: Optional[int] = None
    frequency: int
    percentage_of_analyzed_records: Optional[float] = None
    google_play_count: Optional[int] = None
    youtube_count: Optional[int] = None
    source_coverage: Optional[int] = None
    evidence_confidence: Optional[str] = None
    representative_quotes: Optional[List[Dict[str, Any]]] = None
    source_distribution: Dict[str, int]
    supporting_evidence: List[Dict[str, Any]]


class PaginatedThemes(BaseModel):
    data: List[ThemeSchema]
    total: int
    page: int
    size: int
    message: Optional[str] = None


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
    structured_statement: Optional[str]
    affected_segment: str
    journey_stage: str
    scores: OpportunityScore
    opportunity_score: float
    supporting_evidence: List[Dict[str, Any]]


class WishlistBehaviorSchema(BaseModel):
    total_valid_records: int
    total_wishlist_mentions: int
    bookmarking_vs_intent: Dict[str, int]
    postponement_reasons: Dict[str, int]
    by_source: Dict[str, Any]
    by_segment: Dict[str, Any]
    by_theme: Dict[str, Any]


class PurchaseBarrierSchema(BaseModel):
    total_barriers_identified: int
    top_barriers: Dict[str, Any]
    top_uncertainties: Dict[str, int]
    by_source: Dict[str, Any]
    by_segment: Dict[str, Any]
    by_theme: Dict[str, Any]
    correlation_with_comparison: int


class ExternalResearchSchema(BaseModel):
    total_external_research_events: int
    research_types: Dict[str, int]
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
