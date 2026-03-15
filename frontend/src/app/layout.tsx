import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ApplyAI — Autonomous Job Application Agent",
  description: "Transform your job search with AI. Paste a job URL + upload your resume. Get a tailored cover letter, optimized resume, and cold email in under 60 seconds.",
  keywords: ["AI", "job application", "resume optimizer", "cover letter", "cold email", "LangGraph"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {/* Animated Background Elements */}
        <div className="bg-grid" />
        <div className="bg-radial-glow" />
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />

        {/* Navbar */}
        <nav className="navbar">
          <a href="/" className="navbar-brand">
            <div className="navbar-logo">A</div>
            <span className="navbar-title">ApplyAI</span>
            <span className="navbar-badge">Beta</span>
          </a>
          <div className="navbar-links">
            <a href="https://github.com" target="_blank" rel="noreferrer" className="navbar-link">
              GitHub
            </a>
          </div>
        </nav>

        {/* Page Content */}
        <div className="page-container">
          {children}
        </div>
      </body>
    </html>
  );
}
