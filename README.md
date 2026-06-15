# printer-test-page

Generate an inkjet printer test page as a PDF. Built to be printed on a schedule
(e.g. monthly via the included systemd units) so the print heads lay down every
ink channel regularly and don't clog.

Each page is stamped with the **machine name** that generated it and the
**directory** the generating program lives in, so a printed sheet can always be
traced back to its source.

## Contents

The document is two US-Letter (or A4) pages:

**Page 1 — Color & tone**
- CMYK gradient strips (Cyan, Magenta, Yellow, Black) — one ink channel each
- RGB gradient strips (Red, Green, Blue) — composite ink mixing
- Black step wedge (100% → 5%) — density / tonal check
- Pure-K vs rich-black patches — ink-mixing comparison

**Page 2 — Alignment & diagnostics**
- Nozzle check — staggered hairlines per channel; a clog shows as a missing line
- Convergence grid — C/M/Y/K grids overlaid; misalignment shows as color fringes
- Registration crosshairs — page corners + a center target
- Banding bars — 50% solids per channel reveal feed/banding artifacts
- Synthetic test target — hue wheel, memory-color swatches, neutral gray ramp

## Usage

```bash
uv sync                       # install deps + dev tools
uv run printer-test-page      # writes ./test-page.pdf
uv run printer-test-page -o /tmp/page.pdf --page-size a4
```

## Printing on a schedule

The repo ships systemd **user** units that print the page monthly:

```bash
mkdir -p ~/.config/systemd/user
cp printer-test-page.service printer-test-page.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now printer-test-page.timer
```

The service generates the PDF and sends it to the printer with `lpr`. Adjust the
printer name (`-P ET-3950`) and `WorkingDirectory` in the unit file to match your
setup.

## Development

```bash
uv run pytest        # tests
uv run ruff format   # format
uv run ruff check    # lint
uv run ty check      # type check
```
