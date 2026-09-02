'use client';
import { useEffect, useState } from 'react';
import TopAppBar from '@/components/TopAppBar';
import { ApiClient, DataQuality } from '@/lib/api';

export default function Validation() {
  const [quality, setQuality] = useState<DataQuality | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    ApiClient.getDataQuality()
      .then(q => {
        setQuality(q);
        setLoading(false);
      })
      .catch(e => console.error(e));
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="font-label-md text-label-md text-on-surface-variant">Loading pipeline metrics...</div>
      </div>
    );
  }

  // Calculate some derived metrics
  const totalAnalyzed = (quality?.llm_analyzed || 0) + (quality?.fallback_analyzed || 0);
  const completionPercentage = quality?.eligible ? Math.round((totalAnalyzed / quality.eligible) * 100) : 0;

  return (
    <>
      <TopAppBar title="Discovery Engine" />

      <main className="flex-1 overflow-y-auto custom-scrollbar p-margin-page">
        <div className="max-w-[1440px] mx-auto space-y-gutter">

          {/* Page Header */}
          <div className="flex justify-between items-end mb-8">
            <div>
              <h1 className="font-display-lg text-display-lg text-on-background mb-2">Data Quality & Pipeline</h1>
              <p className="font-body-md text-body-md text-on-surface-variant">Monitor data ingestion, filtering, and analysis health.</p>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 bg-secondary-container/30 border border-secondary-container rounded-full">
              <div className="w-2 h-2 rounded-full bg-primary pipeline-active"></div>
              <span className="font-label-sm text-label-sm text-primary">Pipeline Complete</span>
            </div>
          </div>

          {/* Pipeline Visualization */}
          <section className="bg-white rounded-xl border border-outline-variant p-6 mb-gutter relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-surface-container-low to-transparent opacity-50 pointer-events-none"></div>
            <h3 className="font-h2 text-h2 text-on-surface mb-6 relative z-10">Ingestion Flow</h3>

            <div className="flex items-center justify-between relative z-10 px-4">
              {/* Node 1 */}
              <div className="flex flex-col items-center flex-1 relative">
                <div className="w-16 h-16 rounded-lg bg-surface-container-high border border-outline-variant flex items-center justify-center mb-3 shadow-sm z-10">
                  <span className="material-symbols-outlined text-[28px] text-secondary">database</span>
                </div>
                <span className="font-label-md text-label-md text-on-surface">Raw Data</span>
                <span className="font-display-sm text-display-sm text-on-background mt-1">{quality?.raw || 0}</span>
                <div className="absolute top-8 left-[50%] w-full h-[2px] bg-outline-variant -z-10"></div>
              </div>

              {/* Node 2 */}
              <div className="flex flex-col items-center flex-1 relative">
                <div className="w-16 h-16 rounded-lg bg-surface-container-high border border-outline-variant flex items-center justify-center mb-3 shadow-sm z-10">
                  <span className="material-symbols-outlined text-[28px] text-secondary">filter_alt</span>
                </div>
                <span className="font-label-md text-label-md text-on-surface">Cleaning</span>
                <span className="font-label-sm text-label-sm text-on-surface-variant mt-1">Deduplication & Formatting</span>
                <div className="absolute top-8 left-[50%] w-full h-[2px] bg-outline-variant -z-10"></div>
              </div>

              {/* Node 3 */}
              <div className="flex flex-col items-center flex-1 relative">
                <div className="w-16 h-16 rounded-lg bg-primary/10 border border-primary flex items-center justify-center mb-3 shadow-sm z-10">
                  <span className="material-symbols-outlined text-[28px] text-primary">fact_check</span>
                </div>
                <span className="font-label-md text-label-md text-on-surface">Eligibility Filtering</span>
                <span className="font-display-sm text-display-sm text-primary mt-1">{quality?.eligible || 0}</span>
                <div className="absolute top-8 left-[50%] w-full h-[2px] bg-primary/30 -z-10"></div>
              </div>

              {/* Node 4 */}
              <div className="flex flex-col items-center flex-1 relative">
                <div className="w-16 h-16 rounded-lg bg-primary border border-primary flex items-center justify-center mb-3 shadow-sm z-10 pipeline-active">
                  <span className="material-symbols-outlined text-[28px] text-white">memory</span>
                </div>
                <span className="font-label-md text-label-md text-on-surface">AI Analysis</span>
                <span className="font-label-sm text-label-sm text-on-surface-variant mt-1">Feature Extraction</span>
                <div className="absolute top-8 left-[50%] w-full h-[2px] bg-primary/30 -z-10"></div>
              </div>

              {/* Node 5 */}
              <div className="flex flex-col items-center flex-1 relative">
                <div className="w-16 h-16 rounded-lg bg-surface-container-high border border-outline-variant flex items-center justify-center mb-3 shadow-sm z-10">
                  <span className="material-symbols-outlined text-[28px] text-secondary">insights</span>
                </div>
                <span className="font-label-md text-label-md text-on-surface">Structured Insights</span>
                <span className="font-label-sm text-label-sm text-on-surface-variant mt-1">Ready for Dashboard</span>
              </div>
            </div>
          </section>

          {/* Bento Grid Layout for Details */}
          <div className="grid grid-cols-12 gap-gutter">

            {/* Exclusion Breakdown */}
            <section className="col-span-12 lg:col-span-8 bg-white rounded-xl border border-outline-variant p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-h2 text-h2 text-on-surface">Exclusion Breakdown</h3>
                <button className="font-label-sm text-label-sm text-primary flex items-center gap-1 hover:underline">
                  View Logs <span className="material-symbols-outlined text-[16px]">open_in_new</span>
                </button>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 rounded-lg border border-surface-variant hover:bg-surface-container-low transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center">
                      <span className="material-symbols-outlined text-[16px] text-on-surface-variant">language</span>
                    </div>
                    <span className="font-body-md text-body-md text-on-surface">Non-English</span>
                  </div>
                  <span className="font-h2 text-h2 text-on-surface">{quality?.non_english || 0}</span>
                </div>

                <div className="flex items-center justify-between p-3 rounded-lg border border-surface-variant hover:bg-surface-container-low transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center">
                      <span className="material-symbols-outlined text-[16px] text-on-surface-variant">speaker_notes_off</span>
                    </div>
                    <span className="font-body-md text-body-md text-on-surface">Empty content</span>
                  </div>
                  <span className="font-h2 text-h2 text-on-surface">{quality?.empty_content || 0}</span>
                </div>

                <div className="flex items-center justify-between p-3 rounded-lg border border-surface-variant hover:bg-surface-container-low transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center">
                      <span className="material-symbols-outlined text-[16px] text-on-surface-variant">content_copy</span>
                    </div>
                    <span className="font-body-md text-body-md text-on-surface">Duplicates</span>
                  </div>
                  <span className="font-h2 text-h2 text-on-surface">{quality?.duplicates || 0}</span>
                </div>

                <div className="flex items-center justify-between p-3 rounded-lg border border-surface-variant hover:bg-surface-container-low transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center">
                      <span className="material-symbols-outlined text-[16px] text-on-surface-variant">report</span>
                    </div>
                    <span className="font-body-md text-body-md text-on-surface">Spam</span>
                  </div>
                  <span className="font-h2 text-h2 text-on-surface">{quality?.spam || 0}</span>
                </div>

                <div className="flex items-center justify-between p-3 rounded-lg border border-surface-variant hover:bg-surface-container-low transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center">
                      <span className="material-symbols-outlined text-[16px] text-on-surface-variant">more_horiz</span>
                    </div>
                    <span className="font-body-md text-body-md text-on-surface">Other</span>
                  </div>
                  <span className="font-h2 text-h2 text-on-surface">{quality?.other_exclusions || 0}</span>
                </div>
              </div>
            </section>

            {/* Technical Stats */}
            <div className="col-span-12 lg:col-span-4 flex flex-col gap-gutter">

              <section className="bg-inverse-surface rounded-xl p-6 text-on-primary">
                <div className="flex items-center gap-2 mb-6 text-primary-fixed">
                  <span className="material-symbols-outlined">terminal</span>
                  <h3 className="font-h2 text-h2">AI Execution</h3>
                </div>
                <ul className="space-y-4 font-body-md text-body-md text-surface-variant">
                  <li className="flex justify-between border-b border-white/10 pb-2">
                    <span>Model</span>
                    <span className="font-label-md text-label-md text-white">Qwen 3.8 27B</span>
                  </li>
                  <li className="flex justify-between border-b border-white/10 pb-2">
                    <span>Analyzed</span>
                    <span className="font-label-md text-label-md text-white">{totalAnalyzed}</span>
                  </li>
                  <li className="flex justify-between border-b border-white/10 pb-2">
                    <span>Final failures</span>
                    <span className="font-label-md text-label-md text-white">{quality?.failed || 0}</span>
                  </li>
                  <li className="flex justify-between pb-2">
                    <span>Rate Limited</span>
                    <span className="font-label-md text-label-md text-primary-fixed-dim">{quality?.deferred_rate_limit || 0}</span>
                  </li>
                </ul>
              </section>

              <section className="bg-white rounded-xl border border-outline-variant p-6 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="font-h2 text-h2 text-on-surface mb-2">Analysis Status</h3>
                  <p className="font-body-sm text-body-sm text-on-surface-variant mb-6">Real-time processing overview</p>

                  <div className="mb-2 flex justify-between items-end">
                    <span className="font-label-md text-label-md text-on-surface">{completionPercentage}% Complete</span>
                    <span className="font-micro text-micro text-on-surface-variant uppercase tracking-wider">Done</span>
                  </div>

                  <div className="w-full h-2 bg-surface-variant rounded-full overflow-hidden mb-4">
                    <div className="h-full bg-primary rounded-full" style={{ width: `${completionPercentage}%` }}></div>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-surface-variant">
                  <p className="font-label-md text-label-md text-on-surface mb-1 flex items-center gap-2">
                    <span className="material-symbols-outlined text-[16px] text-primary">check_circle</span>
                    {quality?.eligible || 0} eligible records analyzed
                  </p>
                  <p className="font-label-sm text-label-sm text-on-surface-variant">Pipeline finished successfully</p>
                </div>
              </section>

            </div>
          </div>
        </div>
      </main>
    </>
  );
}
