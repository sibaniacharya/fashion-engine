import ScoreBar from './ScoreBar';

export default function OpportunityCard({ opp }: { opp: any }) {
  const isResolve = opp.opportunity_name.startsWith('Resolve');

  return (
    <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <span className={`badge ${isResolve ? 'badge-danger' : 'badge-cyan'}`} style={{ marginBottom: '8px', display: 'inline-block' }}>
            {isResolve ? 'Blocker' : 'Enhancement'}
          </span>
          <h3 style={{ margin: '8px 0', color: '#fff', fontSize: '1.2rem' }}>{opp.opportunity_name}</h3>
          <p style={{ fontSize: '0.875rem', marginBottom: 0 }}>Segment: {opp.affected_segment}</p>
          <p style={{ fontSize: '0.875rem', marginBottom: 0, marginTop: '4px', fontStyle: 'italic', color: 'var(--accent-violet)' }}>
            "{opp.structured_statement}"
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div className="gradient-text" style={{ fontSize: '1.5rem', fontWeight: 700 }}>
            {opp.opportunity_score}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Final Score</div>
        </div>
      </div>

      <div style={{ background: 'rgba(0,0,0,0.2)', padding: '16px', borderRadius: '8px' }}>
        <ScoreBar label="Purchase Impact" score={opp.scores.purchase_impact} />
        <ScoreBar label="Wishlist/Purchase Relevance" score={opp.wishlist_purchase_relevance || opp.scores.wishlist_relevance} />
        <ScoreBar label="User Pain" score={opp.scores.user_pain} />
        <ScoreBar label="Evidence Confidence" score={opp.scores.evidence_confidence} />
      </div>

      <div style={{ fontSize: '0.85rem' }}>
        <details>
          <summary style={{ color: 'var(--accent-violet)', cursor: 'pointer', fontWeight: 'bold' }}>View Evidence Explorer</summary>
          <ul style={{ paddingLeft: '16px', marginTop: '12px', color: 'var(--text-secondary)' }}>
            {opp.supporting_evidence.map((ev: any, idx: number) => (
              <li key={idx} style={{ marginBottom: '12px' }}>
                <span style={{ color: '#e0e0e0', fontStyle: 'italic' }}>"{ev.quote}"</span>
                <div style={{ fontSize: '0.7rem', color: '#888', marginTop: '4px' }}>
                   Source: <span style={{ color: 'var(--accent-cyan)' }}>{ev.source}</span> | Trace: {ev.trace_id?.substring(0,8) || 'unknown'} | Date: {ev.date}
                </div>
              </li>
            ))}
          </ul>
        </details>
      </div>
    </div>
  );
}
