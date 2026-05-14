from __future__ import annotations

import math
import unittest
from datetime import date
from typing import cast

from GasModelUk.Constants.gas_flow_registry import UNIT
from GasModelUk.Models.demand_gas_flow_record import DemandGasFlowRecord
from GasModelUk.Models.raw_demand_gas_flow_dataset import RawDemandGasFlowDataset
from GasModelUk.Transform.gas_flow_transformer import GasFlowTransformer


class GasFlowTransformerTests(unittest.TestCase):
    def test_transform_formats_gas_day_and_converts_numbers(self) -> None:
        raw_dataset = RawDemandGasFlowDataset(
            records=(
                DemandGasFlowRecord(
                    gas_day=date(2024, 1, 1),
                    ldz=-10,
                    gas_for_power=cast(float, "-2.5"),
                    industry=None,
                ),
            ),
            unit=UNIT,
            source_name="test",
        )

        transformed = GasFlowTransformer().transform(raw_dataset)

        self.assertEqual(transformed.category_key, "demand")
        self.assertEqual(len(transformed.rows), 1)
        row = transformed.rows[0]
        self.assertEqual(row["gas_day"], "2024-01-01")
        self.assertEqual(row["ldz"], -10.0)
        self.assertEqual(row["gas_for_power"], -2.5)
        self.assertTrue(math.isnan(row["industry"]))


if __name__ == "__main__":
    unittest.main()
