from __future__ import annotations

import unittest

from GasModelUk.Extract.demand_scraper import DemandScraper
from GasModelUk.Extract.lng_scraper import LngScraper
from GasModelUk.Extract.production_scraper import ProductionScraper
from GasModelUk.Extract.storage_scraper import StorageScraper


class LngScraperParsingTests(unittest.TestCase):
    def test_isle_of_grain_publication_ids_are_summed_into_one_field(self) -> None:
        response_json = [
            {
                "publicationId": "PUBOB371",
                "publications": [
                    {"applicableFor": "2024-01-01", "value": "2.25"},
                ],
            },
            {
                "publicationId": "PUBOB3473",
                "publications": [
                    {"applicableFor": "2024-01-01", "value": "3.75"},
                ],
            },
        ]

        records = LngScraper()._records_from_response(response_json)

        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0].to_row(),
            {"gas_day": "2024-01-01", "isle_of_grain": 6.0},
        )


class DemandScraperParsingTests(unittest.TestCase):
    def test_demand_values_are_stored_as_negative_numbers(self) -> None:
        response_json = [
            {
                "publicationId": "PUBOBJ1015",
                "publications": [
                    {"applicableFor": "2024-01-01", "value": "5"},
                ],
            },
        ]

        records = DemandScraper()._records_from_response(response_json)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].to_row()["ldz"], -5.0)
        self.assertIsNone(records[0].to_row()["gas_for_power"])
        self.assertIsNone(records[0].to_row()["industry"])


class StorageScraperParsingTests(unittest.TestCase):
    def test_unknown_publication_ids_are_ignored(self) -> None:
        response_json = [
            {
                "publicationId": "UNKNOWN_PUBLICATION_ID",
                "publications": [
                    {"applicableFor": "2024-01-01", "value": "99"},
                ],
            },
        ]

        records = StorageScraper()._records_from_response(response_json)

        self.assertEqual(records, ())


class ProductionScraperParsingTests(unittest.TestCase):
    def test_teesside_publication_ids_are_summed_into_ukcs_teesside(self) -> None:
        response_json = [
            {
                "publicationId": "PUBOB437",
                "publications": [
                    {"applicableFor": "2024-01-01", "value": "4.5"},
                ],
            },
            {
                "publicationId": "PUBOB440",
                "publications": [
                    {"applicableFor": "2024-01-01", "value": "5.5"},
                ],
            },
        ]

        dataset = ProductionScraper()._parse_production_response(response_json)

        self.assertEqual(len(dataset.ncs.records), 1)
        self.assertEqual(len(dataset.ukcs.records), 1)
        self.assertEqual(dataset.ukcs.records[0].to_row()["teesside"], 10.0)
        self.assertIsNone(dataset.ncs.records[0].to_row()["easington_langeled"])


if __name__ == "__main__":
    unittest.main()
