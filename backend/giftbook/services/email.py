from itertools import batched

import httpx

from giftbook.config import EMAIL_API_KEY, EMAIL_API_SEND_EMAIL_URL, EMAIL_FROM_DEFAULT, EMAIL_TO_MAX_SIZE


async def send_email(
    email_to: str, subject: str, text_body: str, html_body: str | None = None, email_from: str = EMAIL_FROM_DEFAULT
) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            EMAIL_API_SEND_EMAIL_URL,
            json={
                "api_key": EMAIL_API_KEY,
                "to": [email_to],
                "sender": email_from,
                "subject": subject,
                "text_body": text_body,
                "html_body": html_body or text_body,
            },
        )

    response.raise_for_status()


async def send_email_batch(email_to: list[str], subject: str, body: str, email_from: str = EMAIL_FROM_DEFAULT) -> None:
    async with httpx.AsyncClient() as client:
        for batch in batched(email_to, EMAIL_TO_MAX_SIZE):
            response = await client.post(
                EMAIL_API_SEND_EMAIL_URL,
                json={
                    "api_key": EMAIL_API_KEY,
                    "to": batch,
                    "sender": email_from,
                    "subject": subject,
                    "text_body": body,
                    "html_body": body,
                },
            )
            response.raise_for_status()
