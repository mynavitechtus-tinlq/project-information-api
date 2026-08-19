from datetime import datetime

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime = Field(description="Access token expiry (UTC, ISO 8601 with offset)")
    refresh_expires_at: datetime = Field(description="Refresh token expiry (UTC, ISO 8601 with offset)")


class LoginResponse(BaseModel):
    status_code: int = 200
    data: LoginData


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=1)
