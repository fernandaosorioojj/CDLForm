from __future__ import annotations

import json
import os
from typing import Any


class JsonManager:
    @staticmethod
    def ensure_file_exists(file_path: str, default_data: Any = None) -> None:
        if default_data is None:
            default_data = []

        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(default_data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def read_json(file_path: str) -> Any:
        JsonManager.ensure_file_exists(file_path, default_data=[])

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @staticmethod
    def write_json(file_path: str, data: Any) -> None:
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)