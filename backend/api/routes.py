from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from collections import defaultdict
from .deps import get_analyzed_data
from .schemas import (
    DashboardMetrics,
    ThemeSchema,
    PaginatedThemes,
    OpportunitySchema,
    WishlistBehaviorSchema,
    PurchaseBarrierSchema,
    ExternalResearchSchema,
    PaginatedEvidence,
)
from ai.analyzer import BehaviorAnalyzer
from ai.opportunity_scorer import OpportunityScorer

router = APIRouter()


def paginate(data: list, page: int, size: int) -> dict:
    start = (page - 1) * size
    end = start + size
    return {"data": data[start:end], "total": len(data), "page": page, "size": size}


def _get_canonical_records():
    records = get_analyzed_data("analysis_records.json")
    if not isinstance(records, list):
        return []
    return [
        r
        for r in records
        if r.get("analysis_status") in ["ANALYZED", "ANALYZED_FALLBACK"]
    ]


def _get_themes():
    import os
    import json

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    themes_path = os.path.join(base_dir, "output", "themes.json")

    if not os.path.exists(themes_path):
        return []

    with open(themes_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_opportunities():
    import os
    import json

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    opps_path = os.path.join(base_dir, "output", "opportunities.json")

    if not os.path.exists(opps_path):
        return []

    with open(opps_path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/dashboard", response_model=DashboardMetrics)
def get_dashboard():
    records = _get_canonical_records()
    themes = _get_themes()
    opps = _get_opportunities()

    top_themes = themes[:3] if isinstance(themes, list) else []
    top_opps = (
        sorted(opps, key=lambda x: x.get("opportunity_score", 0), reverse=True)[:3]
        if isinstance(opps, list)
        else []
    )

    return DashboardMetrics(
        total_records_processed=len(records),
        top_themes=top_themes,
        top_opportunities=top_opps,
    )


@router.get("/themes", response_model=PaginatedThemes)
def get_themes(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    data = _get_themes()
    result = paginate(data, page, size)
    if len(data) == 0:
        result[
            "message"
        ] = "Insufficient evidence to identify reliable recurring themes from the currently analyzed records."
    return result


@router.get("/opportunities", response_model=List[OpportunitySchema])
def get_opportunities():
    return _get_opportunities()


@router.get("/wishlist-behavior", response_model=WishlistBehaviorSchema)
def get_wishlist_behavior():
    analyzer = BehaviorAnalyzer(_get_canonical_records())
    return analyzer.analyze_wishlist_behavior()


@router.get("/purchase-barriers", response_model=PurchaseBarrierSchema)
def get_purchase_barriers():
    analyzer = BehaviorAnalyzer(_get_canonical_records())
    return analyzer.analyze_purchase_barriers()


@router.get("/external-research", response_model=ExternalResearchSchema)
def get_external_research():
    analyzer = BehaviorAnalyzer(_get_canonical_records())
    return analyzer.analyze_external_research()


@router.get("/data-quality")
def get_data_quality():
    # Load base raw numbers from pipeline_metadata
    metadata = get_analyzed_data("pipeline_metadata.json")
    if not isinstance(metadata, dict):
        metadata = {}

    exclusions = metadata.get("exclusion_breakdown", {})
    raw = metadata.get("raw_records", 0)
    valid = metadata.get("valid_records", 0)

    return {
        "raw": raw,
        "valid": valid,
        "eligible": metadata.get("eligible_records", 0),
        "llm_analyzed": metadata.get("llm_analyzed", 0),
        "fallback_analyzed": metadata.get("fallback_analyzed", 0),
        "failed": metadata.get("failed", 0),
        "deferred_rate_limit": metadata.get("deferred_rate_limit", 0),
        "deferred_quota": metadata.get("deferred_quota", 0),
        "duplicates": exclusions.get("duplicates", 0),
        "spam": exclusions.get("spam", 0),
        "other_exclusions": exclusions.get("other", 0),
        "empty_content": exclusions.get("empty_content", 0),
        "non_english": exclusions.get("non_english", 0),
        "source_coverage": metadata.get(
            "sources",
            {
                "Google Play": {
                    "eligible": 0,
                    "analyzed": 0,
                    "failed": 0,
                    "deferred": 0,
                },
                "YouTube": {"eligible": 0, "analyzed": 0, "failed": 0, "deferred": 0},
                "Reddit": {"status": "NOT CONFIGURED"},
            },
        ),
    }


@router.get("/segments")
def get_segments():
    analyzer = BehaviorAnalyzer(_get_canonical_records())
    return analyzer.analyze_user_segments()


@router.get("/sources")
def get_sources():
    data = get_analyzed_data("analysis_records.json")
    sources = set()
    if isinstance(data, list):
        for r in data:
            src = r.get("source")
            if src:
                sources.add(src)
    return {"sources": list(sources)}


@router.get("/evidence", response_model=PaginatedEvidence)
def get_evidence(
    page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), source: str = None
):
    data = _get_canonical_records()
    if source:
        data = [r for r in data if r.get("source") == source]

    return paginate(data, page, size)


@router.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
