'use client';
import { useEffect, useState } from 'react';
import TopAppBar from '@/components/TopAppBar';
import { ApiClient, UserSegments } from '@/lib/api';

export default function Segments() {
  const [data, setData] = useState<UserSegments | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    ApiClient.getSegments()
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setError("Failed to load segments. Please check API connection.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center h-screen">
        <div className="font-label-md text-label-md text-on-surface-variant">Loading segments...</div>
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

  const segmentsList = Array.isArray(data?.segments)
    ? [...data.segments].sort((a: any, b: any) => (b.unique_record_count || 0) - (a.unique_record_count || 0))
    : [];

  return (
    <>
      <TopAppBar title="Behavioral Segments" breadcrumbs={['Discovery Engine', 'Behavioral Segments']} />

      <main className="flex-1 p-margin-page mx-auto w-full max-w-container-max flex flex-col gap-6">
        <div className="flex flex-col gap-1 mb-2">
          <h1 className="font-display-lg text-display-lg text-on-surface">Behavioral Segments</h1>
          <p className="font-body-md text-body-md text-on-surface-variant">User segments derived from feedback data.</p>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm flex flex-col">
          <div className="p-4 border-b border-outline-variant bg-surface flex justify-between items-center">
            <div className="font-h2 text-h2 text-on-surface">User Profiles ({data?.total_records_classified || 0} classified)</div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr>
                  <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Segment Name</th>
                  <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50 text-right">Count</th>
                </tr>
              </thead>
              <tbody className="font-body-md text-body-md text-on-surface">
                {segmentsList.length === 0 ? (
                  <tr>
                    <td colSpan={2} className="py-8 text-center text-on-surface-variant">
                      No segments found.
                    </td>
                  </tr>
                ) : (
                  segmentsList.map((seg: any, idx: number) => (
                    <tr key={idx} className="border-b border-outline-variant hover:bg-surface-container-low transition-colors">
                      <td className="py-4 px-4 font-medium text-on-surface">{seg.segment_name}</td>
                      <td className="py-4 px-4 text-right">
                        <span className="bg-primary/10 text-primary font-medium px-3 py-1 rounded-full">
                          {seg.unique_record_count}
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
