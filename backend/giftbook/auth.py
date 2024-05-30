from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# TODO?: maybe hash and verify password in an executor?


def hash_password(password: str) -> str:
    return PasswordHasher().hash(password)


def verify_password(password: str | bytes, password_hash: str | bytes) -> bool:
    try:
        return PasswordHasher().verify(password_hash, password)
    except VerifyMismatchError:
        return False
