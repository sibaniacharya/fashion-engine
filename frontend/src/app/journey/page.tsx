'use client';
import { useEffect, useState } from 'react';
import { ApiClient, WishlistBehavior, PurchaseBarriers, ExternalResearch } from '@/lib/api';

const WISHLIST_LABELS: Record<string, string> = {
  EXPLICIT_WISHLIST: "Explicit wishlist behavior",
  EXPLICIT_PURCHASE_INTENT: "Explicit purchase intent",
  GENERAL_PRODUCT_INTEREST: "General product interest",
  PURCHASE_EVALUATION: "Purchase evaluation",
  COMPARISON: "Comparison behavior",
  POSTPONEMENT: "Purchase postponement",
  ABANDONMENT: "Purchase abandonment",
  BOOKMARKING: "Bookmarking behavior",
  UNKNOWN: "Unknown intent"
};

export default function Journey() {
  const [wishlist, setWishlist] = useState<WishlistBehavior | null>(null);
  const [barriers, setBarriers] = useState<PurchaseBarriers | null>(null);
  const [research, setResearch] = useState<ExternalResearch | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      ApiClient.getWishlistBehavior(),
      ApiClient.getPurchaseBarriers(),
      ApiClient.getExternalResearch()
    ]).then(([w, b, r]) => {
      setWishlist(w);
      setBarriers(b);
      setResearch(r);
      setLoading(false);
    }).catch(e => console.error(e));
  }, []);

  if (loading) return <div>Loading...</div>;

  const validRecords = wishlist?.total_valid_records || 1;
  const explicitIntent = wishlist?.bookmarking_vs_intent?.EXPLICIT_PURCHASE_INTENT || 0;
  const explicitWishlist = wishlist?.bookmarking_vs_intent?.EXPLICIT_WISHLIST || 0;
  const intentPercentage = Math.round((explicitIntent / validRecords) * 100);

  return (
    <div>
      <h1 className="gradient-text">Journey Analytics</h1>
      <p>Tracking the Wishlist-to-Purchase Funnel</p>

      <div className="grid-2" style={{ marginTop: '32px' }}>
        <div className="glass-card">
          <h2>Why Users Wishlist</h2>
          <p style={{ fontSize: '0.85rem', marginBottom: '16px', color: 'var(--text-secondary)' }}>
            {explicitIntent} of {validRecords} valid records ({intentPercentage}%) contain explicit purchase-intent signals.
          </p>
          {explicitWishlist === 0 && explicitIntent === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>
              No explicit wishlist or purchase intent signals exist in this dataset. Public feedback contains limited direct wishlist evidence.
            </p>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              {Object.entries(wishlist?.bookmarking_vs_intent || {}).map(([intentKey, count]: any) => (
                <div key={intentKey}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>{count}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{WISHLIST_LABELS[intentKey] || intentKey}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="glass-card">
          <h2>Aggregated Purchase Barriers</h2>
          <p style={{ fontSize: '0.85rem', marginBottom: '16px', color: 'var(--text-secondary)' }}>
            Top reasons users abandon or postpone purchases.
          </p>
          {barriers?.top_barriers && Object.keys(barriers.top_barriers).length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {Object.entries(barriers.top_barriers).map(([b, data]: any) => (
                <div key={b} style={{ padding: '12px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong>{b}</strong>
                    <span className="badge badge-violet">{data.percentage_of_relevant}% of barriers</span>
                  </div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                    {data.total_mentions} total mentions across {data.unique_supporting_records} unique records.
                  </div>
                  {data.representative_quotes && data.representative_quotes.length > 0 && (
                     <p style={{ fontSize: '0.8rem', fontStyle: 'italic', marginTop: '8px', color: '#ccc' }}>
                       "{data.representative_quotes[0]}"
                     </p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p>No postponement barriers explicitly logged in this dataset.</p>
          )}
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: '24px' }}>
        <div className="glass-card">
          <h2>External Information Seeking</h2>
          <p style={{ fontSize: '0.85rem', marginBottom: '16px', color: 'var(--text-secondary)' }}>
            Behavior indicating external research outside the platform.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
             {Object.entries(research?.research_types || {}).map(([type, count]: any) => (
                <div key={type}>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--accent-violet)' }}>{count}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{type}</div>
                </div>
             ))}
          </div>

          <h3 style={{ fontSize: '0.9rem', marginTop: '16px' }}>Alternatives Considered</h3>
          {research?.alternatives_considered && research.alternatives_considered.length > 0 ? (
            <ul style={{ paddingLeft: '16px', color: 'var(--text-secondary)' }}>
              {research.alternatives_considered.map((alt: string, i: number) => (
                <li key={i}>{alt}</li>
              ))}
            </ul>
          ) : (
             <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic', fontSize: '0.85rem' }}>No external alternatives found.</p>
          )}
        </div>

        <div className="glass-card">
          <h2>User Segments Affected</h2>
          <ul style={{ paddingLeft: '16px', color: 'var(--text-secondary)' }}>
             {barriers?.by_segment && Object.keys(barriers.by_segment).map((seg: string, i: number) => (
               <li key={i}>{seg}</li>
             ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
