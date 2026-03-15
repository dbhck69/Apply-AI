"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";

interface Results {
  run_id: string;
  status: string;
  cover_letter: string;
  optimized_resume: string;
  cold_email: string;
  errors: string[];
}

const TABS = [
  { key: "cover", label: "Cover Letter", icon: "💌", description: "Personalized, non-generic cover letter" },
  { key: "resume", label: "Optimized Resume", icon: "📄", description: "ATS-optimized resume bullets" },
  { key: "email", label: "Cold Email", icon: "📧", description: "Short outreach to hiring manager" },
] as const;

type TabKey = typeof TABS[number]["key"];

export default function ResultsPage() {
  const [results, setResults] = useState<Results | null>(null);
  const [activeTab, setActiveTab] = useState<TabKey>("cover");
  const [showToast, setShowToast] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const data = sessionStorage.getItem("applyai_results");
    if (data) {
      setResults(JSON.parse(data));
    }
  }, []);

  const getContent = useCallback(() => {
    if (!results) return "";
    switch (activeTab) {
      case "cover": return results.cover_letter;
      case "resume": return results.optimized_resume;
      case "email": return results.cold_email;
      default: return "";
    }
  }, [results, activeTab]);

  const handleCopy = async () => {
    const content = getContent();
    if (!content) return;
    await navigator.clipboard.writeText(content);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 2000);
  };

  const handleDownload = () => {
    const content = getContent();
    if (!content) return;
    const activeTabObj = TABS.find(t => t.key === activeTab);
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `applyai-${activeTabObj?.key || "document"}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!results) {
    return (
      <div className="content-center">
        <div style={{ textAlign: "center" }}>
          <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>📭</div>
          <h2 style={{ fontSize: "1.5rem", fontWeight: 600, marginBottom: "0.5rem" }}>
            No results found
          </h2>
          <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
            Generate an application package first
          </p>
          <button className="btn-primary" style={{ maxWidth: "300px" }} onClick={() => router.push("/")}>
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  const wordCount = getContent().split(/\s+/).filter(Boolean).length;
  const charCount = getContent().length;
  const lineCount = getContent().split("\n").length;

  return (
    <div className="results-container" style={{ paddingTop: "2rem" }}>
      {/* Header */}
      <div className="results-header">
        <h1 className="results-title">
          ✅ Your Application Package
        </h1>
        <p className="results-subtitle">
          Generated for run <code style={{ 
            fontSize: "0.8rem", 
            background: "var(--bg-tertiary)", 
            padding: "2px 8px", 
            borderRadius: "6px",
            fontFamily: "'JetBrains Mono', monospace"
          }}>{results.run_id.slice(0, 8)}</code>
        </p>
      </div>

      {/* Stats */}
      <div className="stats-bar">
        <div className="stat-card">
          <div className="stat-value">{wordCount}</div>
          <div className="stat-label">Words</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{charCount.toLocaleString()}</div>
          <div className="stat-label">Characters</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{lineCount}</div>
          <div className="stat-label">Lines</div>
        </div>
      </div>

      {/* Errors */}
      {results.errors && results.errors.length > 0 && (
        <div className="error-banner" style={{ marginBottom: "1.5rem" }}>
          ⚠️ {results.errors.join(" | ")}
        </div>
      )}

      {/* Tab Bar */}
      <div className="tab-bar">
        {TABS.map(tab => (
          <button
            key={tab.key}
            className={`tab-btn ${activeTab === tab.key ? "active" : ""}`}
            onClick={() => setActiveTab(tab.key)}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Output Card */}
      <div className="output-card">
        <div className="output-card-header">
          <div className="output-card-title">
            <span>{TABS.find(t => t.key === activeTab)?.icon}</span>
            {TABS.find(t => t.key === activeTab)?.description}
          </div>
          <div className="output-card-actions">
            <button className="btn-secondary" onClick={handleCopy} id="copy-btn">
              📋 Copy
            </button>
            <button className="btn-secondary" onClick={handleDownload} id="download-btn">
              ⬇️ Download
            </button>
          </div>
        </div>
        <div className="output-content">
          {getContent() || "No content was generated for this section."}
        </div>
      </div>

      {/* Back Button */}
      <div style={{ textAlign: "center", marginTop: "2rem" }}>
        <button
          className="btn-secondary"
          onClick={() => router.push("/")}
          style={{ padding: "0.75rem 2rem", fontSize: "0.9rem" }}
        >
          ← Generate Another
        </button>
      </div>

      {/* Copy Toast */}
      <div className={`copy-toast ${showToast ? "show" : ""}`}>
        ✅ Copied to clipboard!
      </div>
    </div>
  );
}
