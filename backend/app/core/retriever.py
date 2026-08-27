import asyncio
import httpx
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from readability import Document
import markdownify

async def extract_markdown(html: str) -> str:
    """Extracts main content from HTML and converts it to Markdown."""
    doc = Document(html)
    main_html = doc.summary()
    soup = BeautifulSoup(main_html, "lxml")
    md_content = markdownify.markdownify(
        str(soup), 
        heading_style="ATX", 
        strip=['script', 'style']
    )
    md_content = "\n".join([line for line in md_content.splitlines() if line.strip() or line == ""])
    return md_content.strip()

async def fetch_public(url: str) -> str | None:
    """Attempts to fetch the URL normally. Returns Markdown if successful and not blocked, else None."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            response = await client.get(url)
            
            if response.status_code in (401, 403):
                print("Public fetch hit 401/403.")
                return None
                
            response.raise_for_status()
            
            final_url = str(response.url).lower()
            if "login" in final_url or "signin" in final_url or "auth" in final_url:
                print(f"Public fetch redirected to auth page: {final_url}")
                return None
            
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                return response.text
                
            md = await extract_markdown(response.text)
            
            if len(md.strip()) < 100:
                print("Public fetch returned virtually empty content (likely an SPA shell).")
                return None
                
            return md
    except Exception as e:
        print(f"Public fetch failed: {e}")
        return None

def _fetch_authenticated_sync(url: str) -> str:
    """
    Sync function that runs Playwright in a thread.
    Uses sync_api to avoid the Windows asyncio subprocess bug.
    """
    user_data_dir = "./playwright_profile"
    
    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        
        page = browser_context.new_page()
        
        try:
            print(f"Navigating to {url}...")
            page.goto(url, wait_until="domcontentloaded")
            
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except PlaywrightTimeoutError:
                pass
                
            is_login_page = page.evaluate('''() => {
                return !!document.querySelector('input[type="password"]') || 
                       window.location.href.toLowerCase().includes('login') ||
                       window.location.href.toLowerCase().includes('signin') ||
                       window.location.href.toLowerCase().includes('auth');
            }''')
            
            if is_login_page:
                print("Authentication required. Please log in using the opened browser window.")
                print("Waiting for you to complete login (up to 5 minutes)...")
                
                try:
                    page.wait_for_function('''() => {
                        return !document.querySelector('input[type="password"]') &&
                               !window.location.href.toLowerCase().includes('login');
                    }''', timeout=300000)
                    
                    page.wait_for_load_state("networkidle", timeout=10000)
                    
                    if url not in page.url:
                        print(f"Redirecting back to target resource: {url}")
                        page.goto(url, wait_until="networkidle")
                        
                except PlaywrightTimeoutError:
                    print("Timeout waiting for manual login.")
                    
            print("Extracting content...")
            html_content = page.content()
            
            # Extract markdown synchronously here since we're in a thread
            doc = Document(html_content)
            main_html = doc.summary()
            soup = BeautifulSoup(main_html, "lxml")
            md_content = markdownify.markdownify(
                str(soup), 
                heading_style="ATX", 
                strip=['script', 'style']
            )
            md_content = "\n".join([line for line in md_content.splitlines() if line.strip() or line == ""])
            return md_content.strip()
            
        finally:
            browser_context.close()

async def fetch_authenticated(url: str) -> str:
    """Runs Playwright in a background thread to avoid Windows asyncio issues."""
    return await asyncio.to_thread(_fetch_authenticated_sync, url)

async def get_context(url: str) -> str:
    """Main entrypoint: tries public fetch, falls back to authenticated fetch."""
    print(f"Attempting normal public fetch for: {url}")
    public_result = await fetch_public(url)
    
    if public_result:
        print("Successfully retrieved publicly.")
        return public_result
        
    print("Public fetch failed or requires authentication. Falling back to authorized session...")
    return await fetch_authenticated(url)
