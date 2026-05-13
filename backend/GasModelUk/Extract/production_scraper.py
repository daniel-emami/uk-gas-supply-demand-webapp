from __future__ import annotations

import asyncio
import logging
from typing import Any

from GasModelUk.Constants.gas_flow_registry import PRODUCTION_GROUPS, UNIT
from GasModelUk.Constants.scraper_registry import API_IDS, get_api_url
from GasModelUk.Extract.base_scraper import BaseScraper
from GasModelUk.Models.national_grid_post_request import NationalGridPostRequest
from GasModelUk.Models.ncs_gas_flow_record import NcsGasFlowRecord
from GasModelUk.Models.raw_ncs_gas_flow_dataset import RawNcsGasFlowDataset
from GasModelUk.Models.raw_production_gas_flow_dataset import RawProductionGasFlowDataset
from GasModelUk.Models.raw_ukcs_gas_flow_dataset import RawUkcsGasFlowDataset
from GasModelUk.Models.scrape_request import ScrapeRequest
from GasModelUk.Models.ukcs_gas_flow_record import UkcsGasFlowRecord
from GasModelUk.Utilities.date_utils import parse_gas_day
from GasModelUk.Utilities.number_utils import sum_optional_values
from GasModelUk.Extract.request_creator import RequestCreator


logger = logging.getLogger(__name__)


class ProductionScraper(BaseScraper):
    """Async scraper for NCS and UKCS production flows."""

    source_name = "national_grid"
    category_key = "production"

    async def scrape(self, request: ScrapeRequest) -> RawProductionGasFlowDataset:
        """Return production data split into NCS and UKCS records."""

        logger.info("Starting production scraper")
        await asyncio.sleep(0)

        request_creator = RequestCreator(
            source_name=self.source_name,
            category_key=self.category_key,
            request=request,
        )

        api_request = request_creator.create_national_grid_post_request()
        response = api_request.send()
        dataset = self._parse_production_response(response.json())

        logger.info(
            "Finished production scraper with %s NCS rows and %s UKCS rows.",
            len(dataset.ncs.records),
            len(dataset.ukcs.records),
        )
        return dataset


    def _parse_production_response(
        self,
        response_json: list[dict[str, Any]],
    ) -> RawProductionGasFlowDataset:
        id_map = self._production_id_map()
        values_by_day: dict[str, dict[str, dict[str, float | None]]] = {}

        for publication_group in response_json:
            publication_id = publication_group.get("publicationId")
            if not isinstance(publication_id, str):
                continue

            mapping = id_map.get(publication_id)
            if mapping is None:
                continue

            publications = publication_group.get("publications", [])
            for publication in publications:
                gas_day = publication["applicableFor"]
                value = self._to_float_or_none(publication.get("value"))

                day_values = values_by_day.setdefault(
                    gas_day,
                    {"ncs": {}, "ukcs": {}},
                )
                group_values = day_values[mapping["group"]]
                field_name = mapping["field"]
                group_values[field_name] = sum_optional_values(
                    [group_values.get(field_name), value]
                )

        ncs_records = tuple(
            NcsGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                flows={
                    column: values.get("ncs", {}).get(column)
                    for column in PRODUCTION_GROUPS["ncs"]
                },
            )
            for gas_day, values in sorted(values_by_day.items())
        )
        ukcs_records = tuple(
            UkcsGasFlowRecord(
                gas_day=parse_gas_day(gas_day),
                flows={
                    column: values.get("ukcs", {}).get(column)
                    for column in PRODUCTION_GROUPS["ukcs"]
                },
            )
            for gas_day, values in sorted(values_by_day.items())
        )

        return RawProductionGasFlowDataset(
            ncs=RawNcsGasFlowDataset(ncs_records, UNIT, self.source_name),
            ukcs=RawUkcsGasFlowDataset(ukcs_records, UNIT, self.source_name),
            unit=UNIT,
            source_name=self.source_name,
        )

    def _production_id_map(self) -> dict[str, dict[str, str]]:
        production_entries = API_IDS[self.source_name][self.category_key]
        production_groups = {
            "ncs": set(PRODUCTION_GROUPS["ncs"]),
            "ukcs": set(PRODUCTION_GROUPS["ukcs"]),
        }
        id_map: dict[str, dict[str, str]] = {}

        for group_name, entries in production_entries.items():
            allowed_fields = production_groups[group_name]
            for field_name, entry in entries.items():
                output_field = field_name
                if isinstance(entry, dict):
                    publication_id = entry["publication_id"]
                    output_field = entry.get("output_field", field_name)
                else:
                    publication_id = entry

                if output_field not in allowed_fields:
                    continue

                id_map[publication_id] = {
                    "group": group_name,
                    "field": output_field,
                }

        return id_map

    def _to_float_or_none(self, value: Any) -> float | None:
        if value in {None, ""}:
            return None
        return float(value)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
    scraper = ProductionScraper()
    dataset = asyncio.run(scraper.scrape(test_request))
    print(dataset)
