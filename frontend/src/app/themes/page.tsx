'use client';
import { useEffect, useState } from 'react';
import TopAppBar from '@/components/TopAppBar';
import { ApiClient, PaginatedThemes } from '@/lib/api';

export default function Themes() {
  const [data, setData] = useState<PaginatedThemes | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedTheme, setSelectedTheme] = useState<any | null>(null);

  useEffect(() => {
    ApiClient.getThemes(1, 100)
      .then(d => {
        setData(d);
        setLoading(false);
        if (d?.data && d.data.length > 0) {
          setSelectedTheme(d.data[0]); // Select first theme by default
        }
      })
      .catch(e => console.error(e));
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="font-label-md text-label-md text-on-surface-variant">Loading themes...</div>
      </div>
    );
  }

  return (
    <>
      <TopAppBar title="Themes" breadcrumbs={['Discovery Engine', 'Themes']} />
      
      <main className="flex-1 p-margin-page mx-auto w-full max-w-container-max flex flex-col gap-6">
        {/* Page Header */}
        <div className="flex flex-col gap-1 mb-2">
          <h1 className="font-display-lg text-display-lg text-on-surface">Themes</h1>
          <p className="font-body-md text-body-md text-on-surface-variant">Recurring topics identified across all feedback sources.</p>
        </div>

        {/* Bento Layout for Table and Drawer */}
        <div className="flex gap-6 items-start">
          
          {/* Main Themes Table Container */}
          <div className="flex-1 bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm flex flex-col min-w-[700px]">
            <div className="p-4 border-b border-outline-variant bg-surface flex justify-between items-center">
              <div className="font-h2 text-h2 text-on-surface">Identified Themes</div>
              <button className="flex items-center gap-2 text-primary font-label-sm text-label-sm hover:bg-surface-container-low px-3 py-1.5 rounded-lg border border-outline-variant transition-colors">
                <span className="material-symbols-outlined text-[18px]">filter_list</span>
                Filter
              </button>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr>
                    <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Theme</th>
                    <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Frequency</th>
                    <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Description</th>
                    <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Coverage</th>
                    <th className="font-label-sm text-label-sm text-on-surface-variant border-b border-outline-variant py-3 px-4 font-medium uppercase tracking-wider bg-surface-container-low/50">Confidence</th>
                  </tr>
                </thead>
                <tbody className="font-body-md text-body-md text-on-surface">
                  {!data?.data || data.data.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="py-8 text-center text-on-surface-variant">
                        {data?.message || 'No themes identified.'}
                      </td>
                    </tr>
                  ) : (
                    data.data.map((theme: any, idx: number) => {
                      const isSelected = selectedTheme?.theme_name === theme.theme_name;
                      
                      return (
                        <tr 
                          key={idx} 
                          onClick={() => setSelectedTheme(theme)}
                          className={`border-b border-outline-variant cursor-pointer group h-12 transition-colors ${
                            isSelected 
                              ? 'bg-primary-fixed/20 border-l-4 border-l-primary' 
                              : 'hover:bg-surface-container-low'
                          }`}
                        >
                          <td className={`py-2 px-4 font-medium ${isSelected ? 'text-primary' : 'text-on-surface'}`}>
                            {theme.theme_name}
                          </td>
                          <td className="py-2 px-4">
                            <span className="bg-surface-variant text-on-surface px-2 py-0.5 rounded font-label-sm">
                              {theme.frequency}
                            </span>
                          </td>
                          <td className="py-2 px-4 text-on-surface-variant truncate max-w-[200px]" title={theme.description}>
                            {theme.description}
                          </td>
                          <td className="py-2 px-4">
                            <span className="bg-surface-dim/30 text-on-surface px-2.5 py-1 rounded-full font-label-sm border border-outline-variant">
                              {theme.source_coverage} sources
                            </span>
                          </td>
                          <td className="py-2 px-4">
                            <div className="flex items-center gap-1.5">
                              {theme.evidence_confidence === 'strong' ? (
                                <>
                                  <span className="material-symbols-outlined text-[16px] text-primary" style={{fontVariationSettings: "'FILL' 1"}}>check_circle</span>
                                  <span className="font-label-sm text-primary">Strong</span>
                                </>
                              ) : (
                                <>
                                  <span className="material-symbols-outlined text-[16px] text-on-surface-variant">remove</span>
                                  <span className="font-label-sm text-on-surface-variant">Moderate</span>
                                </>
                              )}
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
          
          {/* Detail Drawer (Right panel) */}
          {selectedTheme && (
            <div className="w-[360px] bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col shadow-sm flex-shrink-0 sticky top-24">
              <div className="p-4 border-b border-outline-variant flex justify-between items-start bg-surface rounded-t-xl">
                <div>
                  <div className="font-label-sm text-label-sm text-primary mb-1 uppercase tracking-wider">Theme Details</div>
                  <h2 className="font-h1 text-h1 text-on-surface leading-tight">{selectedTheme.theme_name}</h2>
                </div>
                <button 
                  onClick={() => setSelectedTheme(null)}
                  className="text-on-surface-variant hover:text-on-surface p-1 rounded hover:bg-surface-variant transition-colors"
                >
                  <span className="material-symbols-outlined">close</span>
                </button>
              </div>
              
              <div className="p-5 flex flex-col gap-6 flex-1 overflow-y-auto">
                {/* Metadata Grid */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="font-label-sm text-label-sm text-on-surface-variant mb-1">Source Coverage</div>
                    <div className="inline-flex items-center gap-1.5 bg-tertiary-container/10 text-tertiary px-2.5 py-1 rounded-md font-label-sm border border-tertiary-container/30">
                      <span className="material-symbols-outlined text-[16px]">visibility</span>
                      {selectedTheme.source_coverage} sources
                    </div>
                  </div>
                  <div>
                    <div className="font-label-sm text-label-sm text-on-surface-variant mb-1">Frequency Volume</div>
                    <div className="font-h2 text-h2 text-on-surface flex items-baseline gap-1">
                      {selectedTheme.frequency} <span className="font-label-sm text-label-sm text-on-surface-variant font-normal">mentions</span>
                    </div>
                  </div>
                </div>
                
                <hr className="border-outline-variant/50" />
                
                {/* Content Sections */}
                <div>
                  <h3 className="font-label-md text-label-md text-secondary mb-2 flex items-center gap-2">
                    <span className="material-symbols-outlined text-[18px]">menu_book</span>
                    Theme Definition
                  </h3>
                  <p className="font-body-md text-body-md text-on-surface leading-relaxed">
                    {selectedTheme.description}
                  </p>
                </div>
                
                {selectedTheme.supporting_evidence && selectedTheme.supporting_evidence.length > 0 && (
                  <div>
                    <h3 className="font-label-md text-label-md text-secondary mb-2 flex items-center gap-2">
                      <span className="material-symbols-outlined text-[18px]">format_quote</span>
                      Example Evidence
                    </h3>
                    <div className="bg-surface-container-low p-4 rounded-lg border-l-4 border-outline-variant relative">
                      <span className="material-symbols-outlined absolute top-2 right-2 text-outline-variant/30 text-4xl">format_quote</span>
                      <p className="font-body-md text-body-md text-on-surface-variant italic relative z-10">
                        "{selectedTheme.supporting_evidence[0].quote}"
                      </p>
                      <div className="mt-3 flex items-center gap-2 font-label-sm text-label-sm text-outline">
                        <span className="material-symbols-outlined text-[14px]">smartphone</span>
                        {selectedTheme.supporting_evidence[0].source}
                      </div>
                    </div>
                  </div>
                )}
                
              </div>
              <div className="p-4 border-t border-outline-variant bg-surface rounded-b-xl">
                <button className="w-full bg-primary text-on-primary font-label-md text-label-md py-2.5 px-4 rounded-lg hover:bg-primary/90 transition-colors shadow-sm flex items-center justify-center gap-2">
                  <span className="material-symbols-outlined text-[18px]">search_insights</span>
                  View related evidence
                </button>
              </div>
            </div>
          )}

        </div>
      </main>
    </>
  );
}
