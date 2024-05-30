from datetime import datetime, timezone

from piccolo.apps.user.tables import BaseUser
from piccolo.columns import UUID, Boolean, Email, Secret, Timestamptz, Varchar
from piccolo.columns.readable import Readable

from giftbook.db import DB


class User(BaseUser, db=DB, tablename="users"):
    id = UUID(primary_key=True)
    username = Varchar(length=255, required=True, unique=True)
    full_name = Varchar(length=255)
    email = Email(index=True)
    password_hash = Secret(length=128)
    is_email_verified = Boolean(default=False)
    is_admin = Boolean(default=False)
    created_at = Timestamptz(default=datetime.now(timezone.utc))
    modified_at = Timestamptz(auto_update=datetime.now(timezone.utc))

    # overwritten to none
    first_name = None
    last_name = None
    password = None

    @classmethod
    def get_readable(cls) -> Readable:
        return Readable(template="%s (%s)", columns=[cls.username, cls.id])
