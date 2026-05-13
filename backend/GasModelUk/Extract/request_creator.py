from __future__ import annotations

from dataclasses import dataclass

from GasModelUk.Constants.scraper_registry import get_api_url, get_ids_by_type
from GasModelUk.Models.base_request import BaseRequest
from GasModelUk.Models.national_grid_post_request import NationalGridPostRequest
from GasModelUk.Models.scrape_request import ScrapeRequest


@dataclass(frozen=True)
class RequestCreator:
    source_name: str
    category_key: str
    request: ScrapeRequest
    latest_value: bool = True
    timeout: int = 60

    def create_national_grid_post_request(self) -> BaseRequest:
        """Build a National Grid/National Gas publications request for a scraper."""

        publication_ids = list(
            get_ids_by_type(self.source_name, self.category_key).values()
        )
        if not publication_ids:
            raise ValueError(
                f"No publication ids configured for source '{self.source_name}' "
                f"and category '{self.category_key}'."
            )

        url = get_api_url(self.source_name)
        if not url:
            raise ValueError(f"No API URL configured for source '{self.source_name}'.")

        return NationalGridPostRequest(
            url=url,
            payload={
                "fromDate": self.request.start_date,
                "toDate": self.request.end_date,
                "publicationIds": publication_ids,
                "latestValue": "Y" if self.latest_value else "N",
            },
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )
