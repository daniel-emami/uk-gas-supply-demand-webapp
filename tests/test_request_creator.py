from __future__ import annotations

import unittest
from typing import cast

from GasModelUk.Extract.request_creator import RequestCreator
from GasModelUk.Models.national_grid_post_request import NationalGridPostRequest
from GasModelUk.Models.scrape_request import ScrapeRequest


class RequestCreatorTests(unittest.TestCase):
    def test_lng_request_contains_configured_publication_ids(self) -> None:
        request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
        api_request = RequestCreator(
            source_name="national_grid",
            category_key="lng",
            request=request,
        ).create_national_grid_post_request()

        self.assertIsInstance(api_request, NationalGridPostRequest)
        api_request = cast(NationalGridPostRequest, api_request)
        self.assertEqual(
            api_request.url,
            "https://api.nationalgas.com/operationaldata/v1/publications/gasday",
        )
        self.assertEqual(api_request.headers, {"Content-Type": "application/json"})
        self.assertEqual(api_request.timeout, 60)
        self.assertEqual(api_request.payload["fromDate"], "2024-01-01")
        self.assertEqual(api_request.payload["toDate"], "2024-01-07")
        self.assertEqual(api_request.payload["latestValue"], "Y")
        self.assertEqual(
            set(api_request.payload["publicationIds"]),
            {"PUBOB3564", "PUBOB371", "PUBOB3473", "PUBOB3480"},
        )

    def test_missing_publication_ids_raises_value_error(self) -> None:
        request = ScrapeRequest(start_date="2024-01-01", end_date="2024-01-07")
        creator = RequestCreator(
            source_name="national_grid",
            category_key="unknown_category",
            request=request,
        )

        with self.assertRaisesRegex(ValueError, "No publication ids configured"):
            creator.create_national_grid_post_request()


if __name__ == "__main__":
    unittest.main()
