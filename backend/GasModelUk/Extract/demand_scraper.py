from __future__ import annotations

import asyncio
import logging
from typing import Any

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.Extract.national_grid_publication_scraper import (
    NationalGridPublicationScraper,
)
from GasModelUk.Models.demand_gas_flow_record import DemandGasFlowRecord
from GasModelUk.Models.raw_demand_gas_flow_dataset import RawDemandGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.date_utils import parse_gas_day


class DemandScraper(NationalGridPublicationScraper):
    """Async placeholder scraper for UK gas demand flows."""

    category_key = "demand"

    def _records_from_response(
        self,
        response_json: list[dict[str, Any]],
    ) -> tuple[DemandGasFlowRecord, ...]:
        values_by_day = self._parse_values_by_day(response_json)

        return tuple(
            DemandGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                ldz=values.get("ldz"),
                gas_for_power=values.get("gas_for_power"),
                industry=values.get("industry"),
            )
            for gas_day, values in sorted(values_by_day.items())
        )

    def _value_from_publication(self, value: Any) -> float | None:
        parsed_value = super()._value_from_publication(value)
        if parsed_value is None:
            return None
        return -abs(parsed_value)

    def _build_dataset(
        self,
        records: tuple[DemandGasFlowRecord, ...],
    ) -> RawDemandGasFlowDataset:
        return RawDemandGasFlowDataset(records=records, unit=UNIT, source_name=self.source_name)


if __name__ == "__main__":
    # Run a quick test scrape if this file is executed directly.
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = DemandScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
