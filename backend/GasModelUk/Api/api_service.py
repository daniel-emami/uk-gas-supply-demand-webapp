from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from GasModelUk.Api.api_models import GasFlowRecordPayload, GasFlowsPayload
from GasModelUk.Constants.gas_flow_registry import (
    LOWEST_LEVEL_COLUMNS,
    PRODUCTION_GROUPS,
    UNIT,
)
from GasModelUk.Exceptions.api_data_error import ApiDataError
from GasModelUk.Exceptions.excel_storage_error import ExcelStorageError
from GasModelUk.Models.cross_border_gas_flow_record import CrossBorderGasFlowRecord
from GasModelUk.Models.daily_gas_flow_record import DailyGasFlowRecord
from GasModelUk.Models.demand_gas_flow_record import DemandGasFlowRecord
from GasModelUk.Models.lng_gas_flow_record import LngGasFlowRecord
from GasModelUk.Models.ncs_gas_flow_record import NcsGasFlowRecord
from GasModelUk.Models.storage_gas_flow_record import StorageGasFlowRecord
from GasModelUk.Models.ukcs_gas_flow_record import UkcsGasFlowRecord
from GasModelUk.Storage.excel_storage import ExcelStorage
from GasModelUk.Utilities.date_utils import (
    ensure_date_order,
    is_within_date_filter,
    parse_gas_day,
)
from GasModelUk.Utilities.number_utils import sum_optional_values

logger = logging.getLogger(__name__)


