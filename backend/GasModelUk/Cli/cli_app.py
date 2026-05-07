from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import typer
import uvicorn

from GasModelUk.Api.api_app import create_app
from GasModelUk.Config.app_settings import AppSettings
from GasModelUk.Orchestration.etl_pipeline import EtlPipeline
from GasModelUk.Utilities.logging_config import configure_logging

app = typer.Typer(help="Console commands for Gas Model UK.")


@app.command("run-etl")
def run_etl(
    start_date: str = typer.Option(..., help="Inclusive ETL start gas day in YYYY-MM-DD format."),
    end_date: str = typer.Option(..., help="Inclusive ETL end gas day in YYYY-MM-DD format."),
    output_path: Path | None = typer.Option(None, help="Output Excel path."),
) -> None:
    """Run the manual ETL pipeline and write successful categories to Excel."""

    configure_logging()
    settings = AppSettings()
    selected_output_path = output_path or settings.default_real_excel_path
    result = asyncio.run(EtlPipeline(selected_output_path).run(start_date=start_date, end_date=end_date))
    typer.echo(f"ETL complete. Output: {result.output_path}")
    typer.echo(f"Successful categories: {', '.join(result.successful_categories) or 'none'}")
    typer.echo(f"Failed categories: {', '.join(result.failed_categories) or 'none'}")


@app.command("run-api")
def run_api(
    excel_path: Path | None = typer.Option(None, help="Excel workbook path used by the API."),
    host: str | None = typer.Option(None, help="API host."),
    port: int | None = typer.Option(None, help="API port."),
) -> None:
    """Run the FastAPI application with uvicorn."""

    configure_logging()
    settings = AppSettings()
    selected_excel_path = excel_path or settings.default_demo_excel_path
    selected_host = host or settings.api_host
    selected_port = port or settings.api_port
    logging.getLogger(__name__).info(
        "Starting API on %s:%s with Excel path %s",
        selected_host,
        selected_port,
        selected_excel_path,
    )
    uvicorn.run(
        create_app(excel_path=selected_excel_path),
        host=selected_host,
        port=selected_port,
    )
