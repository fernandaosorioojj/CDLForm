from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.settings import SETTINGS
from core.exceptions import RepositoryError


class JsonManager:
    @staticmethod
    def ensure_file_exists(file_path: Path, default_data: Any) -> None:
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if not file_path.exists():
                with file_path.open("w", encoding=SETTINGS.default_encoding) as file:
                    json.dump(default_data, file, ensure_ascii=False, indent=4)

        except OSError as exc:
            raise RepositoryError(
                f"no fue posible asegurar la existencia del archivo '{file_path}'"
            ) from exc

    @staticmethod
    def read_json(file_path: Path, default_data: Any) -> Any:
        JsonManager.ensure_file_exists(file_path, default_data)

        try:
            with file_path.open("r", encoding=SETTINGS.default_encoding) as file:
                return json.load(file)

        except json.JSONDecodeError as exc:
            raise RepositoryError(
                f"el archivo '{file_path}' contiene json inválido"
            ) from exc

        except OSError as exc:
            raise RepositoryError(
                f"no fue posible leer el archivo '{file_path}'"
            ) from exc

    @staticmethod
    def write_json(file_path: Path, data: Any) -> None:
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with file_path.open("w", encoding=SETTINGS.default_encoding) as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except OSError as exc:
            raise RepositoryError(
                f"no fue posible escribir el archivo '{file_path}'"
            ) from exc