from litestar import Litestar, MediaType, Request, Response, status_codes
from litestar.config.allowed_hosts import AllowedHostsConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.openapi import OpenAPIConfig
from litestar_granian import GranianPlugin

from giftbook.api import api
from giftbook.config import (
    ALLOWED_HOSTS,
    CACHE_DEFAULT_EXPIRE,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_ORIGINS,
    CSRF_COOKIE_DOMAIN,
    CSRF_COOKIE_HTTPONLY,
    CSRF_COOKIE_NAME,
    CSRF_COOKIE_SAMESITE,
    CSRF_COOKIE_SECURE,
    CSRF_HEADER_NAME,
    CSRF_SECRET,
    RATE_LIMIT_ENABLED,
    RATE_LIMIT_MAX_REQUESTS_PER_SECOND,
    REDIS_URL,
    SESSION_COOKIE_DOMAIN,
    SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_MAX_AGE_SECONDS,
    SESSION_COOKIE_NAME,
    SESSION_COOKIE_SAMESITE,
    SESSION_COOKIE_SECURE,
)
from giftbook.db import close_connection_pool, start_connection_pool
from giftbook.stores import setup_registry_stores


def report_all_errors(request: Request, exc: Exception) -> Response:
    """Default handler for all exceptions."""
    return Response(
        media_type=MediaType.JSON,
        content={"detail": getattr(exc, "detail", str(exc))},
        status_code=getattr(exc, "status_code", status_codes.HTTP_500_INTERNAL_SERVER_ERROR),
    )


def create_app() -> Litestar:
    middleware = [
        ServerSideSessionConfig(
            key=SESSION_COOKIE_NAME,
            max_age=SESSION_COOKIE_MAX_AGE_SECONDS,
            domain=SESSION_COOKIE_DOMAIN,
            secure=SESSION_COOKIE_SECURE,
            httponly=SESSION_COOKIE_HTTPONLY,
            samesite=SESSION_COOKIE_SAMESITE,
        ).middleware,
    ]

    if RATE_LIMIT_ENABLED:
        middleware.append(
            RateLimitConfig(rate_limit=("second", RATE_LIMIT_MAX_REQUESTS_PER_SECOND), store="ratelimit").middleware
        )

    on_startup = [start_connection_pool]
    on_shutdown = [close_connection_pool]

    return Litestar(
        route_handlers=[api],
        openapi_config=OpenAPIConfig(title="Giftbook API", version="0.1.0"),
        exception_handlers={Exception: report_all_errors},
        stores=setup_registry_stores(redis_url=REDIS_URL, ratelimit_enabled=RATE_LIMIT_ENABLED),
        allowed_hosts=AllowedHostsConfig(allowed_hosts=ALLOWED_HOSTS),
        cors_config=CORSConfig(allowed_origins=CORS_ALLOW_ORIGINS, allow_credentials=CORS_ALLOW_CREDENTIALS),
        csrf_config=CSRFConfig(
            secret=CSRF_SECRET,
            cookie_name=CSRF_COOKIE_NAME,
            cookie_domain=CSRF_COOKIE_DOMAIN,
            cookie_httponly=CSRF_COOKIE_HTTPONLY,
            cookie_samesite=CSRF_COOKIE_SAMESITE,
            cookie_secure=CSRF_COOKIE_SECURE,
            header_name=CSRF_HEADER_NAME,
        ),
        response_cache_config=ResponseCacheConfig(store="responses", default_expiration=CACHE_DEFAULT_EXPIRE),
        middleware=middleware,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        plugins=(GranianPlugin(),),
    )
