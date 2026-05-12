from __future__ import annotations

import asyncio
import logging
from typing import Any

from GasModelUk.Constants.scraper_registry import API_IDS
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

        request_creator = RequestCreator(
            source_name=self.source_name,
            category_key=self.category_key,
            request=request,
        )

        api_request = request_creator.create_national_grid_post_request()
        response = api_request.send()
        records = self._parse_demand_response(response.json())

        logger.info("Finished demand scraper with %s rows. %s", len(records))

        return RawDemandGasFlowDataset(
            records=records, unit=UNIT, source_name=self.source_name
        )

    def _parse_demand_response(
        self,
        response_json: list[dict[str, Any]],
    ) -> tuple[DemandGasFlowRecord, ...]:
        id_to_field = {
            publication_id: field_name
            for field_name, publication_id in API_IDS[self.source_name][
                self.category_key
            ].items()
        }

        values_by_day: dict[str, dict[str, float]] = {}

        for demand_type in response_json:
            publication_id = demand_type.get("publicationId")
            if not isinstance(publication_id, str):
                continue

            field_name = id_to_field.get(publication_id)
            if field_name is None:
                continue

            publications = demand_type.get("publications", [])

            for publication in publications:
                gas_day = publication["applicableFor"]
                value = publication["value"]

                values_by_day.setdefault(gas_day, {})[field_name] = -abs(float(value))

        return tuple(
            DemandGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                ldz=values.get("ldz"),
                gas_for_power=values.get("gas_for_power"),
                industry=values.get("industry"),
            )
            for gas_day, values in sorted(values_by_day.items())
        )


if __name__ == "__main__":
    # Run a quick test scrape if this file is executed directly.
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = DemandScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
