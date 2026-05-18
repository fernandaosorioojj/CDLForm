"""Acceso a datos SQL Server para entidades del dominio CDLform.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pyodbc

from database.sql_connection import get_sql_connection
from models.respuesta import Respuesta
from repositories.base_repository import BaseRepository


# FLUJO ACTUAL:
# Sin file_path, este repositorio usa SQL Server para respuestas de formularios.
#
# LEGACY:
# Si se instancia manualmente con file_path, usa JSON. Esa ruta no es parte
# del flujo actual de envio/cierre de formularios.
# Bloque CDLform: clase RespuestaRepository; agrupa estado y comportamiento de esta parte del flujo.
class RespuestaRepository:
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
        return texto.replace("T", " ")

    # Bloque CDLform: funcion/metodo _numero_decimal; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _numero_decimal(valor: Any) -> Any:
        if valor is None or str(valor).strip() == "":
            return None
        return valor

    # Bloque CDLform: funcion/metodo _rows_to_dicts; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _rows_to_dicts(
        cursor: pyodbc.Cursor,
        rows: list[pyodbc.Row],
    ) -> list[dict[str, Any]]:
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    # Bloque CDLform: funcion/metodo _from_dict; encapsula una operacion del flujo del modulo.
    def _from_dict(self, data: dict) -> Respuesta:
        return Respuesta.from_dict(data)

    # Bloque CDLform: funcion/metodo _from_row; encapsula una operacion del flujo del modulo.
    def _from_row(self, row: dict[str, Any]) -> Respuesta:
        numero = row.get("respuesta_numero")
        if numero is not None:
            try:
                numero = int(numero)
            except (TypeError, ValueError):
                pass

        return Respuesta(
            id_respuesta=self._normalizar_texto(row.get("id_respuesta")),
            id_formulario=self._normalizar_texto(row.get("id_formulario")),
            id_pregunta=self._normalizar_texto(row.get("id_pregunta")),
            respuesta_texto=(
                self._normalizar_texto(row.get("respuesta_texto")) or None
            ),
            respuesta_numero=numero,
            id_opcion=self._normalizar_texto(row.get("id_opcion")) or None,
            accion_correctiva_aplicada=(
                self._normalizar_texto(row.get("accion_correctiva_aplicada"))
                or None
            ),
            fecha_creacion=self._serializar_fecha(row.get("fecha_creacion")),
        )

    # Bloque CDLform: funcion/metodo _get_entity_id; encapsula una operacion del flujo del modulo.
    def _get_entity_id(self, entity: Respuesta) -> str:
        return entity.id_respuesta

    # Bloque CDLform: funcion/metodo list_all; encapsula una operacion del flujo del modulo.
    def list_all(self) -> list[Respuesta]:
        if self._usar_json():
            registros = self._json_repository.get_all()
            return [self._from_dict(item) for item in registros]

        sql = """
        SELECT
            [id_respuesta],
            [id_formulario],
            [id_pregunta],
            [respuesta_texto],
            [respuesta_numero],
            [id_opcion],
            [accion_correctiva_aplicada],
            [fecha_creacion]
        FROM [dbo].[respuestas_formulario]
        ORDER BY [fecha_creacion], [id_respuesta];
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return [self._from_row(row) for row in rows]

    # Bloque CDLform: funcion/metodo get_by_id; encapsula una operacion del flujo del modulo.
    def get_by_id(self, id_respuesta: str) -> Respuesta | None:
        id_normalizado = self._normalizar_texto(id_respuesta)
        if not id_normalizado:
            return None

        if self._usar_json():
            data = self._json_repository.find_by_id(id_normalizado)
            if not data:
                return None
            return self._from_dict(data)

        sql = """
        SELECT
            [id_respuesta],
            [id_formulario],
            [id_pregunta],
            [respuesta_texto],
            [respuesta_numero],
            [id_opcion],
            [accion_correctiva_aplicada],
            [fecha_creacion]
        FROM [dbo].[respuestas_formulario]
        WHERE [id_respuesta] = ?;
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return self._from_row(rows[0]) if rows else None

    # Bloque CDLform: funcion/metodo add_respuesta; encapsula una operacion del flujo del modulo.
    def add_respuesta(self, respuesta: Respuesta) -> Respuesta:
        if self._usar_json():
            self._json_repository.add(respuesta.to_dict())
            return respuesta

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO [dbo].[respuestas_formulario] (
                    [id_respuesta],
                    [id_formulario],
                    [id_pregunta],
                    [respuesta_texto],
                    [respuesta_numero],
                    [id_opcion],
                    [accion_correctiva_aplicada],
                    [fecha_creacion]
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, COALESCE(?, SYSDATETIME()));
                """,
                (
                    respuesta.id_respuesta,
                    respuesta.id_formulario,
                    respuesta.id_pregunta,
                    respuesta.respuesta_texto,
                    self._numero_decimal(respuesta.respuesta_numero),
                    respuesta.id_opcion,
                    respuesta.accion_correctiva_aplicada,
                    self._fecha_sql(respuesta.fecha_creacion),
                ),
            )
            conn.commit()
            return respuesta

    # Bloque CDLform: funcion/metodo update; encapsula una operacion del flujo del modulo.
    def update(self, respuesta: Respuesta) -> Respuesta:
        if self._usar_json():
            self._json_repository.update_by_id(
                respuesta.id_respuesta,
                respuesta.to_dict(),
            )
            return respuesta

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE [dbo].[respuestas_formulario]
                SET
                    [id_formulario] = ?,
                    [id_pregunta] = ?,
                    [respuesta_texto] = ?,
                    [respuesta_numero] = ?,
                    [id_opcion] = ?,
                    [accion_correctiva_aplicada] = ?,
                    [fecha_creacion] = COALESCE(?, [fecha_creacion])
                WHERE [id_respuesta] = ?;
                """,
                (
                    respuesta.id_formulario,
                    respuesta.id_pregunta,
                    respuesta.respuesta_texto,
                    self._numero_decimal(respuesta.respuesta_numero),
                    respuesta.id_opcion,
                    respuesta.accion_correctiva_aplicada,
                    self._fecha_sql(respuesta.fecha_creacion),
                    respuesta.id_respuesta,
                ),
            )
            conn.commit()
            return respuesta

    # Bloque CDLform: funcion/metodo delete_by_formulario; encapsula una operacion del flujo del modulo.
    def delete_by_formulario(self, id_formulario: str) -> int:
        id_normalizado = self._normalizar_texto(id_formulario)
        if not id_normalizado:
            return 0

        if self._usar_json():
            respuestas_a_eliminar = [
                respuesta.id_respuesta
                for respuesta in self.list_all()
                if respuesta.id_formulario == id_normalizado
            ]

            eliminadas = 0
            for id_respuesta in respuestas_a_eliminar:
                if self._json_repository.delete_by_id(id_respuesta):
                    eliminadas += 1

            return eliminadas

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM [dbo].[respuestas_formulario]
                WHERE [id_formulario] = ?;
                """,
                (id_normalizado,),
            )
            eliminadas = cursor.rowcount
            conn.commit()
            return int(eliminadas or 0)

    # Bloque CDLform: funcion/metodo get_respuestas_por_formulario; encapsula una operacion del flujo del modulo.
    def get_respuestas_por_formulario(self, id_formulario: str) -> list[Respuesta]:
        id_normalizado = self._normalizar_texto(id_formulario)
        if not id_normalizado:
            return []

        if self._usar_json():
            return [
                respuesta
                for respuesta in self.list_all()
                if respuesta.id_formulario == id_normalizado
            ]

        sql = """
        SELECT
            [id_respuesta],
            [id_formulario],
            [id_pregunta],
            [respuesta_texto],
            [respuesta_numero],
            [id_opcion],
            [accion_correctiva_aplicada],
            [fecha_creacion]
        FROM [dbo].[respuestas_formulario]
        WHERE [id_formulario] = ?
        ORDER BY [fecha_creacion], [id_respuesta];
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return [self._from_row(row) for row in rows]

    # Bloque CDLform: funcion/metodo get_respuestas_por_pregunta; encapsula una operacion del flujo del modulo.
    def get_respuestas_por_pregunta(self, id_pregunta: str) -> list[Respuesta]:
        id_normalizado = self._normalizar_texto(id_pregunta)
        if not id_normalizado:
            return []

        if self._usar_json():
            return [
                respuesta
                for respuesta in self.list_all()
                if respuesta.id_pregunta == id_normalizado
            ]

        sql = """
        SELECT
            [id_respuesta],
            [id_formulario],
            [id_pregunta],
            [respuesta_texto],
            [respuesta_numero],
            [id_opcion],
            [accion_correctiva_aplicada],
            [fecha_creacion]
        FROM [dbo].[respuestas_formulario]
        WHERE [id_pregunta] = ?
        ORDER BY [fecha_creacion], [id_respuesta];
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return [self._from_row(row) for row in rows]
