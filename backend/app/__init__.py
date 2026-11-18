"""ContextPortal backend application package."""

from importlib.metadata import PackageNotFoundError, version

__version__ = "0.5.1"


def get_current_version() -> str:
    """Return the installed release, falling back to the source version."""
    try:
        return version("contextportal")
    except PackageNotFoundError:
        return __version__
