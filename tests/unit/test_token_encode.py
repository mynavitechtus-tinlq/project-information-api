import pytest
from jwt import decode

from app.core.configs import settings
from app.core.constants.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH
from app.core.constants.messages import ErrorMessage
from app.helpers.token_encode import token_encode

pytestmark = pytest.mark.unit


@pytest.fixture
def jwt_secret(monkeypatch):
    monkeypatch.setattr(settings, "JWT_SECRET_KEY", "unit-test-secret-key", raising=False)
    monkeypatch.setattr(settings, "JWT_ALGORITHM", "HS256", raising=False)
    monkeypatch.setattr(settings, "JWT_ACCESS_TOKEN_EXPIRE_SECONDS", 1800, raising=False)
    monkeypatch.setattr(settings, "JWT_REFRESH_TOKEN_EXPIRE_SECONDS", 2592000, raising=False)


def test_token_encode_rejects_empty_payload(jwt_secret):
    with pytest.raises(ValueError, match=ErrorMessage.PAYLOAD_REQUIRED.message):
        token_encode({})


def test_token_encode_rejects_missing_secret(monkeypatch):
    monkeypatch.setattr(settings, "JWT_SECRET_KEY", "", raising=False)
    with pytest.raises(ValueError, match=ErrorMessage.JWT_SECRET_NOT_CONFIGURED.message):
        token_encode({"user_id": "x"}, token_type=TOKEN_TYPE_ACCESS)


def test_token_encode_access_includes_type_and_exp(jwt_secret):
    token = token_encode({"user_id": "550e8400-e29b-41d4-a716-446655440000"}, token_type=TOKEN_TYPE_ACCESS)
    payload = decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    assert payload["type"] == TOKEN_TYPE_ACCESS
    assert payload["user_id"] == "550e8400-e29b-41d4-a716-446655440000"
    assert "exp" in payload and "iat" in payload


def test_token_encode_refresh_uses_refresh_type(jwt_secret):
    token = token_encode({"user_id": "550e8400-e29b-41d4-a716-446655440000"}, token_type=TOKEN_TYPE_REFRESH)
    payload = decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    assert payload["type"] == TOKEN_TYPE_REFRESH
