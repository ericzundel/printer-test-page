from __future__ import annotations

from datetime import datetime
from pathlib import Path

from printer_test_page.metadata import Provenance, machine_name, program_directory


def test_machine_name_is_nonempty() -> None:
    assert machine_name()


def test_program_directory_exists() -> None:
    directory = program_directory()
    assert isinstance(directory, Path)
    assert directory.exists()


def test_provenance_collect_allows_overrides() -> None:
    ts = datetime(2026, 6, 15, 8, 0, 0)
    prov = Provenance.collect(machine="printbox", directory=Path("/srv/app"), generated_at=ts)
    assert prov.machine == "printbox"
    assert prov.directory == Path("/srv/app")
    assert prov.timestamp_text == "2026-06-15 08:00:00"


def test_provenance_collect_defaults() -> None:
    prov = Provenance.collect()
    assert prov.machine == machine_name()
    assert prov.directory == program_directory()
