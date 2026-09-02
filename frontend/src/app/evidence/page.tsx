'use client';
import { useEffect, useState } from 'react';
import { ApiClient, DataQuality, PaginatedEvidence } from '@/lib/api';

export default function Evidence() {
  const [data, setData] = useState<PaginatedEvidence | null>(null);
  const [quality, setQuality] = useState<DataQuality | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      ApiClient.getEvidence(1, 100),
      ApiClient.getDataQuality()
    ]).then(([ev, dq]) => {
      setData(ev);
      setQuality(dq);
      setLoading(false);
    }).catch(e => console.error(e));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="gradient-text">Evidence Explorer</h1>
      <p>Raw AI mapping and data quality verification.</p>

      <div className="glass-card" style={{ marginTop: '32px' }}>
        <h2 style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>Data Quality Report</span>
          <span className="badge badge-cyan">Verified</span>
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '24px', fontSize: '0.875rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Pipeline Stats</h3>
            <div><strong>Raw Records:</strong> {quality?.raw || 0}</div>
            <div><strong>Valid Records:</strong> {quality?.valid || 0}</div>
            <div><strong>Eligible Records:</strong> {quality?.eligible || 0}</div>
            <div><strong>LLM Analyzed:</strong> {quality?.llm_analyzed || 0}</div>
            <div><strong>Fallback Analyzed:</strong> {quality?.fallback_analyzed || 0}</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
             <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Other/Filtered Breakdown</h3>
             <div><strong>Duplicates Removed:</strong> {quality?.duplicates || 0}</div>
             <div><strong>Spam Removed:</strong> {quality?.spam || 0}</div>
             <div><strong>Empty Content:</strong> {quality?.empty_content || 0}</div>
             <div><strong>Non-English:</strong> {quality?.non_english || 0}</div>
             <div><strong>Other Exclusions:</strong> {quality?.other_exclusions || 0}</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
             <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Failure & Deferred</h3>
             <div><strong>Failed Records:</strong> {quality?.failed || 0}</div>
             <div><strong style={{ color: '#ffa500' }}>Deferred (Rate Limit):</strong> {quality?.deferred_rate_limit || 0}</div>
             <div><strong style={{ color: '#ffa500' }}>Deferred (Quota):</strong> {quality?.deferred_quota || 0}</div>
          </div>
        </div>
      </div>

      <h2 style={{ marginTop: '40px' }}>Analyzed Signals Trace</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
        {data?.data?.map((record: any, idx: number) => (
          <div key={idx} className="glass-card" style={{ fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', gap: '12px', marginBottom: '8px' }}>
              <span className="badge badge-violet">{record.source}</span>
              <span style={{ color: 'var(--text-secondary)' }}>Trace ID: {record.record_id?.substring(0, 8) || record.raw_id?.substring(0, 8)}</span>
            </div>
            <p style={{ fontStyle: 'italic', color: '#fff', margin: '8px 0' }}>"{record.text || record.normalized_text}"</p>

            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '6px', color: 'var(--accent-cyan)' }}>
              <strong>AI Extraction:</strong> {record.theme || record.extracted_signals?.theme_candidate || 'Unclassified Theme'}
              {(record.purchase_barrier && record.purchase_barrier !== 'UNKNOWN') && (
                <span> | Barrier: {record.purchase_barrier}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
