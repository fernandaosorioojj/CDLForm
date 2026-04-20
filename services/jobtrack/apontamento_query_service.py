from __future__ import annotations

from typing import Any, Sequence

import pyodbc

from config.sql_server_config import build_connection_string
from services.jobtrack.catalogo_contexto_service import CatalogoContextoService
from services.jobtrack.jobtrack_config_service import JobtrackConfigService


class ApontamentoQueryService:
    COLUMNAS_SUPERVISOR_CANDIDATAS = (
        "Supervisor",
        "CodSupervisor",
        "NombreSupervisor",
        "NomeSupervisor",
        "SupervisorNome",
        "Lider",
        "Encargado",
    )

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
                "Debe indicar al menos un CodRecurso vÃ¡lido para consultar apuntamientos."
            )

        return unicos

    @staticmethod
    def _normalizar_limit(limit: int) -> int:
        limit_normalizado = int(limit)

        if limit_normalizado <= 0:
            raise ValueError("El lÃ­mite debe ser mayor que cero.")

        return limit_normalizado

    @staticmethod
    def _rows_to_dicts(
        cursor: pyodbc.Cursor,
        rows: list[pyodbc.Row],
    ) -> list[dict[str, Any]]:
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    @staticmethod
    def _normalizar_id_apontamentos(
        id_apontamentos: Sequence[Any],
    ) -> list[str]:
        normalizados: list[str] = []
        for valor in id_apontamentos:
            texto = str(valor or "").strip()
            if texto and texto not in normalizados:
                normalizados.append(texto)
        return normalizados

    @staticmethod
    def _normalizar_id_evento(valor: Any) -> str:
        texto = str(valor or "").strip()
        if not texto:
            raise ValueError("El id_evento no puede venir vacio.")
        return texto

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

    def listar_operadores_por_contexto(
        self,
        cod_setor: str,
        cod_recurso: str,
        patron: str | None = None,
        limit: int = 500,
    ) -> list[str]:
        cod_setor_normalizado = str(cod_setor or "").strip()
        cod_recurso_normalizado = str(cod_recurso or "").strip()
        limit_normalizado = self._normalizar_limit(limit)

        if not cod_setor_normalizado:
            raise ValueError("Debe indicar un CodSetor para consultar operadores.")

        if not cod_recurso_normalizado:
            raise ValueError("Debe indicar un CodRecurso para consultar operadores.")

        expresion_operador = "LTRIM(RTRIM(CAST([Operador] AS VARCHAR(160))))"

        sql = f"""
        SELECT DISTINCT TOP ({limit_normalizado})
            {expresion_operador} AS Operador
        FROM [dbo].[Apontamentos]
        WHERE [Operador] IS NOT NULL
          AND {expresion_operador} <> ''
          AND LTRIM(RTRIM(CAST([CodSetor] AS VARCHAR(100)))) = ?
          AND LTRIM(RTRIM(CAST([CodRecurso] AS VARCHAR(100)))) = ?
        """

        params: list[Any] = [cod_setor_normalizado, cod_recurso_normalizado]

        if patron and patron.strip():
            sql += f"\n  AND {expresion_operador} LIKE ?"
            params.append(f"%{patron.strip()}%")

        sql += "\nORDER BY Operador"

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()

        return [str(row[0]).strip() for row in rows if str(row[0]).strip()]

    def listar_operadores_registrados(
        self,
        patron: str | None = None,
        limit: int | None = None,
    ) -> list[str]:
        expresion_operador = "LTRIM(RTRIM(CAST([Operador] AS VARCHAR(160))))"
        top_clause = ""
        if limit is not None:
            top_clause = f"TOP ({self._normalizar_limit(limit)}) "

        sql = f"""
        SELECT DISTINCT {top_clause}
            {expresion_operador} AS Operador
        FROM [dbo].[Apontamentos]
        WHERE [Operador] IS NOT NULL
          AND {expresion_operador} <> ''
        """

        params: list[Any] = []

        if patron and patron.strip():
            sql += f"\n  AND {expresion_operador} LIKE ?"
            params.append(f"%{patron.strip()}%")

        sql += "\nORDER BY Operador"

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()

        return [str(row[0]).strip() for row in rows if str(row[0]).strip()]

    def listar_cod_recursos_por_cod_estacao(
        self,
        cod_estacao: str,
    ) -> list[str]:
        cod_estacao_normalizado = str(cod_estacao or "").strip()
        if not cod_estacao_normalizado:
            raise ValueError("Debe indicar un CodEstacao para homologar recursos.")

        expresion_estacao = "LTRIM(RTRIM(CAST([CodEstacao] AS VARCHAR(100))))"
        expresion_recurso = "LTRIM(RTRIM(CAST([CodRecurso] AS VARCHAR(100))))"

        sql = f"""
        SELECT DISTINCT
            {expresion_recurso} AS CodRecurso
        FROM [dbo].[jbt_EstacaoXMaquinas]
        WHERE [CodEstacao] IS NOT NULL
          AND {expresion_estacao} = ?
          AND [CodRecurso] IS NOT NULL
          AND {expresion_recurso} <> ''
        ORDER BY CodRecurso
        """

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (cod_estacao_normalizado,))
            rows = cursor.fetchall()

        return [str(row[0]).strip() for row in rows if str(row[0]).strip()]

    def _resolver_columna_supervisor(self, cursor: pyodbc.Cursor) -> str | None:
        placeholders = self.catalogo_contexto_service.construir_placeholders_in(
            len(self.COLUMNAS_SUPERVISOR_CANDIDATAS)
        )
        sql = f"""
        SELECT [COLUMN_NAME]
        FROM [INFORMATION_SCHEMA].[COLUMNS]
        WHERE [TABLE_SCHEMA] = 'dbo'
          AND [TABLE_NAME] = 'Apontamentos'
          AND [COLUMN_NAME] IN ({placeholders})
        """
        cursor.execute(sql, tuple(self.COLUMNAS_SUPERVISOR_CANDIDATAS))
        disponibles = {str(row[0]).strip() for row in cursor.fetchall()}

        for columna in self.COLUMNAS_SUPERVISOR_CANDIDATAS:
            if columna in disponibles:
                return columna

        return None

    def listar_supervisores_por_id_apontamentos(
        self,
        id_apontamentos: Sequence[Any],
    ) -> dict[str, str]:
        ids = self._normalizar_id_apontamentos(id_apontamentos)
        if not ids:
            return {}

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            columna_supervisor = self._resolver_columna_supervisor(cursor)
            if not columna_supervisor:
                return {}

            placeholders = self.catalogo_contexto_service.construir_placeholders_in(
                len(ids)
            )
            expresion_id = "LTRIM(RTRIM(CAST([IdApontamento] AS VARCHAR(100))))"
            expresion_supervisor = (
                f"LTRIM(RTRIM(CAST([{columna_supervisor}] AS VARCHAR(160))))"
            )
            sql = f"""
            SELECT
                {expresion_id} AS IdApontamento,
                {expresion_supervisor} AS Supervisor
            FROM [dbo].[Apontamentos]
            WHERE {expresion_id} IN ({placeholders})
              AND [{columna_supervisor}] IS NOT NULL
              AND {expresion_supervisor} <> ''
            """
            cursor.execute(sql, tuple(ids))
            rows = cursor.fetchall()

        supervisores: dict[str, str] = {}
        for row in rows:
            id_apontamento = str(row[0] or "").strip()
            supervisor = str(row[1] or "").strip()
            if id_apontamento and supervisor:
                supervisores[id_apontamento] = supervisor

        return supervisores

    def listar_eventos_op_pendientes(
        self,
        cod_recursos: Sequence[str] | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        limit_normalizado = self._normalizar_limit(limit)
        where_clauses = ["[procesado] = 0"]
        params: list[Any] = []

        if cod_recursos is not None:
            cod_recursos_normalizados = self._normalizar_cod_recursos(cod_recursos)
            placeholders = self.catalogo_contexto_service.construir_placeholders_in(
                len(cod_recursos_normalizados)
            )
            where_clauses.append(
                f"LTRIM(RTRIM(CAST([cod_recurso] AS VARCHAR(100)))) IN ({placeholders})"
            )
            params.extend(cod_recursos_normalizados)

        sql = f"""
        SELECT TOP ({limit_normalizado})
            [id_evento],
            [id_apontamento],
            [num_ordem],
            [cod_recurso],
            [cod_setor],
            [operador],
            [turno],
            [hora_inicio],
            [hora_fim],
            [origen_evento],
            [fecha_deteccion],
            [procesado],
            [fecha_procesado],
            [mensaje_error]
        FROM [dbo].[eventos_op_pendientes]
        WHERE {" AND ".join(where_clauses)}
        ORDER BY [fecha_deteccion] ASC, [id_evento] ASC
        """

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()
            return self._rows_to_dicts(cursor, rows)

    def marcar_evento_op_pendiente_procesado(self, id_evento: Any) -> None:
        id_evento_normalizado = self._normalizar_id_evento(id_evento)
        sql = """
        UPDATE [dbo].[eventos_op_pendientes]
        SET
            [procesado] = 1,
            [fecha_procesado] = GETDATE(),
            [mensaje_error] = NULL
        WHERE [id_evento] = ?
        """

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_evento_normalizado,))
            conn.commit()

    def marcar_evento_op_pendiente_error(
        self,
        id_evento: Any,
        mensaje_error: str,
    ) -> None:
        id_evento_normalizado = self._normalizar_id_evento(id_evento)
        mensaje = str(mensaje_error or "").strip()
        if len(mensaje) > 500:
            mensaje = mensaje[:497] + "..."

        sql = """
        UPDATE [dbo].[eventos_op_pendientes]
        SET [mensaje_error] = ?
        WHERE [id_evento] = ?
        """

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (mensaje, id_evento_normalizado))
            conn.commit()

    def marcar_evento_op_pendiente_omitido(
        self,
        id_evento: Any,
        motivo: str,
    ) -> None:
        id_evento_normalizado = self._normalizar_id_evento(id_evento)
        mensaje = str(motivo or "").strip()
        if len(mensaje) > 500:
            mensaje = mensaje[:497] + "..."

        sql = """
        UPDATE [dbo].[eventos_op_pendientes]
        SET
            [procesado] = 1,
            [fecha_procesado] = GETDATE(),
            [mensaje_error] = ?
        WHERE [id_evento] = ?
        """

        with pyodbc.connect(build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (mensaje, id_evento_normalizado))
            conn.commit()

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

