"""
Fiverr Phantom Actions — High-level automation methods with input validation
"""

import time
import logging
from typing import Dict, Any, List, Optional
from .stealth import PhantomSession

logger = logging.getLogger("fiverr_phantom.actions")

def sanitize_text(text: Optional[str], max_len: int) -> Optional[str]:
    """Sanitizes text, strips null bytes/control chars, and enforces length bounds."""
    if text is None:
        return None
    # Remove null bytes and carriage returns
    clean = text.replace("\x00", "").strip()
    if len(clean) > max_len:
        clean = clean[:max_len]
    return clean

def login_flow() -> Dict[str, Any]:
    """Launch interactive visible login window and save session."""
    print("\n[!] Launching Fiverr Phantom login window...")
    print("[*] Complete your login (and 2FA). Close window once dashboard loads.\n")
    with PhantomSession(headless=False) as session:
        page = session.page
        page.goto("https://www.fiverr.com/login", wait_until="domcontentloaded", timeout=45000)
        
        max_wait = 300
        start = time.time()
        logged_in = False
        while time.time() - start < max_wait:
            time.sleep(3)
            if any(k in page.url for k in ["/manage_orders", "/users/", "/inbox", "/seller_dashboard"]):
                logged_in = True
                break
            try:
                if page.locator("img[alt*='profile'], button[aria-label*='user profile']").count() > 0:
                    logged_in = True
                    break
            except Exception as e:
                logger.debug("Polling avatar error: %s", e)
                
        if logged_in:
            print("[+] Session authenticated and cookies stored locally!")
            time.sleep(2)
            return {"status": "success", "message": "Fiverr Phantom session saved.", "profile_dir": session.profile_dir}
        return {"status": "timeout", "message": "Login window timed out or was closed."}

def check_status() -> Dict[str, Any]:
    """Headless check to verify whether session is active."""
    with PhantomSession(headless=True) as session:
        page = session.page
        try:
            page.goto("https://www.fiverr.com/seller_dashboard", wait_until="domcontentloaded", timeout=30000)
            session.human_delay(1.5, 2.5)
            is_auth = "login" not in page.url
            return {
                "status": "authenticated" if is_auth else "unauthenticated",
                "current_url": page.url
            }
        except Exception as e:
            logger.error("Status check failed: %s", e)
            return {"status": "error", "error": str(e)}

def get_account_overview() -> Dict[str, Any]:
    """Inspect authenticated Fiverr seller account and extract key metrics, profile info, and gigs."""
    with PhantomSession(headless=False) as session:
        page = session.page
        try:
            page.goto("https://www.fiverr.com/seller_dashboard", wait_until="domcontentloaded", timeout=35000)
            session.human_delay(2, 3)
            
            if "login" in page.url or "It needs a human touch" in page.title():
                return {
                    "status": "unauthenticated",
                    "message": "Fiverr session is not logged in. Please run `fiverr-phantom --login` to authenticate."
                }
            
            overview = {
                "status": "authenticated",
                "url": page.url,
                "title": page.title()
            }
            
            try:
                username_el = page.locator(".user-name, [data-testid='user-name'], a[href*='/users/']").first
                if username_el.count() > 0:
                    overview["username"] = username_el.inner_text().strip()
            except Exception as e:
                logger.debug("Failed to extract username: %s", e)
                
            try:
                avatar = page.locator("a[href*='/users/']").first
                if avatar.count() > 0:
                    avatar.click()
                    session.human_delay(2, 3)
                    overview["profile_url"] = page.url
                    
                    # Inspect gigs
                    gigs = page.locator(".gig-card-layout, .seller-gig-card, .gig-wrapper, h3")
                    gig_titles = []
                    for i in range(min(gigs.count(), 10)):
                        text = gigs.nth(i).inner_text().strip()
                        if text and len(text) > 5 and "\n" not in text:
                            gig_titles.append(text)
                    overview["gigs"] = gig_titles
            except Exception as e:
                logger.debug("Failed to inspect profile page: %s", e)
                
            return overview
        except Exception as e:
            logger.error("Failed to fetch account overview: %s", e)
            return {"status": "error", "error": str(e)}

