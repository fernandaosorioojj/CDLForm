from __future__ import annotations

from core.enums import TipoPregunta
from core.exceptions import DuplicateEntityError, NotFoundError
from models.pregunta import Pregunta
from repositories.pregunta_repository import PreguntaRepository
from utils.id_generator import IdGenerator


class PreguntaService:
    def __init__(self) -> None:
        self.repository = PreguntaRepository()

    def list_all(self) -> list[Pregunta]:
        return self.repository.list_all()

    def list_active(self) -> list[Pregunta]:
        return self.repository.get_active()

    def get_by_id(self, id_pregunta: str) -> Pregunta:
        return self.repository.get_by_id(id_pregunta)

    def get_by_rol(self, rol: str, solo_activas: bool = True) -> list[Pregunta]:
        return self.repository.get_by_rol(rol, solo_activas)

    def get_by_area(self, area: str, solo_activas: bool = True) -> list[Pregunta]:
        return self.repository.get_by_area(area, solo_activas)

    def get_by_maquina(self, maquina: str, solo_activas: bool = True) -> list[Pregunta]:
        return self.repository.get_by_maquina(maquina, solo_activas)

    def get_applicable_questions(
        self,
        rol: str,
        area: str,
        maquina: str | None = None,
        solo_activas: bool = True,
    ) -> list[Pregunta]:
        return self.repository.get_applicable_questions(
            rol=rol,
            area=area,
            maquina=maquina,
            solo_activas=solo_activas,
        )

    def create(
        self,
        texto: str,
        tipo: TipoPregunta,
        roles_asociados: list[str],
        areas_asociadas: list[str],
        maquinas_asociadas: list[str] | None = None,
        activa: bool = True,
    ) -> Pregunta:
        preguntas_existentes = self.repository.list_all()
        next_number = len(preguntas_existentes) + 1
        id_pregunta = IdGenerator.generate("PREG", next_number)

        pregunta = Pregunta(
            id_pregunta=id_pregunta,
            texto=texto,
            tipo=tipo,
            activa=activa,
            roles_asociados=roles_asociados,
            areas_asociadas=areas_asociadas,
            maquinas_asociadas=maquinas_asociadas or [],
        )

        self.repository.add(pregunta)
        return pregunta

    def update(
        self,
        id_pregunta: str,
        texto: str,
        tipo: TipoPregunta,
        roles_asociados: list[str],
        areas_asociadas: list[str],
        maquinas_asociadas: list[str] | None = None,
        activa: bool = True,
    ) -> Pregunta:
        pregunta_actual = self.repository.get_by_id(id_pregunta)

        pregunta_actualizada = Pregunta(
            id_pregunta=pregunta_actual.id_pregunta,
            texto=texto,
            tipo=tipo,
            activa=activa,
            roles_asociados=roles_asociados,
            areas_asociadas=areas_asociadas,
            maquinas_asociadas=maquinas_asociadas or [],
        )

        self.repository.update(pregunta_actualizada)
        return pregunta_actualizada

    def activate(self, id_pregunta: str) -> Pregunta:
        pregunta_actual = self.repository.get_by_id(id_pregunta)

        pregunta_actualizada = Pregunta(
            id_pregunta=pregunta_actual.id_pregunta,
            texto=pregunta_actual.texto,
            tipo=pregunta_actual.tipo,
            activa=True,
            roles_asociados=pregunta_actual.roles_asociados,
            areas_asociadas=pregunta_actual.areas_asociadas,
            maquinas_asociadas=pregunta_actual.maquinas_asociadas,
        )

        self.repository.update(pregunta_actualizada)
        return pregunta_actualizada

    def deactivate(self, id_pregunta: str) -> Pregunta:
        pregunta_actual = self.repository.get_by_id(id_pregunta)

        pregunta_actualizada = Pregunta(
            id_pregunta=pregunta_actual.id_pregunta,
            texto=pregunta_actual.texto,
            tipo=pregunta_actual.tipo,
            activa=False,
            roles_asociados=pregunta_actual.roles_asociados,
            areas_asociadas=pregunta_actual.areas_asociadas,
            maquinas_asociadas=pregunta_actual.maquinas_asociadas,
        )

        self.repository.update(pregunta_actualizada)
        return pregunta_actualizada

    def delete(self, id_pregunta: str) -> None:
        self.repository.delete(id_pregunta)

    def ensure_exists(self, id_pregunta: str) -> None:
        try:
            self.repository.get_by_id(id_pregunta)
        except NotFoundError as exc:
            raise NotFoundError(
                f"no existe una pregunta con id '{id_pregunta}'"
            ) from exc