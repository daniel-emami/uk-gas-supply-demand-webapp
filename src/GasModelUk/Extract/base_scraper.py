from __future__ import annotations

from abc import ABC, abstractmethod

from GasModelUk.Models.raw_gas_flow_dataset import RawGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest


class BaseScraper(ABC):
    """Abstract async scraper interface for one gas flow category."""

    category_key: str

    @abstractmethod
    async def scrape(self, request: ScrapeRequest) -> RawGasFlowDataset:
        """Scrape raw gas flow data for the requested date range."""
