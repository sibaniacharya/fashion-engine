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
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, className: 'gradient-text' }}>
            {opp.opportunity_score}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Final Score</div>
        </div>
      </div>
      
      <div style={{ background: 'rgba(0,0,0,0.2)', padding: '16px', borderRadius: '8px' }}>
        <ScoreBar label="Purchase Impact" score={opp.scores.purchase_impact} />
        <ScoreBar label="Wishlist Relevance" score={opp.scores.wishlist_relevance} />
        <ScoreBar label="User Pain" score={opp.scores.user_pain} />
      </div>

      <div style={{ fontSize: '0.85rem' }}>
        <strong style={{ color: 'var(--accent-violet)' }}>Grounding Evidence:</strong>
        <ul style={{ paddingLeft: '16px', marginTop: '8px', color: 'var(--text-secondary)' }}>
          {opp.supporting_evidence.map((ev: string, idx: number) => (
            <li key={idx} style={{ marginBottom: '4px' }}>"{ev}"</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
