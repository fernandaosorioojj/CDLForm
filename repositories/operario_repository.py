from __future__ import annotations

from pathlib import Path

from models.operario import Operario
from repositories.base_repository import BaseRepository


class OperarioRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path or Path("storage/operarios.json"))

    def _from_dict(self, data: dict) -> Operario:
        return Operario.from_dict(data)

    def _get_entity_id(self, entity: Operario) -> str:
        return entity.id_operario

    def get_operarios_activos(self) -> list[Operario]:
        return [operario for operario in self.list_all() if operario.activo]

    def get_operarios_por_area(
        self,
        area: str,
        solo_activos: bool = True,
    ) -> list[Operario]:
        area_normalizada = area.strip().lower()

        operarios = [
            operario
            for operario in self.list_all()
            if operario.area.strip().lower() == area_normalizada
        ]

        if solo_activos:
            operarios = [operario for operario in operarios if operario.activo]

        return operarios

    def get_operarios_por_maquina(
        self,
        maquina: str,
        solo_activos: bool = True,
    ) -> list[Operario]:
        maquina_normalizada = maquina.strip().lower()

        operarios = [
            operario
            for operario in self.list_all()
            if operario.maquina.strip().lower() == maquina_normalizada
        ]

        if solo_activos:
            operarios = [operario for operario in operarios if operario.activo]

        return operarios

    def get_operarios_por_area_y_maquina(
        self,
        area: str,
        maquina: str,
        solo_activos: bool = True,
    ) -> list[Operario]:
        area_normalizada = area.strip().lower()
        maquina_normalizada = maquina.strip().lower()

        operarios = [
            operario
            for operario in self.list_all()
            if operario.area.strip().lower() == area_normalizada
            and operario.maquina.strip().lower() == maquina_normalizada
        ]

        if solo_activos:
            operarios = [operario for operario in operarios if operario.activo]

        return operarios