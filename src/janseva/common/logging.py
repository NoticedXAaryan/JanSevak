"""Structured logging configuration using structlog."""
import logging
import structlog

from janseva.config import settings


def setup_logging() -> None:
    """Configure structured JSON logging for the entire application."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            # In dev: pretty console output. In prod: JSON.
            structlog.dev.ConsoleRenderer()
            if settings.env == "development"
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
