'use client';
import { useEffect, useState } from 'react';

export default function Themes() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/themes')
      .then(res => res.json())
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
        {data.data.map((theme: any, idx: number) => (
          <div key={idx} className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <h3 style={{ margin: 0, color: '#fff', fontSize: '1.2rem' }}>{theme.theme_name}</h3>
              <span className="badge badge-cyan">{theme.frequency} Mentions</span>
            </div>
            <p style={{ fontSize: '0.9rem', marginBottom: 0 }}>{theme.description}</p>
            
            <div style={{ marginTop: 'auto' }}>
              <h4 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '8px' }}>Sources</h4>
              <div style={{ display: 'flex', gap: '8px' }}>
                {Object.keys(theme.source_distribution).map(src => (
                  <span key={src} className="badge badge-violet">{src}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
