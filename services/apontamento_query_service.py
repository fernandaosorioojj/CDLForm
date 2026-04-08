from __future__ import annotations

from typing import Any, Sequence

import pyodbc

from config.sql_server_config import build_connection_string
from services.catalogo_contexto_service import CatalogoContextoService
from services.jobtrack_config_service import JobtrackConfigService


class ApontamentoQueryService:
    def __init__(
        self,
        catalogo_contexto_service: CatalogoContextoService | None = None,
        jobtrack_config_service: JobtrackConfigService | None = None,
    ) -> None:
        self.catalogo_contexto_service = (
            catalogo_contexto_service or CatalogoContextoService()
        )
        self.jobtrack_config_service = (
            jobtrack_config_service or JobtrackConfigService()
        )

    @staticmethod
    def _normalizar_cod_recursos(cod_recursos: Sequence[str]) -> list[str]:
        normalizados = [
            str(cod).strip()
            for cod in cod_recursos
            if str(cod).strip()
        ]

        unicos: list[str] = []
        for cod in normalizados:
            if cod not in unicos:
                unicos.append(cod)

        if not unicos:
            raise ValueError(
                "Debe indicar al menos un CodRecurso válido para consultar apuntamientos."
            )

        return unicos

    @staticmethod
    def _normalizar_limit(limit: int) -> int:
        limit_normalizado = int(limit)

        if limit_normalizado <= 0:
            raise ValueError("El límite debe ser mayor que cero.")

        return limit_normalizado

    @staticmethod
    def _rows_to_dicts(
        cursor: pyodbc.Cursor,
        rows: list[pyodbc.Row],
    ) -> list[dict[str, Any]]:
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    def _listar_valores_distintos(
        self,
        nombre_columna: str,
        alias_columna: str,
        patron: str | None = None,
        limit: int = 100,
    ) -> list[str]:
        limit_normalizado = self._normalizar_limit(limit)

        expresion = f"LTRIM(RTRIM(CAST([{nombre_columna}] AS VARCHAR(100))))"

        sql = f"""
        SELECT DISTINCT TOP ({limit_normalizado})
            {expresion} AS {alias_columna}
        FROM [dbo].[Apontamentos]
        WHERE [{nombre_columna}] IS NOT NULL
          AND {expresion} <> ''
        """

        params: list[Any] = []

        if patron and patron.strip():
            sql += f"\n  AND {expresion} LIKE ?"
            params.append(f"%{patron.strip()}%")

        sql += f"\nORDER BY {alias_columna}"

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()

        return [str(row[0]).strip() for row in rows if str(row[0]).strip()]

    def listar_apontamentos_por_cod_recursos(
        self,
        cod_recursos: Sequence[str],
        limit: int = 20,
        solo_finalizados: bool = True,
    ) -> list[dict[str, Any]]:
        cod_recursos_normalizados = self._normalizar_cod_recursos(cod_recursos)
        limit_normalizado = self._normalizar_limit(limit)
        placeholders = self.catalogo_contexto_service.construir_placeholders_in(
            len(cod_recursos_normalizados)
        )

        where_clauses: list[str] = []
        params: list[Any] = []

        if solo_finalizados:
            where_clauses.append("[HoraFim] IS NOT NULL")
            where_clauses.append("[HoraFim] <> '1899-12-30 00:00:00.000'")

        where_clauses.append(f"LTRIM(RTRIM([CodRecurso])) IN ({placeholders})")
        params.extend(cod_recursos_normalizados)

        sql = f"""
        SELECT TOP ({limit_normalizado})
            [IdApontamento],
            [NumOrdem],
            [CodRecurso],
            [CodSetor],
            [CodAtiv],
            [Turno],
            [HoraFim],
            [Operador],
            [DescricaoOP],
            [DescricaoProcesso],
            [QtdProduzida],
            [QtdPlanejado],
            [QtdPerdas],
            [JustificativaPerda],
            [Obs]
        FROM [dbo].[Apontamentos]
        WHERE {" AND ".join(where_clauses)}
        ORDER BY [HoraFim] DESC, [IdApontamento] DESC
        """

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()
            return self._rows_to_dicts(cursor, rows)

    def listar_apontamentos_por_estacion(
        self,
        estacion: str,
        limit: int = 20,
        solo_finalizados: bool = True,
    ) -> list[dict[str, Any]]:
        cod_recursos = self.catalogo_contexto_service.obtener_cod_recursos_por_estacion(
            estacion
        )

        return self.listar_apontamentos_por_cod_recursos(
            cod_recursos=cod_recursos,
            limit=limit,
            solo_finalizados=solo_finalizados,
        )

    def listar_apontamentos_estacion_actual(
        self,
        limit: int = 20,
        solo_finalizados: bool = True,
    ) -> list[dict[str, Any]]:
        estacion = self.jobtrack_config_service.obtener_estacion_local()

        return self.listar_apontamentos_por_estacion(
            estacion=estacion,
            limit=limit,
            solo_finalizados=solo_finalizados,
        )

    def obtener_contexto_estacion_actual(self) -> dict[str, object]:
        estacion = self.jobtrack_config_service.obtener_estacion_local()
        return self.catalogo_contexto_service.resolver_contexto_desde_estacion(estacion)

    def listar_cod_recursos_disponibles(
        self,
        patron: str | None = None,
        limit: int = 100,
    ) -> list[str]:
        return self._listar_valores_distintos(
            nombre_columna="CodRecurso",
            alias_columna="CodRecurso",
            patron=patron,
            limit=limit,
        )

    def listar_cod_setores_disponibles(
        self,
        patron: str | None = None,
        limit: int = 100,
    ) -> list[str]:
        return self._listar_valores_distintos(
            nombre_columna="CodSetor",
            alias_columna="CodSetor",
            patron=patron,
            limit=limit,
        )

    def listar_turnos_disponibles(
        self,
        patron: str | None = None,
        limit: int = 100,
    ) -> list[str]:
        return self._listar_valores_distintos(
            nombre_columna="Turno",
            alias_columna="Turno",
            patron=patron,
            limit=limit,
        )

    def listar_cod_ativ_disponibles(
        self,
        patron: str | None = None,
        limit: int = 100,
    ) -> list[str]:
        return self._listar_valores_distintos(
            nombre_columna="CodAtiv",
            alias_columna="CodAtiv",
            patron=patron,
            limit=limit,
        )