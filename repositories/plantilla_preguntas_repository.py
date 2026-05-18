"""Acceso a datos SQL Server para entidades del dominio CDLform.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pyodbc

from database.sql_connection import get_sql_connection
from models.plantilla_preguntas import PlantillaPreguntaItem, PlantillaPreguntas
from repositories.base_repository import BaseRepository
from utils.json_manager import JsonManager


# FLUJO ACTUAL:
# Sin file_path, este repositorio usa SQL Server para plantillas y sus items.
#
# LEGACY:
# Si se instancia manualmente con file_path, usa JSON. Esa ruta no participa
# en el flujo vigente de gestion, operario ni MQTT/watchdog.
# Bloque CDLform: clase PlantillaPreguntasRepository; agrupa estado y comportamiento de esta parte del flujo.
class PlantillaPreguntasRepository:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = Path(file_path) if file_path else None
        self._json_repository = BaseRepository(self.file_path) if self.file_path else None

    # Bloque CDLform: funcion/metodo _usar_json; encapsula una operacion del flujo del modulo.
    def _usar_json(self) -> bool:
        # Ruta legacy: solo se activa si alguien entrega file_path explicitamente.
        return self._json_repository is not None

    # Bloque CDLform: funcion/metodo _connect; encapsula una operacion del flujo del modulo.
    def _connect(self) -> pyodbc.Connection:
        return get_sql_connection()

    # Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo _normalizar_contexto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_contexto(valor: Any) -> str:
        return PlantillaPreguntasRepository._normalizar_texto(valor).upper()

    # Bloque CDLform: funcion/metodo _normalizar_bool; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_bool(valor: Any, default: bool = True) -> bool:
        if valor is None:
            return default
        return bool(valor)

    # Bloque CDLform: funcion/metodo _normalizar_int; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_int(valor: Any, default: int = 1) -> int:
        try:
            return int(valor)
        except (TypeError, ValueError):
            return default

    # Bloque CDLform: funcion/metodo _serializar_fecha; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _serializar_fecha(valor: Any) -> str:
        if valor is None:
            return ""
        if isinstance(valor, datetime):
            return valor.isoformat(timespec="seconds")
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo _fecha_sql; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _fecha_sql(valor: Any) -> Any:
        texto = str(valor or "").strip()
        if not texto:
            return None
        return texto

    # Bloque CDLform: funcion/metodo _rows_to_dicts; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _rows_to_dicts(
        cursor: pyodbc.Cursor,
        rows: list[pyodbc.Row],
    ) -> list[dict[str, Any]]:
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    # Bloque CDLform: funcion/metodo _obtener_items_por_plantillas; encapsula una operacion del flujo del modulo.
    def _obtener_items_por_plantillas(
        self,
        conn: pyodbc.Connection,
        ids_plantilla: list[str],
    ) -> dict[str, list[PlantillaPreguntaItem]]:
        ids = [self._normalizar_texto(valor) for valor in ids_plantilla if valor]
        if not ids:
            return {}

        placeholders = ", ".join("?" for _ in ids)
        sql = f"""
        SELECT
            [id_plantilla],
            [id_pregunta],
            [orden]
        FROM [dbo].[plantilla_preguntas_items]
        WHERE [id_plantilla] IN ({placeholders})
        ORDER BY [id_plantilla], [orden], [id_pregunta];
        """
        cursor = conn.cursor()
        cursor.execute(sql, tuple(ids))
        rows = self._rows_to_dicts(cursor, cursor.fetchall())

        items_por_plantilla: dict[str, list[PlantillaPreguntaItem]] = {}
        for row in rows:
            id_plantilla = self._normalizar_texto(row.get("id_plantilla"))
            items_por_plantilla.setdefault(id_plantilla, []).append(
                PlantillaPreguntaItem(
                    id_pregunta=self._normalizar_texto(row.get("id_pregunta")),
                    orden=self._normalizar_int(row.get("orden")),
                )
            )

        return items_por_plantilla

    # Bloque CDLform: funcion/metodo _mapear_plantillas; encapsula una operacion del flujo del modulo.
    def _mapear_plantillas(
        self,
        conn: pyodbc.Connection,
        rows: list[dict[str, Any]],
    ) -> list[PlantillaPreguntas]:
        items_por_plantilla = self._obtener_items_por_plantillas(
            conn,
            [self._normalizar_texto(row.get("id_plantilla")) for row in rows],
        )

        plantillas: list[PlantillaPreguntas] = []
        for row in rows:
            id_plantilla = self._normalizar_texto(row.get("id_plantilla"))
            plantillas.append(
                PlantillaPreguntas(
                    id_plantilla=id_plantilla,
                    clave_plantilla=self._normalizar_texto(
                        row.get("clave_plantilla")
                    ),
                    cod_recurso=self._normalizar_contexto(row.get("cod_recurso")),
                    cod_setor=self._normalizar_contexto(row.get("cod_setor")),
                    version=self._normalizar_int(row.get("version")),
                    activa=self._normalizar_bool(row.get("activa")),
                    fecha_creacion=self._serializar_fecha(row.get("fecha_creacion")),
                    fecha_desactivacion=self._serializar_fecha(
                        row.get("fecha_desactivacion")
                    ),
                    items=items_por_plantilla.get(id_plantilla, []),
                )
            )

        return plantillas

    # Bloque CDLform: funcion/metodo listar_plantillas; encapsula una operacion del flujo del modulo.
    def listar_plantillas(self) -> list[PlantillaPreguntas]:
        if self._usar_json():
            return [
                PlantillaPreguntas.from_dict(item)
                for item in self._json_repository.get_all()
            ]

        sql = """
        SELECT
            [id_plantilla],
            [clave_plantilla],
            [cod_recurso],
            [cod_setor],
            [version],
            [activa],
            [fecha_creacion],
            [fecha_desactivacion]
        FROM [dbo].[plantillas_preguntas]
        ORDER BY [cod_setor], [cod_recurso], [version];
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return self._mapear_plantillas(conn, rows)

    # Bloque CDLform: funcion/metodo obtener_por_id; encapsula una operacion del flujo del modulo.
    def obtener_por_id(self, id_plantilla: str) -> PlantillaPreguntas | None:
        if self._usar_json():
            id_normalizado = str(id_plantilla).strip()
            for plantilla in self.listar_plantillas():
                if plantilla.id_plantilla == id_normalizado:
                    return plantilla
            return None

        id_normalizado = self._normalizar_texto(id_plantilla)
        if not id_normalizado:
            return None

        sql = """
        SELECT
            [id_plantilla],
            [clave_plantilla],
            [cod_recurso],
            [cod_setor],
            [version],
            [activa],
            [fecha_creacion],
            [fecha_desactivacion]
        FROM [dbo].[plantillas_preguntas]
        WHERE [id_plantilla] = ?;
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            plantillas = self._mapear_plantillas(conn, rows)
            return plantillas[0] if plantillas else None

    # Bloque CDLform: funcion/metodo obtener_activa; encapsula una operacion del flujo del modulo.
    def obtener_activa(
        self,
        cod_recurso: str,
        cod_setor: str,
    ) -> PlantillaPreguntas | None:
        cod_recurso_normalizado = self._normalizar_contexto(cod_recurso)
        cod_setor_normalizado = self._normalizar_contexto(cod_setor)

        if self._usar_json():
            candidatas = [
                plantilla
                for plantilla in self.listar_plantillas()
                if plantilla.activa
                and plantilla.cod_recurso == cod_recurso_normalizado
                and plantilla.cod_setor == cod_setor_normalizado
            ]
            if not candidatas:
                return None
            return sorted(
                candidatas,
                key=lambda plantilla: plantilla.version,
                reverse=True,
            )[0]

        sql = """
        SELECT TOP (1)
            [id_plantilla],
            [clave_plantilla],
            [cod_recurso],
            [cod_setor],
            [version],
            [activa],
            [fecha_creacion],
            [fecha_desactivacion]
        FROM [dbo].[plantillas_preguntas]
        WHERE [activa] = 1
          AND [cod_recurso] = ?
          AND [cod_setor] = ?
        ORDER BY [version] DESC;
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (cod_recurso_normalizado, cod_setor_normalizado))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            plantillas = self._mapear_plantillas(conn, rows)
            return plantillas[0] if plantillas else None

    # Bloque CDLform: funcion/metodo listar_por_contexto; encapsula una operacion del flujo del modulo.
    def listar_por_contexto(
        self,
        cod_recurso: str,
        cod_setor: str,
    ) -> list[PlantillaPreguntas]:
        cod_recurso_normalizado = self._normalizar_contexto(cod_recurso)
        cod_setor_normalizado = self._normalizar_contexto(cod_setor)

        if self._usar_json():
            return sorted(
                [
                    plantilla
                    for plantilla in self.listar_plantillas()
                    if plantilla.cod_recurso == cod_recurso_normalizado
                    and plantilla.cod_setor == cod_setor_normalizado
                ],
                key=lambda plantilla: plantilla.version,
            )

        sql = """
        SELECT
            [id_plantilla],
            [clave_plantilla],
            [cod_recurso],
            [cod_setor],
            [version],
            [activa],
            [fecha_creacion],
            [fecha_desactivacion]
        FROM [dbo].[plantillas_preguntas]
        WHERE [cod_recurso] = ?
          AND [cod_setor] = ?
        ORDER BY [version];
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (cod_recurso_normalizado, cod_setor_normalizado))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return self._mapear_plantillas(conn, rows)

    # Bloque CDLform: funcion/metodo guardar; encapsula una operacion del flujo del modulo.
    def guardar(self, plantilla: PlantillaPreguntas) -> PlantillaPreguntas:
        if self._usar_json():
            plantillas = self.listar_plantillas()
            for indice, actual in enumerate(plantillas):
                if actual.id_plantilla == plantilla.id_plantilla:
                    plantillas[indice] = plantilla
                    self._guardar_todas(plantillas)
                    return plantilla

            plantillas.append(plantilla)
            self._guardar_todas(plantillas)
            return plantilla

        with self._connect() as conn:
            cursor = conn.cursor()
            self._guardar_cabecera(cursor, plantilla)
            self._sincronizar_items(cursor, plantilla)
            conn.commit()

        return plantilla

    # Bloque CDLform: funcion/metodo _guardar_cabecera; encapsula una operacion del flujo del modulo.
    def _guardar_cabecera(
        self,
        cursor: pyodbc.Cursor,
        plantilla: PlantillaPreguntas,
    ) -> None:
        cursor.execute(
            """
            UPDATE [dbo].[plantillas_preguntas]
            SET
                [clave_plantilla] = ?,
                [cod_recurso] = ?,
                [cod_setor] = ?,
                [version] = ?,
                [activa] = ?,
                [fecha_creacion] = COALESCE(?, [fecha_creacion]),
                [fecha_desactivacion] = ?
            WHERE [id_plantilla] = ?;
            """,
            (
                plantilla.clave_plantilla,
                plantilla.cod_recurso,
                plantilla.cod_setor,
                plantilla.version,
                1 if plantilla.activa else 0,
                self._fecha_sql(plantilla.fecha_creacion),
                self._fecha_sql(plantilla.fecha_desactivacion),
                plantilla.id_plantilla,
            ),
        )

        if cursor.rowcount > 0:
            return

        cursor.execute(
            """
            INSERT INTO [dbo].[plantillas_preguntas] (
                [id_plantilla],
                [clave_plantilla],
                [cod_recurso],
                [cod_setor],
                [version],
                [activa],
                [fecha_creacion],
                [fecha_desactivacion]
            )
            VALUES (?, ?, ?, ?, ?, ?, COALESCE(?, SYSDATETIME()), ?);
            """,
            (
                plantilla.id_plantilla,
                plantilla.clave_plantilla,
                plantilla.cod_recurso,
                plantilla.cod_setor,
                plantilla.version,
                1 if plantilla.activa else 0,
                self._fecha_sql(plantilla.fecha_creacion),
                self._fecha_sql(plantilla.fecha_desactivacion),
            ),
        )

    # Bloque CDLform: funcion/metodo _sincronizar_items; encapsula una operacion del flujo del modulo.
    def _sincronizar_items(
        self,
        cursor: pyodbc.Cursor,
        plantilla: PlantillaPreguntas,
    ) -> None:
        for item in plantilla.items:
            cursor.execute(
                """
                UPDATE [dbo].[plantilla_preguntas_items]
                SET [orden] = ?
                WHERE [id_plantilla] = ?
                  AND [id_pregunta] = ?;
                """,
                (
                    item.orden,
                    plantilla.id_plantilla,
                    item.id_pregunta,
                ),
            )

            if cursor.rowcount > 0:
                continue

            cursor.execute(
                """
                INSERT INTO [dbo].[plantilla_preguntas_items] (
                    [id_plantilla],
                    [id_pregunta],
                    [orden]
                )
                VALUES (?, ?, ?);
                """,
                (
                    plantilla.id_plantilla,
                    item.id_pregunta,
                    item.orden,
                ),
            )

    # Bloque CDLform: funcion/metodo _guardar_todas; encapsula una operacion del flujo del modulo.
    def _guardar_todas(self, plantillas: list[PlantillaPreguntas]) -> None:
        if not self.file_path:
            raise RuntimeError("No hay archivo JSON configurado para guardar.")

        JsonManager.write_json(
            str(self.file_path),
            [plantilla.to_dict() for plantilla in plantillas],
        )
