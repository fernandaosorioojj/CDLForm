from __future__ import annotations

from pathlib import Path

from repositories.base_repository import BaseRepository
from utils.json_manager import JsonManager


class FormularioRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = Path(file_path or "storage/formularios.json")
        super().__init__(self.file_path)

    def listar_formularios(self) -> list[dict]:
        return self.get_all()

    def _guardar_todos(self, formularios: list[dict]) -> None:
        JsonManager.write_json(str(self.file_path), formularios)

    def obtener_por_id(self, id_formulario: str) -> dict | None:
        id_normalizado = str(id_formulario).strip()

        for formulario in self.get_all():
            if str(formulario.get("id_formulario", "")).strip() == id_normalizado:
                return formulario

        return None

    def obtener_por_id_apontamento(self, id_apontamento: str) -> dict | None:
        id_normalizado = str(id_apontamento).strip()

        for formulario in self.get_all():
            if str(formulario.get("id_apontamento", "")).strip() == id_normalizado:
                return formulario

        return None

    def listar_por_estado(self, estado: str) -> list[dict]:
        estado_normalizado = str(estado).strip()

        return [
            formulario
            for formulario in self.get_all()
            if str(formulario.get("estado", "")).strip() == estado_normalizado
        ]

    def add_formulario(self, formulario: dict) -> dict:
        return self.add(formulario)

    def actualizar_formulario(self, id_formulario: str, cambios: dict) -> dict | None:
        id_normalizado = str(id_formulario).strip()
        formularios = self.get_all()

        for indice, formulario in enumerate(formularios):
            if str(formulario.get("id_formulario", "")).strip() == id_normalizado:
                formulario_actualizado = dict(formulario)
                formulario_actualizado.update(cambios)
                formularios[indice] = formulario_actualizado
                self._guardar_todos(formularios)
                return formulario_actualizado

        return None