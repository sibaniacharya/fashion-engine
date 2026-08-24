'use client';
import { useEffect, useState } from 'react';

export default function Journey() {
  const [wishlist, setWishlist] = useState<any>(null);
  const [barriers, setBarriers] = useState<any>(null);
  const [research, setResearch] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('http://127.0.0.1:8000/api/wishlist-behavior').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/purchase-barriers').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/external-research').then(r => r.json())
    ]).then(([w, b, r]) => {
      setWishlist(w);
      setBarriers(b);
      setResearch(r);
      setLoading(false);
    }).catch(e => console.error(e));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="gradient-text">Journey Analytics</h1>
      <p>Tracking the Wishlist-to-Purchase Funnel</p>
      
      <div className="grid-2" style={{ marginTop: '32px' }}>
        <div className="glass-card">
          <h2>Why Users Wishlist</h2>
          <div style={{ display: 'flex', gap: '16px', marginTop: '16px' }}>
            <div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>{wishlist.bookmarking_vs_intent.bookmarking}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Bookmarking</div>
            </div>
            <div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--accent-violet)' }}>{wishlist.bookmarking_vs_intent.purchase_intent}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Purchase Intent</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card">
          <h2>Why They Postpone Purchase</h2>
          {Object.keys(barriers.top_barriers).length > 0 ? (
            <ul style={{ paddingLeft: '16px', color: 'var(--text-secondary)' }}>
              {Object.entries(barriers.top_barriers).map(([b, count]: any) => (
                <li key={b}>"{b}" ({count} instances)</li>
              ))}
            </ul>
          ) : (
            <p>No postponement barriers explicitly logged in this dataset.</p>
          )}
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: '24px' }}>
        <div className="glass-card">
          <h2>External Information Seeking</h2>
          <p style={{ fontSize: '0.85rem' }}>Where users go when the platform doesn't have the info.</p>
          {research.alternatives_considered.length > 0 ? (
            <ul style={{ paddingLeft: '16px', color: 'var(--text-secondary)' }}>
              {research.alternatives_considered.map((alt: string, i: number) => (
                <li key={i}>{alt}</li>
              ))}
            </ul>
          ) : (
             <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>No external alternatives found.</p>
          )}
        </div>
        
        <div className="glass-card">
          <h2>User Segments Affected</h2>
          <ul style={{ paddingLeft: '16px', color: 'var(--text-secondary)' }}>
             {Object.keys(barriers.by_segment).map((seg: string, i: number) => (
               <li key={i}>{seg}</li>
             ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
