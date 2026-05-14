from __future__ import annotations

import asyncio
from pathlib import Path

from GasModelUk.Constants.gas_flow_registry import CATEGORY_KEYS
from GasModelUk.Models.etl_result import EtlResult
from GasModelUk.Orchestration.etl_pipeline import EtlPipeline
from GasModelUk.Utilities.date_utils import ensure_date_order

ETL_SCOPE_CATEGORIES = {
    "all": CATEGORY_KEYS,
    "supply": ("storage", "lng", "production", "cross_border_flows"),
    "demand": ("demand",),
    "storage": ("storage",),
    "lng": ("lng",),
    "production": ("production",),
    "cross_border_flows": ("cross_border_flows",),
}


class EtlService:
    """Runs ETL jobs for API-triggered workbook updates."""

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)

    async def run_scope(self, scope: str, start_date: str, end_date: str) -> EtlResult:
        ensure_date_order(start_date, end_date)
        category_keys = ETL_SCOPE_CATEGORIES.get(scope)
        if category_keys is None:
            allowed_scopes = ", ".join(sorted(ETL_SCOPE_CATEGORIES))
            raise ValueError(f"Unknown ETL scope '{scope}'. Allowed scopes: {allowed_scopes}.")

        pipeline = EtlPipeline(self.output_path)
        return await pipeline.run(start_date, end_date, category_keys=category_keys)

    def run_scope_sync(self, scope: str, start_date: str, end_date: str) -> EtlResult:
        return asyncio.run(self.run_scope(scope, start_date, end_date))
