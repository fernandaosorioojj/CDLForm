"""Servicios para leer configuracion JobTrack, homologar estaciones y consultar SQL productivo.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from typing import Any


# Bloque CDLform: clase CatalogoContextoService; agrupa estado y comportamiento de esta parte del flujo.
class CatalogoContextoService:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        apontamento_query_service=None,
        usar_sql_catalogos: bool = True,
    ) -> None:
        self.apontamento_query_service = apontamento_query_service
        self.usar_sql_catalogos = usar_sql_catalogos
        self._ultimo_error_catalogo_sql: Exception | None = None
        self._ultimo_error_homologacion_sql: Exception | None = None

    # Bloque CDLform: funcion/metodo _obtener_apontamento_query_service; encapsula una operacion del flujo del modulo.
    def _obtener_apontamento_query_service(self):
        if self.apontamento_query_service is None:
            from services.jobtrack.apontamento_query_service import ApontamentoQueryService

            self.apontamento_query_service = ApontamentoQueryService(
                catalogo_contexto_service=self
            )

        return self.apontamento_query_service

    # Bloque CDLform: funcion/metodo _normalizar_lista; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_lista(valores: list[Any]) -> list[str]:
        normalizados: list[str] = []

        for valor in valores:
            valor_normalizado = str(valor).strip()
            if valor_normalizado and valor_normalizado not in normalizados:
                normalizados.append(valor_normalizado)

        return normalizados

    # Bloque CDLform: funcion/metodo _obtener_catalogo_desde_sql; encapsula una operacion del flujo del modulo.
    def _obtener_catalogo_desde_sql(self, nombre_metodo: str) -> list[str]:
        if not self.usar_sql_catalogos:
            return []

        try:
            query_service = self._obtener_apontamento_query_service()
            metodo = getattr(query_service, nombre_metodo)
            resultado = metodo()
            self._ultimo_error_catalogo_sql = None
            return self._normalizar_lista(resultado)
        except Exception as exc:
            self._ultimo_error_catalogo_sql = exc
            return []

    # Bloque CDLform: funcion/metodo listar_cod_recursos; encapsula una operacion del flujo del modulo.
    def listar_cod_recursos(self) -> list[str]:
        return self._obtener_catalogo_desde_sql(
            "listar_cod_recursos_disponibles"
        )

    # Bloque CDLform: funcion/metodo listar_cod_recurso; encapsula una operacion del flujo del modulo.
    def listar_cod_recurso(self) -> list[str]:
        return self.listar_cod_recursos()

    # Bloque CDLform: funcion/metodo listar_cod_setores; encapsula una operacion del flujo del modulo.
    def listar_cod_setores(self) -> list[str]:
        return self._obtener_catalogo_desde_sql(
            "listar_cod_setores_disponibles"
        )

    # Bloque CDLform: funcion/metodo listar_cod_setor; encapsula una operacion del flujo del modulo.
    def listar_cod_setor(self) -> list[str]:
        return self.listar_cod_setores()

    # Bloque CDLform: funcion/metodo listar_turnos; encapsula una operacion del flujo del modulo.
    def listar_turnos(self) -> list[str]:
        return self._obtener_catalogo_desde_sql(
            "listar_turnos_disponibles"
        )

    # Bloque CDLform: funcion/metodo listar_contextos_recurso_setor; encapsula una operacion del flujo del modulo.
    def listar_contextos_recurso_setor(self) -> list[dict[str, str]]:
        if not self.usar_sql_catalogos:
            return []

        try:
            query_service = self._obtener_apontamento_query_service()
            resultado = query_service.listar_contextos_recurso_setor_disponibles()
            self._ultimo_error_catalogo_sql = None
            return [
                {
                    "cod_recurso": str(item.get("cod_recurso", "")).strip(),
                    "cod_setor": str(item.get("cod_setor", "")).strip(),
                }
                for item in resultado
                if str(item.get("cod_recurso", "")).strip()
                and str(item.get("cod_setor", "")).strip()
            ]
        except Exception as exc:
            self._ultimo_error_catalogo_sql = exc
            return []

    # Bloque CDLform: funcion/metodo listar_tipos_trabajo; encapsula una operacion del flujo del modulo.
    def listar_tipos_trabajo(self) -> list[str]:
        # LEGACY / NO FLUJO ACTUAL:
        # Placeholder conservado por compatibilidad con pantallas antiguas.
        # Actualmente no hay catalogo real de tipo_trabajo.
        return []

    # Bloque CDLform: funcion/metodo obtener_cod_recursos_por_estacion; encapsula una operacion del flujo del modulo.
    def obtener_cod_recursos_por_estacion(self, estacion: str) -> list[str]:
        estacion_normalizada = str(estacion).strip()

        if not estacion_normalizada:
            raise ValueError("La estaciÃ³n no puede venir vacÃ­a.")

        recursos_sql = self._obtener_cod_recursos_estacion_desde_sql(
            estacion_normalizada
        )
        if recursos_sql:
            return recursos_sql

        if self._ultimo_error_homologacion_sql is not None:
            raise RuntimeError(
                "No se pudo consultar la homologacion SQL de estacion a CodRecurso "
                f"para {estacion_normalizada}: {self._ultimo_error_homologacion_sql}"
            ) from self._ultimo_error_homologacion_sql

        raise ValueError(
            "No existe homologaciÃ³n SQL de estaciÃ³n a CodRecurso para: "
            f"{estacion_normalizada}. Revise la tabla "
            "MetricsBetaProductivo.dbo.jbt_EstacaoXMaquinas."
        )

    # Bloque CDLform: funcion/metodo _obtener_cod_recursos_estacion_desde_sql; encapsula una operacion del flujo del modulo.
    def _obtener_cod_recursos_estacion_desde_sql(
        self,
        estacion: str,
    ) -> list[str]:
        if not self.usar_sql_catalogos:
            return []

        try:
            query_service = self._obtener_apontamento_query_service()
            resultado = self._normalizar_lista(
                query_service.listar_cod_recursos_por_cod_estacao(estacion)
            )
            self._ultimo_error_homologacion_sql = None
            return resultado
        except Exception as exc:
            self._ultimo_error_homologacion_sql = exc
            return []

    # Bloque CDLform: funcion/metodo homologar_estacion_a_cod_recursos; encapsula una operacion del flujo del modulo.
    def homologar_estacion_a_cod_recursos(self, estacion: str) -> list[str]:
        return self.obtener_cod_recursos_por_estacion(estacion)

    # Bloque CDLform: funcion/metodo resolver_contexto_desde_estacion; encapsula una operacion del flujo del modulo.
    def resolver_contexto_desde_estacion(self, estacion: str) -> dict[str, object]:
        estacion_normalizada = str(estacion).strip()

        return {
            "estacion": estacion_normalizada,
            "cod_recursos": self.obtener_cod_recursos_por_estacion(
                estacion_normalizada
            ),
        }

    # Bloque CDLform: funcion/metodo construir_placeholders_in; encapsula una operacion del flujo del modulo.
    @staticmethod
    def construir_placeholders_in(cantidad: int) -> str:
        if cantidad <= 0:
            raise ValueError("La cantidad de placeholders debe ser mayor que cero.")

        return ", ".join("?" for _ in range(cantidad))
