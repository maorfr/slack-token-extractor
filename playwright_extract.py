#!/usr/bin/env python3
"""
Slack Token Extractor - Playwright Edition

Extract Slack XOXC and XOXD tokens using Playwright automation.
Modern alternative to Selenium with better performance and reliability.

Features:
- Persistent browser profile (login once, reuse session)
- Automatic token extraction from localStorage and cookies
- Works with multiple workspaces
- Optional .env file export

Requirements:
    pip install playwright
    playwright install chromium

Usage:
    python playwright_extract.py [--workspace URL] [--headless] [--output FILE]

Examples:
    # Interactive mode (opens browser)
    python playwright_extract.py

    # Specific workspace
    python playwright_extract.py --workspace https://mycompany.slack.com

    # Headless mode (requires existing session)
    python playwright_extract.py --headless

    # Save to custom file
    python playwright_extract.py --output ~/.slack_tokens.env
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: Playwright not installed.")
    print("Install with: pip install playwright && playwright install chromium")
    sys.exit(1)


# Default persistent profile location
DEFAULT_PROFILE_DIR = Path.home() / ".slack-token-extractor" / "browser-profile"
DEFAULT_OUTPUT_FILE = ".slack_tokens.env"


def extract_tokens(
    workspace_url: str = "https://app.slack.com/client/",
    headless: bool = False,
    profile_dir: Path = DEFAULT_PROFILE_DIR,
) -> dict | None:
    """
    Extract XOXC token and XOXD cookie from Slack.

    Args:
        workspace_url: Slack workspace URL to open
        headless: Run browser in headless mode (requires existing session)
        profile_dir: Directory for persistent browser profile

    Returns:
        Dictionary with 'xoxc_token', 'xoxd_token', and 'team_id' or None on failure
    """
    profile_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print(f"Launching browser (headless={headless})...")
        print(f"Profile directory: {profile_dir}")

        browser = p.chromium.launch_persistent_context(
            str(profile_dir),
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            viewport={"width": 1280, "height": 800},
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        print(f"Navigating to {workspace_url}...")
        page.goto(workspace_url)

        # Wait for page to load
        try:
            page.wait_for_load_state("networkidle", timeout=30000)
        except PlaywrightTimeout:
            pass  # Continue anyway, page might be loaded enough

        # Check if we need to log in
        current_url = page.url
        if "signin" in current_url or "sign_in" in current_url or "ssb/signin" in current_url:
            if headless:
                print("\nError: Not logged in and running in headless mode.")
                print("Run without --headless first to log in.")
                browser.close()
                return None

            print("\n" + "=" * 60)
            print("Please log in to Slack in the browser window.")
            print("Press ENTER here when you're logged in and see your workspace...")
            print("=" * 60)
            input()

            # Wait for redirect to workspace
            try:
                page.wait_for_url("**/client/**", timeout=10000)
                page.wait_for_load_state("networkidle", timeout=30000)
            except PlaywrightTimeout:
                pass

        # Extract team ID from URL
        current_path = page.url
        team_id_match = re.search(r"/client/([A-Z0-9]+)", current_path)

        if not team_id_match:
            # Try to get it from localStorage
            team_id = page.evaluate("""() => {
                try {
                    const config = JSON.parse(localStorage.localConfig_v2 || '{}');
                    const teams = Object.keys(config.teams || {});
                    return teams[0] || null;
                } catch { return null; }
            }""")
        else:
            team_id = team_id_match.group(1)

        if not team_id:
            print("\nError: Could not determine team ID.")
            print("Make sure you're viewing a Slack workspace.")
            browser.close()
            return None

        print(f"Found team ID: {team_id}")

        # Extract XOXC token from localStorage
        print("Extracting XOXC token from localStorage...")
        xoxc_token = page.evaluate("""(teamId) => {
            try {
                const config = JSON.parse(localStorage.localConfig_v2 || '{}');
                if (config.teams && config.teams[teamId]) {
                    return config.teams[teamId].token;
                }
                // Fallback: search all teams
                for (const [tid, data] of Object.entries(config.teams || {})) {
                    if (data.token && data.token.startsWith('xoxc-')) {
                        return data.token;
                    }
                }
            } catch {}
            return null;
        }""", team_id)

        if not xoxc_token:
            # Fallback: try to find in page content
            xoxc_token = page.evaluate("""() => {
                const match = document.body.innerHTML.match(/"token":"(xoxc-[^"]+)"/);
                return match ? match[1] : null;
            }""")

        if not xoxc_token:
            print("\nError: Could not find XOXC token.")
            print("Make sure you're logged in and the workspace is fully loaded.")
            browser.close()
            return None

        print(f"Found XOXC token: {xoxc_token[:25]}...{xoxc_token[-10:]}")

        # Extract XOXD cookie
        print("Extracting XOXD token from cookies...")
        cookies = browser.cookies()
        xoxd_token = None

        for cookie in cookies:
            if cookie["name"] == "d" and "slack.com" in cookie["domain"]:
                xoxd_token = cookie["value"]
                break

        if not xoxd_token:
            print("\nError: Could not find 'd' cookie (XOXD token).")
            browser.close()
            return None

        print(f"Found XOXD token: {xoxd_token[:25]}...{xoxd_token[-10:]}")

        browser.close()

        return {
            "xoxc_token": xoxc_token,
            "xoxd_token": xoxd_token,
            "team_id": team_id,
        }


def save_tokens(tokens: dict, output_file: str) -> None:
    """Save tokens to a .env file."""
    with open(output_file, "w") as f:
        f.write(f"# Slack tokens extracted by slack-token-extractor\n")
        f.write(f"# Team ID: {tokens['team_id']}\n\n")
        f.write(f"SLACK_MCP_XOXC_TOKEN={tokens['xoxc_token']}\n")
        f.write(f"SLACK_MCP_XOXD_TOKEN={tokens['xoxd_token']}\n")

    # Secure the file
    os.chmod(output_file, 0o600)
    print(f"\nTokens saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract Slack XOXC and XOXD tokens using Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Interactive mode
  %(prog)s --headless                # Headless (needs prior login)
  %(prog)s --workspace https://myco.slack.com
  %(prog)s --output ~/.config/slack/tokens.env
        """,
    )
    parser.add_argument(
        "--workspace",
        "-w",
        default="https://app.slack.com/client/",
        help="Slack workspace URL (default: app.slack.com)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (requires existing session)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output file for tokens (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "--profile-dir",
        type=Path,
        default=DEFAULT_PROFILE_DIR,
        help=f"Browser profile directory (default: {DEFAULT_PROFILE_DIR})",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't prompt to save tokens to file",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Slack Token Extractor - Playwright Edition")
    print("=" * 60)
    print()

    tokens = extract_tokens(
        workspace_url=args.workspace,
        headless=args.headless,
        profile_dir=args.profile_dir,
    )

    if not tokens:
        sys.exit(1)

    print()
    print("=" * 60)
    print("Extraction successful!")
    print("=" * 60)
    print()
    print(f"SLACK_MCP_XOXC_TOKEN={tokens['xoxc_token']}")
    print(f"SLACK_MCP_XOXD_TOKEN={tokens['xoxd_token']}")
    print()

    if not args.no_save:
        save_choice = input(f"Save to {args.output}? [Y/n]: ").strip().lower()
        if save_choice in ("", "y", "yes"):
            save_tokens(tokens, args.output)

    print("\nDone!")


if __name__ == "__main__":
    main()
