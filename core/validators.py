from __future__ import annotations

from typing import Iterable, Sequence

from core.exceptions import ValidationError


def require_non_empty_string(value: str, field_name: str, max_length: int | None = None) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"el campo '{field_name}' debe ser texto")

    normalized = value.strip()
    if not normalized:
        raise ValidationError(f"el campo '{field_name}' es obligatorio")

    if max_length is not None and len(normalized) > max_length:
        raise ValidationError(
            f"el campo '{field_name}' excede el largo máximo permitido de {max_length} caracteres"
        )

    return normalized


def optional_string(value: str | None, field_name: str, max_length: int | None = None) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValidationError(f"el campo '{field_name}' debe ser texto")

    normalized = value.strip()
    if normalized == "":
        return None

    if max_length is not None and len(normalized) > max_length:
        raise ValidationError(
            f"el campo '{field_name}' excede el largo máximo permitido de {max_length} caracteres"
        )

    return normalized


def require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValidationError(f"el campo '{field_name}' debe ser booleano")
    return value


def require_list(value: Sequence, field_name: str) -> list:
    if value is None:
        return []

    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValidationError(f"el campo '{field_name}' debe ser una lista")

    return list(value)


def require_non_empty_iterable(value: Iterable, field_name: str) -> list:
    result = list(value)
    if not result:
        raise ValidationError(f"el campo '{field_name}' debe tener al menos un elemento")
    return result


def normalize_string_list(
    values: Sequence[str] | None,
    field_name: str,
    allow_empty: bool = True,
    unique: bool = True,
) -> list[str]:
    if values is None:
        return []

    raw_values = require_list(values, field_name)
    normalized: list[str] = []

    for index, item in enumerate(raw_values, start=1):
        item_normalized = require_non_empty_string(item, f"{field_name}[{index}]")
        normalized.append(item_normalized)

    if unique:
        seen: set[str] = set()
        deduped: list[str] = []
        for item in normalized:
            key = item.casefold()
            if key not in seen:
                deduped.append(item)
                seen.add(key)
        normalized = deduped

    if not allow_empty and not normalized:
        raise ValidationError(f"el campo '{field_name}' debe tener al menos un valor")

    return normalized


def require_positive_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValidationError(f"el campo '{field_name}' debe ser entero")

    if value <= 0:
        raise ValidationError(f"el campo '{field_name}' debe ser mayor que cero")

    return value


def require_status_in_allowed(value: str, field_name: str, allowed_values: Sequence[str]) -> str:
    normalized = require_non_empty_string(value, field_name).lower()

    allowed_normalized = {item.strip().lower() for item in allowed_values}
    if normalized not in allowed_normalized:
        raise ValidationError(
            f"el campo '{field_name}' debe tener uno de estos valores: {', '.join(sorted(allowed_normalized))}"
        )

    return normalized