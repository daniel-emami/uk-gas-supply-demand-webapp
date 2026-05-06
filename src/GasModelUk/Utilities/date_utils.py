from __future__ import annotations

from datetime import date, datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"


def parse_gas_day(value: str) -> date:
    """Parse a gas day string in strict YYYY-MM-DD format."""

    parsed = datetime.strptime(value, DATE_FORMAT).date()
    if parsed.strftime(DATE_FORMAT) != value:
        raise ValueError(f"Invalid gas_day format: {value}")
    return parsed


def format_gas_day(value: date | datetime | str) -> str:
    """Format a date-like value as YYYY-MM-DD."""

    if isinstance(value, datetime):
        return value.date().strftime(DATE_FORMAT)
    if isinstance(value, date):
        return value.strftime(DATE_FORMAT)
    return parse_gas_day(str(value)).strftime(DATE_FORMAT)


def ensure_date_order(start_date: str | None, end_date: str | None) -> None:
    """Validate that optional start and end gas day filters are ordered correctly."""

    if start_date is not None:
        parse_gas_day(start_date)
    if end_date is not None:
        parse_gas_day(end_date)
    if start_date is not None and end_date is not None:
        if parse_gas_day(start_date) > parse_gas_day(end_date):
            raise ValueError("start_date must be before or equal to end_date")


def gas_day_range(start_date: str, end_date: str) -> list[str]:
    """Return inclusive gas day strings between two YYYY-MM-DD dates."""

    start = parse_gas_day(start_date)
    end = parse_gas_day(end_date)
    if start > end:
        raise ValueError("start_date must be before or equal to end_date")
    days = []
    current = start
    while current <= end:
        days.append(current.strftime(DATE_FORMAT))
        current += timedelta(days=1)
    return days


def is_within_date_filter(gas_day: str, start_date: str | None, end_date: str | None) -> bool:
    """Return whether a gas day is inside optional inclusive date filters."""

    value = parse_gas_day(gas_day)
    if start_date is not None and value < parse_gas_day(start_date):
        return False
    if end_date is not None and value > parse_gas_day(end_date):
        return False
    return True
