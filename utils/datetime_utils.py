from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from config.settings import SETTINGS
from core.exceptions import ValidationError


class DateTimeUtils:
    @staticmethod
    def now() -> datetime:
        
        return datetime.now(ZoneInfo(SETTINGS.timezone_name))

    @staticmethod
    def now_as_string() -> str:
        
        return DateTimeUtils.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def current_date_as_string() -> str:
        
        return DateTimeUtils.now().strftime("%Y-%m-%d")

    @staticmethod
    def parse_datetime(value: str, field_name: str = "fecha_hora") -> datetime:
        
        if not isinstance(value, str):
            raise ValidationError(f"el campo '{field_name}' debe ser texto")

        normalized = value.strip()

        
        if not normalized:
            raise ValidationError(f"el campo '{field_name}' es obligatorio")

        accepted_formats = (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
        )

        
        for fmt in accepted_formats:
            try:
                parsed = datetime.strptime(normalized, fmt)
                return parsed.replace(tzinfo=ZoneInfo(SETTINGS.timezone_name))
            except ValueError:
                continue

        raise ValidationError(
            f"el campo '{field_name}' no tiene un formato válido. use 'YYYY-MM-DD HH:MM:SS', "
            f"'YYYY-MM-DDTHH:MM:SS' o 'YYYY-MM-DD'"
        )

    @staticmethod
    def ensure_not_future(value: str, field_name: str = "fecha_hora") -> str:
        
        parsed = DateTimeUtils.parse_datetime(value, field_name)

        
        if parsed > DateTimeUtils.now():
            raise ValidationError(f"el campo '{field_name}' no puede estar en el futuro")

        return value.strip()

    @staticmethod
    def normalize_datetime_string(value: str, field_name: str = "fecha_hora") -> str:
        
        parsed = DateTimeUtils.parse_datetime(value, field_name)
        return parsed.strftime("%Y-%m-%d %H:%M:%S")