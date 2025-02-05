from typing import Iterable

import structlog
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.config import settings
from src.infrastructure.errors import (
    BaseError,
    custom_base_errors_handler,
    pydantic_validation_errors_handler,
    python_base_error_handler,
)
from src.infrastructure.logging import setup_logging, LoggingMiddleware

__all__ = ("create",)


def create(
    *_,
    rest_routers: Iterable[APIRouter],
    **kwargs,
) -> FastAPI:
    app = FastAPI(**kwargs)

    setup_logging(json_logs=settings.logging.format, log_level=settings.logging.level)

    access_logger = structlog.stdlib.get_logger("api.access")
    app.add_middleware(LoggingMiddleware, access_logger=access_logger)  # noqa
    app.add_middleware(CorrelationIdMiddleware)  # noqa

    for router in rest_routers:
        app.include_router(router)

    app.exception_handler(RequestValidationError)(pydantic_validation_errors_handler)
    app.exception_handler(BaseError)(custom_base_errors_handler)
    app.exception_handler(ValidationError)(pydantic_validation_errors_handler)
    app.exception_handler(Exception)(python_base_error_handler)

    return app
