import os

class Settings:
    def __init__(self):
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", default="postgres")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT", default="5432")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="localhost")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")

        self.DATABASE_URL = (
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        self.DB_CONNECT_TIMEOUT = int(os.getenv("DB_CONNECT_TIMEOUT", default="60"))
        self.DB_ASYNC_TIMEOUT = int(os.getenv("DB_ASYNC_TIMEOUT", default="60"))
        self.DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", default="60"))
        self.DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", default="50"))
        self.DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", default="50"))

        self.PROJECT_NAME = os.getenv("PROJECT_NAME")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", default="local")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")

        self.AWS_REGION = os.getenv("AWS_REGION")
        self.S3_BUCKET = os.getenv("S3_BUCKET")
        self.S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "")
        self.S3_USE_SSL = os.getenv("S3_USE_SSL", "false").lower() == "true"
        self.S3_FORCE_PATH_STYLE = os.getenv("S3_FORCE_PATH_STYLE", "true").lower() == "true"
        self.ENV = os.getenv("ENV", default="local")

        # Mail sandbox / SMTP
        self.SMTP_HOST = os.getenv("SMTP_HOST", "mailpit")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
        self.SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
        self.SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "false").lower() == "true"
        self.SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
        self.EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@example.local")

        self.SLACK_HOOK_URL = os.getenv("SLACK_HOOK_URL", default="")
        self.SLACK_TIMEOUT_SECONDS = float(os.getenv("SLACK_TIMEOUT_SECONDS", "5.0"))
        self.SLACK_MAX_RETRIES = max(int(os.getenv("SLACK_MAX_RETRIES", "2")), 0)
        self.SLACK_RETRY_BACKOFF_SECONDS = max(float(os.getenv("SLACK_RETRY_BACKOFF_SECONDS", "0.5")), 0.0)

        # JWT Configuration
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_DAYS", "30"))
        self.JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "60"))
        self.JWT_ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_SECONDS", "1800"))
        self.JWT_REFRESH_TOKEN_EXPIRE_SECONDS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_SECONDS", "2592000"))
        self.AUTH_LOCKOUT_MAX_ATTEMPTS = max(int(os.getenv("AUTH_LOCKOUT_MAX_ATTEMPTS", "5")), 1)
        self.AUTH_LOCKOUT_DURATION_MINUTES = max(int(os.getenv("AUTH_LOCKOUT_DURATION_MINUTES", "30")), 1)

        # Backward compatibility for legacy env name.
        self.TOKEN_SECRET = os.getenv("TOKEN_SECRET", self.JWT_SECRET_KEY)

        # gzip
        self.GZIP_MINIMUM_SIZE = int(os.getenv("GZIP_MINIMUM_SIZE", default="500"))  # bytes

        # Security
        self.ALLOW_ORIGINS = self._parse_csv_env("ALLOW_ORIGINS", "*")
        self.ALLOW_METHODS = self._parse_csv_env("ALLOW_METHODS", "*")
        self.ALLOW_HEADERS = self._parse_csv_env("ALLOW_HEADERS", "*")

    @staticmethod
    def _parse_csv_env(key: str, default: str) -> list[str]:
        return [value.strip("' ") for value in os.environ.get(key, default).split(",")]


settings = Settings()
