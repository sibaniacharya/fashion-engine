export interface DataQuality {
    raw: number;
    valid: number;
    eligible: number;
    llm_analyzed: number;
    fallback_analyzed: number;
    failed: number;
    deferred_rate_limit: number;
    deferred_quota: number;
    source_coverage: {
        [key: string]: {
            eligible?: number;
            analyzed_llm?: number;
            analyzed_fallback?: number;
            failed?: number;
            deferred_rate_limit?: number;
            deferred_quota?: number;
            status?: string;
        }
    };
}

export interface WishlistCounts {
    EXPLICIT_WISHLIST: number;
    EXPLICIT_PURCHASE_INTENT: number;
    GENERAL_PRODUCT_INTEREST: number;
    PURCHASE_EVALUATION: number;
    COMPARISON: number;
    POSTPONEMENT: number;
    ABANDONMENT: number;
    BOOKMARKING: number;
    UNKNOWN: number;
}

export interface WishlistBehavior {
    total_analyzed: number;
    bookmarking_vs_intent: WishlistCounts;
}

export interface EvidenceRecord {
    quote: string;
    source: string;
    trace_id: string;
    date: string;
    explanation?: string;
}

export interface Theme {
    theme_name: string;
    description: string;
    frequency: number;
    unique_records: number;
    source_coverage: number;
    evidence_confidence: string;
    source_distribution: Record<string, number>;
    supporting_evidence: EvidenceRecord[];
    is_fallback: boolean;
}

export interface Opportunity {
    opportunity_name: string;
    problem: string;
    structured_statement: string;
    affected_segment: string;
    journey_stage: string;
    classification: string;
    opportunity_score: number;
    supporting_evidence: EvidenceRecord[];
    scores?: {
        frequency: number;
        wishlist_relevance: number;
        purchase_impact: number;
        user_pain: number;
        cross_source_consistency: number;
        evidence_confidence: number;
    }
}
