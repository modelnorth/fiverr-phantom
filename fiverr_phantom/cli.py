"""
Fiverr Phantom CLI Entrypoint
"""

import sys
import argparse
import json
from .actions import login_flow, check_status, get_account_overview, update_profile_bio, bulk_add_skills

def main():
    parser = argparse.ArgumentParser(
        prog="fiverr-phantom",
        description="Fiverr Phantom — Autonomous Anti-Ban Stealth Automation Suite for Fiverr Sellers"
    )
    parser.add_argument("--login", action="store_true", help="Launch interactive visible window to log in and save session")
    parser.add_argument("--status", action="store_true", help="Check if current stored session is valid")
    parser.add_argument("--overview", action="store_true", help="Inspect authenticated seller account, active orders, and gigs")
    parser.add_argument("--update-bio", action="store_true", help="Update profile tagline and bio description")
    parser.add_argument("--tagline", type=str, default=None, help="One-liner seller tagline")
    parser.add_argument("--description", type=str, default=None, help="Full seller bio description")
    parser.add_argument("--add-skills", type=str, default=None, help="Comma-separated list of skills to add")
    parser.add_argument("--level", type=str, default="Expert", help="Experience level for added skills (Beginner, Intermediate, Expert)")

    args = parser.parse_args()

    if args.login:
        res = login_flow()
        print(json.dumps(res, indent=2))
    elif args.status:
        res = check_status()
        print(json.dumps(res, indent=2))
    elif args.overview:
        res = get_account_overview()
        print(json.dumps(res, indent=2))
    elif args.update_bio:
        res = update_profile_bio(description=args.description, tagline=args.tagline)
        print(json.dumps(res, indent=2))
    elif args.add_skills:
        skills = [s.strip() for s in args.add_skills.split(",") if s.strip()]
        res = bulk_add_skills(skills, level=args.level)
        print(json.dumps(res, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
