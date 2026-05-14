from __future__ import annotations

import unittest

from GasModelUk.Constants.gas_flow_registry import CATEGORY_KEYS, LOWEST_LEVEL_COLUMNS
from GasModelUk.Constants.scraper_registry import (
    get_ids_by_type,
    get_output_field_by_publication_id,
)


class ScraperRegistryTests(unittest.TestCase):
    def test_lng_ids_include_both_isle_of_grain_publication_ids(self) -> None:
        ids_by_site = get_ids_by_type("national_grid", "lng")

        self.assertEqual(ids_by_site["isle_of_grain_1"], "PUBOB371")
        self.assertEqual(ids_by_site["isle_of_grain_2"], "PUBOB3473")

    def test_lng_publication_ids_map_to_shared_isle_of_grain_field(self) -> None:
        output_fields = get_output_field_by_publication_id("national_grid", "lng")

        self.assertEqual(output_fields["PUBOB371"], "isle_of_grain")
        self.assertEqual(output_fields["PUBOB3473"], "isle_of_grain")

    def test_production_ids_are_flattened_across_ncs_and_ukcs_groups(self) -> None:
        ids_by_field = get_ids_by_type("national_grid", "production")

        self.assertEqual(ids_by_field["easington_langeled"], "PUBOB452")
        self.assertEqual(ids_by_field["teesside_cats"], "PUBOB437")
        self.assertEqual(ids_by_field["teesside_px"], "PUBOB440")

    def test_national_grid_output_fields_are_registered_flow_columns(self) -> None:
        for category_key in CATEGORY_KEYS:
            with self.subTest(category_key=category_key):
                output_fields = get_output_field_by_publication_id(
                    "national_grid",
                    category_key,
                )
                allowed_fields = set(LOWEST_LEVEL_COLUMNS[category_key])

                self.assertTrue(output_fields)
                self.assertLessEqual(set(output_fields.values()), allowed_fields)


if __name__ == "__main__":
    unittest.main()
