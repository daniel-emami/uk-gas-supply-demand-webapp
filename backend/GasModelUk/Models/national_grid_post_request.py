from __future__ import annotations

from dataclasses import dataclass
from GasModelUk.Exceptions.scraper_error import ScraperError
from GasModelUk.Models.base_request import BaseRequest


import logging
import requests

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NationalGridPostRequest(BaseRequest):
    """Reusable National Grid/National Gas publication request configuration."""

    url: str
    payload: dict[str, object]
    headers: dict[str, str]
    timeout: int = 60

    def send(self, session: requests.Session | None = None) -> requests.Response:
        """Post this request and return the raw HTTP response."""

        client = session if session is not None else requests

        response = client.post(
            url=self.url,
            json=self.payload,
            headers=self.headers,
            timeout=self.timeout,
        )

        if response.status_code != 200:
            raise ScraperError(
                f"National Grid API request failed with status code {response.status_code}: {response.text}"
            )

        logger.info(
            "National Grid API request succeeded with status code %s",
            response.status_code,
        )

        return response
