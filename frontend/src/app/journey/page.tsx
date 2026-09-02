'use client';
import { useEffect, useState } from 'react';
import TopAppBar from '@/components/TopAppBar';
import { ApiClient, WishlistBehavior, PurchaseBarriers, ExternalResearch } from '@/lib/api';

const WISHLIST_LABELS: Record<string, string> = {
  EXPLICIT_WISHLIST: "Explicit wishlist",
  EXPLICIT_PURCHASE_INTENT: "Explicit purchase intent",
  GENERAL_PRODUCT_INTEREST: "General product interest",
  PURCHASE_EVALUATION: "Purchase evaluation",
  COMPARISON: "Comparison",
  POSTPONEMENT: "Postponement",
  ABANDONMENT: "Abandonment",
  BOOKMARKING: "Bookmarking",
  UNKNOWN: "Unknown"
};

const JOURNEY_STAGES = [
  "Product Discovery",
  "Product Interest",
  "Wishlist",
  "Wishlist Revisit",
  "Evaluation",
  "Comparison",
  "Purchase Intent",
  "Checkout",
  "Purchase"
];

export default function Journey() {
  const [wishlist, setWishlist] = useState<WishlistBehavior | null>(null);
  const [barriers, setBarriers] = useState<PurchaseBarriers | null>(null);
  const [research, setResearch] = useState<ExternalResearch | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      ApiClient.getWishlistBehavior(),
      ApiClient.getPurchaseBarriers(),
      ApiClient.getExternalResearch()
    ]).then(([w, b, r]) => {
      setWishlist(w);
      setBarriers(b);
      setResearch(r);
      setLoading(false);
    }).catch(e => {
      console.error(e);
      setError("Failed to load journey data.");
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center h-screen">
        <div className="font-label-md text-label-md text-on-surface-variant">Loading journey analytics...</div>
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
      <TopAppBar title="Customer Journey" breadcrumbs={['Discovery Engine', 'Journey Analytics']} />

      <main className="flex-1 p-margin-page mx-auto w-full max-w-container-max flex flex-col gap-8">

        <div className="flex flex-col gap-2">
          <h1 className="font-display-lg text-display-lg text-on-surface">Product Journey Model</h1>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-3xl">
            This research framework tracks qualitative feedback mapped to theoretical stages of the wishlist-to-purchase funnel.
            <br/><span className="text-error font-medium">Disclaimer:</span> This model represents observed friction in public feedback, not actual measured conversion drop-offs.
          </p>
        </div>

        {/* Theoretical Funnel Graphic */}
        <section className="bg-surface-container-lowest border border-outline-variant rounded-xl p-6 shadow-sm">
          <h2 className="font-h2 text-h2 text-on-surface mb-6">Wishlist-to-Purchase Theoretical Framework</h2>
          <div className="flex flex-wrap gap-2 items-center text-sm font-medium text-on-surface-variant">
            {JOURNEY_STAGES.map((stage, idx) => (
              <div key={idx} className="flex items-center gap-2">
                <span className="px-3 py-1.5 bg-surface-container-low border border-outline-variant rounded-full text-center">
                  {stage}
                </span>
                {idx < JOURNEY_STAGES.length - 1 && (
                  <span className="material-symbols-outlined text-outline-variant">arrow_forward</span>
                )}
              </div>
            ))}
          </div>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* Wishlist Intent Signals */}
          <section className="bg-surface-container-lowest border border-outline-variant rounded-xl p-6 shadow-sm flex flex-col">
            <h2 className="font-h2 text-h2 text-on-surface mb-2">Wishlist Intent Signals</h2>
            <p className="font-body-sm text-body-sm text-on-surface-variant mb-6">
              Distribution of intent signals mined from the dataset.
            </p>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {Object.entries(wishlist?.bookmarking_vs_intent || {}).sort((a: any, b: any) => b[1] - a[1]).map(([intentKey, count]: any) => (
                <div key={intentKey} className="bg-surface-container-low p-4 rounded-lg border border-outline-variant">
                  <div className="font-display-md text-display-md text-primary mb-1">{count}</div>
                  <div className="font-label-sm text-label-sm text-on-surface-variant">
                    {WISHLIST_LABELS[intentKey] || intentKey}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Friction Points mapped to Journey */}
          <section className="bg-surface-container-lowest border border-outline-variant rounded-xl p-6 shadow-sm flex flex-col">
            <h2 className="font-h2 text-h2 text-on-surface mb-2">Observed Friction Points</h2>
            <p className="font-body-sm text-body-sm text-on-surface-variant mb-6">
              Top reasons users reported abandoning or postponing purchases.
            </p>

            <div className="flex flex-col gap-3 flex-1 overflow-y-auto">
              {barriers?.top_barriers && Object.entries(barriers.top_barriers).map(([b, data]: any) => (
                <div key={b} className="bg-surface-container-low p-4 rounded-lg border border-outline-variant">
                  <div className="flex justify-between items-start mb-2">
                    <strong className="font-label-md text-label-md text-on-surface">{b}</strong>
                    <span className="font-label-sm text-label-sm px-2 py-0.5 bg-error/10 text-error rounded">
                      {data.total_mentions} mentions
                    </span>
                  </div>
                  {data.representative_quotes && data.representative_quotes.length > 0 && (
                    <p className="font-body-sm text-body-sm text-on-surface-variant italic border-l-2 border-outline-variant pl-2">
                      "{data.representative_quotes[0]}"
                    </p>
                  )}
                </div>
              ))}
            </div>
          </section>

        </div>
      </main>
    </>
  );
}
