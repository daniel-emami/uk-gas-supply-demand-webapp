from __future__ import annotations

from dataclasses import dataclass

from GasModelUk.Models.ncs_gas_flow_record import NcsGasFlowRecord


@dataclass(frozen=True)
class RawNcsGasFlowDataset:
    """Raw NCS dataset returned by a scraper."""

    records: tuple[NcsGasFlowRecord, ...]
    unit: str
    source_name: str

    @property
    def category_key(self) -> str:
        """Return the registry category key for this dataset."""

        return "ncs"

    def to_rows(self) -> list[dict[str, object]]:
        """Return generic raw rows for transformation."""

        return [record.to_row() for record in self.records]
