"""Quality metric and badge generation surface."""

from ..engine import _ROOT


def write_metrics():
    """Generate the repository's metrics and badges through the existing writer."""
    import sys

    sys.path.insert(0, str(_ROOT / "scripts"))
    from metrics import write_all

    return write_all()


__all__ = ["write_metrics"]
