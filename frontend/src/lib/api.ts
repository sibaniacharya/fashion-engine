export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

/**
 * Shared fetcher that safely catches all 404s/500s and returns a fallback structure.
 */
async function fetchSafe<T>(endpoint: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, { cache: 'no-store' });
    if (!res.ok) {
      console.error(`API Error on ${endpoint}: ${res.statusText}`);
      return fallback;
    }
    const data = await res.json();
    return data as T;
  } catch (error) {
    console.error(`Network Error on ${endpoint}:`, error);
    return fallback;
  }
}

// ---------------------------------------------------------
// EXPLICIT RESPONSE TYPES MATCHING BACKEND CONTRACT
// ---------------------------------------------------------

export interface DashboardMetrics {
  total_records_processed: number;
  top_opportunities: any[];
  top_themes: any[];
}

export interface DataQuality {
  raw: number;
  valid: number;
  eligible: number;
  llm_analyzed: number;
  fallback_analyzed: number;
  failed: number;
  deferred_rate_limit: number;
  deferred_quota: number;
  duplicates?: number;
  spam?: number;
  other_exclusions?: number;
  empty_content?: number;
  non_english?: number;
  source_coverage: Record<string, any>;
}

export interface PaginatedThemes {
  data: any[];
  total: number;
  page: number;
  size: number;
  message?: string;
}

export interface PaginatedEvidence {
  data: any[];
  total: number;
  page: number;
  size: number;
}

export interface WishlistBehavior {
  total_valid_records: number;
  total_wishlist_mentions: number;
  bookmarking_vs_intent: Record<string, number>;
  postponement_reasons: Record<string, number>;
  by_source: Record<string, any>;
  by_segment: Record<string, any>;
  by_theme: Record<string, any>;
}

export interface PurchaseBarriers {
  total_barriers_identified: number;
  top_barriers: Record<string, any>;
  top_uncertainties: Record<string, number>;
  by_source: Record<string, any>;
  by_segment: Record<string, any>;
  by_theme: Record<string, any>;
  correlation_with_comparison: number;
}

export interface ExternalResearch {
  total_external_research_events: number;
  research_types: Record<string, number>;
  information_sought: Record<string, number>;
  alternatives_considered: string[];
  by_source: Record<string, any>;
  by_segment: Record<string, any>;
  by_theme: Record<string, any>;
}

export interface UserSegments {
  total_records_classified: number;
  segments: Record<string, any>;
}

// ---------------------------------------------------------
// API CLIENT
// ---------------------------------------------------------

export const ApiClient = {
  getDashboard: () => fetchSafe<DashboardMetrics>('/dashboard', {
    total_records_processed: 0, top_opportunities: [], top_themes: []
  }),

  getDataQuality: () => fetchSafe<DataQuality>('/data-quality', {
    raw: 0, valid: 0, eligible: 0, llm_analyzed: 0, fallback_analyzed: 0,
    failed: 0, deferred_rate_limit: 0, deferred_quota: 0, source_coverage: {}
  }),

  getThemes: (page = 1, size = 10) => fetchSafe<PaginatedThemes>(`/themes?page=${page}&size=${size}`, {
    data: [], total: 0, page: 1, size: 10, message: "Insufficient evidence to identify reliable recurring themes from the currently analyzed records."
  }),

  getWishlistBehavior: () => fetchSafe<WishlistBehavior>('/wishlist-behavior', {
    total_valid_records: 0, total_wishlist_mentions: 0, bookmarking_vs_intent: {},
    postponement_reasons: {}, by_source: {}, by_segment: {}, by_theme: {}
  }),

  getPurchaseBarriers: () => fetchSafe<PurchaseBarriers>('/purchase-barriers', {
    total_barriers_identified: 0, top_barriers: {}, top_uncertainties: {},
    by_source: {}, by_segment: {}, by_theme: {}, correlation_with_comparison: 0
  }),

  getExternalResearch: () => fetchSafe<ExternalResearch>('/external-research', {
    total_external_research_events: 0, research_types: {}, information_sought: {},
    alternatives_considered: [], by_source: {}, by_segment: {}, by_theme: {}
  }),

  getSegments: () => fetchSafe<UserSegments>('/segments', {
    total_records_classified: 0, segments: {}
  }),

  getOpportunities: () => fetchSafe<any[]>('/opportunities', []),

  getEvidence: (page = 1, size = 20) => fetchSafe<PaginatedEvidence>(`/evidence?page=${page}&size=${size}`, {
    data: [], total: 0, page: 1, size: 20
  })
};
