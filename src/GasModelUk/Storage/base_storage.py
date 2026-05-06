from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from GasModelUk.Models.transformed_gas_flow_dataset import TransformedGasFlowDataset


class BaseStorage(ABC):
    """Abstract interface for Excel-backed gas flow storage."""

    @abstractmethod
    def read_category_sheet(self, category_key: str) -> pd.DataFrame:
        """Read one category sheet from storage."""

    @abstractmethod
    def read_all_category_sheets(self) -> dict[str, pd.DataFrame]:
        """Read all registered category sheets from storage."""

    @abstractmethod
    def write_category_sheets(self, datasets: list[TransformedGasFlowDataset]) -> None:
        """Write category sheets independently while preserving untouched sheets."""
