from __future__ import annotations

from typing import Any, Optional

from core.exceptions import NotFoundError, ValidationError
from models.respuesta import Respuesta
from repositories.respuesta_repository import RespuestaRepository
from utils.id_generator import generate_id


class RespuestaService:
    def __init__(self, respuesta_repository: Optional[RespuestaRepository] = None):
        self.respuesta_repository = respuesta_repository or RespuestaRepository()

    def crear_respuesta(
        self,
        id_formulario: str,
        id_pregunta: str,
        respuesta_texto: Optional[str] = None,
        respuesta_numero: Optional[int] = None,
        id_opcion: Optional[str] = None,
        accion_correctiva_aplicada: Optional[str] = None,
    ) -> Respuesta:
        self._validar_datos_obligatorios(
            id_formulario=id_formulario,
            id_pregunta=id_pregunta,
        )

        self._validar_contenido_respuesta(
            respuesta_texto=respuesta_texto,
            respuesta_numero=respuesta_numero,
            id_opcion=id_opcion,
        )

        registros_existentes = [
            respuesta.to_dict() for respuesta in self.respuesta_repository.list_all()
        ]

        id_respuesta = generate_id(
            prefix="RESP",
            records=registros_existentes,
            field_name="id_respuesta",
        )

        respuesta = Respuesta(
            id_respuesta=id_respuesta,
            id_formulario=id_formulario.strip(),
            id_pregunta=id_pregunta.strip(),
            respuesta_texto=respuesta_texto.strip() if isinstance(respuesta_texto, str) else respuesta_texto,
            respuesta_numero=respuesta_numero,
            id_opcion=id_opcion.strip() if isinstance(id_opcion, str) else id_opcion,
            accion_correctiva_aplicada=(
                accion_correctiva_aplicada.strip()
                if isinstance(accion_correctiva_aplicada, str)
                else accion_correctiva_aplicada
            ),
        )

        self.respuesta_repository.add_respuesta(respuesta)
        return respuesta

    def guardar_respuestas_formulario(
        self,
        id_formulario: str,
        respuestas: list[dict[str, Any]],
    ) -> list[Respuesta]:
        if not id_formulario or not str(id_formulario).strip():
            raise ValidationError("El id_formulario es obligatorio.")

        if not isinstance(respuestas, list):
            raise ValidationError("Las respuestas deben venir en una lista.")

        respuestas_creadas: list[Respuesta] = []

        for item in respuestas:
            if not isinstance(item, dict):
                raise ValidationError("Cada respuesta debe venir en formato dict.")

            respuesta = self.crear_respuesta(
                id_formulario=id_formulario.strip(),
                id_pregunta=item.get("id_pregunta", ""),
                respuesta_texto=item.get("respuesta_texto"),
                respuesta_numero=item.get("respuesta_numero"),
                id_opcion=item.get("id_opcion"),
                accion_correctiva_aplicada=item.get("accion_correctiva_aplicada"),
            )
            respuestas_creadas.append(respuesta)

        return respuestas_creadas

    def obtener_respuesta_por_id(self, id_respuesta: str) -> Respuesta:
        if not id_respuesta or not id_respuesta.strip():
            raise ValidationError("El id_respuesta es obligatorio.")

        respuesta = self.respuesta_repository.get_by_id(id_respuesta.strip())
        if not respuesta:
            raise NotFoundError(f"No se encontró la respuesta '{id_respuesta}'.")

        return respuesta

    def listar_respuestas(self) -> list[Respuesta]:
        return self.respuesta_repository.list_all()

    def listar_respuestas_por_formulario(self, id_formulario: str) -> list[Respuesta]:
        if not id_formulario or not id_formulario.strip():
            raise ValidationError("El id_formulario es obligatorio.")

        return self.respuesta_repository.get_respuestas_por_formulario(id_formulario.strip())

    def listar_respuestas_por_pregunta(self, id_pregunta: str) -> list[Respuesta]:
        if not id_pregunta or not id_pregunta.strip():
            raise ValidationError("El id_pregunta es obligatorio.")

        return self.respuesta_repository.get_respuestas_por_pregunta(id_pregunta.strip())

    def actualizar_respuesta(
        self,
        id_respuesta: str,
        id_formulario: str,
        id_pregunta: str,
        respuesta_texto: Optional[str] = None,
        respuesta_numero: Optional[int] = None,
        id_opcion: Optional[str] = None,
        accion_correctiva_aplicada: Optional[str] = None,
    ) -> Respuesta:
        if not id_respuesta or not id_respuesta.strip():
            raise ValidationError("El id_respuesta es obligatorio.")

        self._validar_datos_obligatorios(
            id_formulario=id_formulario,
            id_pregunta=id_pregunta,
        )

        self._validar_contenido_respuesta(
            respuesta_texto=respuesta_texto,
            respuesta_numero=respuesta_numero,
            id_opcion=id_opcion,
        )

        _ = self.obtener_respuesta_por_id(id_respuesta.strip())

        respuesta_actualizada = Respuesta(
            id_respuesta=id_respuesta.strip(),
            id_formulario=id_formulario.strip(),
            id_pregunta=id_pregunta.strip(),
            respuesta_texto=respuesta_texto.strip() if isinstance(respuesta_texto, str) else respuesta_texto,
            respuesta_numero=respuesta_numero,
            id_opcion=id_opcion.strip() if isinstance(id_opcion, str) else id_opcion,
            accion_correctiva_aplicada=(
                accion_correctiva_aplicada.strip()
                if isinstance(accion_correctiva_aplicada, str)
                else accion_correctiva_aplicada
            ),
        )

        self.respuesta_repository.update(respuesta_actualizada)
        return respuesta_actualizada

    def _validar_datos_obligatorios(
        self,
        id_formulario: str,
        id_pregunta: str,
    ) -> None:
        if not id_formulario or not str(id_formulario).strip():
            raise ValidationError("El id_formulario es obligatorio.")

        if not id_pregunta or not str(id_pregunta).strip():
            raise ValidationError("El id_pregunta es obligatorio.")

    def _validar_contenido_respuesta(
        self,
        respuesta_texto: Optional[str],
        respuesta_numero: Optional[int],
        id_opcion: Optional[str],
    ) -> None:
        tiene_texto = isinstance(respuesta_texto, str) and bool(respuesta_texto.strip())
        tiene_numero = respuesta_numero is not None
        tiene_opcion = isinstance(id_opcion, str) and bool(id_opcion.strip())

        if not (tiene_texto or tiene_numero or tiene_opcion):
            raise ValidationError(
                "La respuesta debe tener al menos uno de estos valores: respuesta_texto, respuesta_numero o id_opcion."
            )