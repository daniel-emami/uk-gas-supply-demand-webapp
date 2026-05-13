from __future__ import annotations

UNIT = "mcm/d"

SECTION_KEYS = {
    "demand": "demand",
    "ncs": "ncs",
    "ukcs": "ukcs",
    "storage": "storage",
    "lng": "lng",
    "production": "production",
    "cross_border_flows": "cross_border_flows",
}

SHEET_NAMES = {
    "demand": "Demand",
    "storage": "Storage",
    "lng": "LNG",
    "production": "Production",
    "cross_border_flows": "Cross Border Flows",
}

CATEGORY_KEYS = tuple(SHEET_NAMES.keys())

NCS_COLUMNS = ("easington_langeled", "st_fergus_nsmp", "st_fergus_shell")
UKCS_COLUMNS = (
    "teesside",
    "theddlethorpe",
    "st_fergus_mobil",
    "easington_dimlington",
    "bacton_perenco",
    "bacton_seal",
    "bacton_shell",
)
STORAGE_COLUMNS = (
    "aldbrough",
    "hatfield_moor",
    "hill_top_farm",
    "holehouse_farm",
    "holford",
    "hornsea",
    "humbly_grove",
    "rough",
    "stublach",
)
LNG_COLUMNS = ("dragon", "isle_of_grain", "south_hook")
CROSS_BORDER_FLOW_COLUMNS = ("interconnector", "bbl", "moffat")

LOWEST_LEVEL_COLUMNS = {
    "demand": ("ldz", "gas_for_power", "industry"),
    "storage": STORAGE_COLUMNS,
    "lng": LNG_COLUMNS,
    "ncs": NCS_COLUMNS,
    "ukcs": UKCS_COLUMNS,
    "production": (*NCS_COLUMNS, *UKCS_COLUMNS),
    "cross_border_flows": CROSS_BORDER_FLOW_COLUMNS,
}

PRODUCTION_GROUPS = {
    "ncs": NCS_COLUMNS,
    "ukcs": UKCS_COLUMNS,
}

SUPPLY_SECTION_KEYS = ("ncs", "ukcs", "lng", "cross_border_flows", "storage")

AGGREGATION_RELATIONSHIPS = {
    "demand.total": LOWEST_LEVEL_COLUMNS["demand"],
    "supply.ncs.total": LOWEST_LEVEL_COLUMNS["ncs"],
    "supply.ukcs.total": LOWEST_LEVEL_COLUMNS["ukcs"],
    "supply.lng.total": LOWEST_LEVEL_COLUMNS["lng"],
    "supply.cross_border_flows.total": LOWEST_LEVEL_COLUMNS["cross_border_flows"],
    "supply.storage.total": LOWEST_LEVEL_COLUMNS["storage"],
    "supply.total": SUPPLY_SECTION_KEYS,
    "balance": ("demand.total", "supply.total"),
}

DISPLAY_NAMES = {
    "demand": "Demand",
    "storage": "Storage",
    "lng": "LNG",
    "production": "Production",
    "cross_border_flows": "Cross Border Flows",
    "ncs": "NCS",
    "ukcs": "UKCS",
    "ldz": "LDZ",
    "gas_for_power": "Gas for Power",
    "industry": "Industry",
    "aldbrough": "Aldbrough",
    "hatfield_moor": "Hatfield Moor",
    "hill_top_farm": "Hill Top Farm",
    "holehouse_farm": "Hole House Farm",
    "holford": "Holford",
    "hornsea": "Hornsea",
    "humbly_grove": "Humbly Grove",
    "rough": "Rough",
    "stublach": "Stublach",
    "dragon": "Dragon",
    "isle_of_grain": "Isle of Grain",
    "south_hook": "South Hook",
    "easington_langeled": "Easington Langeled",
    "st_fergus_nsmp": "St Fergus NSMP",
    "st_fergus_shell": "St Fergus Shell",
    "teesside": "Teesside",
    "theddlethorpe": "Theddlethorpe",
    "st_fergus_mobil": "St Fergus Mobil",
    "easington_dimlington": "Easington Dimlington",
    "bacton_perenco": "Bacton Perenco",
    "bacton_seal": "Bacton SEAL",
    "bacton_shell": "Bacton Shell",
    "interconnector": "Interconnector",
    "bbl": "BBL",
    "moffat": "Moffat",
}

UNIT_METADATA = {
    "unit": UNIT,
    "description": "Million cubic metres per day",
}


def get_sheet_name(category_key: str) -> str:
    """Return the Excel sheet name for a persisted category key."""

    return SHEET_NAMES[category_key]


def get_allowed_columns(category_key: str) -> tuple[str, ...]:
    """Return allowed lowest-level flow columns for a section or category key."""

    return LOWEST_LEVEL_COLUMNS[category_key]


def get_expected_sheet_columns(category_key: str) -> tuple[str, ...]:
    """Return the expected Excel columns for a persisted category sheet."""

    return ("gas_day", *get_allowed_columns(category_key))
