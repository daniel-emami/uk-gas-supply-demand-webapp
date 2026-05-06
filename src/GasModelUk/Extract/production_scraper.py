from __future__ import annotations

import asyncio
import logging

from GasModelUk.Constants.gas_flow_registry import PRODUCTION_GROUPS, UNIT
from GasModelUk.DemoData.static_demo_data import DEMO_DATA_NOTICE, get_static_demo_rows
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Models.ncs_gas_flow_record import NcsGasFlowRecord
from GasModelUk.Models.raw_ncs_gas_flow_dataset import RawNcsGasFlowDataset
from GasModelUk.Models.raw_production_gas_flow_dataset import RawProductionGasFlowDataset
from GasModelUk.Models.raw_ukcs_gas_flow_dataset import RawUkcsGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Models.ukcs_gas_flow_record import UkcsGasFlowRecord
from GasModelUk.Utilities.date_utils import parse_gas_day

logger = logging.getLogger(__name__)


class ProductionScraper(BaseScraper):
    """Async placeholder scraper for NCS and UKCS production flows."""

    category_key = "production"

    async def scrape(self, request: ScrapeRequest) -> RawProductionGasFlowDataset:
        """Return fake production data split into NCS and UKCS records."""

        logger.info("Starting production scraper")
        await asyncio.sleep(0)
        # TODO: Replace with real National Grid / National Gas production scraping logic.
        rows = get_static_demo_rows(self.category_key, request.start_date, request.end_date)
        ncs_records = tuple(
            NcsGasFlowRecord(
                gas_day=parse_gas_day(row["gas_day"]),
                flows={column: row.get(column) for column in PRODUCTION_GROUPS["ncs"]},
            )
            for row in rows
        )
        ukcs_records = tuple(
            UkcsGasFlowRecord(
                gas_day=parse_gas_day(row["gas_day"]),
                flows={column: row.get(column) for column in PRODUCTION_GROUPS["ukcs"]},
            )
            for row in rows
        )
        logger.info("Finished production scraper with %s rows. %s", len(rows), DEMO_DATA_NOTICE)
        return RawProductionGasFlowDataset(
            ncs=RawNcsGasFlowDataset(ncs_records, UNIT, "static_fake_demo"),
            ukcs=RawUkcsGasFlowDataset(ukcs_records, UNIT, "static_fake_demo"),
            unit=UNIT,
            source_name="static_fake_demo",
        )
