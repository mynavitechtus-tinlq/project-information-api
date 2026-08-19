from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic_core import ValidationError

from app.api import routes
from app.core.configs import settings
from app.exceptions.exception_handler import exception_handler
from app.exceptions.http_exception_handler import http_exception_handler
from app.exceptions.validation_exception_handler import validation_exception_handler
from app.middlewares.custom_error_middleware import CustomErrorMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.schemas.response.errors import ErrorResponse, ValidationErrorResponse

load_dotenv(dotenv_path="/app/.env")

app = FastAPI()


app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)

app.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MINIMUM_SIZE)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CustomErrorMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(
    routes,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
