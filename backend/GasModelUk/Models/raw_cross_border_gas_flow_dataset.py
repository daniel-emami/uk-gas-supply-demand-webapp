from __future__ import annotations

from dataclasses import dataclass

from GasModelUk.Models.cross_border_gas_flow_record import CrossBorderGasFlowRecord


@dataclass(frozen=True)
class RawCrossBorderGasFlowDataset:
    """Raw cross-border flow dataset returned by a scraper."""

    records: tuple[CrossBorderGasFlowRecord, ...]
    unit: str
    source_name: str

    @property
    def category_key(self) -> str:
        """Return the registry category key for this dataset."""

        return "cross_border_flows"

    def to_rows(self) -> list[dict[str, object]]:
        """Return generic raw rows for transformation."""

        return [record.to_row() for record in self.records]
