from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request

from GasModelUk.Api.api_service import ApiService
from GasModelUk.Exceptions.api_data_error import ApiDataError
from GasModelUk.Utilities.date_utils import ensure_date_order

router = APIRouter()


def get_api_service(request: Request) -> ApiService:
    """Return the configured API service from FastAPI application state."""

    return request.app.state.api_service


def validate_date_filters(start_date: str | None, end_date: str | None) -> None:
    """Validate optional gas day query parameters."""

    try:
        ensure_date_order(start_date, end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/api/gas-flows")
def get_gas_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return all gas flow sections as nested daily records."""

    validate_date_filters(start_date, end_date)
    try:
        return get_api_service(request).get_gas_flows(start_date=start_date, end_date=end_date)
    except ApiDataError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/api/gas-flows/demand")
def get_demand_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return demand flows as daily records."""

    return _get_section(request, "demand", start_date, end_date)


@router.get("/api/gas-flows/storage")
def get_storage_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return storage supply flows as daily records."""

    return _get_section(request, "storage", start_date, end_date)


@router.get("/api/gas-flows/lng")
def get_lng_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return LNG supply flows as daily records."""

    return _get_section(request, "lng", start_date, end_date)


@router.get("/api/gas-flows/ncs")
def get_ncs_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return NCS supply flows as daily records."""

    return _get_section(request, "ncs", start_date, end_date)


@router.get("/api/gas-flows/ukcs")
def get_ukcs_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return UKCS supply flows as daily records."""

    return _get_section(request, "ukcs", start_date, end_date)


@router.get("/api/gas-flows/production")
def get_production_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return production flows as daily records."""

    return _get_section(request, "production", start_date, end_date)


@router.get("/api/gas-flows/cross-border-flows")
def get_cross_border_flows(
    request: Request,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
) -> dict:
    """Return cross-border supply flows as daily records."""

    return _get_section(request, "cross_border_flows", start_date, end_date)


def _get_section(
    request: Request,
    section_key: str,
    start_date: str | None,
    end_date: str | None,
) -> dict:
    validate_date_filters(start_date, end_date)
    try:
        return get_api_service(request).get_section_flows(
            section_key,
            start_date=start_date,
            end_date=end_date,
        )
    except ApiDataError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
