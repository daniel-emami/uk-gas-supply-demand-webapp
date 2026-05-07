from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TransformedGasFlowDataset:
    """Normalized category data ready for Excel persistence."""

    category_key: str
    rows: list[dict[str, Any]]
