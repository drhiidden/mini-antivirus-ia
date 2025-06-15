from __future__ import annotations

import logging
import sys
from typing import Any, Dict

import structlog


def setup_logging(level: int | str = logging.INFO) -> None:  # pragma: no cover
    """Configura logging y structlog con formato key-value."""

    # Configuración básica de logging estándar
    logging.basicConfig(
        level=level,
        format="%(message)s",
        stream=sys.stdout,
    )

    # Procesadores comunes
    shared_processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    ) 