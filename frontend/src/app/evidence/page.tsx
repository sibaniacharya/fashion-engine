'use client';
import { useEffect, useState } from 'react';
import TopAppBar from '@/components/TopAppBar';
import { ApiClient, PaginatedEvidence } from '@/lib/api';

export default function Evidence() {
  const [data, setData] = useState<PaginatedEvidence | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    ApiClient.getEvidence(1, 100)
      .then(ev => {
        setData(ev);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setError("Failed to load evidence.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center h-screen">
        <div className="font-label-md text-label-md text-on-surface-variant">Loading evidence...</div>
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

  const records = data?.data || [];

  return (
    <>
      <TopAppBar title="Evidence Explorer" />

      {/* Content Canvas */}
      <main className="flex-1 p-margin-page flex gap-gutter max-w-container-max mx-auto w-full h-[calc(100vh-64px)] overflow-hidden">

        {/* Filters Sidebar (Left Column) */}
        <aside className="w-72 shrink-0 flex flex-col gap-6 bg-white border border-outline-variant/30 rounded-xl p-6 shadow-sm overflow-y-auto custom-scrollbar">

          {/* Search */}
          <div className="space-y-2">
            <label className="font-label-md text-label-md text-on-surface">Search Evidence</label>
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[20px]">search</span>
              <input
                type="text"
                placeholder="Search quotes..."
                className="w-full pl-10 pr-4 py-2 bg-surface-container-low border border-outline-variant rounded-lg font-body-md text-body-md focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-shadow"
              />
            </div>
          </div>

          <hr className="border-outline-variant/50" />

          {/* Source Filter */}
          <div className="space-y-3">
            <label className="font-label-md text-label-md text-on-surface">Source</label>
            <div className="space-y-2">
              <label className="flex items-center gap-2 cursor-pointer group">
                <input type="checkbox" defaultChecked className="rounded border-outline-variant text-primary focus:ring-primary w-4 h-4" />
                <span className="font-body-md text-body-md text-on-surface-variant group-hover:text-on-surface">Google Play</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer group">
                <input type="checkbox" defaultChecked className="rounded border-outline-variant text-primary focus:ring-primary w-4 h-4" />
                <span className="font-body-md text-body-md text-on-surface-variant group-hover:text-on-surface">YouTube</span>
              </label>
            </div>
          </div>

          {/* Theme Filter */}
          <div className="space-y-3">
            <label className="font-label-md text-label-md text-on-surface">Theme</label>
            <div className="space-y-2">
              <label className="flex items-center gap-2 cursor-pointer group">
                <input type="checkbox" defaultChecked className="rounded border-outline-variant text-primary focus:ring-primary w-4 h-4" />
                <span className="font-body-md text-body-md text-on-surface-variant group-hover:text-on-surface">Return Friction</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer group">
                <input type="checkbox" defaultChecked className="rounded border-outline-variant text-primary focus:ring-primary w-4 h-4" />
                <span className="font-body-md text-body-md text-on-surface-variant group-hover:text-on-surface">Fit Uncertainty</span>
              </label>
            </div>
          </div>

          {/* Purchase Barrier Filter */}
          <div className="space-y-3">
            <label className="font-label-md text-label-md text-on-surface">Purchase Barrier</label>
            <select
              className="w-full p-2 bg-surface-container-low border border-outline-variant rounded-lg font-body-md text-body-md focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary appearance-none bg-no-repeat bg-[right_0.75rem_center] bg-[length:16px_12px]"
              style={{ backgroundImage: "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"%23777587\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><polyline points=\"6 9 12 15 18 9\"/></svg>')" }}
            >
              <option>All Barriers</option>
              <option>Price</option>
              <option>Support</option>
              <option>Trust</option>
            </select>
          </div>
        </aside>

        {/* Results Area (Right Column) */}
        <div className="flex-1 flex flex-col overflow-hidden">

          {/* Results Header */}
          <div className="flex justify-between items-center mb-4 shrink-0">
            <div className="font-label-md text-label-md text-on-surface-variant">
              Showing {records.length} highly relevant evidence pieces
            </div>
            <div className="flex items-center gap-2">
              <span className="font-label-sm text-label-sm text-on-surface-variant">Sort by:</span>
              <select className="bg-transparent border-none text-on-surface font-label-md focus:ring-0 cursor-pointer text-primary">
                <option>Relevance Score</option>
                <option>Date (Newest)</option>
              </select>
            </div>
          </div>

          {/* Cards Container */}
          <div className="flex-1 overflow-y-auto custom-scrollbar pr-2 space-y-4 pb-8">
            {records.map((record: any, idx: number) => {
              // Derive colors based on source for visual variety
              const isYoutube = record.source === 'YOUTUBE';
              const sourceBg = isYoutube ? 'bg-[#fceceb]' : 'bg-[#e4f0f6]';
              const sourceText = isYoutube ? 'text-[#cc0000]' : 'text-[#0066cc]';
              const borderColor = isYoutube ? 'bg-[#ff0000]/70' : 'bg-tertiary-container/80';

              const traceId = record.record_id?.substring(0, 8) || record.raw_id?.substring(0, 8) || 'Unknown';
              const text = record.text || record.normalized_text;
              const theme = record.theme || record.extracted_signals?.theme_candidate || 'Unclassified';
              const barrier = record.purchase_barrier && record.purchase_barrier !== 'UNKNOWN' ? record.purchase_barrier : null;

              return (
                <div key={idx} className="bg-white border border-outline-variant/40 rounded-xl p-6 hover:border-primary/50 transition-colors group shadow-sm flex flex-col gap-4 relative overflow-hidden">
                  <div className={`absolute left-0 top-0 bottom-0 w-1 ${borderColor}`}></div>

                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-3">
                      <span className={`${sourceBg} ${sourceText} font-micro text-micro px-2 py-1 rounded-sm tracking-wide uppercase`}>
                        {record.source || 'UNKNOWN'}
                      </span>
                      <span className="text-on-surface-variant font-label-sm text-label-sm flex items-center gap-1">
                        <span className="material-symbols-outlined text-[14px]">fingerprint</span> Trace {traceId}
                      </span>
                    </div>
                  </div>

                  <blockquote className="font-h1 text-h1 text-on-surface border-l-2 border-outline-variant/30 pl-4 py-1 italic text-gray-800">
                    "{text}"
                  </blockquote>

                  <div className="flex flex-wrap gap-2 pt-2 border-t border-outline-variant/20 mt-2">
                    <span className="px-3 py-1 bg-surface-container text-on-surface-variant font-label-sm text-label-sm rounded-full flex items-center gap-1">
                      <span className="material-symbols-outlined text-[14px]">category</span> {theme}
                    </span>
                    {barrier && (
                      <span className="px-3 py-1 bg-surface-container text-on-surface-variant font-label-sm text-label-sm rounded-full flex items-center gap-1">
                        <span className="material-symbols-outlined text-[14px]">policy</span> {barrier}
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </main>
    </>
  );
}
