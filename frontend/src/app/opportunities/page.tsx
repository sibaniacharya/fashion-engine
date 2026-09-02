'use client';
import { useEffect, useState } from 'react';
import TopAppBar from '@/components/TopAppBar';
import { ApiClient } from '@/lib/api';

export default function Opportunities() {
  const [opportunities, setOpportunities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    ApiClient.getOpportunities()
      .then(d => {
        setOpportunities(d || []);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setError("Failed to load opportunities. Please check API connection.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center h-screen">
        <div className="font-label-md text-label-md text-on-surface-variant">Loading opportunities...</div>
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

  return (
    <>
      <TopAppBar title="Opportunities" breadcrumbs={['Discovery Engine', 'Opportunities']} />

      <main className="flex-1 p-margin-page mx-auto w-full max-w-container-max flex flex-col gap-6">
        <div className="flex flex-col gap-1 mb-2">
          <h1 className="font-display-lg text-display-lg text-on-surface">Opportunities</h1>
          <p className="font-body-md text-body-md text-on-surface-variant">Evidence-backed opportunities to improve wishlist-to-purchase conversion.</p>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm flex flex-col">
          <div className="p-4 border-b border-outline-variant bg-surface flex justify-between items-center">
            <div className="font-h2 text-h2 text-on-surface">All Opportunities</div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr>
                  <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Opportunity</th>
                  <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Problem / Barrier</th>
                  <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50 text-right">Score</th>
                </tr>
              </thead>
              <tbody className="font-body-md text-body-md text-on-surface">
                {opportunities.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="py-8 text-center text-on-surface-variant">
                      No opportunities found.
                    </td>
                  </tr>
                ) : (
                  opportunities.map((opp: any, idx: number) => (
                    <tr key={idx} className="border-b border-outline-variant hover:bg-surface-container-low transition-colors">
                      <td className="py-4 px-4">
                        <div className="font-medium text-on-surface mb-1">{opp.opportunity_name || 'Unnamed Opportunity'}</div>
                        <div className="text-sm text-on-surface-variant">{opp.structured_statement}</div>
                      </td>
                      <td className="py-4 px-4 text-on-surface-variant align-top pt-5">
                        {opp.problem}
                      </td>
                      <td className="py-4 px-4 text-right align-top pt-5">
                        <span className="bg-primary/10 text-primary font-medium px-2 py-1 rounded">
                          {opp.opportunity_score}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </>
  );
}
