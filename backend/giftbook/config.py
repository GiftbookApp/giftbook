import logging
from pathlib import Path

from environs import Env

APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
PROJECT_DIR = BACKEND_DIR.parent
SUPPORTED_DATABASES = ("postgres", "postgresql", "psql", "pgsql", "postgis")

env = Env()


def get_secret(name: str, default: object = None) -> str:
    if value := env.str(name, None):
        logging.warning(f"{name} is set in the environment. Consider using a file secret.")
        return value

    if value := env.str(f"{name}_FILE", None):
        fp = Path(value)
        if not fp.is_file():
            raise FileNotFoundError(f"File not found: {fp}.")
        return fp.read_text()

    if default:
        return default

    raise ValueError(f"Secret {name} not found in environment or file.")


# optionally load .env file
if env.bool("GIFTBOOK_READ_DOT_ENV_FILE", default=False):
    DOT_ENV_FILE_PATH: str = env.str("GIFTBOOK_DOT_ENV_FILE_PATH", default=BACKEND_DIR / ".env")
    env.read_env(DOT_ENV_FILE_PATH)

# CACHE
REDIS_URL: str | None = env.str("GIFTBOOK_REDIS_URL", default=None)
CACHE_DEFAULT_EXPIRE: int = env.int("GIFTBOOK_CACHE_DEFAULT_EXPIRE", default=60)

# CORS
CORS_ALLOW_ORIGINS: list[str] = env.list("GIFTBOOK_CORS_ALLOW_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS: bool = env.bool("GIFTBOOK_CORS_ALLOW_CREDENTIALS", default=False)

# CSRF
CSRF_SECRET: str = get_secret("GIFTBOOK_CSRF_SECRET")
CSRF_COOKIE_SECURE: bool = env.bool("GIFTBOOK_CSRF_COOKIE_SECURE", default=False)
CSRF_COOKIE_NAME: str = env.str("GIFTBOOK_CSRF_COOKIE_NAME", default="csrftoken")
CSRF_COOKIE_HTTPONLY: bool = env.bool("GIFTBOOK_CSRF_COOKIE_HTTPONLY", default=True)
CSRF_COOKIE_SAMESITE: str = env.str("GIFTBOOK_CSRF_COOKIE_SAMESITE", default="lax")
CSRF_COOKIE_DOMAIN: str | None = env.str("GIFTBOOK_CSRF_COOKIE_DOMAIN", default=None)
CSRF_HEADER_NAME: str = env.str("GIFTBOOK_CSRF_HEADER_NAME", default="x-csrftoken")

# RATE LIMIT
RATE_LIMIT_ENABLED: bool = env.bool("GIFTBOOK_RATE_LIMIT_ENABLED", default=True)
RATE_LIMIT_MAX_REQUESTS_PER_SECOND: int = env.int("GIFTBOOK_RATE_LIMIT_MAX_REQUESTS_PER_SECOND", default=10)

# SESSIONS
SESSION_COOKIE_NAME: str = env.str("GIFTBOOK_SESSION_COOKIE_NAME", default="session")
SESSION_COOKIE_MAX_AGE_SECONDS: int = env.int("GIFTBOOK_SESSION_COOKIE_MAX_AGE_SECONDS", default=60 * 60 * 24 * 14)
SESSION_COOKIE_DOMAIN: str = env.str("GIFTBOOK_SESSION_COOKIE_DOMAIN", default=None)
SESSION_COOKIE_SECURE: bool = env.bool("GIFTBOOK_SESSION_COOKIE_SECURE", default=False)
SESSION_COOKIE_HTTPONLY: bool = env.bool("GIFTBOOK_SESSION_COOKIE_HTTPONLY", default=True)
SESSION_COOKIE_SAMESITE: int = env.str("GIFTBOOK_SESSION_COOKIE_SAMESITE", default="lax")

# USERNAME GENERATION
RANDOM_USERNAME_SUFFIX_LENGTH: int = env.int("GIFTBOOK_RANDOM_USERNAME_SUFFIX_LENGTH", default=6)
RANDOM_USERNAME_GENERATOR_RETRIES: int = env.int("GIFTBOOK_RANDOM_USERNAME_GENERATOR_RETRIES", default=5)

# OTP
EMAIL_OTP_LENGTH: int = env.int("GIFTBOOK_EMAIL_OTP_LENGTH", default=8)
EMAIL_OTP_EXPIRES_IN_SECONDS: int = env.int("GIFTBOOK_EMAIL_OTP_EXPIRES_IN_SECONDS", default=60 * 15)

# DATABASE
DATABASE_URL: str = env.str("GIFTBOOK_DATABASE_URL")

# postgres-only check
if all(not DATABASE_URL.lower().startswith(db) for db in SUPPORTED_DATABASES):
    raise ValueError(f"Unsupported database: {DATABASE_URL}. Supported databases: {SUPPORTED_DATABASES}.")
