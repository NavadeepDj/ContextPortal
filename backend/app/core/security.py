import ipaddress
from urllib.parse import urlparse


def validate_url_policy(url: str) -> None:
    """
    Validates that a URL is safe to fetch.
    Rejects non-HTTP(S) schemes, localhost, and private/internal IP ranges.
    Raises ValueError if the URL violates the policy.
    """
    if not url:
        raise ValueError("URL cannot be empty")

    parsed = urlparse(url)

    # 1. Scheme Validation
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Invalid scheme '{parsed.scheme}'. Only http and https are allowed."
        )

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid URL: missing hostname")

    # 2. Block explicitly named localhosts
    if hostname.lower() in ("localhost", "localhost.localdomain"):
        raise ValueError("Access to localhost is forbidden by security policy")

    # 3. IP Address Validation (block private/loopback/link-local)
    try:
        # Check if the hostname is directly an IP address
        # Strip brackets for IPv6 compatibility if present
        clean_hostname = hostname.strip("[]")
        ip = ipaddress.ip_address(clean_hostname)
        if (
            ip.is_loopback
            or ip.is_private
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_unspecified
        ):
            raise ValueError(
                f"Access to internal/private IP ({hostname}) is forbidden by security policy"
            )
    except ValueError as e:
        # Not an IP address string.
        # Note: If a custom exception is raised from ipaddress parsing, we catch it.
        # We re-raise our own ValueError if we blocked it inside the try block.
        if "forbidden by security policy" in str(e):
            raise
