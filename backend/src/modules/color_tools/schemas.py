from pydantic import BaseModel, Field


class HexColorRequest(BaseModel):
    hex_color: str = Field(min_length=3, max_length=9)


class RgbColorRequest(BaseModel):
    r: int = Field(ge=0, le=255)
    g: int = Field(ge=0, le=255)
    b: int = Field(ge=0, le=255)


class HslColorRequest(BaseModel):
    h: float = Field(ge=0, le=360)
    s: float = Field(ge=0, le=100)
    l: float = Field(ge=0, le=100)


class ColorPaletteRequest(BaseModel):
    hex_color: str = Field(min_length=3, max_length=9)


class ColorResponse(BaseModel):
    hex: str
    rgb: str
    hsl: str
    r: int
    g: int
    b: int
    h: float
    s: float
    l: float


class ColorPaletteResponse(BaseModel):
    base: ColorResponse
    lighter: list[ColorResponse]
    darker: list[ColorResponse]
