from __future__ import annotations

from config.settings import SETTINGS
from models.pregunta import Pregunta
from repositories.base_repository import BaseRepository


class PreguntaRepository(BaseRepository[Pregunta]):
    def __init__(self) -> None:
        super().__init__(SETTINGS.paths.preguntas_file)

    def _from_dict(self, data: dict) -> Pregunta:
        return Pregunta.from_dict(data)

    def _get_entity_id(self, entity: Pregunta) -> str:
        return entity.id_pregunta

    def get_active(self) -> list[Pregunta]:
        return [pregunta for pregunta in self.list_all() if pregunta.activa]

    def get_by_rol(self, rol: str, solo_activas: bool = True) -> list[Pregunta]:
        normalized_rol = rol.strip().casefold()
        source = self.get_active() if solo_activas else self.list_all()

        return [
            pregunta
            for pregunta in source
            if normalized_rol in {item.casefold() for item in pregunta.roles_asociados}
        ]

    def get_by_area(self, area: str, solo_activas: bool = True) -> list[Pregunta]:
        normalized_area = area.strip().casefold()
        source = self.get_active() if solo_activas else self.list_all()

        return [
            pregunta
            for pregunta in source
            if normalized_area in {item.casefold() for item in pregunta.areas_asociadas}
        ]

    def get_by_maquina(self, maquina: str, solo_activas: bool = True) -> list[Pregunta]:
        normalized_maquina = maquina.strip().casefold()
        source = self.get_active() if solo_activas else self.list_all()

        return [
            pregunta
            for pregunta in source
            if normalized_maquina in {item.casefold() for item in pregunta.maquinas_asociadas}
        ]

    def get_applicable_questions(
        self,
        rol: str,
        area: str,
        maquina: str | None = None,
        solo_activas: bool = True,
    ) -> list[Pregunta]:
        normalized_rol = rol.strip().casefold()
        normalized_area = area.strip().casefold()
        normalized_maquina = maquina.strip().casefold() if maquina else None

        source = self.get_active() if solo_activas else self.list_all()
        result: list[Pregunta] = []

        for pregunta in source:
            roles = {item.casefold() for item in pregunta.roles_asociados}
            areas = {item.casefold() for item in pregunta.areas_asociadas}
            maquinas = {item.casefold() for item in pregunta.maquinas_asociadas}

            cumple_rol = normalized_rol in roles
            cumple_area = normalized_area in areas
            cumple_maquina = True

            if normalized_maquina is not None and maquinas:
                cumple_maquina = normalized_maquina in maquinas

            if cumple_rol and cumple_area and cumple_maquina:
                result.append(pregunta)

        return result