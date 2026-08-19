import pytest

from app.helpers.password_hash import hash_password, verify_password

pytestmark = pytest.mark.unit


def test_hash_password_produces_verifiable_string():
    hashed = hash_password("my-secret-password")
    assert isinstance(hashed, str)
    assert hashed != "my-secret-password"
    assert verify_password("my-secret-password", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("correct")
    assert verify_password("wrong", hashed) is False


def test_verify_password_returns_false_on_invalid_hash():
    assert verify_password("password", "not-a-valid-bcrypt-hash") is False
