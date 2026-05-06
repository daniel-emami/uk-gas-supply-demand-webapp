from __future__ import annotations

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure standard-library logging for console usage."""

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
