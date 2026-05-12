from __future__ import annotations

import asyncio
import logging
import requests

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.DemoData.static_demo_data import DEMO_DATA_NOTICE, get_static_demo_rows
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Extract.request_creator import RequestCreator
from GasModelUk.Models.demand_gas_flow_record import DemandGasFlowRecord
from GasModelUk.Models.raw_demand_gas_flow_dataset import RawDemandGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.date_utils import parse_gas_day

logger = logging.getLogger(__name__)


class DemandScraper(BaseScraper):
    """Async placeholder scraper for UK gas demand flows."""

    source_name = "national_grid"
    category_key = "demand"

    async def scrape(self, request: ScrapeRequest) -> RawDemandGasFlowDataset:
        """Return fake signed demand data for the requested gas days."""

        logger.info("Starting demand scraper")
        await asyncio.sleep(0)
        # TODO: Replace with real National Grid / National Gas demand scraping logic.

        request_creator = RequestCreator(
            source_name=self.source_name,
            category_key=self.category_key,
            request=request,
        )

        api_request = request_creator.create_national_grid_post_request()

        response = api_request.send()

        rows = get_static_demo_rows(
            self.category_key, request.start_date, request.end_date
        )
        records = tuple(
            DemandGasFlowRecord(
                gas_day=parse_gas_day(row["gas_day"]),
                ldz=row.get("ldz"),
                gas_for_power=row.get("gas_for_power"),
                industry=row.get("industry"),
            )
            for row in rows
        )
        logger.info(
            "Finished demand scraper with %s rows. %s", len(records), DEMO_DATA_NOTICE
        )
        return RawDemandGasFlowDataset(
            records=records, unit=UNIT, source_name="static_fake_demo"
        )


if __name__ == "__main__":
    # Run a quick test scrape if this file is executed directly.
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = DemandScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
