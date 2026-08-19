import logging
from typing import Any, Dict, List, Union

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from app.helpers.safe_json_response import SafeJSONResponse
from pydantic_core import ValidationError
from starlette import status

from app.core.constants.messages import ErrorMessage, ValidationMessage
from app.helpers.slack_webhook_handler import SlackWebhookHelper
from app.schemas.response.errors import ErrorDetail, ValidationErrorResponse

logger = logging.getLogger()
slack = SlackWebhookHelper()


def parse_error_detail(error: Dict[str, Any]) -> ErrorDetail:
    # Parse error detail from the exception
    ctx = error.get("ctx", {})
    error_detail = ctx.get("error")
    error_type = error.get("type")
    loc = error.get("loc")

    error_field = loc[0] if isinstance(loc, (tuple, list)) and len(loc) > 0 else ""
    error_code = ValidationMessage.DEFAULT_VALIDATION_ERROR.error_code

    if error_type == "value_error" and isinstance(error_detail, ValueError):
        message = error_detail.args[0] if len(error_detail.args) > 0 else ErrorMessage.UNKNOWN_ERROR.message
        field = error_detail.args[1].get("field", "") if len(error_detail.args) > 1 else ""

    elif error_type == "json_invalid" and error_field == "body":
        message = ValidationMessage.INVALID_JSON_IN_REQUEST_BODY.message
        field = error_field

    elif error_type == "missing" and error_field == "body":
        message = ValidationMessage.MISSING_REQUEST_BODY.message
        field = error_field

    else:
        message = error["msg"]
        field = error_field

    return ErrorDetail(
        message=str(message),
        error_code=str(error_code),
        field=str(field),
    )


def extract_errors(exc: Union[RequestValidationError, ValidationError]) -> List[ErrorDetail]:
    # Extract and parse errors from the exception
    return [parse_error_detail(error) for error in exc.errors()]


async def validation_exception_handler(_request: Request, exc: Union[RequestValidationError, ValidationError]):
    request_id = getattr(_request.state, "request_id", None)
    logger.exception(exc, extra={"type": "api-error", "request_id": request_id})

    errors = extract_errors(exc)

    response = ValidationErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=ErrorMessage.VALIDATION_ERROR.message,
        error_code=ErrorMessage.VALIDATION_ERROR.error_code,
        errors=errors,
    )

    return SafeJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response,
    )
