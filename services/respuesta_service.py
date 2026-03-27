from __future__ import annotations

from core.exceptions import NotFoundError
from models.respuesta import Respuesta
from repositories.respuesta_repository import RespuestaRepository
from services.formulario_service import FormularioService
from utils.id_generator import IdGenerator


class RespuestaService:
    def __init__(self) -> None:
        self.repository = RespuestaRepository()
        self.formulario_service = FormularioService()

    def list_all(self) -> list[Respuesta]:
        return self.repository.list_all()

    def get_by_id(self, id_respuesta: str) -> Respuesta:
        return self.repository.get_by_id(id_respuesta)

    def get_by_formulario(self, id_formulario: str) -> list[Respuesta]:
        return self.repository.get_by_formulario(id_formulario)

    def get_by_pregunta(self, id_pregunta: str) -> list[Respuesta]:
        return self.repository.get_by_pregunta(id_pregunta)

    def create(
        self,
        id_formulario: str,
        id_pregunta: str,
        respuesta_texto: str | None = None,
        respuesta_numero: float | int | None = None,
        id_opcion: str | None = None,
    ) -> Respuesta:
        self.formulario_service.ensure_exists(id_formulario)

        respuestas_existentes = self.repository.list_all()
        next_number = len(respuestas_existentes) + 1
        id_respuesta = IdGenerator.generate("RESP", next_number)

        respuesta = Respuesta(
            id_respuesta=id_respuesta,
            id_formulario=id_formulario,
            id_pregunta=id_pregunta,
            respuesta_texto=respuesta_texto,
            respuesta_numero=respuesta_numero,
            id_opcion=id_opcion,
        )

        self.repository.add(respuesta)
        return respuesta

    def delete(self, id_respuesta: str) -> None:
        self.repository.delete(id_respuesta)

    def ensure_exists(self, id_respuesta: str) -> None:
        try:
            self.repository.get_by_id(id_respuesta)
        except NotFoundError as exc:
            raise NotFoundError(
                f"no existe una respuesta con id '{id_respuesta}'"
            ) from exc