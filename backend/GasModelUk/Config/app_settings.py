from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    """Small application settings container for local console usage."""

    default_demo_excel_path: Path = Path("data/demo_data.xlsx")
    default_real_excel_path: Path = Path("data/gas_flows.xlsx")
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    app_name: str = "Gas Model UK"
