import logging

from fastapi import HTTPException, Request
from app.helpers.safe_json_response import SafeJSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.constants.messages import get_http_error_code
from app.helpers.slack_webhook_handler import SlackWebhookHelper
from app.schemas.response.errors import ErrorResponse

logger = logging.getLogger()
slack = SlackWebhookHelper()


async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", None)
    logger.exception(exc, extra={"type": "api-error", "request_id": request_id})

    if exc.status_code >= HTTP_500_INTERNAL_SERVER_ERROR:
        slack.notify(
            status_code=exc.status_code,
            message=str(exc.detail),
            level_error="ERROR",
            request=request,
        )

    response = ErrorResponse(
        status_code=exc.status_code,
        message=str(exc.detail),
        error_code=get_http_error_code(exc.status_code),
    )

    return SafeJSONResponse(
        status_code=exc.status_code,
        content=response,
    )
