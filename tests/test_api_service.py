from __future__ import annotations

import unittest
from typing import Any, cast

import pandas as pd

from GasModelUk.Api.api_service import ApiService


class ApiServiceTests(unittest.TestCase):
    def test_build_daily_record_calculates_totals_and_balance(self) -> None:
        service = ApiService("data/gas_flows.xlsx")
        frames = {
            "demand": pd.DataFrame(
                [
                    {
                        "gas_day": "2024-01-01",
                        "ldz": -10.0,
                        "gas_for_power": -2.0,
                        "industry": -3.0,
                    },
                ]
            ),
            "storage": pd.DataFrame(
                [
                    {
                        "gas_day": "2024-01-01",
                        "aldbrough": 1.0,
                        "rough": 2.0,
                    },
                ]
            ),
            "lng": pd.DataFrame(
                [
                    {
                        "gas_day": "2024-01-01",
                        "dragon": 4.0,
                        "isle_of_grain": 5.0,
                    },
                ]
            ),
            "cross_border_flows": pd.DataFrame(
                [
                    {
                        "gas_day": "2024-01-01",
                        "interconnector": 6.0,
                    },
                ]
            ),
            "production": pd.DataFrame(
                [
                    {
                        "gas_day": "2024-01-01",
                        "easington_langeled": 7.0,
                        "teesside": 8.0,
                    },
                ]
            ),
        }

        payload = service._build_daily_record("2024-01-01", frames).to_payload()
        demand = cast(dict[str, Any], payload["demand"])
        supply = cast(dict[str, Any], payload["supply"])
        storage = cast(dict[str, Any], supply["storage"])
        lng = cast(dict[str, Any], supply["lng"])
        cross_border_flows = cast(dict[str, Any], supply["cross_border_flows"])
        ncs = cast(dict[str, Any], supply["ncs"])
        ukcs = cast(dict[str, Any], supply["ukcs"])

        self.assertEqual(demand["total"], -15.0)
        self.assertEqual(storage["total"], 3.0)
        self.assertEqual(lng["total"], 9.0)
        self.assertEqual(cross_border_flows["total"], 6.0)
        self.assertEqual(ncs["total"], 7.0)
        self.assertEqual(ukcs["total"], 8.0)
        self.assertEqual(supply["total"], 33.0)
        self.assertEqual(payload["balance"], 18.0)

    def test_number_or_none_converts_nan_to_none(self) -> None:
        service = ApiService("data/gas_flows.xlsx")

        self.assertIsNone(service._number_or_none(float("nan")))
        self.assertEqual(service._number_or_none("2.1234"), 2.123)


if __name__ == "__main__":
    unittest.main()
