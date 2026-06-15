"""Provenance information stamped onto the test page footer.

The footer answers two questions when a printed page turns up on a desk weeks
later: which machine produced it, and where the generating program lives so it
can be found and re-run.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def machine_name() -> str:
    """Return the hostname of the machine generating the page."""
    return socket.gethostname()


def program_directory() -> Path:
    """Return the directory the generating program lives in.

    Resolves to the project root (the parent of the ``src`` layout) for an
    editable install, or the installed package directory otherwise. Either way
    it points at the code that produced the page.
    """
    package_dir = Path(__file__).resolve().parent
    src_parent = package_dir.parent
    if src_parent.name == "src":
        return src_parent.parent
    return package_dir


@dataclass(frozen=True)
class Provenance:
    """Where and when a test page was generated."""

    machine: str
    directory: Path
    generated_at: datetime

    @classmethod
    def collect(
        cls,
        *,
        machine: str | None = None,
        directory: Path | None = None,
        generated_at: datetime | None = None,
    ) -> Provenance:
        """Gather provenance, allowing any field to be overridden (for tests)."""
        return cls(
            machine=machine if machine is not None else machine_name(),
            directory=directory if directory is not None else program_directory(),
            generated_at=generated_at if generated_at is not None else datetime.now(),
        )

    @property
    def timestamp_text(self) -> str:
        return self.generated_at.strftime("%Y-%m-%d %H:%M:%S")
