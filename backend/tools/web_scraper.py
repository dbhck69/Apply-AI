import asyncio
import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def _extract_text_from_html(html: str) -> str:
    """Parse HTML and extract meaningful text."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove noise elements
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "svg", "iframe"]):
        tag.decompose()
    
    text = soup.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 15]
    return "\n".join(lines[:200])  # First 200 meaningful lines

@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=1, max=4))
async def _scrape_with_httpx(url: str) -> str:
    """Fast scrape using httpx (no browser needed)."""
    async with httpx.AsyncClient(follow_redirects=True, timeout=20.0, headers=HEADERS) as client:
        response = await client.get(url)
        response.raise_for_status()
        return _extract_text_from_html(response.text)

def _scrape_with_playwright_sync(url: str) -> str:
    """Fallback: scrape using Playwright synchronously (handles JS-rendered pages)."""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(2000)
            html = page.content()
        finally:
            browser.close()
    
    return _extract_text_from_html(html)

async def scrape_job_posting(url: str) -> str:
    """Scrape job description from URL. 
    First tries httpx (fast, no dependencies), 
    falls back to Playwright sync in a thread if needed.
    """
    # Attempt 1: Fast httpx scrape
    try:
        text = await _scrape_with_httpx(url)
        if len(text) > 200:
            return text
    except Exception:
        pass
    
    # Attempt 2: Playwright in a thread pool (avoids asyncio subprocess issues on Windows)
    try:
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, _scrape_with_playwright_sync, url)
        if len(text) > 200:
            return text
    except Exception:
        pass
    
    # Attempt 3: Return whatever httpx got, even if short
    try:
        text = await _scrape_with_httpx(url)
        if text:
            return text
    except Exception as e:
        raise RuntimeError(f"All scraping methods failed for {url}: {str(e)}")
    
    raise RuntimeError(f"Could not extract meaningful content from {url}")