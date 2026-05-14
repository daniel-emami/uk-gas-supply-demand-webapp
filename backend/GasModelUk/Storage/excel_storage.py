from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from GasModelUk.Constants.gas_flow_registry import (
    CATEGORY_KEYS,
    get_expected_sheet_columns,
    get_sheet_name,
)
from GasModelUk.Exceptions.excel_storage_error import ExcelStorageError
from GasModelUk.Models.transformed_gas_flow_dataset import TransformedGasFlowDataset
from GasModelUk.Storage.base_storage import BaseStorage
from GasModelUk.Utilities.date_utils import format_gas_day

logger = logging.getLogger(__name__)


class ExcelStorage(BaseStorage):
    """Excel storage implementation using pandas and openpyxl."""

    def __init__(self, workbook_path: str | Path) -> None:
        """Create storage bound to one Excel workbook path."""

        self.workbook_path = Path(workbook_path)

    def read_category_sheet(self, category_key: str) -> pd.DataFrame:
        """Read, validate, and normalize one category sheet from Excel."""

        sheet_name = get_sheet_name(category_key)
        logger.info("Reading Excel sheet %s from %s", sheet_name, self.workbook_path)
        if not self.workbook_path.exists():
            raise ExcelStorageError(f"Workbook does not exist: {self.workbook_path}")
        try:
            frame = pd.read_excel(self.workbook_path, sheet_name=sheet_name)
            return self._validate_and_normalize_frame(category_key, frame)
        except ExcelStorageError:
            raise
        except Exception as exc:
            raise ExcelStorageError(f"Failed to read sheet {sheet_name}: {exc}") from exc

    def read_all_category_sheets(self) -> dict[str, pd.DataFrame]:
        """Read all registered category sheets from Excel."""

        return {
            category_key: self.read_category_sheet(category_key)
            for category_key in CATEGORY_KEYS
        }

    def write_category_sheets(self, datasets: list[TransformedGasFlowDataset]) -> None:
        """Write each supplied category sheet independently to Excel."""

        self.workbook_path.parent.mkdir(parents=True, exist_ok=True)
        for dataset in datasets:
            self._write_category_sheet(dataset)

    def _write_category_sheet(self, dataset: TransformedGasFlowDataset) -> None:
        sheet_name = get_sheet_name(dataset.category_key)
        expected_columns = list(get_expected_sheet_columns(dataset.category_key))
        frame = pd.DataFrame(dataset.rows)
        frame = self._merge_with_existing_rows(dataset.category_key, frame)
        for column in expected_columns:
            if column not in frame.columns:
                logger.warning(
                    "Adding missing column %s to %s before Excel write",
                    column,
                    sheet_name,
                )
                frame[column] = pd.NA
        frame = frame[expected_columns]
        logger.info("Writing Excel sheet %s to %s", sheet_name, self.workbook_path)
        try:
            if self.workbook_path.exists():
                with pd.ExcelWriter(
                    self.workbook_path,
                    engine="openpyxl",
                    mode="a",
                    if_sheet_exists="replace",
                ) as writer:
                    frame.to_excel(writer, sheet_name=sheet_name, index=False, na_rep="")
            else:
                with pd.ExcelWriter(self.workbook_path, engine="openpyxl", mode="w") as writer:
                    frame.to_excel(writer, sheet_name=sheet_name, index=False, na_rep="")
        except Exception as exc:
            raise ExcelStorageError(f"Failed to write sheet {sheet_name}: {exc}") from exc

    def _merge_with_existing_rows(self, category_key: str, frame: pd.DataFrame) -> pd.DataFrame:
        if not self.workbook_path.exists():
            return frame
        try:
            existing_frame = self.read_category_sheet(category_key)
        except ExcelStorageError:
            return frame

        if existing_frame.empty:
            return frame

        frame = frame.copy()
        frame["gas_day"] = frame["gas_day"].map(self._format_excel_gas_day)
        combined = pd.concat([existing_frame, frame], ignore_index=True)
        return (
            combined.drop_duplicates(subset=["gas_day"], keep="last")
            .sort_values("gas_day")
            .reset_index(drop=True)
        )

    def _validate_and_normalize_frame(self, category_key: str, frame: pd.DataFrame) -> pd.DataFrame:
        expected_columns = list(get_expected_sheet_columns(category_key))
        expected_set = set(expected_columns)
        frame = frame.copy()
        frame.columns = [str(column).strip() for column in frame.columns]

        unknown_columns = sorted(set(frame.columns) - expected_set)
        if unknown_columns:
            logger.warning(
                "Ignoring unknown columns in %s: %s",
                get_sheet_name(category_key),
                ", ".join(unknown_columns),
            )

        for column in expected_columns:
            if column not in frame.columns:
                logger.warning("Missing column %s in %s; filling with blanks", column, category_key)
                frame[column] = pd.NA

        frame = frame[expected_columns]
        frame["gas_day"] = frame["gas_day"].map(self._format_excel_gas_day)
        for column in expected_columns[1:]:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        return frame

    def _format_excel_gas_day(self, value: Any) -> str:
        if pd.isna(value):
            raise ExcelStorageError("Encountered blank gas_day in Excel input")
        return format_gas_day(value)
