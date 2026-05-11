from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class NationalGridPostRequest:
    """Reusable National Grid/National Gas publication request configuration."""

    url: str
    payload: dict[str, object]
    headers: dict[str, str]
    timeout: int = 60

    def send_post(self, session: requests.Session | None = None) -> requests.Response:
        """Post this request and return the raw HTTP response."""

        client = session if session is not None else requests
        return client.post(
            url=self.url,
            json=self.payload,
            headers=self.headers,
            timeout=self.timeout,
        )
