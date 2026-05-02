from pydantic import BaseModel, Field


class UnitConversionRequest(BaseModel):
    category: str = Field(min_length=1)
    from_unit: str = Field(min_length=1)
    to_unit: str = Field(min_length=1)
    value: float
    base_font_size: float = Field(default=16, gt=0)


class UnitConversionResponse(BaseModel):
    category: str
    from_unit: str
    to_unit: str
    input_value: float
    result: float
    formula: str


class FormulaRequest(BaseModel):
    formula_type: str = Field(min_length=1)
    values: dict[str, float]


class FormulaResponse(BaseModel):
    formula_type: str
    result: float
    expression: str
    description: str
