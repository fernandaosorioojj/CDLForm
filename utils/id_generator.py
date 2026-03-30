from __future__ import annotations

from typing import Iterable


def generate_id(prefix: str, records: Iterable[dict], field_name: str) -> str:
    """
    Genera un ID secuencial con formato PREFIX-0001.

    Ejemplos:
    - FORM-0001
    - RESP-0001
    - EVT-0001

    Parámetros:
    - prefix: prefijo del ID
    - records: colección de registros existentes
    - field_name: nombre del campo donde está guardado el ID
    """

    if not prefix or not str(prefix).strip():
        raise ValueError("El prefijo es obligatorio.")

    if not field_name or not str(field_name).strip():
        raise ValueError("El nombre del campo es obligatorio.")

    prefix = str(prefix).strip().upper()
    field_name = str(field_name).strip()

    max_number = 0

    for record in records or []:
        if not isinstance(record, dict):
            continue

        raw_id = record.get(field_name)
        if not isinstance(raw_id, str):
            continue

        raw_id = raw_id.strip().upper()

        if not raw_id.startswith(f"{prefix}-"):
            continue

        correlativo = raw_id[len(prefix) + 1:]

        if correlativo.isdigit():
            max_number = max(max_number, int(correlativo))

    next_number = max_number + 1
    return f"{prefix}-{next_number:04d}"