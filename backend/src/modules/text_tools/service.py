import re

from src.modules.text_tools.schemas import TextConvertRequest, TextRequest


def clean_text(payload: TextRequest) -> dict[str, str]:
    cleaned = re.sub(r"[ \t]+", " ", payload.value)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()

    return {
        "original": payload.value,
        "cleaned": cleaned,
    }


def convert_text(payload: TextConvertRequest) -> dict[str, str]:
    modes = {
        "upper": payload.value.upper(),
        "lower": payload.value.lower(),
        "title": payload.value.title(),
        "capitalize": payload.value.capitalize(),
    }

    return {
        "original": payload.value,
        "converted": modes[payload.mode],
        "mode": payload.mode,
    }


def count_text(payload: TextRequest) -> dict[str, int]:
    words = re.findall(r"\b\w+\b", payload.value, flags=re.UNICODE)

    return {
        "characters": len(payload.value),
        "characters_without_spaces": len(payload.value.replace(" ", "")),
        "words": len(words),
        "lines": len(payload.value.splitlines()) or 1,
    }
