from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScrapeRequest:
    """Date-bounded request passed to each category scraper."""

    start_date: str
    end_date: str
