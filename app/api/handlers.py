import logging

from cleanstack.exceptions import DomainError, NotFoundError
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from app.domain.exceptions import UnprocessableContentError

logger = logging.getLogger(__name__)


def add_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def app_exception_handler(request: Request, error: DomainError) -> Response:
        if isinstance(error, NotFoundError):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": str(error)},
            )
        if isinstance(error, UnprocessableContentError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": str(error)},
            )

        logger.error("Unhandled DomainError", exc_info=True)
        return PlainTextResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )
