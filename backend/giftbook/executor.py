from concurrent.futures import ThreadPoolExecutor

from litestar import Litestar
from litestar.concurrency import get_asyncio_executor, set_asyncio_executor


def start_executor(app: Litestar) -> None:
    tpe = ThreadPoolExecutor(thread_name_prefix="giftbook-executor-")
    set_asyncio_executor(tpe)


def stop_executor(app: Litestar) -> None:
    tpe = get_asyncio_executor()
    tpe.shutdown()
