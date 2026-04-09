from __future__ import annotations

from pathlib import Path

from models.formulario import Formulario
from repositories.base_repository import BaseRepository
from utils.json_manager import JsonManager


class FormularioRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = Path(file_path or "storage/formularios.json")
        super().__init__(self.file_path)

    def _leer_todos_crudos(self) -> list[dict]:
        return self.get_all()

    def _guardar_todos(self, formularios: list[Formulario]) -> None:
        JsonManager.write_json(
            str(self.file_path),
            [formulario.to_dict() for formulario in formularios],
        )

    def listar_formularios(self) -> list[Formulario]:
        return [
            Formulario.from_dict(item)
            for item in self._leer_todos_crudos()
        ]

    def obtener_por_id(self, id_formulario: str) -> Formulario | None:
        id_normalizado = str(id_formulario).strip()

        for formulario in self.listar_formularios():
            if formulario.id_formulario == id_normalizado:
                return formulario

        return None

    def obtener_por_id_apontamento(self, id_apontamento: str) -> Formulario | None:
        id_normalizado = str(id_apontamento).strip()

        for formulario in self.listar_formularios():
            if formulario.id_apontamento == id_normalizado:
                return formulario

        return None

    def listar_por_estado(self, estado: str) -> list[Formulario]:
        estado_normalizado = str(estado).strip()

        return [
            formulario
            for formulario in self.listar_formularios()
            if formulario.estado == estado_normalizado
        ]

    def guardar(self, formulario: Formulario) -> Formulario:
        formularios = self.listar_formularios()

        for indice, actual in enumerate(formularios):
            if actual.id_formulario == formulario.id_formulario:
                formularios[indice] = formulario
                self._guardar_todos(formularios)
                return formulario

        formularios.append(formulario)
        self._guardar_todos(formularios)
        return formulario

    def add_formulario(self, formulario: Formulario) -> Formulario:
        if self.obtener_por_id(formulario.id_formulario):
            raise ValueError(
                f"Ya existe un formulario con id {formulario.id_formulario}."
            )
        return self.guardar(formulario)

    def actualizar_formulario(
        self,
        id_formulario: str,
        cambios: dict,
    ) -> Formulario | None:
        formulario = self.obtener_por_id(id_formulario)
        if not formulario:
            return None

        formulario.actualizar(cambios)
        return self.guardar(formulario)