from giftbook.auth import hash_password
from giftbook.config import (
    EMAIL_OTP_EXPIRES_IN_SECONDS,
    EMAIL_OTP_LENGTH,
    RANDOM_USERNAME_GENERATOR_RETRIES,
    RANDOM_USERNAME_SUFFIX_LENGTH,
)
from giftbook.services.email import send_email
from giftbook.stores import get_otp_store
from giftbook.tables.users import User
from giftbook.utils.generators import generate_string


async def _make_username(full_name: str | None = None) -> str:
    full_name = full_name.lower().replace(" ", "-") if full_name else "user"
    for _ in range(RANDOM_USERNAME_GENERATOR_RETRIES):
        username = f"{full_name}-{generate_string(length=RANDOM_USERNAME_SUFFIX_LENGTH)}"
        if not await User.exists().where(User.username == username):
            return username

    # FIXME: use a custom exception
    raise ValueError(f"Cannot generate username after {RANDOM_USERNAME_GENERATOR_RETRIES} retries.")


async def create_user(
    *,
    email: str | None = None,
    username: str | None = None,
    password: str | None = None,
    full_name: str | None = None,
) -> User:
    user = User(
        username=username or await _make_username(full_name),
        email=email,
        password_hash=hash_password(password) if password else None,
        full_name=full_name,
    )
    await user.save()
    store = get_otp_store()
    otp = generate_string(length=EMAIL_OTP_LENGTH)
    await store.set(user.id, otp, expires_in=EMAIL_OTP_EXPIRES_IN_SECONDS)
    await send_email(email_to=user.email, subject="Verify your email", text_body=f"Your OTP is: {otp}")
    return user


async def verify_user_email(user_id: str, code: str) -> User:
    store = get_otp_store()
    if stored_code := await store.get(user_id):
        if stored_code == code:
            user = (
                await User.update({User.is_email_verified: True})
                .where(User.id == user_id)
                .returning(*User.all_columns())
            )
            await store.delete(user_id)
            return user

        raise ValueError("Invalid OTP.")  # FIXME: use a custom exception
    raise ValueError("No OTP found for user.")  # FIXME: use a custom exception
