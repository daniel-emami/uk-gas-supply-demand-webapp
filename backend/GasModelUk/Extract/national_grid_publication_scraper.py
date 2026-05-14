from __future__ import annotations

import asyncio
import logging
from abc import abstractmethod
from typing import Any

from GasModelUk.Constants.scraper_registry import get_output_field_by_publication_id
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Extract.request_creator import RequestCreator
from GasModelUk.Models.raw_gas_flow_dataset import RawGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Utilities.number_utils import sum_optional_values

logger = logging.getLogger(__name__)


class NationalGridPublicationScraper(BaseScraper):
    """Template scraper for National Grid publication-based gas flow categories."""

    source_name = "national_grid"

    async def scrape(self, request: ScrapeRequest) -> RawGasFlowDataset:
        """Scrape a National Grid publication category using the shared request flow."""

        logger.info("Starting %s scraper", self.category_key)
        await asyncio.sleep(0)

        request_creator = RequestCreator(
            source_name=self.source_name,
            category_key=self.category_key,
            request=request,
        )

        api_request = request_creator.create_national_grid_post_request()
        response = api_request.send()
        records = self._records_from_response(response.json())

        logger.info("Finished %s scraper with %s rows.", self.category_key, len(records))
        return self._build_dataset(records)

    def _parse_values_by_day(
        self,
        response_json: list[dict[str, Any]],
    ) -> dict[str, dict[str, float | None]]:
        """Return gas-day values mapped by configured output field."""

        id_to_field = get_output_field_by_publication_id(
            self.source_name,
            self.category_key,
        )
        values_by_day: dict[str, dict[str, float | None]] = {}

        for publication_group in response_json:
            publication_id = publication_group.get("publicationId")
            if not isinstance(publication_id, str):
                continue

            field_name = id_to_field.get(publication_id)
            if field_name is None:
                continue

            field_data_by_day = publication_group.get("publications", [])
            for daily_data in field_data_by_day:
                gas_day = daily_data["applicableFor"]
                value = self._value_from_publication(daily_data.get("value"))

                day_values = values_by_day.setdefault(gas_day, {})
                day_values[field_name] = sum_optional_values(
                    [day_values.get(field_name), value]
                )

        return values_by_day

    def _value_from_publication(self, value: Any) -> float | None:
        if value in {None, ""}:
            return None
        return float(value)

    @abstractmethod
    def _records_from_response(self, response_json: list[dict[str, Any]]) -> tuple[Any, ...]:
        """Build category-specific record objects from a publication API response."""

    @abstractmethod
    def _build_dataset(self, records: tuple[Any, ...]) -> RawGasFlowDataset:
        """Wrap category-specific record objects in their raw dataset."""
