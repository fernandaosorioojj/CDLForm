from __future__ import annotations

from typing import Any

from services.workflows.apontamento_procesado_service import ApontamentoProcesadoService


class EventProcessor:
    def __init__(
        self,
        apontamento_procesado_service: ApontamentoProcesadoService | None = None,
    ) -> None:
        self.apontamento_procesado_service = (
            apontamento_procesado_service or ApontamentoProcesadoService()
        )

    def procesar_evento_externo(
        self,
        evento: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.procesar_ciclo_estacion_actual(
            evento=evento,
        )

    def procesar_ciclo_estacion_actual(
        self,
        evento: dict[str, Any] | None = None,
        limit_consulta: int = 50,
        solo_con_num_ordem: bool = True,
    ) -> dict[str, Any]:
        origen_sincronizacion = "cola_sql"
        resultado_sincronizacion = (
            self.apontamento_procesado_service.sincronizar_y_crear_formularios_desde_cola_sql(
                limit_consulta=limit_consulta,
                solo_con_num_ordem=solo_con_num_ordem,
            )
        )

        # Respaldo de emergencia documentado:
        # Si la cola [dbo].[eventos_op_pendientes] queda inutilizable, un
        # desarrollador puede ejecutar manualmente
        # ApontamentoProcesadoService.sincronizar_y_crear_formularios_estacion_actual(...)
        # para reconstruir desde [dbo].[Apontamentos]. No se usa como fallback
        # automatico para mantener limpia y auditable la logica productiva.

        return {
            "evento_recibido": evento or {},
            "origen_sincronizacion": origen_sincronizacion,
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
            "total_omitidos_ya_procesados": resultado_sincronizacion.get(
                "total_omitidos_ya_procesados", 0
            ),
            "total_omitidos_sin_num_ordem": resultado_sincronizacion.get(
                "total_omitidos_sin_num_ordem", 0
            ),
            "errores": resultado_sincronizacion.get("errores", []),
        }
