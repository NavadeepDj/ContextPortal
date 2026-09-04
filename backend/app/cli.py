import argparse
import sys
import asyncio
from typing import Optional

def run_mcp() -> None:
    """Run the ContextPortal MCP server."""
    from app.mcp.server import main as mcp_main
    mcp_main()

def run_login(start_url: Optional[str] = None) -> None:
    """Launch persistent browser for manual login and session seeding."""
    from playwright.sync_api import sync_playwright
    import time
    from pathlib import Path
    
    # Use global profile directory so sessions persist no matter where the CLI is run
    profile_dir = Path.home() / ".contextportal" / "playwright_profile"
    print(f"Using persistent profile at: {profile_dir}")
    print("A browser window will now open.")
    print("1. Navigate to the websites you want your AI agent to access.")
    print("2. Log in manually (solve captchas, use SSO, etc.).")
    print("3. Close the browser window when you are finished.")
    print("\nLaunching browser...\n")
    
    with sync_playwright() as p:
        # We launch headful (headless=False) so the user can interact
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            channel="chrome",  # ADR-003: Transparent automation
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        
        if start_url:
            print(f"Navigating to {start_url}...")
            page.goto(start_url)
        else:
            page.goto("about:blank")
            
        print("\nWaiting for you to close the browser window...")
        print("Your session will be saved automatically.")
        
        # Keep process alive until user closes the context/browser
        try:
            while browser_context.pages:
                time.sleep(1)
        except Exception:
            pass
            
    print("\nBrowser closed. Session saved successfully!")
    print("You can now ask your AI agent to fetch authenticated resources.")

def run_fetch(url: str) -> None:
    """Fetch a URL directly from the CLI (useful for testing without an agent)."""
    from app.core.retriever import get_context
    
    print(f"Fetching context for: {url}\n")
    
    async def _do_fetch():
        result = await get_context(url)
        if not result:
            print("Error: Could not retrieve content.")
            sys.exit(1)
            
        print("="*80)
        print(f"Title: {result.title}")
        print(f"Retrieval Method: {result.retrieval_method} (Authenticated: {result.authenticated})")
        print("="*80)
        print(result.content)
        
    asyncio.run(_do_fetch())

def run_setup(client_filter: str = "all", dry_run: bool = False) -> None:
    """Auto-configure MCP clients to connect to ContextPortal."""
    from app.core.setup import get_supported_clients, inject_mcp_config
    
    print("=" * 60)
    print("  [ContextPortal] Auto-Configuration Setup")
    print("=" * 60)
    print("Detecting and configuring AI agent clients...\n")

    clients = get_supported_clients()
    if client_filter != "all":
        clients = [c for c in clients if c.name == client_filter]
        if not clients:
            print(f"Unknown client '{client_filter}'. Available options: all, claude, cursor, antigravity")
            sys.exit(1)

    configured_any = False
    is_specific = client_filter != "all"
    for client in clients:
        success, message = inject_mcp_config(client.config_path, key_name=client.key_name, dry_run=dry_run, force=is_specific)
        is_skipped = "skipped" in message.lower()
        symbol = "[-]" if is_skipped else ("[+]" if success else "[!]")
        print(f"  {symbol} {client.display_name:<16}: {message}")
        print(f"      Target: {client.config_path}")
        if success and not is_skipped and "failed" not in message.lower():
            configured_any = True

    print("\n" + "=" * 60)
    if dry_run:
        print("Dry run completed. No files were modified.")
    else:
        print("Done! Restart your AI agent client to load ContextPortal.")
        print("Run 'contextportal doctor' anytime to verify your environment.")
    print("=" * 60 + "\n")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ContextPortal — The authenticated fetch layer for AI agents."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # MCP Server Command
    subparsers.add_parser(
        "mcp", 
        help="Start the Model Context Protocol (MCP) server over STDIO."
    )
    
    # Login Command
    login_parser = subparsers.add_parser(
        "login", 
        help="Open a browser to manually authenticate and save your session."
    )
    login_parser.add_argument(
        "--url", 
        type=str, 
        help="Optional starting URL to open for login (e.g., https://github.com/login)."
    )
    
    # Fetch Command
    fetch_parser = subparsers.add_parser(
        "fetch", 
        help="Test retrieval of a URL directly from the CLI."
    )
    fetch_parser.add_argument(
        "url", 
        type=str, 
        help="The URL to fetch."
    )

    # Setup Command (Release 0.2)
    setup_parser = subparsers.add_parser(
        "setup",
        help="Auto-configure MCP connections in Claude, Cursor, and Antigravity."
    )
    setup_parser.add_argument(
        "--client",
        choices=["all", "claude", "cursor", "antigravity"],
        default="all",
        help="Specific AI client to configure (default: all)"
    )
    setup_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to configuration files."
    )

    # Doctor / Diagnostics Command (Release 0.2)
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check system health, browser storage, and MCP client readiness."
    )
    subparsers.add_parser(
        "status",
        help="Alias for 'doctor'."
    )
    
    args = parser.parse_args()
    
    if args.command == "mcp":
        run_mcp()
    elif args.command == "login":
        run_login(args.url)
    elif args.command == "fetch":
        run_fetch(args.url)
    elif args.command == "setup":
        run_setup(client_filter=args.client, dry_run=args.dry_run)
    elif args.command in ("doctor", "status"):
        from app.core.doctor import run_doctor
        run_doctor()

if __name__ == "__main__":
    main()

