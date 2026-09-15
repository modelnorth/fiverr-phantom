"""
Fiverr Phantom — Stealth Browser Engine
Implements anti-ban, anti-fingerprinting, and humanized heuristics using Patchright.
"""

import os
import time
import glob
import secrets
import logging
from typing import Optional
from patchright.sync_api import sync_playwright, BrowserContext, Page

logger = logging.getLogger("fiverr_phantom.stealth")

DEFAULT_PROFILE_DIR = os.path.expanduser("~/.fiverr-phantom/profile")

def find_stealth_browser() -> Optional[str]:
    """Dynamically locates the Patchright/Playwright Chromium binary across OS platforms."""
    # Check custom environment variable first
    env_path = os.getenv("FIVERR_PHANTOM_CHROME_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path

    # Search common Patchright / Playwright cache directories in user home
    home = os.path.expanduser("~")
    search_patterns = [
        os.path.join(home, ".linkedin-mcp", "patchright-browsers", "**", "chrome.exe"),
        os.path.join(home, ".cache", "patchright", "**", "chrome.exe"),
        os.path.join(home, "AppData", "Local", "ms-playwright", "**", "chrome.exe"),
        os.path.join(home, ".cache", "patchright", "**", "chrome"),
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser"
    ]
    for pattern in search_patterns:
        matches = glob.glob(pattern, recursive=True)
        for match in matches:
            if os.path.isfile(match):
                return match
    return None

class PhantomSession:
    def __init__(self, profile_dir: str = DEFAULT_PROFILE_DIR, headless: bool = False):
        self.profile_dir = os.path.abspath(os.path.expanduser(profile_dir))
        self.headless = headless
        self.chrome_path = find_stealth_browser()
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
        """Launches stealth browser with anti-detection args and sandbox enabled."""
        self._playwright = sync_playwright().start()
        
        # Anti-detection launch args (sandbox preserved for host security)
        args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-dev-shm-usage",
            "--lang=en-US,en",
            "--start-maximized"
        ]
        
        # Only add --no-sandbox if explicitly mandated by environment (e.g. root container)
        if os.getenv("DOCKER_CONTAINER") == "1" or os.getenv("CI") == "true":
            args.append("--no-sandbox")
        
        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.profile_dir,
            executable_path=self.chrome_path,
            headless=self.headless,
            args=args,
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            locale="en-US"
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
        if self.context:
            try:
                self.context.close()
            except Exception as e:
                logger.debug("Error closing context: %s", e)
        if self._playwright:
            try:
                self._playwright.stop()
            except Exception as e:
                logger.debug("Error stopping playwright: %s", e)

    def human_delay(self, min_s: float = 0.8, max_s: float = 2.0):
        """Randomized human pause between interactions using secure random generator."""
        delay = min_s + secrets.randbelow(int((max_s - min_s) * 1000) + 1) / 1000.0  # nosec B311
        time.sleep(delay)

    def human_type(self, selector_or_locator, text: str, min_delay_ms: int = 35, max_delay_ms: int = 100):
        """Simulate realistic keystroke timings with variable speed."""
        el = selector_or_locator if hasattr(selector_or_locator, "click") else self.page.locator(selector_or_locator)
        el.click()
        self.human_delay(0.2, 0.4)
        
        for char in text:
            self.page.keyboard.type(char)
            # Secure micro-delay jitter
            jitter_ms = min_delay_ms + secrets.randbelow(max_delay_ms - min_delay_ms + 1)  # nosec B311
            time.sleep(jitter_ms / 1000.0)
            if char in [".", ",", "!", "\n"]:
                p_delay = 0.15 + (secrets.randbelow(200) / 1000.0)  # nosec B311
                time.sleep(p_delay)

    def human_scroll(self, distance: int = 400, steps: int = 5):
        """Smooth, staggered scrolling to mimic human browsing."""
        step_dist = distance / steps
        for _ in range(steps):
            delta = step_dist + (secrets.randbelow(31) - 15)  # nosec B311
            self.page.mouse.wheel(0, delta)
            time.sleep(0.1 + (secrets.randbelow(100) / 1000.0))  # nosec B311
        self.human_delay(0.3, 0.7)
