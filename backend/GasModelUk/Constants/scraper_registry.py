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
        "cross_border_flows": {
            "interconnector": "PUBOB2038",
            "bbl": "PUBOBJ1307",
            "moffat": "PUBOB2039",
        },
        "storage": {
            "aldbrough": "PUBOB2896",
            "avonmouth": "PUBOB1872",
            "hatfield_moor": "PUBOB1882",
            "hill_top_farm": "PUBOBJ2041",
            "holehouse_farm": "PUBOB1936",
            "holford": "PUBOBJ2002",
            "hornsea": "PUBOB1939",
            "humbly_grove": "PUBOB1941",
            "rough": "PUBOB1995",
            "stublach": "PUBOBJ11555",
        },
        "lng": {
            "dragon": "PUBOB3564",
            "isle_of_grain_1": "PUBOB371",
            "isle_of_grain_2": "PUBOB3473",
            "south_hook": "PUBOB3480",
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
