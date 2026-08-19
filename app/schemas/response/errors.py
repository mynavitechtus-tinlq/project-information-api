from typing import List

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: int
    error_code: str
    message: str


class ErrorDetail(BaseModel):
    error_code: str
    field: str
    message: str


class ValidationErrorResponse(ErrorResponse):
    errors: List[ErrorDetail]
