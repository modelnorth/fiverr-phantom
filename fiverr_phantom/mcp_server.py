"""
Fiverr Phantom FastMCP Server
Exposes anti-ban Fiverr automation tools to Claude Desktop, Antigravity, and Cursor.
"""

from typing import Optional, List, Dict, Any
import json
from mcp.server.fastmcp import FastMCP
from .actions import check_status, get_account_overview, login_flow, update_profile_bio, bulk_add_skills

mcp = FastMCP("fiverr-phantom")

@mcp.tool()
def fiverr_get_status() -> str:
    """Check if the Fiverr Phantom browser session is authenticated and valid."""
    res = check_status()
    return f"Status: {res.get('status')}, Current URL: {res.get('current_url')}"

@mcp.tool()
def fiverr_get_overview() -> str:
    """Inspect the authenticated Fiverr seller account: username, profile URL, and existing gigs."""
    res = get_account_overview()
    return json.dumps(res, indent=2)

@mcp.tool()
def fiverr_launch_login() -> str:
    """Launch interactive visible window to log into Fiverr and persist the session."""
    res = login_flow()
    return json.dumps(res, indent=2)

@mcp.tool()
def fiverr_update_profile(description: Optional[str] = None, tagline: Optional[str] = None) -> str:
    """
    Update seller profile description and/or tagline on Fiverr with anti-ban humanized timing.
    """
    res = update_profile_bio(description=description, tagline=tagline)
    return str(res)

@mcp.tool()
def fiverr_add_skills(skills: List[str], level: str = "Expert") -> str:
    """
    Bulk-add search-indexed skills to the Fiverr seller profile.
    Levels: 'Beginner', 'Intermediate', 'Expert'
    """
    res = bulk_add_skills(skills=skills, level=level)
    return str(res)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
