from datetime import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from src.modules.date_tools.schemas import (
    DateAddRequest,
    DateDifferenceRequest,
    DateFormatRequest,
)

PORTUGUESE_MONTHS = {
    "janeiro": "january",
    "fevereiro": "february",
    "março": "march",
    "marco": "march",
    "abril": "april",
    "maio": "may",
    "junho": "june",
    "julho": "july",
    "agosto": "august",
    "setembro": "september",
    "outubro": "october",
    "novembro": "november",
    "dezembro": "december",
}

FORMAT_ALIASES = {
    "br": "%d/%m/%Y",
    "iso": "%Y-%m-%d",
    "datetime-br": "%d/%m/%Y %H:%M:%S",
    "datetime-iso": "%Y-%m-%d %H:%M:%S",
}


def normalize_portuguese_months(value: str) -> str:
    normalized = value.lower()

    for portuguese, english in PORTUGUESE_MONTHS.items():
        normalized = normalized.replace(portuguese, english)

    return normalized


def resolve_output_format(output_format: str) -> str:
    return FORMAT_ALIASES.get(output_format, output_format)


def parse_numeric_date(value: str) -> tuple[datetime, str]:
    if len(value) == 8:
        try:
            return datetime.strptime(value, "%d%m%Y"), "DDMMAAAA"
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Data numérica inválida. Use o formato DDMMAAAA, exemplo: 05021992.",
            )

    if len(value) == 10:
        try:
            return datetime.fromtimestamp(int(value)), "timestamp-segundos"
        except (ValueError, OSError, OverflowError):
            raise HTTPException(status_code=400, detail="Timestamp inválido.")

    if len(value) == 13:
        try:
            return datetime.fromtimestamp(int(value) // 1000), "timestamp-milissegundos"
        except (ValueError, OSError, OverflowError):
            raise HTTPException(status_code=400, detail="Timestamp inválido.")

    raise HTTPException(
        status_code=400,
        detail="Formato numérico inválido. Use DDMMAAAA, timestamp de 10 dígitos ou timestamp de 13 dígitos.",
    )


def parse_date(value: str) -> tuple[datetime, str]:
    cleaned = value.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Informe uma data válida.")

    if cleaned.isdigit():
        return parse_numeric_date(cleaned)

    normalized = normalize_portuguese_months(cleaned)

    known_formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%d.%m.%Y",
    ]

    for date_format in known_formats:
        try:
            return datetime.strptime(cleaned, date_format), date_format
        except ValueError:
            continue

    try:
        parsed = parser.parse(normalized, dayfirst=True, fuzzy=True)
        return parsed, "auto"
    except (ValueError, OverflowError):
        raise HTTPException(
            status_code=400,
            detail="Não foi possível interpretar a data informada.",
        )


def format_human_difference(total_days: int) -> str:
    absolute_days = abs(total_days)
    years = absolute_days // 365
    remaining_days = absolute_days % 365
    months = remaining_days // 30
    days = remaining_days % 30

    parts = []

    if years:
        parts.append(f"{years} ano{'s' if years != 1 else ''}")

    if months:
        parts.append(f"{months} mês{'es' if months != 1 else ''}")

    if days or not parts:
        parts.append(f"{days} dia{'s' if days != 1 else ''}")

    return ", ".join(parts)


def format_date(payload: DateFormatRequest) -> dict:
    date, detected_format = parse_date(payload.value)
    output_format = resolve_output_format(payload.output_format)

    return {
        "original": payload.value,
        "formatted": date.strftime(output_format),
        "iso": date.isoformat(),
        "timestamp": int(date.timestamp()),
        "detected_format": detected_format,
    }


def difference_between_dates(payload: DateDifferenceRequest) -> dict:
    start_date, _ = parse_date(payload.start_date)
    end_date, _ = parse_date(payload.end_date)

    difference = end_date - start_date
    total_seconds = int(difference.total_seconds())
    total_days = difference.days

    return {
        "start_date": start_date.strftime("%d/%m/%Y"),
        "end_date": end_date.strftime("%d/%m/%Y"),
        "total_days": total_days,
        "absolute_days": abs(total_days),
        "total_hours": total_seconds // 3600,
        "total_minutes": total_seconds // 60,
        "total_seconds": total_seconds,
        "human_readable": format_human_difference(total_days),
    }


def add_to_date(payload: DateAddRequest) -> dict:
    date, _ = parse_date(payload.value)
    multiplier = -1 if payload.operation == "subtract" else 1

    result = date + relativedelta(
        days=payload.days * multiplier,
        months=payload.months * multiplier,
        years=payload.years * multiplier,
    )

    output_format = resolve_output_format(payload.output_format)

    return {
        "original": payload.value,
        "result": result.strftime(output_format),
        "iso": result.isoformat(),
        "operation": payload.operation,
        "days": payload.days,
        "months": payload.months,
        "years": payload.years,
    }
