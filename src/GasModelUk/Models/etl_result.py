from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EtlResult:
    """Summary returned after a manual ETL run."""

    successful_categories: tuple[str, ...]
    failed_categories: tuple[str, ...]
    output_path: Path
