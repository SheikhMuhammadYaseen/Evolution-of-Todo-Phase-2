"""
Global error handling middleware.
Converts HTTPExceptions to consistent JSON error responses.
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions and return consistent JSON error format.

    Args:
        request: FastAPI request object
        exc: HTTPException instance

    Returns:
        JSONResponse with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": get_error_code(exc.status_code),
                "message": exc.detail,
            }
        },
    )


def get_error_code(status_code: int) -> str:
    """
    Map HTTP status code to error code string.

    Args:
        status_code: HTTP status code

    Returns:
        Error code string
    """
    error_codes = {
        400: "VALIDATION_ERROR",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        500: "INTERNAL_ERROR",
    }
    return error_codes.get(status_code, "UNKNOWN_ERROR")
