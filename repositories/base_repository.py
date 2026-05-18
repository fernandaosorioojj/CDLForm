"""Acceso a datos SQL Server para entidades del dominio CDLform.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from utils.json_manager import JsonManager


# LEGACY / NO FLUJO ACTUAL:
# Repositorio generico JSON conservado solo para compatibilidad tecnica o pruebas
# antiguas. Gestion, operario, MQTT y watchdog usan repositorios SQL Server.
class BaseRepository:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, file_path: Path) -> None:
        self.file_path = Path(file_path)
        JsonManager.ensure_file_exists(str(self.file_path), default_data=[])

    # Bloque CDLform: funcion/metodo get_all; encapsula una operacion del flujo del modulo.
    def get_all(self) -> list[dict[str, Any]]:
        data = JsonManager.read_json(str(self.file_path))
        if not isinstance(data, list):
            return []
        return data

    # Bloque CDLform: funcion/metodo find_by_id; encapsula una operacion del flujo del modulo.
    def find_by_id(self, item_id: str) -> Optional[dict[str, Any]]:
        data = self.get_all()
        for item in data:
            if self._get_item_id(item) == item_id:
                return item
        return None

    # Bloque CDLform: funcion/metodo add; encapsula una operacion del flujo del modulo.
    def add(self, item: dict[str, Any]) -> dict[str, Any]:
        data = self.get_all()
        data.append(item)
        JsonManager.write_json(str(self.file_path), data)
        return item

    # Bloque CDLform: funcion/metodo update_by_id; encapsula una operacion del flujo del modulo.
    def update_by_id(self, item_id: str, new_data: dict[str, Any]) -> bool:
        data = self.get_all()

        for index, item in enumerate(data):
            if self._get_item_id(item) == item_id:
                data[index] = new_data
                JsonManager.write_json(str(self.file_path), data)
                return True

        return False

    # Bloque CDLform: funcion/metodo delete_by_id; encapsula una operacion del flujo del modulo.
    def delete_by_id(self, item_id: str) -> bool:
        data = self.get_all()
        new_data = [item for item in data if self._get_item_id(item) != item_id]

        if len(new_data) == len(data):
            return False

        JsonManager.write_json(str(self.file_path), new_data)
        return True

    # Bloque CDLform: funcion/metodo filter; encapsula una operacion del flujo del modulo.
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

    # Bloque CDLform: funcion/metodo _get_item_id; encapsula una operacion del flujo del modulo.
    def _get_item_id(self, item: dict[str, Any]) -> Optional[str]:
        for key, value in item.items():
            if key.startswith("id_"):
                return value
        return None
