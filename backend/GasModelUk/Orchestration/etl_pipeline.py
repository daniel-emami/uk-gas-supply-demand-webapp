from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from GasModelUk.Constants.gas_flow_registry import CATEGORY_KEYS
from GasModelUk.Extract.scraper_factory import ScraperFactory
from GasModelUk.Models.etl_result import EtlResult
from GasModelUk.Models.raw_gas_flow_dataset import RawGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Models.transformed_gas_flow_dataset import TransformedGasFlowDataset
from GasModelUk.Storage.excel_storage import ExcelStorage
from GasModelUk.Transform.gas_flow_transformer import GasFlowTransformer
from GasModelUk.Utilities.date_utils import ensure_date_order

logger = logging.getLogger(__name__)


class EtlPipeline:
    """Coordinates scraping, transformation, and Excel persistence."""

    def __init__(self, output_path: str | Path) -> None:
        """Create a pipeline that writes successful categories to an Excel workbook."""

        self.output_path = Path(output_path)
        self.scraper_factory = ScraperFactory()
        self.transformer = GasFlowTransformer()
        self.storage = ExcelStorage(self.output_path)

    async def run(
        self,
        start_date: str,
        end_date: str,
        category_keys: tuple[str, ...] = CATEGORY_KEYS,
    ) -> EtlResult:
        """Run all category scrapers concurrently for an inclusive gas day range."""

        ensure_date_order(start_date, end_date)
        logger.info(
            "Starting ETL run from %s to %s for categories: %s",
            start_date,
            end_date,
            category_keys,
        )
        request = ScrapeRequest(start_date=start_date, end_date=end_date)
        scrape_results = await self._scrape_all(request, category_keys)

        successful_datasets: list[TransformedGasFlowDataset] = []
        failed_categories: list[str] = []

        for category_key, result in scrape_results.items():
            if isinstance(result, Exception):
                logger.exception(
                    "Scraper/category failed and will be preserved: %s",
                    category_key,
                    exc_info=result,
                )
                failed_categories.append(category_key)
                continue
            try:
                transformed = self.transformer.transform(result)
                successful_datasets.append(transformed)
            except Exception:
                logger.exception(
                    "Transform failed and existing sheet will be preserved: %s",
                    category_key,
                )
                failed_categories.append(category_key)

        if successful_datasets:
            self.storage.write_category_sheets(successful_datasets)

        successful_categories = tuple(dataset.category_key for dataset in successful_datasets)
        for category_key in failed_categories:
            logger.info("Preserved existing Excel sheet for failed category %s", category_key)
        logger.info(
            "Finished ETL run. Successful categories: %s. Failed categories: %s",
            successful_categories,
            tuple(failed_categories),
        )
        return EtlResult(successful_categories, tuple(failed_categories), self.output_path)

    async def _scrape_all(
        self,
        request: ScrapeRequest,
        category_keys: tuple[str, ...],
    ) -> dict[str, RawGasFlowDataset | Exception]:
        scrapers = [self.scraper_factory.create(category_key) for category_key in category_keys]
        tasks = [scraper.scrape(request) for scraper in scrapers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            scraper.category_key: result
            for scraper, result in zip(scrapers, results, strict=True)
        }
