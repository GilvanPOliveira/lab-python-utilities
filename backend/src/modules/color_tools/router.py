from fastapi import APIRouter

from src.modules.color_tools.schemas import ColorPaletteRequest, HexColorRequest, HslColorRequest, RgbColorRequest
from src.modules.color_tools.service import (
    convert_hex_color,
    convert_hsl_color,
    convert_rgb_color,
    generate_palette,
)

router = APIRouter()


@router.post("/hex")
def convert_hex_route(payload: HexColorRequest):
    return convert_hex_color(payload.hex_color)


@router.post("/rgb")
def convert_rgb_route(payload: RgbColorRequest):
    return convert_rgb_color(payload.r, payload.g, payload.b)


@router.post("/hsl")
def convert_hsl_route(payload: HslColorRequest):
    return convert_hsl_color(payload.h, payload.s, payload.l)


@router.post("/palette")
def palette_route(payload: ColorPaletteRequest):
    return generate_palette(payload.hex_color)
