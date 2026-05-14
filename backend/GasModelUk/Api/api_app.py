from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from GasModelUk.Api.api_router import router
from GasModelUk.Api.api_service import ApiService
from GasModelUk.Api.etl_service import EtlService
from GasModelUk.Config.app_settings import AppSettings

logger = logging.getLogger(__name__)


def create_app(excel_path: str | Path | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = AppSettings()
    selected_excel_path = (
        Path(excel_path) if excel_path is not None else settings.default_excel_path
    )
    app = FastAPI(title=settings.app_name)
    app.state.api_service = ApiService(selected_excel_path)
    app.state.etl_service = EtlService(selected_excel_path)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    logger.info("API application created with Excel path %s", selected_excel_path)

    @app.get("/health")
    def health_check() -> dict[str, str]:
        """Return a simple health check payload."""

        return {"status": "ok"}

    return app


app = create_app()
