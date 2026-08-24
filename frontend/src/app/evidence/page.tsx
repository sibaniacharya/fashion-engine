'use client';
import { useEffect, useState } from 'react';

export default function Evidence() {
  const [data, setData] = useState<any>(null);
  const [quality, setQuality] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('http://127.0.0.1:8000/api/evidence').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/data-quality').then(r => r.json())
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
          <span className="badge badge-cyan">{quality.status}</span>
        </h2>
        <div style={{ display: 'flex', gap: '24px', fontSize: '0.875rem' }}>
          <div><strong>Total Normalized:</strong> {quality.total_records_processed}</div>
          <div><strong>Duplicates Removed:</strong> {quality.records_removed.duplicates}</div>
          <div><strong>Spam Removed:</strong> {quality.records_removed.spam_or_meaningless}</div>
          <div><strong>PII Masked:</strong> {quality.records_modified.pii_masked}</div>
        </div>
      </div>

      <h2 style={{ marginTop: '40px' }}>Analyzed Signals Trace</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
        {data.data.map((record: any, idx: number) => (
          <div key={idx} className="glass-card" style={{ fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', gap: '12px', marginBottom: '8px' }}>
              <span className="badge badge-violet">{record.source}</span>
              <span style={{ color: 'var(--text-secondary)' }}>Trace ID: {record.id.substring(0, 8)}</span>
            </div>
            <p style={{ fontStyle: 'italic', color: '#fff', margin: '8px 0' }}>"{record.normalized_text}"</p>
            
            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '6px', color: 'var(--accent-cyan)' }}>
              <strong>AI Extraction:</strong> {record.extracted_signals.theme_candidate || 'Unclassified Theme'}
              {record.extracted_signals.purchase_barrier && <span> | Barrier: {record.extracted_signals.purchase_barrier}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
