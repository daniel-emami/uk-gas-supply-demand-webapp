from __future__ import annotations


from GasModelUk.Constants.scraper_registry import get_api_url, get_ids_by_type
from GasModelUk.Models.national_grid_post_request import NationalGridPostRequest
from GasModelUk.Models.scrape_request import ScrapeRequest


def create_national_grid_request(
    source_name: str,
    category_key: str,
    request: ScrapeRequest,
    *,
    latest_value: bool = True,
    timeout: int = 60,
) -> NationalGridPostRequest:
    """Build a National Grid/National Gas publications request for a scraper."""

    publication_ids = list(get_ids_by_type(source_name, category_key).values())
    if not publication_ids:
        raise ValueError(
            f"No publication ids configured for source '{source_name}' "
            f"and category '{category_key}'."
        )

    url = get_api_url(source_name)
    if not url:
        raise ValueError(f"No API URL configured for source '{source_name}'.")

    return NationalGridPostRequest(
        url=url,
        payload={
            "fromDate": request.start_date,
            "toDate": request.end_date,
            "publicationIds": publication_ids,
            "latestValue": "Y" if latest_value else "N",
        },
        headers={"Content-Type": "application/json"},
        timeout=timeout,
    )
