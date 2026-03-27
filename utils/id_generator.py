from __future__ import annotations

from core.exceptions import ValidationError
from core.validators import require_non_empty_string, require_positive_int


class IdGenerator:
    @staticmethod
    def generate(prefix: str, next_number: int, length: int = 4) -> str:
        normalized_prefix = require_non_empty_string(prefix, "prefix").upper()
        normalized_number = require_positive_int(next_number, "next_number")
        normalized_length = require_positive_int(length, "length")

        if normalized_length < len(str(normalized_number)):
            raise ValidationError(
                "el largo indicado para el id es insuficiente para representar el correlativo solicitado"
            )

        return f"{normalized_prefix}-{str(normalized_number).zfill(normalized_length)}"