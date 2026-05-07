from __future__ import annotations

import asyncio
import logging

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.DemoData.static_demo_data import DEMO_DATA_NOTICE, get_static_demo_rows
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Models.lng_gas_flow_record import LngGasFlowRecord
from GasModelUk.Models.raw_lng_gas_flow_dataset import RawLngGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.date_utils import parse_gas_day

logger = logging.getLogger(__name__)


class LngScraper(BaseScraper):
    """Async placeholder scraper for UK LNG flows."""

    category_key = "lng"

    async def scrape(self, request: ScrapeRequest) -> RawLngGasFlowDataset:
        """Return fake LNG data for the requested gas days."""

        logger.info("Starting LNG scraper")
        await asyncio.sleep(0)
        # TODO: Replace with real National Grid / National Gas LNG scraping logic.
        rows = get_static_demo_rows(self.category_key, request.start_date, request.end_date)
        records = tuple(
            LngGasFlowRecord(
                gas_day=parse_gas_day(row["gas_day"]),
                flows={key: value for key, value in row.items() if key != "gas_day"},
            )
            for row in rows
        )
        logger.info("Finished LNG scraper with %s rows. %s", len(records), DEMO_DATA_NOTICE)
        return RawLngGasFlowDataset(records=records, unit=UNIT, source_name="static_fake_demo")
