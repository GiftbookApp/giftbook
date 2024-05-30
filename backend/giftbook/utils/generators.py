import string
from random import choice

DERFAULT_STRING_CHARACTERS = string.ascii_letters + string.digits


def generate_string(length: int, characters: str = DERFAULT_STRING_CHARACTERS) -> str:
    return "".join(choice(characters) for _ in range(length))
