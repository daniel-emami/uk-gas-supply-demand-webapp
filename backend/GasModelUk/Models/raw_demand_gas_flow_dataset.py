from __future__ import annotations

from dataclasses import dataclass

from GasModelUk.Models.demand_gas_flow_record import DemandGasFlowRecord


@dataclass(frozen=True)
class RawDemandGasFlowDataset:
    """Raw demand dataset returned by the demand scraper."""

    records: tuple[DemandGasFlowRecord, ...]
    unit: str
    source_name: str

    @property
    def category_key(self) -> str:
        """Return the registry category key for demand."""

        return "demand"

    def to_rows(self) -> list[dict[str, object]]:
        """Return generic raw rows for transformation."""

        return [record.to_row() for record in self.records]
