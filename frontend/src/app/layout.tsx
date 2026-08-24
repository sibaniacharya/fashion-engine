import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "Discovery Dashboard",
  description: "AI-Powered Wishlist Behavior Analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="dashboard-layout">
          <Sidebar />
          <main className="main-content glass-panel" style={{ margin: '16px', borderRadius: '24px' }}>
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
