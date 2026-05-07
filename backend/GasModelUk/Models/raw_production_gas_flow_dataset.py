from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from GasModelUk.Models.raw_ncs_gas_flow_dataset import RawNcsGasFlowDataset
from GasModelUk.Models.raw_ukcs_gas_flow_dataset import RawUkcsGasFlowDataset
from GasModelUk.Utilities.date_utils import format_gas_day


@dataclass(frozen=True)
class RawProductionGasFlowDataset:
    """Raw production dataset containing NCS and UKCS scraper output."""

    ncs: RawNcsGasFlowDataset
    ukcs: RawUkcsGasFlowDataset
    unit: str
    source_name: str

    @property
    def category_key(self) -> str:
        """Return the Excel category key for the combined production sheet."""

        return "production"

    def to_rows(self) -> list[dict[str, object]]:
        """Return merged NCS and UKCS rows for the production Excel sheet."""

        ncs_by_day = {record.gas_day: dict(record.flows) for record in self.ncs.records}
        ukcs_by_day = {record.gas_day: dict(record.flows) for record in self.ukcs.records}
        gas_days = sorted(set(ncs_by_day) | set(ukcs_by_day))
        return [self._build_row(gas_day, ncs_by_day, ukcs_by_day) for gas_day in gas_days]

    def _build_row(
        self,
        gas_day: date,
        ncs_by_day: dict[date, dict[str, float | None]],
        ukcs_by_day: dict[date, dict[str, float | None]],
    ) -> dict[str, object]:
        return {
            "gas_day": format_gas_day(gas_day),
            **ncs_by_day.get(gas_day, {}),
            **ukcs_by_day.get(gas_day, {}),
        }
