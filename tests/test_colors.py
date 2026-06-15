from __future__ import annotations

from reportlab.lib.colors import CMYKColor

from printer_test_page.colors import (
    CMYK_STRIPS,
    PROCESS_CHANNELS,
    RGB_STRIPS,
    STEP_WEDGE_LEVELS,
)


def test_cmyk_strips_drive_single_channels() -> None:
    labels = [s.label for s in CMYK_STRIPS]
    assert labels == ["Cyan", "Magenta", "Yellow", "Black (K)"]
    # Each strip ends at a pure single-channel ink value.
    ends = [s.end for s in CMYK_STRIPS]
    assert ends[0] == CMYKColor(1, 0, 0, 0)
    assert ends[3] == CMYKColor(0, 0, 0, 1)


def test_rgb_strips_present() -> None:
    assert [s.label for s in RGB_STRIPS] == ["Red", "Green", "Blue"]


def test_step_wedge_levels_descend_within_range() -> None:
    descending = list(STEP_WEDGE_LEVELS) == sorted(STEP_WEDGE_LEVELS, reverse=True)
    assert descending
    assert all(level > 0.0 and level <= 1.0 for level in STEP_WEDGE_LEVELS)


def test_process_channels_are_cmyk() -> None:
    assert [name for name, _ in PROCESS_CHANNELS] == ["C", "M", "Y", "K"]
    assert all(isinstance(color, CMYKColor) for _, color in PROCESS_CHANNELS)
