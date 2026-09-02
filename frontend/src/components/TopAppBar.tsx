export default function TopAppBar({ title, breadcrumbs }: { title?: string, breadcrumbs?: string[] }) {
  return (
    <header className="flex justify-between items-center h-16 px-gutter bg-surface dark:bg-surface-container-low border-b border-outline-variant dark:border-outline sticky top-0 z-40">
      <div className="flex items-center gap-2">
        {breadcrumbs && breadcrumbs.length > 0 ? (
          <div className="font-h2 text-h2 text-on-surface dark:text-on-surface-variant flex items-center gap-2">
            {breadcrumbs.map((crumb, idx) => (
              <span key={idx} className="flex items-center gap-2">
                <span className={idx === breadcrumbs.length - 1 ? '' : 'text-on-surface-variant/50'}>
                  {crumb}
                </span>
                {idx < breadcrumbs.length - 1 && (
                  <span className="text-on-surface-variant/30">/</span>
                )}
              </span>
            ))}
          </div>
        ) : (
          <div className="flex flex-col">
            <span className="font-h1 text-h1 text-primary">{title || 'Discovery Engine'}</span>
            <span className="font-label-sm text-label-sm text-on-surface-variant">
              AI-powered customer feedback intelligence
            </span>
          </div>
        )}
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-4 text-on-surface-variant dark:text-on-secondary-fixed-variant">
          <button className="hover:text-primary dark:hover:text-primary-fixed-dim transition-colors p-2 rounded-full hover:bg-surface-container-highest">
            <span className="material-symbols-outlined">notifications</span>
          </button>
          <button className="hover:text-primary dark:hover:text-primary-fixed-dim transition-colors p-2 rounded-full hover:bg-surface-container-highest">
            <span className="material-symbols-outlined">settings</span>
          </button>
          <div className="w-8 h-8 rounded-full bg-secondary-container flex items-center justify-center border border-outline-variant cursor-pointer ml-2 overflow-hidden">
            <span className="material-symbols-outlined text-on-secondary-container">person</span>
          </div>
        </div>
      </div>
    </header>
  );
}
