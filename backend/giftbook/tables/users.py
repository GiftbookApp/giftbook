from datetime import datetime, timezone

from piccolo.columns import UUID, Boolean, Email, Secret, Timestamptz, Varchar
from piccolo.columns.readable import Readable
from piccolo.table import Table

from giftbook.db import DB


class User(Table, db=DB, tablename="users"):
    id = UUID(primary_key=True)
    username = Varchar(length=255, required=True, unique=True)
    password_hash = Secret(length=128)
    email = Email(index=True)
    is_email_verified = Boolean(default=False)
    full_name = Varchar(length=255)
    is_admin = Boolean(default=False)
    created_at = Timestamptz(default=datetime.now(timezone.utc))
    modified_at = Timestamptz(auto_update=datetime.now(timezone.utc))

    @classmethod
    def get_readable(cls) -> Readable:
        return Readable(template="%s (%s)", columns=[cls.username, cls.id])
