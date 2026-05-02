import secrets
import string

from fastapi import HTTPException

from src.modules.password_tools.schemas import PasswordRequest


def generate_password(payload: PasswordRequest) -> dict[str, str | int]:
    chars = ""

    if payload.include_uppercase:
        chars += string.ascii_uppercase

    if payload.include_lowercase:
        chars += string.ascii_lowercase

    if payload.include_numbers:
        chars += string.digits

    if payload.include_symbols:
        chars += "!@#$%&*()-_=+[]{};:,.?/"

    if not chars:
        raise HTTPException(
            status_code=400,
            detail="Selecione pelo menos um tipo de caractere.",
        )

    password = "".join(secrets.choice(chars) for _ in range(payload.length))

    return {
        "password": password,
        "length": payload.length,
    }
