"""Color definitions and palettes used across the test page.

Process colors (C, M, Y, K) are defined in the DeviceCMYK space so each strip
or patch drives exactly one ink channel where intended. Composite/memory colors
are defined in RGB. Keeping these as plain data makes the layout code declarative
and lets the tests assert on the palette without rendering a PDF.
"""

from __future__ import annotations

from dataclasses import dataclass

from reportlab.lib.colors import CMYKColor, Color

WHITE = Color(1, 1, 1)
BLACK = Color(0, 0, 0)
# White in the CMYK space (no ink). Gradient endpoints must share a color space,
# so CMYK strips start here rather than from the RGB ``WHITE``.
CMYK_WHITE = CMYKColor(0, 0, 0, 0)

# A color that lays down all four inks at full strength. Standard choice for
# registration/alignment marks: every head must hit the same spot for the mark
# to print cleanly.
REGISTRATION = CMYKColor(1, 1, 1, 1)


@dataclass(frozen=True)
class GradientStrip:
    """A single 0 -> 100% linear gradient strip."""

    label: str
    start: Color
    end: Color


# CMYK process-color gradients: white -> full single channel.
CMYK_STRIPS: tuple[GradientStrip, ...] = (
    GradientStrip("Cyan", CMYK_WHITE, CMYKColor(1, 0, 0, 0)),
    GradientStrip("Magenta", CMYK_WHITE, CMYKColor(0, 1, 0, 0)),
    GradientStrip("Yellow", CMYK_WHITE, CMYKColor(0, 0, 1, 0)),
    GradientStrip("Black (K)", CMYK_WHITE, CMYKColor(0, 0, 0, 1)),
)

# Composite RGB gradients: white -> full primary (exercises ink mixing).
RGB_STRIPS: tuple[GradientStrip, ...] = (
    GradientStrip("Red", WHITE, Color(1, 0, 0)),
    GradientStrip("Green", WHITE, Color(0, 1, 0)),
    GradientStrip("Blue", WHITE, Color(0, 0, 1)),
)

# Discrete tint levels for the black step wedge (density / tonal check).
STEP_WEDGE_LEVELS: tuple[float, ...] = (1.0, 0.8, 0.6, 0.4, 0.2, 0.05)


@dataclass(frozen=True)
class BlackPatch:
    """A labelled black patch, used to compare pure-K vs composite 'rich' black."""

    label: str
    color: CMYKColor


# Pure black uses only the K channel; rich black adds CMY underneath. Side by
# side they reveal how the printer mixes inks and whether K alone looks washed.
BLACK_PATCHES: tuple[BlackPatch, ...] = (
    BlackPatch("Pure K", CMYKColor(0, 0, 0, 1)),
    BlackPatch("Rich black", CMYKColor(0.6, 0.4, 0.4, 1)),
)

# Per-channel solids for banding bars (50% tints reveal feed/banding artifacts).
BANDING_BARS: tuple[tuple[str, CMYKColor], ...] = (
    ("Cyan 50%", CMYKColor(0.5, 0, 0, 0)),
    ("Magenta 50%", CMYKColor(0, 0.5, 0, 0)),
    ("Yellow 50%", CMYKColor(0, 0, 0.5, 0)),
    ("Black 50%", CMYKColor(0, 0, 0, 0.5)),
    ("Composite 50%", CMYKColor(0.5, 0.5, 0.5, 0.5)),
)

# Channels used for nozzle-check rows and the overlapping convergence grid.
PROCESS_CHANNELS: tuple[tuple[str, CMYKColor], ...] = (
    ("C", CMYKColor(1, 0, 0, 0)),
    ("M", CMYKColor(0, 1, 0, 0)),
    ("Y", CMYKColor(0, 0, 1, 0)),
    ("K", CMYKColor(0, 0, 0, 1)),
)

# "Memory colors": hues people judge accuracy by. (name, (r, g, b)).
MEMORY_COLORS: tuple[tuple[str, tuple[float, float, float]], ...] = (
    ("Sky", (0.40, 0.62, 0.86)),
    ("Foliage", (0.36, 0.58, 0.27)),
    ("Skin", (0.94, 0.78, 0.66)),
    ("Skin (deep)", (0.55, 0.38, 0.29)),
    ("Apple red", (0.78, 0.16, 0.16)),
    ("Orange", (0.95, 0.55, 0.16)),
)
