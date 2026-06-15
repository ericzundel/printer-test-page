"""Command-line entry point: write the test page to a PDF file."""

from __future__ import annotations

import argparse
from pathlib import Path

from .page import PAGE_SIZES, render_test_page


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="printer-test-page",
        description="Generate an inkjet printer test page (gradients, nozzle/alignment "
        "patterns, synthetic test target) as a PDF.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("test-page.pdf"),
        help="output PDF path (default: test-page.pdf)",
    )
    parser.add_argument(
        "--page-size",
        choices=sorted(PAGE_SIZES),
        default="letter",
        help="page size (default: letter)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out = render_test_page(args.output, page_size=args.page_size)
    print(f"Wrote {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
