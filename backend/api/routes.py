from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from .deps import get_analyzed_data
from .schemas import (
    DashboardMetrics, ThemeSchema, PaginatedThemes, OpportunitySchema, 
    WishlistBehaviorSchema, PurchaseBarrierSchema, ExternalResearchSchema,
    PaginatedEvidence
)

router = APIRouter()

def paginate(data: list, page: int, size: int) -> dict:
    start = (page - 1) * size
    end = start + size
    return {
        "data": data[start:end],
        "total": len(data),
        "page": page,
        "size": size
    }

@router.get("/dashboard", response_model=DashboardMetrics)
def get_dashboard():
    # Load primary datasets
    themes = get_analyzed_data("themes.json")
    opps = get_analyzed_data("opportunities.json")
    signals = get_analyzed_data("phase3_signals.json")
    
    # Safe fallback if lists are empty
    top_themes = sorted(themes, key=lambda x: x.get("frequency", 0), reverse=True)[:3] if isinstance(themes, list) else []
    top_opps = sorted(opps, key=lambda x: x.get("opportunity_score", 0), reverse=True)[:3] if isinstance(opps, list) else []
    
    return DashboardMetrics(
        total_records_processed=len(signals) if isinstance(signals, list) else 0,
        top_themes=top_themes,
        top_opportunities=top_opps
    )

@router.get("/themes", response_model=PaginatedThemes)
def get_themes(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    data = get_analyzed_data("themes.json")
    if not isinstance(data, list):
        data = []
    return paginate(data, page, size)

@router.get("/opportunities", response_model=List[OpportunitySchema])
def get_opportunities():
    # Return all ranked opportunities, no pagination needed as they are highly aggregated
    data = get_analyzed_data("opportunities.json")
    if not isinstance(data, list):
        data = []
    return data

@router.get("/wishlist-behavior", response_model=WishlistBehaviorSchema)
def get_wishlist_behavior():
    return get_analyzed_data("wishlist_behavior.json")

@router.get("/purchase-barriers", response_model=PurchaseBarrierSchema)
def get_purchase_barriers():
    return get_analyzed_data("purchase_barriers.json")

@router.get("/external-research", response_model=ExternalResearchSchema)
def get_external_research():
    return get_analyzed_data("external_information_seeking.json")

@router.get("/data-quality")
def get_data_quality():
    return get_analyzed_data("data_quality_report.json")

@router.get("/segments")
def get_segments():
    # Helper to return unique segments
    data = get_analyzed_data("phase3_signals.json")
    segments = set()
    if isinstance(data, list):
        for r in data:
            ext = r.get("extracted_signals", {})
            seg = ext.get("user_segment")
            if seg:
                segments.add(seg)
    return {"segments": list(segments)}

@router.get("/sources")
def get_sources():
    # Helper to return unique sources
    data = get_analyzed_data("phase3_signals.json")
    sources = set()
    if isinstance(data, list):
        for r in data:
            src = r.get("source")
            if src:
                sources.add(src)
    return {"sources": list(sources)}

@router.get("/evidence", response_model=PaginatedEvidence)
def get_evidence(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), source: str = None):
    # Returns raw signals for detailed evidence tracing
    data = get_analyzed_data("phase3_signals.json")
    if not isinstance(data, list):
        data = []
        
    if source:
        data = [r for r in data if r.get("source") == source]
        
    return paginate(data, page, size)

@router.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
