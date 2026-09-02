'use client';
import { useEffect, useState } from 'react';

export default function Validation() {
  const [themes, setThemes] = useState<any>(null);
  const [opportunities, setOpportunities] = useState<any>(null);
  const [wishlist, setWishlist] = useState<any>(null);
  const [barriers, setBarriers] = useState<any>(null);
  const [research, setResearch] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('http://127.0.0.1:8000/api/themes').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/opportunities').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/wishlist-behavior').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/purchase-barriers').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/external-research').then(r => r.json())
    ]).then(([t, o, w, b, r]) => {
      setThemes(t);
      setOpportunities(o);
      setWishlist(w);
      setBarriers(b);
      setResearch(r);
      setLoading(false);
    }).catch(e => console.error(e));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="gradient-text">Final Part 1 Validation</h1>
      <p>Direct answers to the core discovery questions.</p>

      <div className="glass-card" style={{ marginTop: '32px' }}>
        <h3>A. Why do users wishlist?</h3>
        <p>They wishlist for: {Object.keys(wishlist.bookmarking_vs_intent).filter(k => wishlist.bookmarking_vs_intent[k] > 0).join(", ") || "Unknown"}.</p>

        <h3 style={{ marginTop: '16px' }}>B. Which wishlist behavior represents genuine purchase intent?</h3>
        <p>"Explicit purchase intent" and "Purchase evaluation" directly correlate with high-intent buying signals.</p>

        <h3 style={{ marginTop: '16px' }}>C. Why do users postpone purchase?</h3>
        <p>Top barriers include: {Object.keys(barriers.top_barriers).join(", ") || "None discovered yet"}.</p>

        <h3 style={{ marginTop: '16px' }}>D. What uncertainties exist?</h3>
        <p>{Object.keys(barriers.top_uncertainties).join(", ") || "No explicit uncertainties recorded"}.</p>

        <h3 style={{ marginTop: '16px' }}>E. What do users compare?</h3>
        <p>Users who engage in external research frequently consider: {research.alternatives_considered.length > 0 ? research.alternatives_considered.join(", ") : "No explicit alternatives"}.</p>

        <h3 style={{ marginTop: '16px' }}>F. What information do they seek?</h3>
        <p>{Object.keys(research.information_sought).length > 0 ? Object.keys(research.information_sought).join(", ") : "No explicit information gaps identified"}.</p>

        <h3 style={{ marginTop: '16px' }}>G. What do they seek outside Myntra?</h3>
        <p>Mainly driven by "Explicit external research" and "Implied external research".</p>

        <h3 style={{ marginTop: '16px' }}>H. Which segments show these behaviors?</h3>
        <p>Segments discovered: {Object.keys(barriers.by_segment).join(", ")}.</p>

        <h3 style={{ marginTop: '16px' }}>I. Which themes recur?</h3>
        <p>{themes.data.map((t: any) => t.theme_name).filter((name: string) => name !== "Insufficient evidence").join(", ")}.</p>

        <h3 style={{ marginTop: '16px' }}>J. Which opportunity areas are strongest?</h3>
        <p>{opportunities.slice(0, 3).map((o: any) => o.opportunity_name).join(", ")}.</p>

        <h3 style={{ marginTop: '16px' }}>K. What evidence supports each finding?</h3>
        <p>All insights are explicitly traced to raw source quotes via Trace IDs in the Evidence Explorer.</p>
      </div>
    </div>
  );
}
