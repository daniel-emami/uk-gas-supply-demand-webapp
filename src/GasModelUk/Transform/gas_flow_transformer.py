from __future__ import annotations

import logging
from math import nan
from typing import Any

from GasModelUk.Constants.gas_flow_registry import UNIT, get_expected_sheet_columns
from GasModelUk.Exceptions.transform_error import TransformError
from GasModelUk.Models.raw_gas_flow_dataset import RawGasFlowDataset
from GasModelUk.Models.transformed_gas_flow_dataset import TransformedGasFlowDataset
from GasModelUk.Transform.base_transformer import BaseTransformer
from GasModelUk.Utilities.date_utils import format_gas_day

logger = logging.getLogger(__name__)


class GasFlowTransformer(BaseTransformer):
    """Default transformer strategy for category gas flow datasets."""

    def transform(self, raw_dataset: RawGasFlowDataset) -> TransformedGasFlowDataset:
        """Normalize raw rows to gas_day strings and mcm/d numeric values."""

        logger.info("Starting transform for category %s", raw_dataset.category_key)
        if raw_dataset.unit != UNIT:
            logger.info("Normalizing %s from %s to %s", raw_dataset.category_key, raw_dataset.unit, UNIT)
        try:
            expected_columns = get_expected_sheet_columns(raw_dataset.category_key)
            expected_set = set(expected_columns)
            transformed_rows: list[dict[str, Any]] = []
            for row in raw_dataset.to_rows():
                unknown_columns = sorted(set(row) - expected_set)
                if unknown_columns:
                    logger.warning(
                        "Ignoring unknown columns for %s: %s",
                        raw_dataset.category_key,
                        ", ".join(unknown_columns),
                    )
                transformed_row = {"gas_day": format_gas_day(row["gas_day"])}
                for column in expected_columns[1:]:
                    transformed_row[column] = self._to_float_or_nan(row.get(column))
                transformed_rows.append(transformed_row)
        except Exception as exc:
            raise TransformError(f"Failed to transform {raw_dataset.category_key}: {exc}") from exc
        logger.info(
            "Finished transform for category %s with %s rows",
            raw_dataset.category_key,
            len(transformed_rows),
        )
        return TransformedGasFlowDataset(raw_dataset.category_key, transformed_rows)

    def _to_float_or_nan(self, value: Any) -> float:
        if value is None or value == "":
            return nan
        return float(value)
