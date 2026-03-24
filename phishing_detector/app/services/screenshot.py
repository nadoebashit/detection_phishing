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
                context = await browser.new_context(viewport={"width": 1280, "height": 720})
                page = await context.new_page()
                
                logger.info(f"Navigating to {url}")
                await page.goto(url, timeout=timeout, wait_until="networkidle")
                
                logger.info(f"Taking screenshot for {url}")
                await page.screenshot(path=screenshot_path, full_page=False)
                
                await browser.close()
                return screenshot_path
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while trying to capture {url}")
            raise Exception("Timeout while loading page")
        except Exception as e:
            logger.error(f"Error capturing {url}: {e}")
            raise e
