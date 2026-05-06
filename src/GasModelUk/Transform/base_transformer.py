from __future__ import annotations

from abc import ABC, abstractmethod

from GasModelUk.Models.raw_gas_flow_dataset import RawGasFlowDataset
from GasModelUk.Models.transformed_gas_flow_dataset import TransformedGasFlowDataset


class BaseTransformer(ABC):
    """Abstract interface for transforming raw gas data into normalized rows."""

    @abstractmethod
    def transform(self, raw_dataset: RawGasFlowDataset) -> TransformedGasFlowDataset:
        """Transform raw scraper data into an Excel-ready dataset."""
