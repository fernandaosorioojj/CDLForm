from __future__ import annotations

from typing import Any

from models.formulario import Formulario
from services.formulario_service import FormularioService
from services.respuesta_service import RespuestaService


class ReporteService:
    def __init__(
        self,
        formulario_service: FormularioService | None = None,
        respuesta_service: RespuestaService | None = None,
    ) -> None:
        self.formulario_service = formulario_service or FormularioService()
        self.respuesta_service = respuesta_service or RespuestaService()

    @staticmethod
    def _formulario_a_dict(formulario: Formulario) -> dict[str, Any]:
        return formulario.to_dict()

    def listar_formularios(self) -> list[Formulario]:
        return self.formulario_service.listar_formularios()

    def listar_formularios_completados(self) -> list[Formulario]:
        return self.formulario_service.listar_formularios_por_estado("completado")

    def obtener_formulario(self, id_formulario: str) -> Formulario | None:
        return self.formulario_service.obtener_formulario_por_id(id_formulario)

    def obtener_respuestas_de_formulario(self, id_formulario: str) -> list[dict]:
        respuestas = self.respuesta_service.listar_respuestas_por_formulario(
            id_formulario
        )
        return [respuesta.to_dict() for respuesta in respuestas]

    def generar_reporte(
        self,
        estado: str | None = None,
    ) -> list[dict[str, Any]]:
        formularios = self.formulario_service.listar_formularios()

        estado_normalizado = str(estado or "").strip()
        if estado_normalizado:
            formularios = [
                formulario
                for formulario in formularios
                if formulario.estado == estado_normalizado
            ]

        formularios_ordenados = sorted(
            formularios,
            key=lambda formulario: (
                formulario.fecha_formulario,
                formulario.id_formulario,
            ),
            reverse=True,
        )

        return [
            self._formulario_a_dict(formulario)
            for formulario in formularios_ordenados
        ]