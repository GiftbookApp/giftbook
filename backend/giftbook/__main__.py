from importlib import import_module

from giftbook.config import (
    ASGI_HOST,
    ASGI_PORT,
    ASGI_THREADING_MODE,
    ASGI_THREADS,
    ASGI_WORKERS,
)
from granian import Granian
from granian.constants import Interfaces
from litestar import Litestar


def app_loader(target: str) -> Litestar:
    module_name, app_factory_name = target.split(":")
    module = import_module(module_name)
    app_factory = getattr(module, app_factory_name)
    return app_factory()


if __name__ == "__main__":
    Granian(
        target="giftbook.app:create_app",
        address=ASGI_HOST,
        port=ASGI_PORT,
        interface=Interfaces.ASGI,
        workers=ASGI_WORKERS,
        threads=ASGI_THREADS,
        threading_mode=ASGI_THREADING_MODE,
        reload=True,
    ).serve(target_loader=app_loader)
