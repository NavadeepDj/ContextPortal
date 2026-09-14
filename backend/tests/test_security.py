import pytest

from app.core.security import validate_url_policy


def test_validate_url_policy_allowed():
    # Public URLs should pass
    validate_url_policy("https://example.com")
    validate_url_policy("http://public-api.com/data")
    validate_url_policy("https://project-dynamo.learn.joinhandshake.com/introduction")


def test_validate_url_policy_rejected_schemes():
    # Only http and https are allowed
    with pytest.raises(ValueError, match="Invalid scheme"):
        validate_url_policy("file:///etc/passwd")

    with pytest.raises(ValueError, match="Invalid scheme"):
        validate_url_policy("javascript:alert(1)")

    with pytest.raises(ValueError, match="Invalid scheme"):
        validate_url_policy("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")

    with pytest.raises(ValueError, match="Invalid scheme"):
        validate_url_policy("ftp://example.com/file")


def test_validate_url_policy_rejected_localhost():
    # Localhost strings are blocked
    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("http://localhost:8000/api")

    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("https://localhost.localdomain")

    # Localhost loopback IPs are blocked
    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("https://127.0.0.1")

    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("http://[::1]/")


def test_validate_url_policy_rejected_private_ips():
    # RFC 1918 private networks are blocked
    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("http://192.168.1.1/admin")

    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("http://10.0.0.5")

    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("https://172.16.0.100")
