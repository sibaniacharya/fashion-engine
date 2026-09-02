'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { name: 'Overview', href: '/', icon: 'dashboard' },
    { name: 'Themes', href: '/themes', icon: 'topic' },
    { name: 'Customer Journey', href: '/journey', icon: 'alt_route' },
    { name: 'Opportunities', href: '/opportunities', icon: 'lightbulb' },
    { name: 'Evidence Explorer', href: '/evidence', icon: 'search_insights' },
    { name: 'Behavioral Segments', href: '/segments', icon: 'groups' },
    { name: 'Data Quality', href: '/data-quality', icon: 'data_thresholding' },
  ];

  return (
    <nav className="fixed left-0 top-0 h-full w-[240px] bg-inverse-surface dark:bg-inverse-surface flex flex-col z-50 text-white">
      {/* Brand Header */}
      <div className="px-6 py-8 border-b border-white/10">
        <h1 className="font-h1 text-h1 text-primary-fixed dark:text-primary-fixed-dim tracking-tight">
          Discovery Engine
        </h1>
        <p className="font-label-sm text-label-sm text-secondary-fixed-dim mt-1 uppercase tracking-wider">
          Enterprise Analytics
        </p>
      </div>

      {/* Main Navigation */}
      <div className="flex-1 py-6 overflow-y-auto custom-scrollbar">
        <ul className="space-y-1">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={`flex items-center gap-3 px-4 py-3 transition-colors duration-200 ${
                    isActive
                      ? 'bg-white/10 text-white border-l-4 border-primary-fixed opacity-100'
                      : 'text-secondary-fixed-dim hover:text-white hover:bg-white/5'
                  }`}
                >
                  <span
                    className={`material-symbols-outlined ${isActive ? 'icon-filled' : ''}`}
                    style={{ fontSize: '20px' }}
                  >
                    {link.icon}
                  </span>
                  <span className="font-label-md text-label-md">{link.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </div>

      {/* Footer Navigation */}
      <div className="px-4 py-6 border-t border-white/10">
        <ul className="space-y-1">
          <li>
            <a
              href="#"
              className="flex items-center gap-3 text-secondary-fixed-dim hover:text-white px-4 py-2 hover:bg-white/5 transition-colors duration-200"
            >
              <span className="material-symbols-outlined text-[18px]">sync</span>
              <span className="font-label-sm text-label-sm">Analysis Status</span>
            </a>
          </li>
          <li>
            <a
              href="#"
              className="flex items-center gap-3 text-secondary-fixed-dim hover:text-white px-4 py-2 hover:bg-white/5 transition-colors duration-200"
            >
              <span className="material-symbols-outlined text-[18px]">history</span>
              <span className="font-label-sm text-label-sm">Data Freshness</span>
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
}
