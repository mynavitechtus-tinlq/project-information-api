from typing import Dict

from jwt import decode

from app.core.configs import settings
from app.core.constants.messages import ErrorMessage


def token_decode(token: str) -> Dict:
    """Decode a JWT token from the given token string."""
    if not token:
        raise ValueError(ErrorMessage.TOKEN_REQUIRED.message)
    if not settings.JWT_SECRET_KEY:
        raise ValueError(ErrorMessage.JWT_SECRET_NOT_CONFIGURED.message)

    return decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
