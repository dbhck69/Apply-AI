"""Simple test to check each pipeline step."""
import sys
import os
import asyncio

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def main():
    # Step 1: Find and parse resume
    print("=== STEP 1: Parse Resume ===")
    import glob
    files = glob.glob(os.path.join(os.path.dirname(__file__), "..", "*Resume*"))
    print(f"Found resume files: {files}")
    
    if not files:
        print("ERROR: No resume file found!")
        return
    
    from tools.pdf_parser import parse_resume_pdf
    with open(files[0], "rb") as f:
        resume_text = parse_resume_pdf(f.read())
    
    print(f"Resume text length: {len(resume_text)}")
    print(f"First 200 chars: {resume_text[:200]}")
    
    # Step 2: Test scraper
    print("\n=== STEP 2: Scrape Job ===")
    from tools.web_scraper import scrape_job_posting
    job_url = "https://www.linkedin.com/jobs/view/4378325278"
    try:
        job_text = await scrape_job_posting(job_url)
        print(f"Scraped text length: {len(job_text)}")
        print(f"First 200 chars: {job_text[:200]}")
    except Exception as e:
        print(f"Scraping error: {e}")
        job_text = "fallback"
    
    # Step 3: Full pipeline
    print("\n=== STEP 3: Full Pipeline ===")
    from agents.orchestrator import run_application_agent
    try:
        result = await run_application_agent(
            resume_text=resume_text,
            job_url=job_url
        )
        print(f"Status: {result.get('status')}")
        print(f"Errors: {result.get('errors', [])}")
        print(f"Job Profile: {result.get('job_profile', {})}")
        print(f"Cover Letter length: {len(result.get('cover_letter', ''))}")
        print(f"Optimized Resume length: {len(result.get('optimized_resume', ''))}")
        print(f"Cold Email length: {len(result.get('cold_email', ''))}")
        
        if result.get("cover_letter"):
            print(f"\nCover Letter Preview:\n{result['cover_letter'][:300]}")
    except Exception as e:
        print(f"Pipeline error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
