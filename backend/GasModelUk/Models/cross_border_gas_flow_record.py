from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from GasModelUk.Models.flow_types import FlowValue
from GasModelUk.Utilities.date_utils import format_gas_day
from GasModelUk.Utilities.number_utils import sum_optional_values


@dataclass(frozen=True)
class CrossBorderGasFlowRecord:
    """Daily cross-border supply values by interconnector or border point."""

    gas_day: date
    interconnector: FlowValue
    bbl: FlowValue
    moffat: FlowValue

    @property
    def total(self) -> float | None:
        """Return the row-wise total for this gas flow group."""

        return sum_optional_values([self.interconnector, self.bbl, self.moffat])

    def to_row(self) -> dict[str, object]:
        """Return a lowest-level Excel-ready row without aggregate columns."""

        return {
            "gas_day": format_gas_day(self.gas_day),
            "interconnector": self.interconnector,
            "bbl": self.bbl,
            "moffat": self.moffat,
        }

    def to_payload(self) -> dict[str, float | None]:
        """Return a frontend-ready API payload including the calculated total."""

        return {
            "interconnector": self.interconnector,
            "bbl": self.bbl,
            "moffat": self.moffat,
            "total": self.total,
        }
