"""Vector drawing primitives for the test page.

Every function draws into a region of a reportlab canvas described by a bottom-left
origin ``(x, y)`` and a ``width``/``height`` (reportlab's coordinate system has the
origin at the bottom-left of the page, y increasing upward).
"""

from __future__ import annotations

import colorsys

from reportlab.lib.colors import CMYKColor, Color
from reportlab.pdfgen.canvas import Canvas

from .colors import (
    BANDING_BARS,
    BLACK,
    MEMORY_COLORS,
    PROCESS_CHANNELS,
    REGISTRATION,
)

LABEL_FONT = "Helvetica"
LABEL_SIZE = 7


def _label(c: Canvas, x: float, y: float, text: str) -> None:
    c.setFont(LABEL_FONT, LABEL_SIZE)
    c.setFillColor(BLACK)
    c.drawString(x, y, text)


def gradient_strip(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    start: Color,
    end: Color,
    label: str,
) -> None:
    """Draw a labelled left-to-right linear gradient with a hairline border."""
    _label(c, x, y + height + 2, label)
    c.saveState()
    path = c.beginPath()
    path.rect(x, y, width, height)
    c.clipPath(path, stroke=0, fill=0)
    c.linearGradient(x, y, x + width, y, [start, end], extend=True)
    c.restoreState()
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.5)
    c.rect(x, y, width, height, stroke=1, fill=0)


def step_wedge(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    levels: tuple[float, ...],
    label: str,
) -> None:
    """Draw a row of discrete black tint patches at the given levels."""
    _label(c, x, y + height + 2, label)
    n = len(levels)
    pw = width / n
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.5)
    for i, level in enumerate(levels):
        px = x + i * pw
        c.setFillColor(CMYKColor(0, 0, 0, level))
        c.rect(px, y, pw, height, stroke=1, fill=1)
        # Percent label, placed for contrast against the patch.
        c.setFont(LABEL_FONT, LABEL_SIZE)
        c.setFillColor(Color(1, 1, 1) if level >= 0.5 else BLACK)
        c.drawCentredString(px + pw / 2, y + height / 2 - 3, f"{int(level * 100)}%")


def black_patches(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    patches: tuple,
    label: str,
) -> None:
    """Draw side-by-side labelled black patches (pure-K vs rich black)."""
    _label(c, x, y + height + 2, label)
    n = len(patches)
    gap = 6
    pw = (width - gap * (n - 1)) / n
    for i, patch in enumerate(patches):
        px = x + i * (pw + gap)
        c.setFillColor(patch.color)
        c.setStrokeColor(BLACK)
        c.setLineWidth(0.5)
        c.rect(px, y, pw, height, stroke=1, fill=1)
        c.setFont(LABEL_FONT, LABEL_SIZE)
        c.setFillColor(Color(1, 1, 1))
        c.drawCentredString(px + pw / 2, y + 4, patch.label)


def nozzle_check(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    """Draw staggered hairline rows per channel; a clog shows as a missing line."""
    rows = len(PROCESS_CHANNELS)
    gap = 4
    row_h = (height - gap * (rows - 1)) / rows
    n = 64
    spacing = width / n
    for r, (name, color) in enumerate(PROCESS_CHANNELS):
        ry = y + r * (row_h + gap)
        c.setStrokeColor(color)
        c.setLineWidth(0.4)
        for i in range(n):
            lx = x + i * spacing + spacing / 2
            # Interlock even/odd lines vertically so individual nozzles resolve.
            if i % 2:
                c.line(lx, ry, lx, ry + row_h * 0.7)
            else:
                c.line(lx, ry + row_h * 0.3, lx, ry + row_h)
        _label(c, x - 10, ry + row_h / 2 - 3, name)


def registration_mark(c: Canvas, cx: float, cy: float, size: float) -> None:
    """Draw a crosshair-in-circle in registration color centered at (cx, cy)."""
    c.setStrokeColor(REGISTRATION)
    c.setLineWidth(0.5)
    c.line(cx - size, cy, cx + size, cy)
    c.line(cx, cy - size, cx, cy + size)
    c.circle(cx, cy, size * 0.6, stroke=1, fill=0)


def convergence_grid(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    step: float = 9.0,
) -> None:
    """Overlay the same fine grid in C, M, Y and K.

    On a well-converged printer the four channels stack into clean near-black
    lines; misalignment shows up as colored fringes on the grid lines.
    """
    for _name, color in PROCESS_CHANNELS:
        c.setStrokeColor(color)
        c.setLineWidth(0.3)
        gx = x
        while gx <= x + width + 0.01:
            c.line(gx, y, gx, y + height)
            gx += step
        gy = y
        while gy <= y + height + 0.01:
            c.line(x, gy, x + width, gy)
            gy += step
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.5)
    c.rect(x, y, width, height, stroke=1, fill=0)


