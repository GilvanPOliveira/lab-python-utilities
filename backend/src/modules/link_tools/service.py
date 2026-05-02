from urllib.parse import parse_qsl, quote, unquote, urlencode, urlparse, urlunparse

import httpx
from fastapi import HTTPException

TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "utm_id",
    "fbclid",
    "gclid",
    "msclkid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "ref",
    "ref_src",
}

IS_GD_CREATE_URL = "https://is.gd/create.php"


def normalize_url(url: str) -> str:
    cleaned = url.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Informe uma URL válida.")

    if not cleaned.startswith(("http://", "https://")):
        cleaned = f"https://{cleaned}"

    return cleaned


def parse_valid_url(url: str):
    normalized = normalize_url(url)
    parsed = urlparse(normalized)

    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="URL inválida.")

    return normalized, parsed


def clean_url(url: str) -> dict:
    normalized, parsed = parse_valid_url(url)

    query_params = parse_qsl(parsed.query, keep_blank_values=True)
    kept_params = []
    removed_params = []

    for key, value in query_params:
        if key.lower() in TRACKING_PARAMS:
            removed_params.append(key)
        else:
            kept_params.append((key, value))

    cleaned_query = urlencode(kept_params, doseq=True)

    cleaned_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            cleaned_query,
            "",
        )
    )

    return {
        "original_url": normalized,
        "cleaned_url": cleaned_url,
        "removed_params": removed_params,
        "domain": parsed.netloc,
        "is_valid": True,
    }


def encode_url_value(value: str) -> dict:
    return {
        "original": value,
        "encoded": quote(value, safe=""),
    }


def decode_url_value(value: str) -> dict:
    return {
        "original": value,
        "decoded": unquote(value),
    }


async def shorten_url(url: str, custom_code: str | None = None) -> dict:
    normalized, _ = parse_valid_url(url)

    params = {
        "format": "json",
        "url": normalized,
    }

    if custom_code:
        params["shorturl"] = custom_code.strip()

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(IS_GD_CREATE_URL, params=params)
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível conectar ao serviço de encurtamento.",
        )

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Resposta inválida do serviço de encurtamento.",
        )

    if response.status_code >= 400 or "errormessage" in data:
        message = data.get("errormessage") or "Não foi possível encurtar a URL."
        raise HTTPException(status_code=400, detail=message)

    short_url = data.get("shorturl")

    if not short_url:
        raise HTTPException(
            status_code=502,
            detail="O serviço de encurtamento não retornou uma URL curta.",
        )

    return {
        "original_url": normalized,
        "short_url": short_url,
        "provider": "is.gd",
    }
