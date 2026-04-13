from __future__ import annotations

from typing import Any

from services.workflows.apontamento_procesado_service import ApontamentoProcesadoService
from services.workflows.disparador_service import DisparadorService


class EventProcessor:
    def __init__(
        self,
        apontamento_procesado_service: ApontamentoProcesadoService | None = None,
        disparador_service: DisparadorService | None = None,
    ) -> None:
        self.apontamento_procesado_service = (
            apontamento_procesado_service or ApontamentoProcesadoService()
        )
        self.disparador_service = disparador_service or DisparadorService()

    def procesar_evento_externo(
        self,
        evento: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.procesar_ciclo_estacion_actual(evento=evento)

    def procesar_ciclo_estacion_actual(
        self,
        evento: dict[str, Any] | None = None,
        limit_consulta: int = 50,
        limit_creacion: int = 50,
        solo_finalizados: bool = True,
        solo_con_num_ordem: bool = True,
    ) -> dict[str, Any]:
        resultado_sincronizacion = (
            self.apontamento_procesado_service.sincronizar_y_crear_formularios_estacion_actual(
                limit_consulta=limit_consulta,
                limit_creacion=limit_creacion,
                solo_finalizados=solo_finalizados,
                solo_con_num_ordem=solo_con_num_ordem,
            )
        )

        resultado_disparo = self.disparador_service.disparar_siguiente_formulario_pendiente()

        return {
            "evento_recibido": evento or {},
            "contexto": resultado_sincronizacion["contexto"],
            "total_consultados": resultado_sincronizacion["total_consultados"],
            "total_pendientes_nuevos": resultado_sincronizacion[
                "total_pendientes_nuevos"
            ],
            "total_registrados_en_cola": resultado_sincronizacion[
                "total_registrados_en_cola"
            ],
            "total_formularios_creados": resultado_sincronizacion[
                "total_formularios_creados"
            ],
            "total_formularios_existentes": resultado_sincronizacion[
                "total_formularios_existentes"
            ],
            "total_errores_formulario": resultado_sincronizacion[
                "total_errores_formulario"
            ],
            "resultado_disparo": resultado_disparo,
        }
