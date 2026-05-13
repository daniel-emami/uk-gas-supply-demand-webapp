from __future__ import annotations

import asyncio
import logging
from typing import Any

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.Constants.scraper_registry import API_IDS
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Extract.request_creator import RequestCreator
from GasModelUk.Models.cross_border_gas_flow_record import CrossBorderGasFlowRecord
from GasModelUk.Models.raw_cross_border_gas_flow_dataset import (
    RawCrossBorderGasFlowDataset,
)
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.date_utils import parse_gas_day

logger = logging.getLogger(__name__)


class CrossBorderFlowsScraper(BaseScraper):
    """Async placeholder scraper for UK cross-border flow flows."""

    source_name = "national_grid"
    category_key = "cross_border_flows"

    async def scrape(self, request: ScrapeRequest) -> RawCrossBorderGasFlowDataset:
        """Return fake cross-border flow data for the requested gas days."""

        logger.info("Starting cross-border flow scraper")
        await asyncio.sleep(0)

        request_creator = RequestCreator(
            source_name=self.source_name,
            category_key=self.category_key,
            request=request,
        )

        api_request = request_creator.create_national_grid_post_request()
        response = api_request.send()
        records = self._parse_cross_border_flows_response(response.json())

        logger.info(
            "Finished cross-border flow scraper with %s rows. %s",
            len(records),
        )
        return RawCrossBorderGasFlowDataset(
            records=records, unit=UNIT, source_name=self.source_name
        )

    def _parse_cross_border_flows_response(
        self,
        response_json: list[dict[str, Any]],
    ) -> tuple[CrossBorderGasFlowRecord, ...]:
        id_to_field = {
            publication_id: field_name
            for field_name, publication_id in API_IDS[self.source_name][
                self.category_key
            ].items()
        }

        values_by_day: dict[str, dict[str, float]] = {}

        for pipeline in response_json:
            publication_id = pipeline.get("publicationId")
            if not isinstance(publication_id, str):
                continue

            field_name = id_to_field.get(publication_id)
            if field_name is None:
                continue

            publications = pipeline.get("publications", [])

            for publication in publications:
                gas_day = publication["applicableFor"]
                value = publication["value"]

                values_by_day.setdefault(gas_day, {})[field_name] = float(value)

        return tuple(
            CrossBorderGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                flows=values,
            )
            for gas_day, values in sorted(values_by_day.items())
        )


if __name__ == "__main__":
    # Run a quick test scrape if this file is executed directly.
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = CrossBorderFlowsScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
