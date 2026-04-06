from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pyodbc


class ApontamentoQueryService:
    def __init__(
        self,
        server: str,
        database: str,
        username: str,
        password: str,
        driver: str = "ODBC Driver 18 for SQL Server",
        estaciones_file: str | Path = "storage/estaciones_recursos.json",
        usar_estacion_como_recurso_por_defecto: bool = True,
    ) -> None:
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver

        self.estaciones_file = Path(estaciones_file)
        self.usar_estacion_como_recurso_por_defecto = usar_estacion_como_recurso_por_defecto
        self._ensure_estaciones_file()

    def _ensure_estaciones_file(self) -> None:
        self.estaciones_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.estaciones_file.exists():
            self.estaciones_file.write_text("[]", encoding="utf-8")

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def _read_estaciones_data(self) -> list[dict[str, Any]]:
        try:
            data = json.loads(self.estaciones_file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
            return []
        except Exception:
            return []

    def _normalizar_lista_recursos(self, valor: Any) -> list[str]:
        if valor is None:
            return []

        if isinstance(valor, list):
            resultado: list[str] = []
            for item in valor:
                texto = self._normalizar_texto(item)
                if texto and texto not in resultado:
                    resultado.append(texto)
            return resultado

        texto = self._normalizar_texto(valor)
        if not texto:
            return []

        if "," in texto:
            resultado: list[str] = []
            for item in texto.split(","):
                normalizado = self._normalizar_texto(item)
                if normalizado and normalizado not in resultado:
                    resultado.append(normalizado)
            return resultado

        return [texto]

    def _resolver_codigos_recurso(self, estacion: str) -> list[str]:
        estacion_normalizada = self._normalizar_texto(estacion)

        if not estacion_normalizada:
            return []

        for item in self._read_estaciones_data():
            estacion_item = self._normalizar_texto(
                item.get("estacion")
                or item.get("estacao")
                or item.get("estacao_local")
            )

            if estacion_item != estacion_normalizada:
                continue

            recursos = self._normalizar_lista_recursos(
                item.get("codigos_recurso")
                or item.get("cod_recurso")
                or item.get("recursos")
            )

            if recursos:
                return recursos

        if self.usar_estacion_como_recurso_por_defecto:
            return [estacion_normalizada]

        return []

    def _get_connection(self) -> pyodbc.Connection:
        connection_string = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "TrustServerCertificate=yes;"
        )
        return pyodbc.connect(connection_string)

    def buscar_apontamentos_pendientes(
        self,
        estacion: str,
        ids_excluidos: set[str] | None = None,
    ) -> list[dict[str, Any]]:
        codigos_recurso = self._resolver_codigos_recurso(estacion)

        if not codigos_recurso:
            return []

        ids_excluidos = ids_excluidos or set()
        placeholders = ", ".join("?" for _ in codigos_recurso)

        sql = f"""
        SELECT
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
            [JustificativaPerda]
        FROM [MetricsProd].[dbo].[Apontamentos]
        WHERE [HoraFim] IS NOT NULL
          AND [HoraFim] <> '1899-12-30 00:00:00.000'
          AND [CodRecurso] IN ({placeholders})
        ORDER BY [HoraFim] DESC
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(codigos_recurso))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

        candidatos: list[dict[str, Any]] = []

        for row in rows:
            registro = dict(zip(columns, row))
            id_apontamento = self._normalizar_texto(registro.get("IdApontamento"))

            if not id_apontamento:
                continue

            if id_apontamento in ids_excluidos:
                continue

            candidatos.append(registro)

        return candidatos