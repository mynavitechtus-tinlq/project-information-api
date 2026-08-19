from http import HTTPStatus

from fastapi import Request, status
from app.helpers.safe_json_response import SafeJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.constants.messages import get_http_error_code
from app.schemas.response.errors import ErrorResponse


class CustomErrorMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED]:
            status_code = response.status_code
            payload = ErrorResponse(
                status_code=status_code,
                message=HTTPStatus(status_code).phrase,
                error_code=get_http_error_code(status_code),
            )

            return SafeJSONResponse(status_code=status_code, content=payload)

        return response
