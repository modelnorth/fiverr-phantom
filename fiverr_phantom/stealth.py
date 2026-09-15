"""
Fiverr Phantom — Stealth Browser Engine
Implements anti-ban, anti-fingerprinting, and humanized heuristics using Patchright.
"""

import os
import time
import random
from typing import Optional
from patchright.sync_api import sync_playwright, BrowserContext, Page

DEFAULT_PROFILE_DIR = os.path.expanduser("~/.fiverr-phantom/profile")
CHROME_PATH = r"C:\Users\DELL\.linkedin-mcp\patchright-browsers\chromium-1234\chrome-win64\chrome.exe"

class PhantomSession:
    def __init__(self, profile_dir: str = DEFAULT_PROFILE_DIR, headless: bool = False):
        self.profile_dir = profile_dir
        self.headless = headless
        self.chrome_path = CHROME_PATH if os.path.exists(CHROME_PATH) else None
        os.makedirs(self.profile_dir, exist_ok=True)
        self._playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self):
        """Launches stealth browser with anti-detection args."""
        self._playwright = sync_playwright().start()
        
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--disable-dev-shm-usage",
            "--lang=en-US,en",
            "--start-maximized"
        ]
        
        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_dir,
            executable_path=self.chrome_path,
            headless=self.headless,
            args=args,
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="Asia/Dubai"
        )
        
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        
        # Deep stealth evasions injection
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            window.chrome = {
                runtime: {},
                loadTimes: () => {},
                csi: () => {}
            };
        """)

    def close(self):
        """Gracefully closes browser resources."""
        try:
            if self.context:
                self.context.close()
        except Exception:
            pass
        try:
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass

    def human_delay(self, min_s: float = 0.8, max_s: float = 2.0):
        """Randomized human pause between interactions."""
        time.sleep(random.uniform(min_s, max_s))

    def human_type(self, selector_or_locator, text: str, min_delay_ms: int = 35, max_delay_ms: int = 100):
        """Simulate realistic keystroke timings with variable speed."""
        el = selector_or_locator if hasattr(selector_or_locator, "click") else self.page.locator(selector_or_locator)
        el.click()
        self.human_delay(0.2, 0.4)
        
        for char in text:
            self.page.keyboard.type(char)
            time.sleep(random.uniform(min_delay_ms / 1000.0, max_delay_ms / 1000.0))
            if char in [".", ",", "!", "\n"]:
                time.sleep(random.uniform(0.15, 0.35))

    def human_scroll(self, distance: int = 400, steps: int = 5):
        """Smooth, staggered scrolling to mimic human browsing."""
        step_dist = distance / steps
        for _ in range(steps):
            self.page.mouse.wheel(0, step_dist + random.randint(-15, 15))
            time.sleep(random.uniform(0.1, 0.2))
        self.human_delay(0.3, 0.7)
