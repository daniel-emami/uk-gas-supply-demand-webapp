from __future__ import annotations

import math
from collections.abc import Iterable


def sum_optional_values(values: Iterable[float | None]) -> float | None:
    """Return the sum of available numeric values, or None if all values are missing."""

    numbers: list[float] = []
    for value in values:
        if value is None:
            continue
        if isinstance(value, float) and math.isnan(value):
            continue
        numbers.append(float(value))

    if not numbers:
        return None
    return round(sum(numbers), 3)
