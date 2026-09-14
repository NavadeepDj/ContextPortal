import importlib.metadata
import shutil
import subprocess
import sys

import httpx
from packaging import version

PYPI_URL = "https://pypi.org/pypi/contextportal/json"


def get_current_version() -> str:
    """Returns the currently installed ContextPortal version."""
    try:
        return importlib.metadata.version("contextportal")
    except importlib.metadata.PackageNotFoundError:
        # Fallback to package __version__ if running directly from source tree
        from app import __version__

        return __version__


def get_latest_version(pypi_url: str = PYPI_URL, timeout: float = 5.0) -> str | None:
    """Fetches the latest published ContextPortal version from PyPI."""
    try:
        response = httpx.get(pypi_url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                info = data.get("info")
                if isinstance(info, dict):
                    version_val = info.get("version")
                    if isinstance(version_val, str):
                        return version_val
    except Exception as e:
        print(f"Warning: Could not check PyPI for updates: {e}")
    return None


def is_newer_version(latest: str, current: str) -> bool:
    """Returns True if latest version is strictly newer than current version."""
    try:
        return version.parse(latest) > version.parse(current)
    except Exception:
        return False


def detect_install_manager() -> str:
    """Detects the tool used to manage the ContextPortal installation.

    Returns: 'uv', 'pipx', or 'pip'.
    """
    # Check if uv is installed and manages contextportal
    uv_bin = shutil.which("uv")
    if uv_bin:
        try:
            result = subprocess.run(
                [uv_bin, "tool", "list"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and "contextportal" in result.stdout:
                return "uv"
        except Exception:
            pass

    # Check if pipx is installed and manages contextportal
    pipx_bin = shutil.which("pipx")
    if pipx_bin:
        try:
            result = subprocess.run(
                [pipx_bin, "list"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and "contextportal" in result.stdout:
                return "pipx"
        except Exception:
            pass

    # Fallback to standard pip
    return "pip"


def get_upgrade_command(tool: str) -> list[str]:
    """Returns the upgrade command arguments for the detected tool."""
    if tool == "uv":
        return ["uv", "tool", "upgrade", "contextportal"]
    elif tool == "pipx":
        return ["pipx", "upgrade", "contextportal"]
    else:
        return [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "contextportal",
        ]


def run_upgrade(tool: str) -> tuple[bool, str]:
    """Executes the upgrade command. Returns (success, message)."""
    cmd = get_upgrade_command(tool)
    cmd_str = " ".join(cmd)
    try:
        print(f"Executing: {cmd_str}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr or result.stdout
    except Exception as e:
        return False, str(e)


def run_update(check_only: bool = False, pypi_url: str = PYPI_URL) -> None:
    """CLI handler for 'contextportal update'."""
    print("=" * 60)
    print("  [ContextPortal] Updater")
    print("=" * 60)

    current = get_current_version()
    print(f"\nChecking for updates... (Current version: v{current})")

    latest = get_latest_version(pypi_url=pypi_url)
    if not latest:
        print("[!] Could not connect to PyPI to check for updates.")
        print("    Please check your network connection or try again later.")
        return

    print(f"Latest version available on PyPI: v{latest}")

    if not is_newer_version(latest, current):
        print(f"\n[+] ContextPortal is already up to date (v{current}).")
        return

    print(f"\n[*] Update available: v{current} -> v{latest}")

    if check_only:
        tool = detect_install_manager()
        cmd = " ".join(get_upgrade_command(tool))
        print("\nTo upgrade, run:")
        print(f"    {cmd}\n")
        return

    tool = detect_install_manager()
    print(f"Detected installation manager: {tool}")
    print(f"Upgrading ContextPortal to v{latest}...")

    success, output = run_upgrade(tool)
    if success:
        print(f"\n[+] Successfully updated ContextPortal to v{latest}!")
        print("    Restart your AI agent client to apply changes.")
    else:
        print("\n[!] Failed to update automatically:")
        print(f"    {output}")
        cmd = " ".join(get_upgrade_command(tool))
        print("\nPlease try running manually:")
        print(f"    {cmd}")
