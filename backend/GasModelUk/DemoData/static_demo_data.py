from __future__ import annotations

from typing import Any

from GasModelUk.Constants.gas_flow_registry import CATEGORY_KEYS, UNIT
from GasModelUk.Utilities.date_utils import is_within_date_filter

DEMO_DATA_NOTICE = "Fake static demo data for development only. Not real UK gas market data."

DEMO_DATA_BY_CATEGORY: dict[str, list[dict[str, Any]]] = {
    "demand": [
        {"gas_day": "2026-01-01", "ldz": -172.0, "gas_for_power": -48.0, "industry": -24.0},
        {"gas_day": "2026-01-02", "ldz": -174.0, "gas_for_power": -49.0, "industry": -24.5},
        {"gas_day": "2026-01-03", "ldz": -169.0, "gas_for_power": -50.0, "industry": -25.0},
        {"gas_day": "2026-01-04", "ldz": -171.5, "gas_for_power": -47.0, "industry": -24.0},
        {"gas_day": "2026-01-05", "ldz": -176.0, "gas_for_power": -46.5, "industry": -23.5},
        {"gas_day": "2026-01-06", "ldz": -180.0, "gas_for_power": -45.0, "industry": -23.0},
        {"gas_day": "2026-01-07", "ldz": -177.5, "gas_for_power": -46.0, "industry": -24.2},
    ],
    "storage": [
        {"gas_day": "2026-01-01", "aldbrough": 6.0, "hatfield_moor": 1.5, "hill_top_farm": 0.8, "holehouse_farm": 0.7, "holford": 4.5, "hornsea": 5.2, "humbly_grove": 2.1, "rough": 8.7, "stublach": 5.5},
        {"gas_day": "2026-01-02", "aldbrough": 6.2, "hatfield_moor": 1.6, "hill_top_farm": 0.8, "holehouse_farm": 0.7, "holford": 4.7, "hornsea": 5.3, "humbly_grove": 2.1, "rough": 9.0, "stublach": 5.6},
        {"gas_day": "2026-01-03", "aldbrough": 5.8, "hatfield_moor": 1.5, "hill_top_farm": 0.7, "holehouse_farm": 0.7, "holford": 4.3, "hornsea": 5.1, "humbly_grove": 2.0, "rough": 8.8, "stublach": 5.6},
        {"gas_day": "2026-01-04", "aldbrough": 5.6, "hatfield_moor": 1.4, "hill_top_farm": 0.7, "holehouse_farm": 0.6, "holford": 4.2, "hornsea": 5.0, "humbly_grove": 1.9, "rough": 8.5, "stublach": 5.6},
        {"gas_day": "2026-01-05", "aldbrough": 6.1, "hatfield_moor": 1.6, "hill_top_farm": 0.8, "holehouse_farm": 0.7, "holford": 4.6, "hornsea": 5.2, "humbly_grove": 2.1, "rough": 9.0, "stublach": 5.6},
        {"gas_day": "2026-01-06", "aldbrough": 6.3, "hatfield_moor": 1.6, "hill_top_farm": 0.8, "holehouse_farm": 0.8, "holford": 4.7, "hornsea": 5.4, "humbly_grove": 2.2, "rough": 9.0, "stublach": 5.4},
        {"gas_day": "2026-01-07", "aldbrough": 6.2, "hatfield_moor": 1.6, "hill_top_farm": 0.8, "holehouse_farm": 0.7, "holford": 4.6, "hornsea": 5.3, "humbly_grove": 2.1, "rough": 9.0, "stublach": 5.6},
    ],
    "lng": [
        {"gas_day": "2026-01-01", "dragon": 16.0, "isle_of_grain": 19.0, "south_hook": 22.0},
        {"gas_day": "2026-01-02", "dragon": 16.5, "isle_of_grain": 19.2, "south_hook": 22.5},
        {"gas_day": "2026-01-03", "dragon": 15.5, "isle_of_grain": 18.6, "south_hook": 21.5},
        {"gas_day": "2026-01-04", "dragon": 15.8, "isle_of_grain": 18.9, "south_hook": 21.7},
        {"gas_day": "2026-01-05", "dragon": 16.2, "isle_of_grain": 19.3, "south_hook": 22.5},
        {"gas_day": "2026-01-06", "dragon": 16.8, "isle_of_grain": 19.5, "south_hook": 22.8},
        {"gas_day": "2026-01-07", "dragon": 16.1, "isle_of_grain": 19.1, "south_hook": 22.3},
    ],
    "production": [
        {"gas_day": "2026-01-01", "easington_langeled": 24.0, "st_fergus_nsmp": 18.0, "st_fergus_shell": 16.0, "teesside": 7.0, "theddlethorpe": 3.5, "st_fergus_mobil": 10.0, "easington_dimlington": 6.0, "bacton_perenco": 11.0, "bacton_seal": 8.0, "bacton_shell": 14.5},
        {"gas_day": "2026-01-02", "easington_langeled": 24.2, "st_fergus_nsmp": 18.1, "st_fergus_shell": 16.2, "teesside": 7.1, "theddlethorpe": 3.6, "st_fergus_mobil": 10.1, "easington_dimlington": 6.1, "bacton_perenco": 11.1, "bacton_seal": 8.1, "bacton_shell": 14.4},
        {"gas_day": "2026-01-03", "easington_langeled": 24.1, "st_fergus_nsmp": 18.0, "st_fergus_shell": 16.0, "teesside": 7.0, "theddlethorpe": 3.5, "st_fergus_mobil": 10.0, "easington_dimlington": 6.0, "bacton_perenco": 11.0, "bacton_seal": 8.0, "bacton_shell": 14.5},
        {"gas_day": "2026-01-04", "easington_langeled": 23.8, "st_fergus_nsmp": 17.8, "st_fergus_shell": 15.9, "teesside": 6.9, "theddlethorpe": 3.4, "st_fergus_mobil": 9.9, "easington_dimlington": 5.9, "bacton_perenco": 10.9, "bacton_seal": 7.9, "bacton_shell": 14.8},
        {"gas_day": "2026-01-05", "easington_langeled": 24.0, "st_fergus_nsmp": 18.1, "st_fergus_shell": 16.1, "teesside": 7.0, "theddlethorpe": 3.5, "st_fergus_mobil": 10.0, "easington_dimlington": 6.0, "bacton_perenco": 11.1, "bacton_seal": 8.1, "bacton_shell": 14.7},
        {"gas_day": "2026-01-06", "easington_langeled": 24.3, "st_fergus_nsmp": 18.2, "st_fergus_shell": 16.1, "teesside": 7.1, "theddlethorpe": 3.6, "st_fergus_mobil": 10.1, "easington_dimlington": 6.1, "bacton_perenco": 11.2, "bacton_seal": 8.1, "bacton_shell": 14.6},
        {"gas_day": "2026-01-07", "easington_langeled": 24.0, "st_fergus_nsmp": 18.1, "st_fergus_shell": 16.0, "teesside": 7.0, "theddlethorpe": 3.5, "st_fergus_mobil": 10.0, "easington_dimlington": 6.0, "bacton_perenco": 11.1, "bacton_seal": 8.1, "bacton_shell": 15.2},
    ],
    "cross_border_flows": [
        {"gas_day": "2026-01-01", "interconnector": 15.0, "bbl": 12.0, "moffat": 6.5},
        {"gas_day": "2026-01-02", "interconnector": 15.5, "bbl": 12.5, "moffat": 6.7},
        {"gas_day": "2026-01-03", "interconnector": 15.8, "bbl": 12.3, "moffat": 6.9},
        {"gas_day": "2026-01-04", "interconnector": 15.6, "bbl": 12.2, "moffat": 7.0},
        {"gas_day": "2026-01-05", "interconnector": 14.9, "bbl": 11.8, "moffat": 6.4},
        {"gas_day": "2026-01-06", "interconnector": 14.8, "bbl": 11.7, "moffat": 6.4},
        {"gas_day": "2026-01-07", "interconnector": 16.0, "bbl": 12.6, "moffat": 6.9},
    ],
}


def get_static_demo_rows(category_key: str, start_date: str, end_date: str) -> list[dict[str, Any]]:
    """Return fake demo rows for a category and inclusive date range."""

    if category_key not in CATEGORY_KEYS:
        raise KeyError(f"Unknown demo category: {category_key}")
    return [
        dict(row)
        for row in DEMO_DATA_BY_CATEGORY[category_key]
        if is_within_date_filter(row["gas_day"], start_date, end_date)
    ]


def get_all_static_demo_data() -> dict[str, list[dict[str, Any]]]:
    """Return all fake demo rows keyed by category."""

    return {category_key: [dict(row) for row in rows] for category_key, rows in DEMO_DATA_BY_CATEGORY.items()}


def get_demo_unit() -> str:
    """Return the unit used by the fake demo dataset."""

    return UNIT
