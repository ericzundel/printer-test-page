"""Compose the full two-page printer test document."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from . import patterns
from .colors import (
    BLACK,
    BLACK_PATCHES,
    CMYK_STRIPS,
    RGB_STRIPS,
    STEP_WEDGE_LEVELS,
)
from .metadata import Provenance

PAGE_SIZES = {"letter": letter, "a4": A4}

MARGIN = 0.5 * inch
STRIP_HEIGHT = 16
SECTION_GAP = 14
LABEL_GAP = 12  # vertical room reserved for a section/strip label


def _heading(c: Canvas, x: float, y: float, text: str) -> None:
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(BLACK)
    c.drawString(x, y, text)


def _corner_registration(c: Canvas, width: float, height: float) -> None:
    size = 12
    # Sit in the true corners, clear of the content margin so the crosshairs
    # never overlap the title or footer text.
    inset = 20
    for cx in (inset, width - inset):
        for cy in (inset, height - inset):
            patterns.registration_mark(c, cx, cy, size)


def _footer(c: Canvas, width: float, prov: Provenance, page_num: int, total: int) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(BLACK)
    left = MARGIN
    right = width - MARGIN
    c.drawString(left, 30, f"Machine: {prov.machine}")
    c.drawString(left, 21, f"Program: {prov.directory}")
    c.drawRightString(right, 30, f"Page {page_num} of {total}")
    c.drawRightString(right, 21, f"Generated: {prov.timestamp_text}")


def _draw_color_page(c: Canvas, width: float, height: float, prov: Provenance) -> None:
    content_w = width - 2 * MARGIN
    x = MARGIN
    cursor = height - MARGIN

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(BLACK)
    c.drawString(x, cursor - 14, "Inkjet Printer Test Page")
    c.setFont("Helvetica", 9)
    c.drawString(x, cursor - 28, "Color & tone — gradients, density wedge, ink mixing")
    cursor -= 48

    _heading(c, x, cursor, "CMYK gradients")
    cursor -= LABEL_GAP + 4
    for strip in CMYK_STRIPS:
        cursor -= STRIP_HEIGHT
        patterns.gradient_strip(
            c, x, cursor, content_w, STRIP_HEIGHT, strip.start, strip.end, strip.label
        )
        cursor -= LABEL_GAP
    cursor -= SECTION_GAP

    _heading(c, x, cursor, "RGB gradients")
    cursor -= LABEL_GAP + 4
    for strip in RGB_STRIPS:
        cursor -= STRIP_HEIGHT
        patterns.gradient_strip(
            c, x, cursor, content_w, STRIP_HEIGHT, strip.start, strip.end, strip.label
        )
        cursor -= LABEL_GAP
    cursor -= SECTION_GAP

    _heading(c, x, cursor, "Black step wedge")
    cursor -= LABEL_GAP + 4
    wedge_h = 24
    cursor -= wedge_h
    patterns.step_wedge(
        c, x, cursor, content_w, wedge_h, STEP_WEDGE_LEVELS, "K density (100% → 5%)"
    )
    cursor -= LABEL_GAP + SECTION_GAP

    _heading(c, x, cursor, "Composite black")
    cursor -= LABEL_GAP + 4
    patch_h = 36
    cursor -= patch_h
    patterns.black_patches(
        c, x, cursor, content_w * 0.6, patch_h, BLACK_PATCHES, "Pure K vs rich black"
    )


def _draw_diagnostics_page(c: Canvas, width: float, height: float, prov: Provenance) -> None:
    content_w = width - 2 * MARGIN
    x = MARGIN
    cursor = height - MARGIN

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(BLACK)
    c.drawString(x, cursor - 14, "Alignment & Diagnostics")
    c.setFont("Helvetica", 9)
    c.drawString(x, cursor - 28, "Nozzle check, registration, convergence, banding, test target")
    cursor -= 48

    _heading(c, x, cursor, "Nozzle check")
    cursor -= LABEL_GAP + 4
    nozzle_h = 70
    cursor -= nozzle_h
    patterns.nozzle_check(c, x + 12, cursor, content_w - 12, nozzle_h)
    cursor -= SECTION_GAP

    _heading(c, x, cursor, "Convergence grid")
    cursor -= LABEL_GAP + 4
    grid_h = 90
    cursor -= grid_h
    patterns.convergence_grid(c, x, cursor, content_w * 0.5, grid_h)
    # Center registration target alongside the grid.
    patterns.registration_mark(c, x + content_w * 0.75, cursor + grid_h / 2, 22)
    c.setFont("Helvetica", 7)
    c.setFillColor(BLACK)
    c.drawCentredString(x + content_w * 0.75, cursor - 4, "Center registration target")
    cursor -= LABEL_GAP + SECTION_GAP

    _heading(c, x, cursor, "Banding bars")
    cursor -= LABEL_GAP + 4
    band_h = 80
    cursor -= band_h
    patterns.banding_bars(c, x, cursor, content_w, band_h)
    cursor -= SECTION_GAP

    target_h = 120
    cursor -= target_h
    patterns.test_target(c, x, cursor, content_w, target_h)


def render_test_page(
    output: Path | str,
    *,
    page_size: str = "letter",
    provenance: Provenance | None = None,
) -> Path:
    """Render the test page to ``output`` and return its resolved path."""
    if page_size not in PAGE_SIZES:
        raise ValueError(f"unknown page size {page_size!r}; choose from {sorted(PAGE_SIZES)}")
    width, height = PAGE_SIZES[page_size]
    prov = provenance if provenance is not None else Provenance.collect()
    out_path = Path(output)

    c = Canvas(str(out_path), pagesize=(width, height))
    c.setTitle("Inkjet Printer Test Page")
    c.setAuthor(prov.machine)

    pages = (_draw_color_page, _draw_diagnostics_page)
    total = len(pages)
    for i, draw in enumerate(pages, start=1):
        _corner_registration(c, width, height)
        draw(c, width, height, prov)
        _footer(c, width, prov, i, total)
        c.showPage()
    c.save()
    return out_path