def banding_bars(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    """Draw stacked 50% solid bars per channel to reveal horizontal banding."""
    n = len(BANDING_BARS)
    gap = 3
    bar_h = (height - gap * (n - 1)) / n
    for i, (name, color) in enumerate(BANDING_BARS):
        by = y + (n - 1 - i) * (bar_h + gap)
        c.setFillColor(color)
        c.rect(x, by, width, bar_h, stroke=0, fill=1)
        c.setFont(LABEL_FONT, LABEL_SIZE)
        c.setFillColor(Color(1, 1, 1))
        c.drawString(x + 4, by + bar_h / 2 - 3, name)


def color_wheel(c: Canvas, cx: float, cy: float, radius: float, segments: int = 36) -> None:
    """Draw a full-saturation hue wheel from RGB wedges."""
    extent = 360.0 / segments
    for i in range(segments):
        hue = i / segments
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        c.setFillColorRGB(r, g, b)
        c.setStrokeColorRGB(r, g, b)
        c.wedge(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            i * extent,
            extent,
            stroke=0,
            fill=1,
        )


def swatch_row(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    swatches: tuple,
    label: str,
) -> None:
    """Draw a labelled row of RGB swatches (name, (r, g, b))."""
    _label(c, x, y + height + 2, label)
    n = len(swatches)
    gap = 4
    pw = (width - gap * (n - 1)) / n
    for i, (name, rgb) in enumerate(swatches):
        px = x + i * (pw + gap)
        c.setFillColorRGB(*rgb)
        c.setStrokeColor(BLACK)
        c.setLineWidth(0.5)
        c.rect(px, y, pw, height, stroke=1, fill=1)
        c.setFont(LABEL_FONT, 6)
        c.setFillColor(BLACK)
        c.drawCentredString(px + pw / 2, y - 8, name)


def gray_ramp(
    c: Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    steps: int = 11,
    label: str = "Neutral ramp",
) -> None:
    """Draw a continuous-ish neutral gray ramp (white -> black) for cast check."""
    _label(c, x, y + height + 2, label)
    pw = width / steps
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.5)
    for i in range(steps):
        level = 1.0 - i / (steps - 1)
        c.setFillColorRGB(level, level, level)
        c.rect(x + i * pw, y, pw, height, stroke=0, fill=1)
    c.rect(x, y, width, height, stroke=1, fill=0)


def test_target(c: Canvas, x: float, y: float, width: float, height: float) -> None:
    """Draw the synthetic photographic test target.

    Combines a hue wheel, a row of 'memory color' swatches and a neutral gray
    ramp -- the things the eye judges photo realism by, without needing a bundled
    photograph.
    """
    _label(c, x, y + height + 4, "Synthetic test target")
    radius = min(height, width * 0.35) / 2
    wheel_cx = x + radius + 4
    wheel_cy = y + height - radius - 4
    color_wheel(c, wheel_cx, wheel_cy, radius)

    right_x = x + 2 * radius + 24
    right_w = x + width - right_x
    swatch_h = 26
    swatch_row(
        c,
        right_x,
        y + height - swatch_h - 12,
        right_w,
        swatch_h,
        MEMORY_COLORS,
        "Memory colors",
    )
    gray_ramp(c, right_x, y + height - swatch_h - 12 - 22 - swatch_h, right_w, swatch_h)
