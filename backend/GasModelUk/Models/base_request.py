from __future__ import annotations

from abc import ABC, abstractmethod

import requests


class BaseRequest(ABC):
    """Interface for reusable scraper HTTP requests."""

    @abstractmethod
    def send(self, session: requests.Session | None = None) -> requests.Response:
        """Send the request and return the raw HTTP response."""