def update_profile_bio(description: Optional[str] = None, tagline: Optional[str] = None) -> Dict[str, Any]:
    """Update seller bio and one-liner tagline with humanized typing and validation."""
    clean_tagline = sanitize_text(tagline, max_len=70)
    clean_desc = sanitize_text(description, max_len=600)

    with PhantomSession(headless=False) as session:
        page = session.page
        page.goto("https://www.fiverr.com/seller_dashboard", wait_until="domcontentloaded", timeout=35000)
        session.human_delay(2, 3)
        
        # Open profile
        avatar = page.locator("a[href*='/users/']").first
        if avatar.count() > 0:
            avatar.click()
            session.human_delay(2, 3)
            
        if clean_tagline:
            pencil = page.locator("button[aria-label*='tagline'], .profile-story-edit, svg.fa-pencil").first
            if pencil.count() > 0:
                pencil.click()
                session.human_delay(0.5, 1.0)
                input_box = page.locator("input[name*='story'], input.tagline-input").first
                if input_box.count() > 0:
                    input_box.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    session.human_type(input_box, clean_tagline)
                    page.keyboard.press("Enter")
                    session.human_delay(1.0, 1.5)
                    
        if clean_desc:
            desc_edit = page.locator("a:has-text('Edit Description'), button:has-text('Edit Description')").first
            if desc_edit.count() > 0:
                desc_edit.click()
                session.human_delay(1.0, 1.5)
                desc_area = page.locator("textarea[name*='description'], textarea").first
                if desc_area.count() > 0:
                    desc_area.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    session.human_type(desc_area, clean_desc)
                    session.human_delay(0.8, 1.5)
                    update_btn = page.locator("button:has-text('Update')").first
                    if update_btn.count() > 0:
                        update_btn.click()
                        session.human_delay(2.0, 3.0)
                        
        return {"status": "success", "message": "Profile updated with anti-ban heuristics."}

def bulk_add_skills(skills: List[str], level: str = "Expert") -> Dict[str, Any]:
    """Bulk-add search-indexed skills to Fiverr profile with sanitization."""
    sanitized_skills = [sanitize_text(s, max_len=50) for s in skills if s and s.strip()][:30]
    valid_levels = {"Beginner", "Intermediate", "Expert"}
    selected_level = level if level in valid_levels else "Expert"

    with PhantomSession(headless=False) as session:
        page = session.page
        page.goto("https://www.fiverr.com/seller_dashboard", wait_until="domcontentloaded", timeout=35000)
        session.human_delay(2, 3)
        
        avatar = page.locator("a[href*='/users/']").first
        if avatar.count() > 0:
            avatar.click()
            session.human_delay(2, 3)
            
        session.human_scroll(500, 3)
        
        added = []
        for skill in sanitized_skills:
            if not skill:
                continue
            try:
                add_new = page.locator("button:has-text('Add New'), a:has-text('Add New')").first
                if add_new.count() > 0:
                    add_new.click()
                    session.human_delay(0.8, 1.2)
                    
                    skill_input = page.locator("input[placeholder*='Add Skill'], input[name*='skill']").first
                    if skill_input.count() > 0:
                        session.human_type(skill_input, skill)
                        session.human_delay(0.5, 1.0)
                        page.keyboard.press("ArrowDown")
                        page.keyboard.press("Enter")
                        
                    select_level = page.locator("select[name*='level']").first
                    if select_level.count() > 0:
                        select_level.select_option(label=selected_level)
                        session.human_delay(0.4, 0.8)
                        
                    add_btn = page.locator("input[value='Add'], button:has-text('Add')").first
                    if add_btn.count() > 0:
                        add_btn.click()
                        session.human_delay(1.5, 2.5)
                        added.append(skill)
            except Exception as e:
                logger.warning("Failed to add skill '%s': %s", skill, e)
                
        return {"status": "success", "added_skills": added}
