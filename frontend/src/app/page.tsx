"use client";
import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";

const AGENT_STEPS = [
  { id: "scrape", emoji: "🔍", label: "Scraping job posting..." },
  { id: "analyze", emoji: "🧠", label: "Analyzing requirements with AI..." },
  { id: "optimize", emoji: "📝", label: "Optimizing your resume for ATS..." },
  { id: "write", emoji: "✍️", label: "Writing cover letter & cold email..." },
];

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobUrl, setJobUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(-1);
  const [error, setError] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const router = useRouter();

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith(".pdf")) {
      setFile(droppedFile);
    }
  }, []);

  const handleSubmit = async () => {
    if (!file || !jobUrl) return;
    setLoading(true);
    setError("");

    // Animate step progress while waiting
    AGENT_STEPS.forEach((_, i) => {
      setTimeout(() => setActiveStep(i), i * 5000);
    });

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_url", jobUrl);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/apply`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ detail: "Server error" }));
        throw new Error(errData.detail || "Request failed");
      }

      const data = await res.json();
      sessionStorage.setItem("applyai_results", JSON.stringify(data));
      router.push("/results");
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
      setLoading(false);
      setActiveStep(-1);
    }
  };

  return (
    <div className="content-center">
      <div className="hero">
        {/* Pill badge */}
        <div className="hero-pill">
          <span className="hero-pill-dot" />
          Powered by GPT-4o + LangGraph
        </div>

        {/* Title */}
        <h1 className="hero-title">
          Your AI-Powered<br />
          <span className="hero-title-gradient">Job Application Agent</span>
        </h1>

        {/* Subtitle */}
        <p className="hero-subtitle">
          Upload your resume, paste a job URL, and get a tailored cover letter, 
          ATS-optimized resume, and cold email — all in under 60 seconds.
        </p>

        {/* Form Card */}
        <div className="glass-card" style={{ textAlign: "left" }}>
          {/* Resume Upload */}
          <div className="form-group">
            <label className="form-label">
              <span className="form-label-icon">📄</span>
              Resume
            </label>
            <div
              className={`upload-zone ${file ? "has-file" : ""} ${dragActive ? "has-file" : ""}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                id="resume-upload"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              {file ? (
                <div className="upload-file-name">
                  ✅ {file.name}
                </div>
              ) : (
                <>
                  <div className="upload-icon">📎</div>
                  <div className="upload-text">
                    <strong>Click to upload</strong> or drag & drop
                  </div>
                  <div className="upload-hint">PDF only · Max 10MB</div>
                </>
              )}
            </div>
          </div>

          {/* Job URL Input */}
          <div className="form-group">
            <label className="form-label" htmlFor="job-url">
              <span className="form-label-icon">🔗</span>
              Job Posting URL
            </label>
            <input
              id="job-url"
              type="url"
              className="url-input"
              value={jobUrl}
              onChange={(e) => setJobUrl(e.target.value)}
              placeholder="https://jobs.lever.co/company/senior-engineer"
            />
          </div>

          {/* Submit Button */}
          <button
            id="submit-btn"
            className="btn-primary"
            onClick={handleSubmit}
            disabled={loading || !file || !jobUrl}
          >
            {loading ? (
              <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
                <span className="spinner" />
                Agents are working...
              </span>
            ) : (
              "Generate Application Package →"
            )}
          </button>

          {/* Error Banner */}
          {error && (
            <div className="error-banner">
              ⚠️ {error}
            </div>
          )}

          {/* Agent Progress Panel */}
          {loading && (
            <div className="progress-panel">
              <div className="progress-title">Agent Pipeline</div>
              {AGENT_STEPS.map((step, i) => {
                let status: string;
                if (i < activeStep) status = "done";
                else if (i === activeStep) status = "active";
                else status = "pending";

                return (
                  <div className="progress-step" key={step.id}>
                    <div className={`progress-indicator ${status}`}>
                      {status === "done" ? "✓" : status === "active" ? "●" : (i + 1)}
                    </div>
                    <span className={`progress-text ${status}`}>
                      {step.emoji} {step.label}
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Feature Highlights */}
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <div className="feature-title">ATS Optimized</div>
            <div className="feature-desc">Resume bullets rewritten to match the job&apos;s keywords</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <div className="feature-title">Multi-Agent AI</div>
            <div className="feature-desc">4 specialized agents work together via LangGraph</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <div className="feature-title">Under 60s</div>
            <div className="feature-desc">Full cover letter, resume, and cold email in seconds</div>
          </div>
        </div>
      </div>
    </div>
  );
}
