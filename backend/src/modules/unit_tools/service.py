from fastapi import HTTPException

LENGTH_FACTORS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

MASS_FACTORS = {
    "mg": 0.001,
    "g": 1,
    "kg": 1000,
    "t": 1_000_000,
    "oz": 28.349523125,
    "lb": 453.59237,
}

STORAGE_FACTORS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024**2,
    "GB": 1024**3,
    "TB": 1024**4,
}

AREA_FACTORS = {
    "cm2": 0.0001,
    "m2": 1,
    "km2": 1_000_000,
    "ha": 10_000,
}

VOLUME_FACTORS = {
    "ml": 0.001,
    "l": 1,
    "m3": 1000,
}

SUPPORTED_UNITS = {
    "length": LENGTH_FACTORS,
    "mass": MASS_FACTORS,
    "storage": STORAGE_FACTORS,
    "area": AREA_FACTORS,
    "volume": VOLUME_FACTORS,
}


def round_result(value: float) -> float:
    return round(value, 6)


def convert_temperature(value: float, from_unit: str, to_unit: str) -> dict:
    valid_units = {"c", "f", "k"}

    if from_unit not in valid_units or to_unit not in valid_units:
        raise HTTPException(status_code=400, detail="Unidade de temperatura inválida.")

    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit == "c":
        result = celsius
    elif to_unit == "f":
        result = (celsius * 9 / 5) + 32
    else:
        result = celsius + 273.15

    return {
        "category": "temperature",
        "from_unit": from_unit,
        "to_unit": to_unit,
        "input_value": value,
        "result": round_result(result),
        "formula": "Conversão de temperatura usando Celsius como base intermediária.",
    }


def convert_px_rem(value: float, from_unit: str, to_unit: str, base_font_size: float) -> dict:
    valid_units = {"px", "rem"}

    if from_unit not in valid_units or to_unit not in valid_units:
        raise HTTPException(status_code=400, detail="Unidade inválida para conversão px/rem.")

    if from_unit == to_unit:
        result = value
        formula = "Unidades iguais, valor mantido."
    elif from_unit == "px" and to_unit == "rem":
        result = value / base_font_size
        formula = f"{value}px / {base_font_size}px = {round_result(result)}rem"
    else:
        result = value * base_font_size
        formula = f"{value}rem * {base_font_size}px = {round_result(result)}px"

    return {
        "category": "px-rem",
        "from_unit": from_unit,
        "to_unit": to_unit,
        "input_value": value,
        "result": round_result(result),
        "formula": formula,
    }


def convert_unit(category: str, from_unit: str, to_unit: str, value: float, base_font_size: float) -> dict:
    normalized_category = category.lower().strip()
    normalized_from = from_unit.strip()
    normalized_to = to_unit.strip()

    if normalized_category == "temperature":
        return convert_temperature(value, normalized_from.lower(), normalized_to.lower())

    if normalized_category == "px-rem":
        return convert_px_rem(value, normalized_from.lower(), normalized_to.lower(), base_font_size)

    factors = SUPPORTED_UNITS.get(normalized_category)

    if not factors:
        raise HTTPException(status_code=400, detail="Categoria de conversão inválida.")

    if normalized_from not in factors or normalized_to not in factors:
        raise HTTPException(status_code=400, detail="Unidade inválida para esta categoria.")

    base_value = value * factors[normalized_from]
    result = base_value / factors[normalized_to]

    return {
        "category": normalized_category,
        "from_unit": normalized_from,
        "to_unit": normalized_to,
        "input_value": value,
        "result": round_result(result),
        "formula": f"{value} {normalized_from} → base → {round_result(result)} {normalized_to}",
    }


def require_value(values: dict[str, float], key: str) -> float:
    if key not in values:
        raise HTTPException(status_code=400, detail=f"Informe o valor de '{key}'.")

    return values[key]


def calculate_formula(formula_type: str, values: dict[str, float]) -> dict:
    normalized = formula_type.lower().strip()

    if normalized == "percentage_of":
        percentage = require_value(values, "percentage")
        total = require_value(values, "total")
        result = (percentage / 100) * total

        return {
            "formula_type": normalized,
            "result": round_result(result),
            "expression": f"{percentage}% de {total} = {round_result(result)}",
            "description": "Calcula quanto uma porcentagem representa de um valor.",
        }

    if normalized == "percentage_change":
        initial = require_value(values, "initial")
        final = require_value(values, "final")

        if initial == 0:
            raise HTTPException(status_code=400, detail="O valor inicial não pode ser zero.")

        result = ((final - initial) / initial) * 100

        return {
            "formula_type": normalized,
            "result": round_result(result),
            "expression": f"(({final} - {initial}) / {initial}) * 100 = {round_result(result)}%",
            "description": "Calcula a variação percentual entre dois valores.",
        }

    if normalized == "rule_of_three":
        a = require_value(values, "a")
        b = require_value(values, "b")
        c = require_value(values, "c")

        if a == 0:
            raise HTTPException(status_code=400, detail="O valor A não pode ser zero.")

        result = (b * c) / a

        return {
            "formula_type": normalized,
            "result": round_result(result),
            "expression": f"({b} * {c}) / {a} = {round_result(result)}",
            "description": "Regra de três simples.",
        }

    if normalized == "bmi":
        weight = require_value(values, "weight")
        height = require_value(values, "height")

        if height <= 0:
            raise HTTPException(status_code=400, detail="A altura deve ser maior que zero.")

        result = weight / (height * height)

        return {
            "formula_type": normalized,
            "result": round_result(result),
            "expression": f"{weight} / ({height} * {height}) = {round_result(result)}",
            "description": "Calcula IMC usando peso em kg e altura em metros.",
        }

    raise HTTPException(status_code=400, detail="Fórmula inválida.")
