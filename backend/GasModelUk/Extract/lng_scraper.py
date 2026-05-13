from __future__ import annotations

import asyncio
import logging
from typing import Any

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.Constants.scraper_registry import get_output_field_by_publication_id
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Extract.request_creator import RequestCreator
from GasModelUk.Models.lng_gas_flow_record import LngGasFlowRecord
from GasModelUk.Models.raw_lng_gas_flow_dataset import RawLngGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.date_utils import parse_gas_day
from GasModelUk.Utilities.number_utils import sum_optional_values

logger = logging.getLogger(__name__)


class LngScraper(BaseScraper):
    """Async placeholder scraper for UK LNG flows."""

    source_name = "national_grid"
    category_key = "lng"

    async def scrape(self, request: ScrapeRequest) -> RawLngGasFlowDataset:
        """Return fake LNG data for the requested gas days."""

        logger.info("Starting LNG scraper")
        await asyncio.sleep(0)
        request_creator = RequestCreator(
            source_name=self.source_name,
            category_key=self.category_key,
            request=request,
        )

        api_request = request_creator.create_national_grid_post_request()
        response = api_request.send()
        records = self._parse_lng_flows_response(response.json())

        logger.info(
            "Finished LNG flow scraper with %s rows. %s",
            len(records),
        )
        return RawLngGasFlowDataset(
            records=records, unit=UNIT, source_name=self.source_name
        )

    def _parse_lng_flows_response(
        self,
        response_json: list[dict[str, Any]],
    ) -> tuple[LngGasFlowRecord, ...]:
        id_to_field = get_output_field_by_publication_id(
            self.source_name,
            self.category_key,
        )

        values_by_day: dict[str, dict[str, float | None]] = {}

        for lng_site in response_json:
            publication_id = lng_site.get("publicationId")
            if not isinstance(publication_id, str):
                continue

            field_name = id_to_field.get(publication_id)
            if field_name is None:
                continue

            publications = lng_site.get("publications", [])

            for publication in publications:
                gas_day = publication["applicableFor"]
                value = publication["value"]

                day_values = values_by_day.setdefault(gas_day, {})
                day_values[field_name] = sum_optional_values(
                    [day_values.get(field_name), self._to_float_or_none(value)]
                )

        return tuple(
            LngGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                flows=values,
            )
            for gas_day, values in sorted(values_by_day.items())
        )

    def _to_float_or_none(self, value: Any) -> float | None:
        if value in {None, ""}:
            return None
        return float(value)


if __name__ == "__main__":
    # Run a quick test scrape if this file is executed directly.
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = LngScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
