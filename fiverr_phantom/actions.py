"""
Fiverr Phantom Actions — High-level automation methods
"""

import time
from typing import Dict, Any, List, Optional
from .stealth import PhantomSession

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
            except Exception:
                pass
                
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
            return {"status": "error", "error": str(e)}

def update_profile_bio(description: Optional[str] = None, tagline: Optional[str] = None) -> Dict[str, Any]:
    """Update seller bio and one-liner tagline with humanized typing."""
    with PhantomSession(headless=False) as session:
        page = session.page
        page.goto("https://www.fiverr.com/seller_dashboard", wait_until="domcontentloaded", timeout=35000)
        session.human_delay(2, 3)
        
        # Open profile
        avatar = page.locator("a[href*='/users/']").first
        if avatar.count() > 0:
            avatar.click()
            session.human_delay(2, 3)
            
        if tagline:
            pencil = page.locator("button[aria-label*='tagline'], .profile-story-edit, svg.fa-pencil").first
            if pencil.count() > 0:
                pencil.click()
                session.human_delay(0.5, 1.0)
                input_box = page.locator("input[name*='story'], input.tagline-input").first
                if input_box.count() > 0:
                    input_box.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    session.human_type(input_box, tagline)
                    page.keyboard.press("Enter")
                    session.human_delay(1.0, 1.5)
                    
        if description:
            desc_edit = page.locator("a:has-text('Edit Description'), button:has-text('Edit Description')").first
            if desc_edit.count() > 0:
                desc_edit.click()
                session.human_delay(1.0, 1.5)
                desc_area = page.locator("textarea[name*='description'], textarea").first
                if desc_area.count() > 0:
                    desc_area.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    session.human_type(desc_area, description)
                    session.human_delay(0.8, 1.5)
                    update_btn = page.locator("button:has-text('Update')").first
                    if update_btn.count() > 0:
                        update_btn.click()
                        session.human_delay(2.0, 3.0)
                        
        return {"status": "success", "message": "Profile updated with anti-ban heuristics."}

def bulk_add_skills(skills: List[str], level: str = "Expert") -> Dict[str, Any]:
    """Bulk-add search-indexed skills to Fiverr profile."""
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
        for skill in skills:
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
                        select_level.select_option(label=level)
                        session.human_delay(0.4, 0.8)
                        
                    add_btn = page.locator("input[value='Add'], button:has-text('Add')").first
                    if add_btn.count() > 0:
                        add_btn.click()
                        session.human_delay(1.5, 2.5)
                        added.append(skill)
            except Exception:
                pass
                
        return {"status": "success", "added_skills": added}
