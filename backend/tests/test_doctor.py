import pytest
from app.core.doctor import check_cli_in_path, check_browser_profile, check_clients_status

def test_check_browser_profile():
    profile = check_browser_profile()
    assert "path" in profile
    assert "exists" in profile
    assert "writable" in profile
    assert profile["writable"] is True

def test_check_clients_status():
    statuses = check_clients_status()
    assert len(statuses) >= 3
    client_names = [s["name"] for s in statuses]
    assert "claude" in client_names
    assert "cursor" in client_names
    assert "antigravity" in client_names

