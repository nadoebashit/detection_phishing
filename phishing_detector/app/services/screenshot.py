import os
import uuid
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from loguru import logger

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

class ScreenshotService:
    @staticmethod
    async def capture(url: str, timeout: int = 30000) -> str:
        """Captures a screenshot of the given URL."""
        if not url.startswith("http"):
            url = "http://" + url
            
        screenshot_filename = f"{uuid.uuid4()}.png"
        screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                # Use a modern standard User-Agent to prevent anti-bot systems (like Cloudflare or Akamai) 
                # from blocking the screenshot request, which often results in a blank/white page.
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                logger.info(f"Navigating to {url}")
                
                # Navigate using "domcontentloaded" first as it's faster and less prone to getting stuck on endless tracking pixels
                try:
                    await page.goto(url, timeout=timeout, wait_until="domcontentloaded")
                except PlaywrightTimeoutError:
                    logger.warning(f"Timeout on 'domcontentloaded' event for {url}, attempting to continue")
                
                # Wait for "load" or "networkidle" state with a smaller timeout so we don't hang on background assets
                try:
                    await page.wait_for_load_state("load", timeout=10000)
                except PlaywrightTimeoutError:
                    logger.warning(f"Timeout waiting for 'load' state for {url}, continuing")
                    
                try:
                    await page.wait_for_load_state("networkidle", timeout=5000)
                except PlaywrightTimeoutError:
                    logger.warning(f"Timeout waiting for 'networkidle' state for {url}, continuing")
                
                # Give JavaScript and client-side hydration/rendering extra time to build the UI (crucial for SPAs)
                # 3000ms is standard and reliable to ensure all elements are visible and loaders have disappeared.
                logger.info("Waiting 3 seconds for dynamic content to render...")
                await page.wait_for_timeout(3000)
                
                logger.info(f"Taking screenshot for {url}")
                await page.screenshot(path=screenshot_path, full_page=False)
                
                await browser.close()
                return screenshot_path
        except Exception as e:
            logger.error(f"Error capturing {url}: {e}")
            raise e
