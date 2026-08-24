'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { href: '/', label: 'Overview & Ranking' },
    { href: '/themes', label: 'Themes & Care' },
    { href: '/journey', label: 'Journey Analytics' },
    { href: '/evidence', label: 'Evidence Explorer' },
  ];

  return (
    <div className="sidebar">
      <div style={{ marginBottom: '40px' }}>
        <h2 className="gradient-text" style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0 }}>
          Discovery Engine
        </h2>
        <p style={{ fontSize: '0.8rem', marginTop: '4px' }}>AI Wishlist Analysis</p>
      </div>

      <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {links.map((link) => {
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              style={{
                textDecoration: 'none',
                padding: '12px 16px',
                borderRadius: '8px',
                color: isActive ? '#fff' : 'var(--text-secondary)',
                background: isActive ? 'rgba(255,255,255,0.1)' : 'transparent',
                fontWeight: isActive ? 600 : 400,
                transition: 'all 0.2s',
                border: isActive ? '1px solid rgba(255,255,255,0.15)' : '1px solid transparent'
              }}
            >
              {link.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
