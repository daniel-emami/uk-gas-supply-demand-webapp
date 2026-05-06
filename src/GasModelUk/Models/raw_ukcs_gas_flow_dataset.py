from __future__ import annotations

from dataclasses import dataclass

from GasModelUk.Models.ukcs_gas_flow_record import UkcsGasFlowRecord


@dataclass(frozen=True)
class RawUkcsGasFlowDataset:
    """Raw UKCS dataset returned by a scraper."""

    records: tuple[UkcsGasFlowRecord, ...]
    unit: str
    source_name: str

    @property
    def category_key(self) -> str:
        """Return the registry category key for this dataset."""

        return "ukcs"

    def to_rows(self) -> list[dict[str, object]]:
        """Return generic raw rows for transformation."""

        return [record.to_row() for record in self.records]
