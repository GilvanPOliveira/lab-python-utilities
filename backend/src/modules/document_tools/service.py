import re

from src.modules.document_tools.schemas import DocumentRequest


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def validate_cpf_number(cpf: str) -> bool:
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    total = sum(int(cpf[index]) * (10 - index) for index in range(9))
    first_digit = 11 - (total % 11)
    first_digit = 0 if first_digit >= 10 else first_digit

    total = sum(int(cpf[index]) * (11 - index) for index in range(10))
    second_digit = 11 - (total % 11)
    second_digit = 0 if second_digit >= 10 else second_digit

    return cpf[-2:] == f"{first_digit}{second_digit}"


def validate_cnpj_number(cnpj: str) -> bool:
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_weights = [6] + first_weights

    total = sum(int(cnpj[index]) * first_weights[index] for index in range(12))
    first_digit = 11 - (total % 11)
    first_digit = 0 if first_digit >= 10 else first_digit

    total = sum(int(cnpj[index]) * second_weights[index] for index in range(13))
    second_digit = 11 - (total % 11)
    second_digit = 0 if second_digit >= 10 else second_digit

    return cnpj[-2:] == f"{first_digit}{second_digit}"


def format_cpf_value(cpf: str) -> str | None:
    if len(cpf) != 11:
        return None

    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def format_cnpj_value(cnpj: str) -> str | None:
    if len(cnpj) != 14:
        return None

    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def validate_cpf(payload: DocumentRequest) -> dict:
    digits = only_digits(payload.value)

    return {
        "valid": validate_cpf_number(digits),
        "value": payload.value,
        "formatted": format_cpf_value(digits),
        "digits": digits,
    }


def validate_cnpj(payload: DocumentRequest) -> dict:
    digits = only_digits(payload.value)

    return {
        "valid": validate_cnpj_number(digits),
        "value": payload.value,
        "formatted": format_cnpj_value(digits),
        "digits": digits,
    }
