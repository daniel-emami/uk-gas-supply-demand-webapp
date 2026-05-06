from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GasFlowRecord:
    """One lowest-level gas flow value for one gas day."""

    gas_day: str
    category_key: str
    flow_key: str
    value: float | None
