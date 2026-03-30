from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from utils.json_manager import JsonManager


class BaseRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = Path(file_path)
        JsonManager.ensure_file_exists(str(self.file_path), default_data=[])

    def get_all(self) -> list[dict[str, Any]]:
        data = JsonManager.read_json(str(self.file_path))
        if not isinstance(data, list):
            return []
        return data

    def find_by_id(self, item_id: str) -> Optional[dict[str, Any]]:
        data = self.get_all()
        for item in data:
            if self._get_item_id(item) == item_id:
                return item
        return None

    def add(self, item: dict[str, Any]) -> dict[str, Any]:
        data = self.get_all()
        data.append(item)
        JsonManager.write_json(str(self.file_path), data)
        return item

    def update_by_id(self, item_id: str, new_data: dict[str, Any]) -> bool:
        data = self.get_all()

        for index, item in enumerate(data):
            if self._get_item_id(item) == item_id:
                data[index] = new_data
                JsonManager.write_json(str(self.file_path), data)
                return True

        return False

    def delete_by_id(self, item_id: str) -> bool:
        data = self.get_all()
        new_data = [item for item in data if self._get_item_id(item) != item_id]

        if len(new_data) == len(data):
            return False

        JsonManager.write_json(str(self.file_path), new_data)
        return True

    def filter(self, **criteria: Any) -> list[dict[str, Any]]:
        data = self.get_all()
        resultado = []

        for item in data:
            coincide = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    coincide = False
                    break

            if coincide:
                resultado.append(item)

        return resultado

    def _get_item_id(self, item: dict[str, Any]) -> Optional[str]:
        for key, value in item.items():
            if key.startswith("id_"):
                return value
        return None