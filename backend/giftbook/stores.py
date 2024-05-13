from litestar.stores.base import Store
from litestar.stores.registry import StoreRegistry

REDIS_STORE_PREFIX = "giftbook"
ROOT_STORE_NAME = "root"
SESSIONS_STORE_NAME = "sessions"
RESPONSES_STORE_NAME = "responses"
OTP_STORE_NAME = "otp"
RATELIMIT_STORE_NAME = "ratelimit"

registry = StoreRegistry()


def setup_registry_stores(redis_url: str | None, ratelimit_enabled: bool = False) -> StoreRegistry:
    stores = {}
    if redis_url:
        from litestar.stores.redis import RedisStore

        root_store = RedisStore.with_client(redis_url, prefix=REDIS_STORE_PREFIX)
        stores.update(
            {
                ROOT_STORE_NAME: root_store,
                SESSIONS_STORE_NAME: root_store.with_namespace(SESSIONS_STORE_NAME),
                RESPONSES_STORE_NAME: root_store.with_namespace(RESPONSES_STORE_NAME),
                OTP_STORE_NAME: root_store.with_namespace(OTP_STORE_NAME),
            }
        )
        if ratelimit_enabled:
            stores[RATELIMIT_STORE_NAME] = root_store.with_namespace(RATELIMIT_STORE_NAME)
    else:
        from litestar.stores.memory import MemoryStore

        stores.update(
            {
                ROOT_STORE_NAME: MemoryStore(),
                SESSIONS_STORE_NAME: MemoryStore(),
                RESPONSES_STORE_NAME: MemoryStore(),
                OTP_STORE_NAME: MemoryStore(),
            }
        )
        if ratelimit_enabled:
            stores[RATELIMIT_STORE_NAME] = MemoryStore()

    for name, store in stores.items():
        registry.register(name, store)

    return registry


def get_root_store() -> Store:
    return registry.get(ROOT_STORE_NAME)


def get_session_store() -> Store:
    return registry.get(SESSIONS_STORE_NAME)


def get_response_store() -> Store:
    return registry.get(RESPONSES_STORE_NAME)


def get_otp_store() -> Store:
    return registry.get(OTP_STORE_NAME)


def get_ratelimit_store() -> Store | None:
    return registry.get(RATELIMIT_STORE_NAME) if RATELIMIT_STORE_NAME in registry._stores else None
