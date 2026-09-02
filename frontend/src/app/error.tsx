'use client';
import { useEffect } from 'react';
import TopAppBar from '@/components/TopAppBar';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error("Next.js Application Error caught by boundary:", error);
  }, [error]);

  return (
    <>
      <TopAppBar title="Discovery Engine" />
      <div className="flex-1 flex flex-col items-center justify-center p-6 h-[calc(100vh-64px)]">
        <div className="bg-surface-container-low border border-error/20 p-8 rounded-xl max-w-md text-center shadow-sm">
          <span className="material-symbols-outlined text-error text-[48px] mb-4">error</span>
          <h2 className="font-h1 text-h1 text-on-surface mb-2">Unable to load this analysis section.</h2>
          <p className="font-body-md text-body-md text-on-surface-variant mb-6">
            A rendering or data error occurred while trying to display this page.
          </p>
          <button
            onClick={() => reset()}
            className="bg-primary text-on-primary px-6 py-2 rounded-full font-label-md text-label-md hover:bg-primary/90 transition-colors"
          >
            Try again
          </button>
        </div>
      </div>
    </>
  );
}
