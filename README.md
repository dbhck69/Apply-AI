# ApplyAI — Autonomous Job Application Agent

> Transform your job search with AI. Paste a job URL + upload your resume. Get a tailored cover letter, optimized resume, and cold email in under 60 seconds.

![ApplyAI Demo](docs/demo.gif)

## What It Does

ApplyAI is a **multi-agent AI system** built with LangGraph that autonomously:
1. Scrapes and analyzes any job posting URL
2. Rewrites your resume bullets to match the job's keywords and requirements
3. Writes a personalized, non-generic cover letter
4. Drafts a cold outreach email to the hiring manager

## Architecture
```
User Input (Resume PDF + Job URL)
        ↓
  Orchestrator Agent (LangGraph)
  ├── Job Analyst Agent → Extracts skills, requirements, culture
  ├── Resume Optimizer Agent → Tailors resume for ATS + recruiter
  └── Writer Agent → Cover letter + cold email
        ↓
  Output: Complete application package
```

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph |
| LLM | GPT-4o-mini + GPT-4o |
| Backend | FastAPI + Python 3.11 |
| Frontend | Next.js 14 + Tailwind CSS |
| Vector DB | ChromaDB |
| Monitoring | LangSmith |
| Deployment | Railway |

## Quick Start
```bash
git clone https://github.com/yourusername/applyai
cd applyai/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Add your .env file (see .env.example)
uvicorn main:app --reload

# In another terminal
cd ../frontend && npm install && npm run dev
```

Open http://localhost:3000

## Environment Variables
```
OPENAI_API_KEY=           # Required
LANGCHAIN_API_KEY=        # Optional (for LangSmith tracing)
LANGCHAIN_TRACING_V2=true # Optional
```

## Resume Bullet Points (copy to your CV)

- Built a production-grade **multi-agent AI system** using LangGraph with 4 specialized agents (orchestrator, job analyst, resume optimizer, writer)
- Implemented **autonomous web scraping pipeline** using Playwright to extract and parse job postings from any URL
- Designed **stateful agent graph** with conditional edges for error handling, retry logic, and graceful degradation
- Integrated **LangSmith observability** for real-time agent tracing, token monitoring, and performance optimization
- Deployed full-stack application (FastAPI + Next.js) on Railway with Docker, achieving ~45 second end-to-end agent run time

## Live Demo
[applyai.up.railway.app](https://applyai.up.railway.app)