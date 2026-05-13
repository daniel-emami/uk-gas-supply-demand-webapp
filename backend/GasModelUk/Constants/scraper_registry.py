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
            "isle_of_grain_1": {
                "publication_id": "PUBOB371",
                "output_field": "isle_of_grain",
            },
            "isle_of_grain_2": {
                "publication_id": "PUBOB3473",
                "output_field": "isle_of_grain",
            },
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


def _publication_entry_to_id(entry: str | dict[str, str]) -> str:
    if isinstance(entry, str):
        return entry
    return entry["publication_id"]


def get_ids_by_type(source_name: str, category_key: str) -> dict[str, str]:
    """Return allowed lowest-level flow columns for a section or category key."""

    entries = API_IDS.get(source_name, {}).get(category_key, {})
    return {
        field_name: _publication_entry_to_id(entry)
        for field_name, entry in entries.items()
    }


def get_output_field_by_publication_id(
    source_name: str,
    category_key: str,
) -> dict[str, str]:
    """Return publication id to output-field mapping for a category."""

    entries = API_IDS.get(source_name, {}).get(category_key, {})
    output_fields: dict[str, str] = {}
    for field_name, entry in entries.items():
        publication_id = _publication_entry_to_id(entry)
        if isinstance(entry, str):
            output_fields[publication_id] = field_name
        else:
            output_fields[publication_id] = entry.get("output_field", field_name)
    return output_fields
