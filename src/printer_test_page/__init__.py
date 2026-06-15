"""Generate an inkjet printer test page as a PDF."""

from __future__ import annotations

from .metadata import Provenance
from .page import render_test_page

__all__ = ["Provenance", "render_test_page"]
