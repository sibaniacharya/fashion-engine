'use client';
import { useEffect, useState } from 'react';
import MetricCard from '@/components/MetricCard';
import OpportunityCard from '@/components/OpportunityCard';
import { ApiClient, DashboardMetrics, DataQuality, PaginatedThemes, WishlistBehavior, PurchaseBarriers, ExternalResearch, UserSegments } from '@/lib/api';

export default function Overview() {
  const [data, setData] = useState<DashboardMetrics | null>(null);
  const [quality, setQuality] = useState<DataQuality | null>(null);
  const [themes, setThemes] = useState<PaginatedThemes | null>(null);
  const [wishlist, setWishlist] = useState<WishlistBehavior | null>(null);
  const [barriers, setBarriers] = useState<PurchaseBarriers | null>(null);
  const [research, setResearch] = useState<ExternalResearch | null>(null);
  const [segments, setSegments] = useState<UserSegments | null>(null);
  const [opportunities, setOpportunities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      ApiClient.getDashboard(),
      ApiClient.getDataQuality(),
      ApiClient.getThemes(),
      ApiClient.getWishlistBehavior(),
      ApiClient.getPurchaseBarriers(),
      ApiClient.getExternalResearch(),
      ApiClient.getSegments(),
      ApiClient.getOpportunities()
    ]).then(([d, q, t, w, b, r, s, o]) => {
      setData(d);
      setQuality(q);
      setThemes(t);
      setWishlist(w);
      setBarriers(b);
      setResearch(r);
      setSegments(s);
      setOpportunities(o);
      setLoading(false);
    }).catch(e => console.error(e));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="gradient-text">Cross-Source Discovery Analysis</h1>
      <p>Identify recurring behavioral patterns and opportunity areas from Google Play and YouTube.</p>

      {/* LIMITATIONS BANNER */}
      <div style={{ backgroundColor: 'rgba(255, 100, 100, 0.1)', borderLeft: '4px solid #ff4d4d', padding: '16px', marginTop: '24px', borderRadius: '4px' }}>
        <h3 style={{ color: '#ff4d4d', fontSize: '1rem', margin: '0 0 8px 0' }}>Discovery Limitations</h3>
        <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          <li>Google Play contains many app-level complaints and may have limited explicit wishlist behavior.</li>
          <li>YouTube comments may have different sampling bias toward visual/styling feedback.</li>
          <li>Absence of evidence is not evidence of absence (e.g. users may comparison shop without explicitly mentioning it).</li>
          <li>Reddit is NOT included (API access unavailable).</li>
        </ul>
      </div>

      {/* 1. SOURCE OVERVIEW & DATA QUALITY */}
      <div className="glass-card" style={{ marginTop: '24px', padding: '16px' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>1. Data Quality & Pipeline Status</h2>
        <div style={{ display: 'flex', gap: '32px', fontSize: '0.9rem', flexWrap: 'wrap', marginBottom: '24px' }}>
          <div><strong>Raw:</strong> {quality?.raw || 0}</div>
          <div><strong>Valid:</strong> {quality?.valid || 0}</div>
          <div><strong>Eligible:</strong> {quality?.eligible || 0}</div>
        </div>

        <h3 style={{ fontSize: '1rem', marginTop: '16px', marginBottom: '12px' }}>Other/Filtered Breakdown</h3>
        <div style={{ display: 'flex', gap: '32px', fontSize: '0.9rem', flexWrap: 'wrap', marginBottom: '24px', padding: '12px', background: 'rgba(255,255,255,0.05)', borderRadius: '6px' }}>
          <div style={{ color: 'var(--text-secondary)' }}><strong>Duplicates Removed:</strong> {quality?.duplicates || 0}</div>
          <div style={{ color: 'var(--text-secondary)' }}><strong>Spam Removed:</strong> {quality?.spam || 0}</div>
          <div style={{ color: 'var(--text-secondary)' }}><strong>Empty Content:</strong> {quality?.empty_content || 0}</div>
          <div style={{ color: 'var(--text-secondary)' }}><strong>Non-English:</strong> {quality?.non_english || 0}</div>
          <div style={{ color: 'var(--text-secondary)' }}><strong>Other Exclusions:</strong> {quality?.other_exclusions || 0}</div>
        </div>
        <div style={{ display: 'flex', gap: '32px', fontSize: '0.9rem', flexWrap: 'wrap', marginBottom: '24px' }}>
          <div style={{ color: 'var(--accent-cyan)' }}><strong>LLM Analyzed:</strong> {quality?.llm_analyzed || 0}</div>
          <div style={{ color: 'var(--accent-cyan)' }}><strong>Fallback Analyzed:</strong> {quality?.fallback_analyzed || 0}</div>
          <div style={{ color: '#ff4d4d' }}><strong>Failed:</strong> {quality?.failed || 0}</div>
          <div style={{ color: '#ffa500' }}><strong>Deferred (Rate Limit):</strong> {quality?.deferred_rate_limit || 0}</div>
          <div style={{ color: '#ffa500' }}><strong>Deferred (Quota):</strong> {quality?.deferred_quota || 0}</div>
        </div>

        <h3 style={{ fontSize: '1rem', marginTop: '16px', marginBottom: '12px' }}>Source Coverage</h3>
        <div style={{ display: 'flex', gap: '32px', fontSize: '0.9rem', flexWrap: 'wrap' }}>
          <div>
            <strong style={{ color: 'var(--accent-cyan)' }}>Google Play</strong>
            <div style={{ marginTop: '4px' }}>Eligible: {quality?.source_coverage?.['GOOGLE_PLAY']?.eligible || 0}</div>
            <div style={{ marginTop: '4px' }}>Analyzed: {quality?.source_coverage?.['GOOGLE_PLAY']?.analyzed || 0}</div>
            <div style={{ marginTop: '4px' }}>Deferred: {quality?.source_coverage?.['GOOGLE_PLAY']?.deferred || 0}</div>
          </div>
          <div>
            <strong style={{ color: 'var(--accent-cyan)' }}>YouTube</strong>
            <div style={{ marginTop: '4px' }}>Eligible: {quality?.source_coverage?.['YOUTUBE']?.eligible || 0}</div>
            <div style={{ marginTop: '4px' }}>Analyzed: {quality?.source_coverage?.['YOUTUBE']?.analyzed || 0}</div>
            <div style={{ marginTop: '4px' }}>Deferred: {quality?.source_coverage?.['YOUTUBE']?.deferred || 0}</div>
          </div>
          <div>
            <strong style={{ color: 'var(--text-secondary)' }}>Reddit</strong>
            <div style={{ marginTop: '4px', color: 'var(--text-secondary)' }}>Status: NOT CONFIGURED</div>
          </div>
        </div>
      </div>

      {/* 2. CROSS-SOURCE THEMES */}
      <div className="glass-card" style={{ marginTop: '24px', padding: '16px' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>2. Cross-source Themes</h2>
        <table style={{ width: '100%', textAlign: 'left', fontSize: '0.9rem', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border)' }}>
              <th style={{ padding: '8px 0' }}>Theme</th>
              <th>Frequency</th>
              <th>Google Play</th>
              <th>YouTube</th>
              <th>Coverage</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {themes?.data?.slice(0, 5).map((t: any, i: number) => (
              <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '12px 0' }}>{t.theme_name}</td>
                <td>{t.frequency}</td>
                <td>{t.source_distribution?.['GOOGLE_PLAY'] || 0}</td>
                <td>{t.source_distribution?.['YOUTUBE'] || 0}</td>
                <td>{t.source_coverage || 1} sources</td>
                <td>
                  <span style={{
                    padding: '2px 6px', borderRadius: '4px', fontSize: '0.7rem',
                    backgroundColor: t.evidence_confidence === 'strong' ? 'rgba(0,255,0,0.1)' : 'rgba(255,255,255,0.1)',
                    color: t.evidence_confidence === 'strong' ? '#4dff4d' : 'var(--text-secondary)'
                  }}>
                    {t.evidence_confidence?.toUpperCase() || 'UNKNOWN'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="grid-2" style={{ marginTop: '24px' }}>
        {/* 3. WISHLIST BEHAVIOR */}
        <div className="glass-card" style={{ padding: '16px' }}>
          <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>3. Wishlist Behavior</h2>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, fontSize: '0.9rem' }}>
            {Object.entries(wishlist?.bookmarking_vs_intent || {}).map(([key, val]: [string, any], i) => (
              <li key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <span>{key}</span>
                <strong style={{ color: 'var(--accent-violet)' }}>{val}</strong>
              </li>
            ))}
          </ul>
        </div>

        {/* 4. PURCHASE BARRIERS */}
        <div className="glass-card" style={{ padding: '16px' }}>
          <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>4. Purchase Barriers</h2>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, fontSize: '0.9rem' }}>
            {Object.entries(barriers?.top_barriers || {}).slice(0, 5).map(([key, val]: [string, any], i) => (
              <li key={i} style={{ padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 'bold' }}>{key}</span>
                  <strong style={{ color: '#ff4d4d' }}>{val.total_mentions}</strong>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  {val.unique_supporting_records} unique records
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: '24px' }}>
        {/* 5. EXTERNAL INFORMATION SEEKING */}
        <div className="glass-card" style={{ padding: '16px' }}>
          <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>5. External Information Seeking</h2>
          <div style={{ marginBottom: '16px' }}>
            {Object.entries(research?.research_types || {}).map(([key, val]: [string, any], i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '4px' }}>
                <span>{key}</span>
                <strong>{val}</strong>
              </div>
            ))}
          </div>
          <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Information Sought:</h3>
          <ul style={{ paddingLeft: '20px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            {Object.entries(research?.information_sought || {}).slice(0, 5).map(([key, val]: [string, any], i) => (
              <li key={i}>{key} ({val})</li>
            ))}
          </ul>
        </div>

        {/* 6. USER SEGMENTS */}
        <div className="glass-card" style={{ padding: '16px' }}>
          <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>6. User Segments</h2>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, fontSize: '0.9rem' }}>
            {Object.entries(segments?.segments || {}).slice(0, 5).map(([key, val]: [string, any], i) => (
              <li key={i} style={{ padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 'bold', color: 'var(--accent-cyan)' }}>{key}</span>
                  <strong>{val.count}</strong>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  Top Barrier: {val.top_barriers?.[0] || 'None'}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 7. OPPORTUNITY RANKING & 8. EVIDENCE EXPLORER */}
      <h2 style={{ marginTop: '48px' }}>7. Opportunity Ranking & 8. Evidence Explorer</h2>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '24px' }}>
        Opportunities are scored transparently (0-5). Click 'View Evidence' to see the exact user quotes backing this opportunity.
      </p>

      <div className="grid-2">
        {opportunities?.map((opp: any, idx: number) => (
          <OpportunityCard key={idx} opp={opp} />
        ))}
      </div>
    </div>
  );
}
