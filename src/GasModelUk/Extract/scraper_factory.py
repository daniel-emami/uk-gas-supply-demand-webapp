from __future__ import annotations

from GasModelUk.Exceptions.configuration_error import ConfigurationError
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Extract.cross_border_flows_scraper import CrossBorderFlowsScraper
from GasModelUk.Extract.demand_scraper import DemandScraper
from GasModelUk.Extract.lng_scraper import LngScraper
from GasModelUk.Extract.production_scraper import ProductionScraper
from GasModelUk.Extract.storage_scraper import StorageScraper


class ScraperFactory:
    """Factory for selecting the correct scraper strategy for a category."""

    _scraper_types: dict[str, type[BaseScraper]] = {
        "demand": DemandScraper,
        "storage": StorageScraper,
        "lng": LngScraper,
        "production": ProductionScraper,
        "cross_border_flows": CrossBorderFlowsScraper,
    }

    def create(self, category_key: str) -> BaseScraper:
        """Create a scraper for the requested category key."""

        scraper_type = self._scraper_types.get(category_key)
        if scraper_type is None:
            raise ConfigurationError(f"No scraper registered for category: {category_key}")
        return scraper_type()
