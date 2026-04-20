from __future__ import annotations

from typing import Any


class CatalogoContextoService:
    def __init__(
        self,
        apontamento_query_service=None,
        usar_sql_catalogos: bool = True,
    ) -> None:
        self.apontamento_query_service = apontamento_query_service
        self.usar_sql_catalogos = usar_sql_catalogos

    def _obtener_apontamento_query_service(self):
        if self.apontamento_query_service is None:
            from services.jobtrack.apontamento_query_service import ApontamentoQueryService

            self.apontamento_query_service = ApontamentoQueryService(
                catalogo_contexto_service=self
            )

        return self.apontamento_query_service

    @staticmethod
    def _normalizar_lista(valores: list[Any]) -> list[str]:
        normalizados: list[str] = []

        for valor in valores:
            valor_normalizado = str(valor).strip()
            if valor_normalizado and valor_normalizado not in normalizados:
                normalizados.append(valor_normalizado)

        return normalizados

    def _obtener_catalogo_desde_sql(self, nombre_metodo: str) -> list[str]:
        if not self.usar_sql_catalogos:
            return []

        try:
            query_service = self._obtener_apontamento_query_service()
            metodo = getattr(query_service, nombre_metodo)
            resultado = metodo()
            return self._normalizar_lista(resultado)
        except Exception:
            return []

    def listar_cod_recursos(self) -> list[str]:
        return self._obtener_catalogo_desde_sql(
            "listar_cod_recursos_disponibles"
        )

    def listar_cod_recurso(self) -> list[str]:
        return self.listar_cod_recursos()

    def listar_cod_setores(self) -> list[str]:
        return self._obtener_catalogo_desde_sql(
            "listar_cod_setores_disponibles"
        )

    def listar_cod_setor(self) -> list[str]:
        return self.listar_cod_setores()

    def listar_turnos(self) -> list[str]:
        return self._obtener_catalogo_desde_sql(
            "listar_turnos_disponibles"
        )

    def listar_tipos_trabajo(self) -> list[str]:
        return []

    def obtener_cod_recursos_por_estacion(self, estacion: str) -> list[str]:
        estacion_normalizada = str(estacion).strip()

        if not estacion_normalizada:
            raise ValueError("La estaciÃ³n no puede venir vacÃ­a.")

        recursos_sql = self._obtener_cod_recursos_estacion_desde_sql(
            estacion_normalizada
        )
        if recursos_sql:
            return recursos_sql

        raise ValueError(
            "No existe homologaciÃ³n SQL de estaciÃ³n a CodRecurso para: "
            f"{estacion_normalizada}. Revise la tabla "
            "MetricsBetaProductivo.dbo.jbt_EstacaoXMaquinas."
        )

    def _obtener_cod_recursos_estacion_desde_sql(
        self,
        estacion: str,
    ) -> list[str]:
        if not self.usar_sql_catalogos:
            return []

        try:
            query_service = self._obtener_apontamento_query_service()
            return self._normalizar_lista(
                query_service.listar_cod_recursos_por_cod_estacao(estacion)
            )
        except Exception:
            return []

    def homologar_estacion_a_cod_recursos(self, estacion: str) -> list[str]:
        return self.obtener_cod_recursos_por_estacion(estacion)

    def resolver_contexto_desde_estacion(self, estacion: str) -> dict[str, object]:
        estacion_normalizada = str(estacion).strip()

        return {
            "estacion": estacion_normalizada,
            "cod_recursos": self.obtener_cod_recursos_por_estacion(
                estacion_normalizada
            ),
        }

    @staticmethod
    def construir_placeholders_in(cantidad: int) -> str:
        if cantidad <= 0:
            raise ValueError("La cantidad de placeholders debe ser mayor que cero.")

        return ", ".join("?" for _ in range(cantidad))
