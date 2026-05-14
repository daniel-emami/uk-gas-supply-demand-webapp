from __future__ import annotations

import asyncio
import logging
from typing import Any

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.Extract.national_grid_publication_scraper import (
    NationalGridPublicationScraper,
)
from GasModelUk.Models.cross_border_gas_flow_record import CrossBorderGasFlowRecord
from GasModelUk.Models.raw_cross_border_gas_flow_dataset import (
    RawCrossBorderGasFlowDataset,
)
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.date_utils import parse_gas_day


class CrossBorderFlowsScraper(NationalGridPublicationScraper):
    """Async placeholder scraper for UK cross-border flow flows."""

    category_key = "cross_border_flows"

    def _records_from_response(
        self,
        response_json: list[dict[str, Any]],
    ) -> tuple[CrossBorderGasFlowRecord, ...]:
        values_by_day = self._parse_values_by_day(response_json)

        return tuple(
            CrossBorderGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                flows=values,
            )
            for gas_day, values in sorted(values_by_day.items())
        )

    def _build_dataset(
        self,
        records: tuple[CrossBorderGasFlowRecord, ...],
    ) -> RawCrossBorderGasFlowDataset:
        return RawCrossBorderGasFlowDataset(
            records=records,
            unit=UNIT,
            source_name=self.source_name,
        )


if __name__ == "__main__":
    # Run a quick test scrape if this file is executed directly.
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = CrossBorderFlowsScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
