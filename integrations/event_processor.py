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
        usar_fallback_consulta: bool = True,
    ) -> dict[str, Any]:
        return self.procesar_ciclo_estacion_actual(
            evento=evento,
            usar_fallback_consulta=usar_fallback_consulta,
        )

    def procesar_ciclo_estacion_actual(
        self,
        evento: dict[str, Any] | None = None,
        limit_consulta: int = 50,
        limit_creacion: int = 50,
        solo_finalizados: bool = True,
        solo_con_num_ordem: bool = True,
        usar_fallback_consulta: bool = True,
    ) -> dict[str, Any]:
        origen_sincronizacion = "cola_sql"

        try:
            resultado_sincronizacion = (
                self.apontamento_procesado_service.sincronizar_y_crear_formularios_desde_cola_sql(
                    limit_consulta=limit_consulta,
                    solo_con_num_ordem=solo_con_num_ordem,
                )
            )
        except Exception as exc:
            if not usar_fallback_consulta:
                raise

            origen_sincronizacion = "consulta_apontamentos"
            resultado_sincronizacion = (
                self.apontamento_procesado_service.sincronizar_y_crear_formularios_estacion_actual(
                    limit_consulta=limit_consulta,
                    limit_creacion=limit_creacion,
                    solo_finalizados=solo_finalizados,
                    solo_con_num_ordem=solo_con_num_ordem,
                )
            )
            resultado_sincronizacion["error_cola_sql"] = str(exc)

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
