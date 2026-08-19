import logging
from http import HTTPStatus

from fastapi import Request
from app.helpers.safe_json_response import SafeJSONResponse
from starlette import status

from app.core.constants.messages import get_http_error_code
from app.helpers.slack_webhook_handler import SlackWebhookHelper
from app.schemas.response.errors import ErrorResponse

logger = logging.getLogger()
slack = SlackWebhookHelper()


async def exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    logger.exception(exc, extra={"type": "app-error", "request_id": request_id})

    message_error_500 = HTTPStatus(status.HTTP_500_INTERNAL_SERVER_ERROR).phrase
    message_error = exc if exc else message_error_500

    slack.notify(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(message_error),
        level_error="ERROR",
        request=request,
    )

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=message_error_500,
        error_code=get_http_error_code(status.HTTP_500_INTERNAL_SERVER_ERROR),
    )

    return SafeJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)
