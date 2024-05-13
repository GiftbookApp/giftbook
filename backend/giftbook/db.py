import itertools
from urllib.parse import unquote, unquote_plus, urlparse

from piccolo.engine.base import Engine
from piccolo.engine.postgres import PostgresEngine

from giftbook.config import DATABASE_URL


def _parse_postgres_url(db_url: str) -> dict[str, str | None]:
    url = urlparse(db_url)
    path = unquote_plus(url.path[1:].split("?", 2)[0])
    user_host = url.netloc.rsplit("@", 1)

    if "," in user_host[-1]:  # cluster
        hinfo = list(itertools.zip_longest(*(host.rsplit(":", 1) for host in user_host[-1].split(","))))
        hostname = ",".join(hinfo[0])
        port = ",".join(filter(None, hinfo[1])) if len(hinfo) == 2 else ""
    else:  # single db
        hostname = url.hostname
        port = url.port

    if path.startswith("/"):
        hostname, path = path.rsplit("/", 1)

    return {
        "host": hostname,
        "port": port,
        "user": unquote(url.username) if isinstance(url.username, str) else url.username,
        "password": unquote(url.password) if isinstance(url.password, str) else url.password,
        "database": path,
    }


DB: Engine = PostgresEngine(config=_parse_postgres_url(DATABASE_URL))


async def start_connection_pool():
    await DB.start_connection_pool()


async def close_connection_pool():
    await DB.close_connection_pool()
