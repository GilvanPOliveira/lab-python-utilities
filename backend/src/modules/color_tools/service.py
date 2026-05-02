import colorsys
import re

from fastapi import HTTPException


HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def normalize_hex(hex_color: str) -> str:
    value = hex_color.strip()

    match = HEX_PATTERN.match(value)

    if not match:
        raise HTTPException(status_code=400, detail="Informe uma cor HEX válida.")

    hex_value = match.group(1)

    if len(hex_value) == 3:
        hex_value = "".join(char * 2 for char in hex_value)

    return f"#{hex_value.upper()}"


def hex_to_rgb_values(hex_color: str) -> tuple[int, int, int]:
    normalized = normalize_hex(hex_color).replace("#", "")

    r = int(normalized[0:2], 16)
    g = int(normalized[2:4], 16)
    b = int(normalized[4:6], 16)

    return r, g, b


def rgb_to_hex_value(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl_values(r: int, g: int, b: int) -> tuple[float, float, float]:
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    return round(h * 360, 2), round(s * 100, 2), round(l * 100, 2)


def hsl_to_rgb_values(h: float, s: float, l: float) -> tuple[int, int, int]:
    normalized_h = h / 360
    normalized_s = s / 100
    normalized_l = l / 100

    r, g, b = colorsys.hls_to_rgb(normalized_h, normalized_l, normalized_s)

    return round(r * 255), round(g * 255), round(b * 255)


def build_color_response_from_rgb(r: int, g: int, b: int) -> dict:
    h, s, l = rgb_to_hsl_values(r, g, b)
    hex_value = rgb_to_hex_value(r, g, b)

    return {
        "hex": hex_value,
        "rgb": f"rgb({r}, {g}, {b})",
        "hsl": f"hsl({h}, {s}%, {l}%)",
        "r": r,
        "g": g,
        "b": b,
        "h": h,
        "s": s,
        "l": l,
    }


def convert_hex_color(hex_color: str) -> dict:
    r, g, b = hex_to_rgb_values(hex_color)
    return build_color_response_from_rgb(r, g, b)


def convert_rgb_color(r: int, g: int, b: int) -> dict:
    return build_color_response_from_rgb(r, g, b)


def convert_hsl_color(h: float, s: float, l: float) -> dict:
    r, g, b = hsl_to_rgb_values(h, s, l)
    return build_color_response_from_rgb(r, g, b)


def generate_palette(hex_color: str) -> dict:
    base = convert_hex_color(hex_color)

    lighter = []
    darker = []

    for amount in [10, 20, 30]:
        lighter_l = clamp(base["l"] + amount, 0, 100)
        darker_l = clamp(base["l"] - amount, 0, 100)

        lighter.append(convert_hsl_color(base["h"], base["s"], lighter_l))
        darker.append(convert_hsl_color(base["h"], base["s"], darker_l))

    return {
        "base": base,
        "lighter": lighter,
        "darker": darker,
    }
