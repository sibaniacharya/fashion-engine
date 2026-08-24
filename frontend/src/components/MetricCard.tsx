export default function MetricCard({ title, value, subtitle }: { title: string, value: string | number, subtitle?: string }) {
  return (
    <div className="glass-card">
      <h3 style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        {title}
      </h3>
      <div style={{ fontSize: '2rem', fontWeight: 700, color: '#fff' }}>
        {value}
      </div>
      {subtitle && <p style={{ fontSize: '0.8rem', marginTop: '4px', marginBottom: 0 }}>{subtitle}</p>}
    </div>
  );
}
