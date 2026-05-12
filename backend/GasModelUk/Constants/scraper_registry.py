API_URLS = {
    "national_grid": "https://api.nationalgas.com/operationaldata/v1/publications/gasday",
}

CATALOGUE_API_URLS = {
    "national_grid": "https://api.nationalgas.com/operationaldata/v1/publications/catalogue",
}

API_IDS = {
    "national_grid": {  # national_grid id's are found on https://api.nationalgas.com/operationaldata/v1/publications/catalogue
        "demand": {
            "ldz": "PUBOBJ1015",
            "gas_for_power": "PUBOBJ1017",
            "industry": "PUBOBJ1018",
        },
    },
    "de_api_name": {
        "demand": {"placeholder": "DE_DEMAND_ID"},
    },
}


def get_api_url(source_name: str) -> str:
    """Return the API URL for a persisted source name."""

    return API_URLS.get(source_name, "")


def get_ids_by_type(source_name: str, category_key: str) -> dict[str, str]:
    """Return allowed lowest-level flow columns for a section or category key."""

    return API_IDS.get(source_name, {}).get(category_key, {})
