export default function ScoreBar({ label, score, max = 5 }: { label: string, score: number, max?: number }) {
  const percentage = (score / max) * 100;
  
  return (
    <div style={{ marginBottom: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '4px' }}>
        <span>{label}</span>
        <span style={{ color: 'var(--accent-cyan)' }}>{score}/{max}</span>
      </div>
      <div className="score-track">
        <div className="score-fill" style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  );
}
