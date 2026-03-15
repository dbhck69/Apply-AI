"""End-to-end test of the ApplyAI pipeline."""
import asyncio
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_pipeline():
    print("=" * 60)
    print("  ApplyAI - End-to-End Pipeline Test")
    print("=" * 60)
    
    # Step 1: Parse resume
    print("\n[1/4] Parsing resume PDF...")
    from tools.pdf_parser import parse_resume_pdf
    
    resume_path = os.path.join(os.path.dirname(__file__), "..", "Deepak's_Resume.pdf")
    resume_path = os.path.abspath(resume_path)
    print(f"  Looking for: {resume_path}")
    
    if not os.path.exists(resume_path):
        print(f"  ERROR: Resume not found at {resume_path}")
        return
    
    with open(resume_path, "rb") as f:
        resume_bytes = f.read()
    
    resume_text = parse_resume_pdf(resume_bytes)
    print(f"  OK - Extracted {len(resume_text)} characters from resume")
    print(f"  Preview: {resume_text[:150]}...")
    
    # Step 2: Scrape job posting
    print("\n[2/4] Scraping job posting...")
    from tools.web_scraper import scrape_job_posting
    
    job_url = "https://www.linkedin.com/jobs/view/4378325278"
    job_text = None
    try:
        job_text = await scrape_job_posting(job_url)
        print(f"  OK - Scraped {len(job_text)} characters from job posting")
        print(f"  Preview: {job_text[:150]}...")
    except Exception as e:
        print(f"  WARN - Scraping failed: {e}")
        print("  Using sample job text for testing...")
        job_text = None
    
    # If scraping failed, inject sample text directly into state
    if not job_text or len(job_text) < 100:
        print("  Using fallback sample job text...")
        job_text = """
Software Engineer - Full Stack at TechCorp
Location: Bangalore, India (Remote)
Experience: 2-4 years

About the Role:
We are looking for a talented Full Stack Software Engineer to join our engineering team.
You will design, develop, and maintain scalable web applications serving millions of users.

Required Skills:
- Python, JavaScript/TypeScript
- React.js or Next.js
- Node.js, FastAPI or Django
- PostgreSQL, MongoDB
- REST APIs, GraphQL
- Git, CI/CD pipelines

Nice to Have:
- Docker, Kubernetes
- AWS or GCP
- Machine Learning basics
- Agile/Scrum methodology

Tech Stack: Python, FastAPI, React, Next.js, PostgreSQL, Redis, Docker, AWS, LangChain

Company Culture: Innovation, collaboration, growth mindset, diversity, work-life balance, continuous learning

About TechCorp:
TechCorp is a leading technology company building AI-powered solutions for enterprise customers.
We value creativity, technical excellence, and a passion for solving complex problems.
        """
    
    # Step 3: Run the full agent pipeline
    print("\n[3/4] Running agent pipeline (this may take 30-60s)...")
    from agents.orchestrator import run_application_agent
    
    try:
        result = await run_application_agent(
            resume_text=resume_text,
            job_url=job_url,
            preferences="professional, concise"
        )
    except Exception as e:
        print(f"  ERROR in pipeline: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Display results
    print("\n[4/4] Results:")
    print(f"  Status: {result.get('status', 'unknown')}")
    errors = result.get('errors', [])
    if errors:
        print(f"  Errors: {errors}")
    
    if result.get("job_profile"):
        jp = result["job_profile"]
        print(f"\n  Job Profile:")
        print(f"     Title: {jp.get('title', 'N/A')}")
        print(f"     Company: {jp.get('company', 'N/A')}")
        print(f"     Skills: {jp.get('required_skills', [])}")
    
    if result.get("optimized_resume"):
        print(f"\n  Optimized Resume: {len(result['optimized_resume'])} chars")
        print(f"     Preview: {result['optimized_resume'][:150]}...")
    
    if result.get("cover_letter"):
        print(f"\n  Cover Letter: {len(result['cover_letter'])} chars")
        print(f"     Preview: {result['cover_letter'][:150]}...")
    
    if result.get("cold_email"):
        print(f"\n  Cold Email: {len(result['cold_email'])} chars")
        print(f"     Preview: {result['cold_email'][:150]}...")
    
    print("\n" + "=" * 60)
    if result.get("status") == "done":
        print("  PIPELINE TEST PASSED!")
    else:
        print("  Pipeline completed with issues - check errors above")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_pipeline())
