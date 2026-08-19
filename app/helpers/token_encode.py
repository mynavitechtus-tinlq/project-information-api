"""JWT token encoding helper utilities."""

from datetime import timedelta
from typing import Any

from jwt import encode

from app.core.configs import settings
from app.core.constants.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH
from app.core.constants.messages import ErrorMessage
from app.helpers.utc_datetime import utc_now_aware

_TOKEN_LIFETIME_SECONDS = {
    TOKEN_TYPE_ACCESS: lambda: settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
    TOKEN_TYPE_REFRESH: lambda: settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
}


def token_encode(payload: dict[str, Any], *, token_type: str = TOKEN_TYPE_ACCESS) -> str:
    """Encode a JWT with `type`, `iat`, and `exp` (seconds-based)."""
    if not payload:
        raise ValueError(ErrorMessage.PAYLOAD_REQUIRED.message)
    if not settings.JWT_SECRET_KEY:
        raise ValueError(ErrorMessage.JWT_SECRET_NOT_CONFIGURED.message)
    if token_type not in _TOKEN_LIFETIME_SECONDS:
        raise ValueError(ErrorMessage.PAYLOAD_REQUIRED.message)

    now = utc_now_aware()
    lifetime_seconds = _TOKEN_LIFETIME_SECONDS[token_type]()
    expires = now + timedelta(seconds=lifetime_seconds)
    token_payload = {
        **payload,
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
        "type": token_type,
    }

    return encode(token_payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
