from enum import Enum


class ErrorMessage(Enum):
    UNKNOWN_ERROR = ("Unknown error", "SYS_01")
    VALIDATION_ERROR = ("Validation error", "ERROR_422")
    AUTHORIZATION_ERROR = ("Authorization failed", "AUTH_01")
    MISSING_CREDENTIALS = ("Missing credentials", "AUTH_02")
    EXPIRED_CREDENTIALS = ("Expired credentials", "AUTH_03")
    INVALID_CREDENTIALS = ("Invalid credentials", "AUTH_04")
    USER_NOT_FOUND = ("User not found", "AUTH_05")
    PAYLOAD_REQUIRED = ("Payload is required", "AUTH_06")
    TOKEN_REQUIRED = ("Token is required", "AUTH_07")
    JWT_SECRET_NOT_CONFIGURED = ("JWT secret key is not configured", "AUTH_08")
    AUTH_SERVICE_UNAVAILABLE = ("Authentication service temporarily unavailable", "AUTH_09")

    @property
    def message(self) -> str:
        return self.value[0]

    @property
    def error_code(self) -> str:
        return self.value[1]


class ValidationMessage(Enum):
    DEFAULT_VALIDATION_ERROR = ("Validation field error", "CODE_BASE_ERROR")
    ERROR_JSON_INVALID = ("Invalid JSON format", "VAL_01")
    INVALID_JSON_IN_REQUEST_BODY = ("Invalid JSON in request body", "VAL_02")
    MISSING_REQUEST_BODY = ("Missing request body", "VAL_03")
    FIELD_REQUIRED = ("This field is required", "ERR_01")
    # Example placeholders for future keys:
    # FIELD_INVALID = ("This field is invalid", "ERR_02")
    # FIELD_NOT_FOUND = ("This field is not found", "ERR_03")
    # FIELD_NOT_ALLOWED = ("This field is not allowed", "ERR_04")

    @property
    def message(self) -> str:
        return self.value[0]

    @property
    def error_code(self) -> str:
        return self.value[1]


class LogMessage(Enum):
    NO_REQUEST = ("No Request", "LOG_01")
    USER_NOT_FOUND_FOR_TOKEN_SUBJECT = ("User not found for token subject", "LOG_02")

    @property
    def message(self) -> str:
        return self.value[0]

    @property
    def error_code(self) -> str:
        return self.value[1]


class HttpErrorCode(str, Enum):
    BAD_REQUEST = "ERROR_400"
    UNAUTHORIZED = "ERROR_401"
    FORBIDDEN = "ERROR_403"
    NOT_FOUND = "ERROR_404"
    METHOD_NOT_ALLOWED = "ERROR_405"
    UNPROCESSABLE_ENTITY = "ERROR_422"
    INTERNAL_SERVER_ERROR = "ERROR_500"


def get_http_error_code(status_code: int) -> str:
    mapping = {
        400: HttpErrorCode.BAD_REQUEST.value,
        401: HttpErrorCode.UNAUTHORIZED.value,
        403: HttpErrorCode.FORBIDDEN.value,
        404: HttpErrorCode.NOT_FOUND.value,
        405: HttpErrorCode.METHOD_NOT_ALLOWED.value,
        422: HttpErrorCode.UNPROCESSABLE_ENTITY.value,
        500: HttpErrorCode.INTERNAL_SERVER_ERROR.value,
    }
    return mapping.get(status_code, f"ERROR_{status_code}")


# Backward-compatible aliases for old names.
ErrorMessages = ErrorMessage
ValidateMessage = ValidationMessage
MessageValidation = ValidationMessage