class ApiService:
    """Reads Excel storage and returns frontend-ready gas flow payloads."""

    def __init__(self, excel_path: str | Path) -> None:
        """Create the API service for a selected Excel workbook path."""

        self.excel_path = Path(excel_path)
        self.storage = ExcelStorage(self.excel_path)

    def get_gas_flows(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> GasFlowsPayload:
        """Return full nested daily gas flow records with calculated aggregates."""

        ensure_date_order(start_date, end_date)
        frames = self._read_filtered_frames(start_date, end_date)
        gas_days = self._get_sorted_gas_days(frames)
        records = [self._build_daily_record(gas_day, frames).to_payload() for gas_day in gas_days]
        return {
            "unit": UNIT,
            "is_demo_data": self.excel_path.name == "demo_data.xlsx",
            "records": records,
        }

    def get_section_flows(
        self,
        section_key: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> GasFlowsPayload:
        """Return one section of nested daily gas flow records."""

        full_payload = self.get_gas_flows(start_date=start_date, end_date=end_date)
        records = []
        for record in full_payload["records"]:
            section_payload = self._extract_section_payload(record, section_key)
            records.append({"gas_day": record["gas_day"], section_key: section_payload})
        return {
            "unit": full_payload["unit"],
            "is_demo_data": full_payload["is_demo_data"],
            "section": section_key,
            "records": records,
        }

    def _extract_section_payload(self, record: GasFlowRecordPayload, section_key: str) -> object:
        if section_key == "demand":
            return record["demand"]
        if section_key in {"ncs", "ukcs", "lng", "storage", "cross_border_flows"}:
            return record["supply"][section_key]
        if section_key == "production":
            ncs = record["supply"]["ncs"]
            ukcs = record["supply"]["ukcs"]
            return {
                "ncs": ncs,
                "ukcs": ukcs,
                "total": sum_optional_values([ncs["total"], ukcs["total"]]),
            }
        raise ApiDataError(f"Unknown section key: {section_key}")

    def _read_filtered_frames(
        self,
        start_date: str | None,
        end_date: str | None,
    ) -> dict[str, pd.DataFrame]:
        try:
            frames = self.storage.read_all_category_sheets()
        except ExcelStorageError as exc:
            raise ApiDataError(f"Could not read API workbook: {exc}") from exc
        return {
            category_key: self._filter_frame(frame, start_date, end_date)
            for category_key, frame in frames.items()
        }

    def _filter_frame(
        self,
        frame: pd.DataFrame,
        start_date: str | None,
        end_date: str | None,
    ) -> pd.DataFrame:
        if start_date is None and end_date is None:
            return frame
        mask = frame["gas_day"].map(
            lambda gas_day: is_within_date_filter(gas_day, start_date, end_date)
        )
        return frame.loc[mask].reset_index(drop=True)

    def _get_sorted_gas_days(self, frames: dict[str, pd.DataFrame]) -> list[str]:
        gas_days: set[str] = set()
        for frame in frames.values():
            gas_days.update(frame["gas_day"].dropna().astype(str).tolist())
        return sorted(gas_days)

    def _build_daily_record(
        self,
        gas_day: str,
        frames: dict[str, pd.DataFrame],
    ) -> DailyGasFlowRecord:
        
        production_row = self._row_for_gas_day(gas_day, frames["production"])
        return DailyGasFlowRecord(
            gas_day=parse_gas_day(gas_day),
            demand = self._build_demand(gas_day, frames["demand"]),
            ncs=self._build_ncs(gas_day, production_row),
            ukcs=self._build_ukcs(gas_day, production_row),
            lng=self._build_lng(gas_day, frames["lng"]),
            cross_border_flows=self._build_cross_border_flows(
                gas_day, frames["cross_border_flows"]
            ),
            storage=self._build_storage(gas_day, frames["storage"]),
        )

    def _build_demand(self, gas_day: str, frame: pd.DataFrame) -> DemandGasFlowRecord:
        row = self._row_for_gas_day(gas_day, frame)
        return DemandGasFlowRecord(
            gas_day=parse_gas_day(gas_day),
            ldz=self._number_or_none(row.get("ldz")),
            gas_for_power=self._number_or_none(row.get("gas_for_power")),
            industry=self._number_or_none(row.get("industry")),
        )

    def _build_storage(self, gas_day: str, frame: pd.DataFrame) -> StorageGasFlowRecord:
        row = self._row_for_gas_day(gas_day, frame)
        return StorageGasFlowRecord(
            gas_day=parse_gas_day(gas_day),
            flows=self._flow_values(row, LOWEST_LEVEL_COLUMNS["storage"]),
        )

    def _build_lng(self, gas_day: str, frame: pd.DataFrame) -> LngGasFlowRecord:
        row = self._row_for_gas_day(gas_day, frame)
        return LngGasFlowRecord(
            gas_day=parse_gas_day(gas_day),
            flows=self._flow_values(row, LOWEST_LEVEL_COLUMNS["lng"]),
        )

    def _build_cross_border_flows(
        self,
        gas_day: str,
        frame: pd.DataFrame,
    ) -> CrossBorderGasFlowRecord:
        row = self._row_for_gas_day(gas_day, frame)
        return CrossBorderGasFlowRecord(
            gas_day=parse_gas_day(gas_day),
            interconnector=self._number_or_none(row.get("interconnector")),
            bbl=self._number_or_none(row.get("bbl")),
            moffat=self._number_or_none(row.get("moffat")),
        )

    def _build_ncs(self, gas_day: str, row: dict[str, Any]) -> NcsGasFlowRecord:
        return NcsGasFlowRecord(
            gas_day=parse_gas_day(gas_day),
            flows=self._flow_values(row, PRODUCTION_GROUPS["ncs"]),
        )

    def _build_ukcs(self, gas_day: str, row: dict[str, Any]) -> UkcsGasFlowRecord:
        return UkcsGasFlowRecord(
            gas_day=parse_gas_day(gas_day),
            flows=self._flow_values(row, PRODUCTION_GROUPS["ukcs"]),
        )

    def _flow_values(
        self,
        row: dict[str, Any],
        columns: tuple[str, ...],
    ) -> dict[str, float | None]:
        return {column: self._number_or_none(row.get(column)) for column in columns}

    def _row_for_gas_day(self, gas_day: str, frame: pd.DataFrame) -> dict[str, Any]:
        matches = frame.loc[frame["gas_day"] == gas_day]
        if matches.empty:
            return {}
        return matches.iloc[0].to_dict()

    def _number_or_none(self, value: Any) -> float | None:
        if value is None or pd.isna(value):
            return None
        return round(float(value), 3)
