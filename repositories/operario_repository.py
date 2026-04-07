from __future__ import annotations

from pathlib import Path

from repositories.base_repository import BaseRepository
from utils.json_manager import JsonManager


class OperarioRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = Path(file_path or "storage/operarios.json")
        super().__init__(self.file_path)

    def list_all(self) -> list[dict]:
        return self.get_all()

    def listar_operarios(self) -> list[dict]:
        return self.get_all()

    def obtener_por_id(self, id_operario: str) -> dict | None:
        id_normalizado = str(id_operario).strip()

        for operario in self.get_all():
            if str(operario.get("id_operario", "")).strip() == id_normalizado:
                return operario

        return None

    def add_operario(self, operario: dict) -> dict:
        return self.add(operario)

    def actualizar_operario(self, id_operario: str, cambios: dict) -> dict | None:
        id_normalizado = str(id_operario).strip()
        operarios = self.get_all()

        for indice, operario in enumerate(operarios):
            if str(operario.get("id_operario", "")).strip() == id_normalizado:
                operario_actualizado = dict(operario)
                operario_actualizado.update(cambios)
                operarios[indice] = operario_actualizado
                JsonManager.write_json(str(self.file_path), operarios)
                return operario_actualizado

        return None