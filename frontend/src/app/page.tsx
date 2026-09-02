'use client';
import { useEffect, useState } from 'react';
import TopAppBar from '@/components/TopAppBar';
import { ApiClient, DashboardMetrics, DataQuality, PaginatedThemes, WishlistBehavior, PurchaseBarriers, ExternalResearch, UserSegments } from '@/lib/api';

export default function Overview() {
  const [data, setData] = useState<DashboardMetrics | null>(null);
  const [quality, setQuality] = useState<DataQuality | null>(null);
  const [themes, setThemes] = useState<PaginatedThemes | null>(null);
  const [wishlist, setWishlist] = useState<WishlistBehavior | null>(null);
  const [barriers, setBarriers] = useState<PurchaseBarriers | null>(null);
  const [research, setResearch] = useState<ExternalResearch | null>(null);
  const [segments, setSegments] = useState<UserSegments | null>(null);
  const [opportunities, setOpportunities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      ApiClient.getDashboard(),
      ApiClient.getDataQuality(),
      ApiClient.getThemes(),
      ApiClient.getWishlistBehavior(),
      ApiClient.getPurchaseBarriers(),
      ApiClient.getExternalResearch(),
      ApiClient.getSegments(),
      ApiClient.getOpportunities()
    ]).then(([d, q, t, w, b, r, s, o]) => {
      setData(d);
      setQuality(q);
      setThemes(t);
      setWishlist(w);
      setBarriers(b);
      setResearch(r);
      setSegments(s);
      setOpportunities(o || []);
      setLoading(false);
    }).catch(e => {
      console.error(e);
      setError("Failed to load dashboard data. Please check API connection.");
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center h-screen">
        <div className="font-label-md text-label-md text-on-surface-variant">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center h-screen">
        <div className="font-label-md text-label-md text-error">{error}</div>
      </div>
    );
  }

  // Pick top 4 barriers as "Key Findings" for the UI cards
  const topBarriers = Object.entries(barriers?.top_barriers || {}).slice(0, 4);

  return (
    <>
      <TopAppBar title="Discovery Engine" />
      <main className="flex-1 p-margin-page max-w-container-max mx-auto w-full">
        {/* Hero */}
        <div className="mb-stack-lg">
          <h1 className="font-display-sm text-display-sm text-on-surface mb-stack-xs">Customer Feedback Intelligence</h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant">Turn public customer feedback into actionable product opportunities.</p>
        </div>

        {/* KPI Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-stack-md mb-stack-lg">
          <div className="bg-white/70 backdrop-blur-md p-4 rounded-xl col-span-1 flex flex-col justify-center items-start shadow-sm border border-outline-variant">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Raw Records</span>
            <span className="font-display-lg text-display-lg text-primary">{quality?.raw || 0}</span>
          </div>
          <div className="bg-white/70 backdrop-blur-md p-4 rounded-xl col-span-1 flex flex-col justify-center items-start shadow-sm border border-outline-variant">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Eligible</span>
            <span className="font-display-lg text-display-lg text-primary">{quality?.eligible || 0}</span>
          </div>
          <div className="bg-white/70 backdrop-blur-md p-4 rounded-xl col-span-1 flex flex-col justify-center items-start shadow-sm border border-outline-variant">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">AI-Analyzed</span>
            <span className="font-display-lg text-display-lg text-primary">{quality?.llm_analyzed || 0}</span>
          </div>
          <div className="bg-white/70 backdrop-blur-md p-4 rounded-xl col-span-1 flex flex-col justify-center items-start shadow-sm border border-outline-variant">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Themes</span>
            <span className="font-display-lg text-display-lg text-on-surface">{themes?.total || 0}</span>
          </div>
          <div className="bg-white/70 backdrop-blur-md p-4 rounded-xl col-span-1 flex flex-col justify-center items-start shadow-sm border border-outline-variant">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Barriers</span>
            <span className="font-display-lg text-display-lg text-error">{Object.keys(barriers?.top_barriers || {}).length}</span>
          </div>
          <div className="bg-white/70 backdrop-blur-md p-4 rounded-xl col-span-1 flex flex-col justify-center items-start shadow-sm border border-outline-variant relative overflow-hidden">
            <div className="absolute inset-0 bg-primary/5"></div>
            <span className="font-label-sm text-label-sm text-primary uppercase tracking-wider mb-1 relative z-10">Opportunities</span>
            <span className="font-display-lg text-display-lg text-primary relative z-10">{opportunities?.length || 0}</span>
          </div>
        </div>

        {/* Key Findings Cards */}
        <div className="mb-stack-lg">
          <div className="flex items-center justify-between mb-stack-sm">
            <h2 className="font-h2 text-h2 text-on-surface">Top Purchase Barriers</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-stack-md">
            {topBarriers.map(([barrierName, barrierData]: [string, any], idx) => (
              <div key={idx} className="bg-surface rounded-xl border border-outline-variant p-6 flex flex-col h-full hover:border-primary transition-colors cursor-pointer group">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="font-h1 text-h1 text-on-surface">{barrierName}</h3>
                  <span className="bg-secondary-container text-on-secondary-container px-2 py-1 rounded-full font-micro text-micro flex items-center gap-1">
                    <span className="material-symbols-outlined text-[14px]">description</span> {barrierData.total_mentions}
                  </span>
                </div>
                <p className="font-body-md text-body-md text-on-surface-variant flex-1 mb-4">
                  This barrier was mentioned {barrierData.total_mentions} times across {barrierData.unique_supporting_records} unique records.
                </p>
                <div className="mt-auto">
                  <button className="font-label-sm text-label-sm text-primary flex items-center gap-1 group-hover:underline">
                    View evidence <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Opportunities Table */}
        <div className="mb-stack-lg">
          <div className="bg-surface rounded-xl border border-outline-variant overflow-hidden">
            <div className="p-6 border-b border-outline-variant bg-surface-container-lowest">
              <h2 className="font-h2 text-h2 text-on-surface">Top Wishlist → Purchase Opportunities</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-container-low border-b border-outline-variant">
                    <th className="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider font-semibold">Opportunity</th>
                    <th className="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider font-semibold">Outcome</th>
                    <th className="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider font-semibold text-right">Score</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-outline-variant font-body-md text-body-md">
                  {opportunities?.slice(0, 5).map((opp: any, idx: number) => (
                    <tr key={idx} className="hover:bg-surface-variant/50 transition-colors">
                      <td className="p-4 font-label-md text-label-md text-on-surface">{opp.structured_statement || opp.opportunity_name}</td>
                      <td className="p-4 text-on-surface-variant">{opp.problem}</td>
                      <td className="p-4 text-right font-label-md text-label-md text-on-surface">{opp.opportunity_score}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="p-3 bg-surface-container-low border-t border-outline-variant flex justify-end gap-4 font-label-sm text-label-sm text-on-surface-variant">
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-primary/50"></span> Validation opportunity</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-outline"></span> Requires primary research</span>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
