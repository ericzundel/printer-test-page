from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from printer_test_page import render_test_page
from printer_test_page.cli import main
from printer_test_page.metadata import Provenance


@pytest.fixture
def provenance() -> Provenance:
    return Provenance.collect(
        machine="testhost",
        directory=Path("/opt/printer-test-page"),
        generated_at=datetime(2026, 6, 15, 8, 0, 0),
    )


def test_render_writes_valid_two_page_pdf(tmp_path: Path, provenance: Provenance) -> None:
    out = render_test_page(tmp_path / "page.pdf", provenance=provenance)
    assert out.exists()
    data = out.read_bytes()
    assert data.startswith(b"%PDF-")
    assert b"%%EOF" in data
    assert data.count(b"/Type /Page\n") == 2  # exactly two page objects
    assert len(data) > 2000


def test_render_rejects_unknown_page_size(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unknown page size"):
        render_test_page(tmp_path / "page.pdf", page_size="tabloid")


def test_render_supports_a4(tmp_path: Path, provenance: Provenance) -> None:
    out = render_test_page(tmp_path / "a4.pdf", page_size="a4", provenance=provenance)
    assert out.read_bytes().startswith(b"%PDF-")


def test_cli_writes_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    target = tmp_path / "cli.pdf"
    rc = main(["-o", str(target), "--page-size", "letter"])
    assert rc == 0
    assert target.exists()
    assert "Wrote" in capsys.readouterr().out
