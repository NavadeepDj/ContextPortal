import sys
from unittest.mock import MagicMock, patch

import pytest

from app.core.updater import (
    detect_install_manager,
    get_current_version,
    get_latest_version,
    get_upgrade_command,
    is_newer_version,
    run_update,
    run_upgrade,
)


def test_get_current_version() -> None:
    ver = get_current_version()
    assert isinstance(ver, str)
    assert len(ver) > 0


def test_is_newer_version() -> None:
    assert is_newer_version("0.3.0", "0.2.0") is True
    assert is_newer_version("0.2.1", "0.2.0") is True
    assert is_newer_version("1.0.0", "0.3.0") is True
    assert is_newer_version("0.2.0", "0.2.0") is False
    assert is_newer_version("0.1.9", "0.2.0") is False
    assert is_newer_version("invalid", "0.2.0") is False


@patch("httpx.get")
def test_get_latest_version_success(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"info": {"version": "0.3.0"}}
    mock_get.return_value = mock_response

    latest = get_latest_version(pypi_url="https://fake.pypi/json")
    assert latest == "0.3.0"


@patch("httpx.get")
def test_get_latest_version_network_error(mock_get: MagicMock) -> None:
    mock_get.side_effect = Exception("Connection refused")
    latest = get_latest_version(pypi_url="https://fake.pypi/json")
    assert latest is None


@patch("httpx.get")
def test_get_latest_version_non_200(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    latest = get_latest_version(pypi_url="https://fake.pypi/json")
    assert latest is None


@patch("subprocess.run")
@patch("shutil.which")
def test_detect_install_manager_uv(mock_which: MagicMock, mock_run: MagicMock) -> None:
    mock_which.side_effect = lambda cmd: "/usr/local/bin/uv" if cmd == "uv" else None
    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_proc.stdout = "contextportal v0.2.0\n  - contextportal\n"
    mock_run.return_value = mock_proc

    assert detect_install_manager() == "uv"


@patch("subprocess.run")
@patch("shutil.which")
def test_detect_install_manager_pipx(
    mock_which: MagicMock, mock_run: MagicMock
) -> None:
    mock_which.side_effect = lambda cmd: (
        "/usr/local/bin/pipx" if cmd == "pipx" else None
    )
    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_proc.stdout = "package contextportal 0.2.0, installed using Python 3.12"
    mock_run.return_value = mock_proc

    assert detect_install_manager() == "pipx"


@patch("shutil.which")
def test_detect_install_manager_fallback_pip(mock_which: MagicMock) -> None:
    mock_which.return_value = None
    assert detect_install_manager() == "pip"


def test_get_upgrade_command() -> None:
    assert get_upgrade_command("uv") == ["uv", "tool", "upgrade", "contextportal"]
    assert get_upgrade_command("pipx") == ["pipx", "upgrade", "contextportal"]
    assert get_upgrade_command("pip") == [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "contextportal",
    ]


@patch("subprocess.run")
def test_run_upgrade_success(mock_run: MagicMock) -> None:
    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_proc.stdout = "Updated contextportal to 0.3.0"
    mock_run.return_value = mock_proc

    success, msg = run_upgrade("uv")
    assert success is True
    assert "Updated contextportal" in msg


@patch("subprocess.run")
def test_run_upgrade_failure(mock_run: MagicMock) -> None:
    mock_proc = MagicMock()
    mock_proc.returncode = 1
    mock_proc.stderr = "Upgrade failed: permission denied"
    mock_run.return_value = mock_proc

    success, msg = run_upgrade("uv")
    assert success is False
    assert "permission denied" in msg


@patch("app.core.updater.get_latest_version")
@patch("app.core.updater.get_current_version")
def test_run_update_already_up_to_date(
    mock_curr: MagicMock, mock_latest: MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_curr.return_value = "0.3.0"
    mock_latest.return_value = "0.3.0"

    run_update(check_only=False)
    captured = capsys.readouterr().out
    assert "already up to date" in captured


@patch("app.core.updater.detect_install_manager")
@patch("app.core.updater.get_latest_version")
@patch("app.core.updater.get_current_version")
def test_run_update_check_only_new_version(
    mock_curr: MagicMock,
    mock_latest: MagicMock,
    mock_mgr: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_curr.return_value = "0.2.0"
    mock_latest.return_value = "0.3.0"
    mock_mgr.return_value = "uv"

    run_update(check_only=True)
    captured = capsys.readouterr().out
    assert "Update available: v0.2.0 -> v0.3.0" in captured
    assert "uv tool upgrade contextportal" in captured


@patch("app.core.updater.run_upgrade")
@patch("app.core.updater.detect_install_manager")
@patch("app.core.updater.get_latest_version")
@patch("app.core.updater.get_current_version")
def test_run_update_auto_upgrade(
    mock_curr: MagicMock,
    mock_latest: MagicMock,
    mock_mgr: MagicMock,
    mock_upgrade: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_curr.return_value = "0.2.0"
    mock_latest.return_value = "0.3.0"
    mock_mgr.return_value = "uv"
    mock_upgrade.return_value = (True, "Installed 0.3.0")

    run_update(check_only=False)
    captured = capsys.readouterr().out
    assert "Successfully updated ContextPortal to v0.3.0!" in captured
