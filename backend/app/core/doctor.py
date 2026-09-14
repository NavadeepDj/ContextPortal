import json
import shutil
import sys
from pathlib import Path
from typing import Any

from app.core.setup import get_contextportal_mcp_entry, get_supported_clients


def check_cli_in_path() -> bool:
    """Checks if 'contextportal' executable is found in the current system PATH."""
    return shutil.which("contextportal") is not None


def check_browser_profile() -> dict[str, Any]:
    """Checks the persistent browser profile directory status."""
    profile_dir = Path.home() / ".contextportal" / "playwright_profile"
    exists = profile_dir.exists()
    writable = False

    if exists:
        try:
            test_file = profile_dir / ".write_test"
            test_file.touch()
            test_file.unlink()
            writable = True
        except Exception:
            writable = False
    else:
        try:
            profile_dir.mkdir(parents=True, exist_ok=True)
            writable = True
        except Exception:
            writable = False

    return {"path": str(profile_dir), "exists": exists, "writable": writable}


def check_clients_status() -> list[dict[str, Any]]:
    """Inspects all supported AI agent clients to check if ContextPortal is configured."""
    results = []
    target_entry = get_contextportal_mcp_entry()

    for client in get_supported_clients():
        status = {
            "name": client.name,
            "display_name": client.display_name,
            "config_path": str(client.config_path),
            "detected": client.config_path.exists()
            or client.config_path.parent.exists(),
            "configured": False,
            "error": None,
        }

        if client.config_path.exists():
            try:
                with open(client.config_path, encoding="utf-8") as f:
                    data = json.load(f)
                    servers = data.get(client.key_name, {})
                    cp_entry = servers.get("context-portal")
                    if cp_entry == target_entry:
                        status["configured"] = True
                    elif cp_entry is not None:
                        status["error"] = "Configured with different command/args"
            except Exception as e:
                status["error"] = f"Unreadable JSON: {e}"

        results.append(status)

    return results


def run_doctor() -> None:
    """Runs a complete system health check and prints a diagnostic report."""
    print("=" * 60)
    print("  [ContextPortal] Doctor - Health & Diagnostics")
    print("=" * 60)

    # 1. Python Environment
    print("\n[1] Runtime Environment:")
    print(f"  * Python Executable : {sys.executable}")
    print(f"  * Python Version    : {sys.version.split()[0]}")

    in_path = check_cli_in_path()
    path_symbol = "[+]" if in_path else "[!]"
    print(
        f"  * CLI in PATH       : {path_symbol} ({'Found' if in_path else 'Not found in PATH - ensure uv tool bin is in PATH'})"
    )

    # 2. Browser Storage
    print("\n[2] Browser Storage:")
    profile = check_browser_profile()
    profile_symbol = "[+]" if profile["writable"] else "[-]"
    print(f"  * Profile Directory : {profile['path']}")
    print(
        f"  * Profile Status    : {profile_symbol} ({'Active & Writable' if profile['writable'] else 'Error writing to directory'})"
    )

    # 3. AI Agent Clients
    print("\n[3] AI Agent Clients Configuration:")
    clients = check_clients_status()
    for c in clients:
        if c["configured"]:
            mark = "[+]"
            detail = "Configured & Ready"
        elif c["detected"]:
            mark = "[?]"
            detail = "Client found, but MCP not configured. Run 'contextportal setup'"
        else:
            mark = "[-]"
            detail = "Client not detected on this system"

        if c["error"]:
            detail += f" ({c['error']})"

        print(f"  * {c['display_name']:<18}: {mark} {detail}")
        print(f"    Path: {c['config_path']}")

    print("\n" + "=" * 60)
    all_ready = any(c["configured"] for c in clients)
    if all_ready:
        print("System status: Ready! Your configured agents can call ContextPortal.")
    else:
        print(
            "Recommendation: Run 'contextportal setup' to auto-configure your agents."
        )
    print("=" * 60 + "\n")
