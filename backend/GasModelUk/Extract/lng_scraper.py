from __future__ import annotations

import asyncio
import logging
from typing import Any

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.Extract.national_grid_publication_scraper import (
    NationalGridPublicationScraper,
)
from GasModelUk.Models.lng_gas_flow_record import LngGasFlowRecord
from GasModelUk.Models.raw_lng_gas_flow_dataset import RawLngGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.date_utils import parse_gas_day


class LngScraper(NationalGridPublicationScraper):
    """Async placeholder scraper for UK LNG flows."""

    category_key = "lng"
    log_name = "LNG flow"

    def _records_from_response(
        self,
        response_json: list[dict[str, Any]],
    ) -> tuple[LngGasFlowRecord, ...]:
        values_by_day = self._parse_values_by_day(response_json)

        return tuple(
            LngGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                flows=values,
            )
            for gas_day, values in sorted(values_by_day.items())
        )

    def _build_dataset(
        self,
        records: tuple[LngGasFlowRecord, ...],
    ) -> RawLngGasFlowDataset:
        return RawLngGasFlowDataset(records=records, unit=UNIT, source_name=self.source_name)


if __name__ == "__main__":
    # Run a quick test scrape if this file is executed directly.
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = LngScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
