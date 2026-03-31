from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from models.formulario import Formulario
from repositories.base_repository import BaseRepository


class FormularioRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path or Path("storage/formularios.json"))

    def _from_dict(self, data: dict) -> Formulario:
        return Formulario.from_dict(data)

    def _get_entity_id(self, entity: Formulario) -> str:
        return entity.id_formulario

    def list_all(self) -> List[Formulario]:
        registros = self.get_all()
        return [self._from_dict(item) for item in registros]

    def get_by_id(self, id_formulario: str) -> Optional[Formulario]:
        if not id_formulario or not str(id_formulario).strip():
            return None

        data = self.find_by_id(str(id_formulario).strip())
        if not data:
            return None

        return self._from_dict(data)

    def add_formulario(self, formulario: Formulario) -> Formulario:
        self.add(formulario.to_dict())
        return formulario

    def update_formulario(self, id_formulario: str, formulario: Formulario) -> Formulario:
        self.update_by_id(id_formulario, formulario.to_dict())
        return formulario

    def get_formularios_por_estado(self, estado: str) -> List[Formulario]:
        if not estado or not str(estado).strip():
            return []

        estado_normalizado = str(estado).strip().lower()

        registros = self.filter(
            lambda item: str(item.get("estado", "")).strip().lower() == estado_normalizado
        )
        return [self._from_dict(item) for item in registros]

    def get_formularios_por_operario(self, operario: str) -> List[Formulario]:
        if not operario or not str(operario).strip():
            return []

        operario_normalizado = str(operario).strip().lower()

        registros = self.filter(
            lambda item: str(item.get("operario", "")).strip().lower() == operario_normalizado
        )
        return [self._from_dict(item) for item in registros]

    def get_formularios_por_identificador(self, identificador: str) -> List[Formulario]:
        if not identificador or not str(identificador).strip():
            return []

        identificador_normalizado = str(identificador).strip().lower()

        registros = self.filter(
            lambda item: str(item.get("identificador", "")).strip().lower() == identificador_normalizado
        )
        return [self._from_dict(item) for item in registros]