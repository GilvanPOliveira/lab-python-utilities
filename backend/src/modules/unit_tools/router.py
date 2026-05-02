from fastapi import APIRouter

from src.modules.unit_tools.schemas import FormulaRequest, UnitConversionRequest
from src.modules.unit_tools.service import calculate_formula, convert_unit

router = APIRouter()


@router.post("/convert")
def convert_unit_route(payload: UnitConversionRequest):
    return convert_unit(
        category=payload.category,
        from_unit=payload.from_unit,
        to_unit=payload.to_unit,
        value=payload.value,
        base_font_size=payload.base_font_size,
    )


@router.post("/formula")
def formula_route(payload: FormulaRequest):
    return calculate_formula(
        formula_type=payload.formula_type,
        values=payload.values,
    )
