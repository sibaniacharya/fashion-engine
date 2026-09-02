'use client';
import { useEffect, useState } from 'react';
import { ApiClient, PaginatedThemes } from '@/lib/api';

export default function Themes() {
  const [data, setData] = useState<PaginatedThemes | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    ApiClient.getThemes(1, 100)
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => console.error(e));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="gradient-text">What Users Care About</h1>
      <p>Recurring themes discovered across all feedback sources.</p>

      <div className="grid-2" style={{ marginTop: '32px' }}>
        {!data?.data || data.data.length === 0 ? (
          <div style={{ gridColumn: '1 / -1', padding: '32px', textAlign: 'center', background: 'rgba(255,255,255,0.02)', borderRadius: '8px' }}>
            <p style={{ color: 'var(--text-secondary)' }}>{data?.message || 'Insufficient evidence to identify reliable recurring themes from the currently analyzed records.'}</p>
          </div>
        ) : (
          data.data.map((theme: any, idx: number) => (
            <div key={idx} className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <h3 style={{ margin: 0, color: '#fff', fontSize: '1.2rem' }}>{theme.theme_name}</h3>
                <span className="badge badge-cyan">{theme.frequency} Mentions</span>
              </div>
              <p style={{ fontSize: '0.9rem', marginBottom: 0 }}>{theme.description}</p>

              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                <strong>Confidence:</strong> {theme.evidence_confidence} | <strong>Coverage:</strong> {theme.source_coverage} source(s)
              </div>

              <div style={{ marginTop: 'auto' }}>
                <h4 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '8px' }}>Sources</h4>
                <div style={{ display: 'flex', gap: '8px' }}>
                  {Object.keys(theme.source_distribution || {}).map(src => (
                    <span key={src} className="badge badge-violet">{src}</span>
                  ))}
                </div>
              </div>

              {theme.supporting_evidence && theme.supporting_evidence.length > 0 && (
                <div style={{ marginTop: '12px', padding: '12px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }}>
                  <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '8px' }}>Representative Evidence</h4>
                  <p style={{ fontSize: '0.85rem', fontStyle: 'italic', margin: 0, color: '#ddd' }}>
                    "{theme.supporting_evidence[0]?.quote}"
                  </p>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
