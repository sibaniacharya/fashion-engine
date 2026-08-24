'use client';
import { useEffect, useState } from 'react';
import MetricCard from '@/components/MetricCard';
import OpportunityCard from '@/components/OpportunityCard';

export default function Overview() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/dashboard')
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
      <h1 className="gradient-text">Overview & Impact Ranking</h1>
      <p>Data-driven opportunities mapped directly from Wishlist behavior to Purchase completion.</p>
      
      <div className="grid-3" style={{ marginTop: '32px' }}>
        <MetricCard title="Total Records Processed" value={data.total_records_processed} subtitle="Analyzed by AI Pipeline" />
        <MetricCard title="Top Discovery Theme" value={data.top_themes?.[0]?.theme_name || "N/A"} subtitle="Highest frequency signal" />
        <MetricCard title="Critical Blocker" value={data.top_opportunities.find((o:any) => o.opportunity_name.includes('Resolve'))?.problem || "N/A"} subtitle="Highest purchase impact" />
      </div>

      <h2 style={{ marginTop: '48px' }}>Ranked Opportunities</h2>
      <div className="grid-2">
        {data.top_opportunities.map((opp: any, idx: number) => (
          <OpportunityCard key={idx} opp={opp} />
        ))}
      </div>
    </div>
  );
}
