from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from GasModelUk.Models.flow_types import FlowValue
from GasModelUk.Utilities.date_utils import format_gas_day
from GasModelUk.Utilities.number_utils import sum_optional_values


@dataclass(frozen=True)
class DemandGasFlowRecord:
    """Daily demand flow values represented as negative numbers."""

    gas_day: date
    ldz: FlowValue
    gas_for_power: FlowValue
    industry: FlowValue

    @property
    def total(self) -> float | None:
        """Return total demand for the gas day as a negative value."""

        return sum_optional_values([self.ldz, self.gas_for_power, self.industry])

    def to_row(self) -> dict[str, object]:
        """Return a lowest-level Excel-ready row without aggregate columns."""

        return {
            "gas_day": format_gas_day(self.gas_day),
            "ldz": self.ldz,
            "gas_for_power": self.gas_for_power,
            "industry": self.industry,
        }

    def to_payload(self) -> dict[str, float | str | None]:
        """Return a frontend-ready API payload including the calculated total."""

        return {
            "ldz": self.ldz,
            "gas_for_power": self.gas_for_power,
            "industry": self.industry,
            "total": self.total,
        }
