from __future__ import annotations

from dataclasses import dataclass

from GasModelUk.Models.storage_gas_flow_record import StorageGasFlowRecord


@dataclass(frozen=True)
class RawStorageGasFlowDataset:
    """Raw storage dataset returned by a scraper."""

    records: tuple[StorageGasFlowRecord, ...]
    unit: str
    source_name: str

    @property
    def category_key(self) -> str:
        """Return the registry category key for this dataset."""

        return "storage"

    def to_rows(self) -> list[dict[str, object]]:
        """Return generic raw rows for transformation."""

        return [record.to_row() for record in self.records]
