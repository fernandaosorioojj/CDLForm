"""Acceso a datos SQL Server para entidades del dominio CDLform.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import pyodbc

from database.sql_connection import get_sql_connection
from repositories.base_repository import BaseRepository


# FLUJO ACTUAL:
# Sin file_path, este repositorio usa SQL Server para preguntas y opciones.
#
# LEGACY:
# Si se instancia manualmente con file_path, usa JSON. Esa ruta no forma parte
# del flujo vigente de gestion ni del formulario operario.
# Bloque CDLform: clase PreguntaRepository; agrupa estado y comportamiento de esta parte del flujo.
class PreguntaRepository:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, file_path: Path | None = None) -> None:
        self._json_repository = BaseRepository(file_path) if file_path else None

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

    # Bloque CDLform: funcion/metodo _filtros_a_json; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _filtros_a_json(filtros: Any) -> str | None:
        if not filtros:
            return None
        return json.dumps(filtros, ensure_ascii=False)

    # Bloque CDLform: funcion/metodo _filtros_desde_json; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _filtros_desde_json(valor: Any) -> dict:
        texto = str(valor or "").strip()
        if not texto:
            return {}
        try:
            data = json.loads(texto)
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    # Bloque CDLform: funcion/metodo _rows_to_dicts; encapsula una operacion del flujo del modulo.
    def _rows_to_dicts(
        self,
        cursor: pyodbc.Cursor,
        rows: list[pyodbc.Row],
    ) -> list[dict[str, Any]]:
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    # Bloque CDLform: funcion/metodo _obtener_opciones_por_preguntas; encapsula una operacion del flujo del modulo.
    def _obtener_opciones_por_preguntas(
        self,
        conn: pyodbc.Connection,
        ids_pregunta: list[str],
    ) -> dict[str, list[dict[str, Any]]]:
        ids = [self._normalizar_texto(valor) for valor in ids_pregunta if valor]
        if not ids:
            return {}

        placeholders = ", ".join("?" for _ in ids)
        sql = f"""
        SELECT
            [id_pregunta],
            [id_opcion],
            [clave_opcion],
            [valor],
            [accion_correctiva],
            [activa],
            [version],
            [orden]
        FROM [dbo].[pregunta_opciones]
        WHERE [id_pregunta] IN ({placeholders})
        ORDER BY [id_pregunta], [orden], [id_opcion];
        """
        cursor = conn.cursor()
        cursor.execute(sql, tuple(ids))
        rows = self._rows_to_dicts(cursor, cursor.fetchall())

        opciones_por_pregunta: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            id_pregunta = self._normalizar_texto(row.get("id_pregunta"))
            opciones_por_pregunta.setdefault(id_pregunta, []).append(
                {
                    "id_opcion": self._normalizar_texto(row.get("id_opcion")),
                    "valor": self._normalizar_texto(row.get("valor")),
                    "accion_correctiva": self._normalizar_texto(
                        row.get("accion_correctiva")
                    ),
                    "activa": self._normalizar_bool(row.get("activa")),
                    "version": self._normalizar_int(row.get("version")),
                    "clave_opcion": self._normalizar_texto(
                        row.get("clave_opcion")
                    ),
                }
            )

        return opciones_por_pregunta

    # Bloque CDLform: funcion/metodo _mapear_preguntas; encapsula una operacion del flujo del modulo.
    def _mapear_preguntas(
        self,
        conn: pyodbc.Connection,
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        opciones_por_pregunta = self._obtener_opciones_por_preguntas(
            conn,
            [self._normalizar_texto(row.get("id_pregunta")) for row in rows],
        )

        preguntas: list[dict[str, Any]] = []
        for row in rows:
            id_pregunta = self._normalizar_texto(row.get("id_pregunta"))
            preguntas.append(
                {
                    "id_pregunta": id_pregunta,
                    "texto": self._normalizar_texto(row.get("texto")),
                    "tipo": self._normalizar_texto(row.get("tipo")),
                    "activa": self._normalizar_bool(row.get("activa")),
                    "obligatoria": self._normalizar_bool(row.get("obligatoria")),
                    "orden": self._normalizar_int(row.get("orden")),
                    "version": self._normalizar_int(row.get("version")),
                    "clave_pregunta": self._normalizar_texto(
                        row.get("clave_pregunta")
                    )
                    or id_pregunta,
                    "fecha_creacion": self._serializar_fecha(
                        row.get("fecha_creacion")
                    ),
                    "fecha_actualizacion": self._serializar_fecha(
                        row.get("fecha_actualizacion")
                    ),
                    "fecha_desactivacion": self._serializar_fecha(
                        row.get("fecha_desactivacion")
                    ),
                    "reemplazada_por": self._normalizar_texto(
                        row.get("reemplazada_por")
                    ),
                    "filtros_contexto": self._filtros_desde_json(
                        row.get("filtros_contexto_json")
                    ),
                    "opciones_respuesta": opciones_por_pregunta.get(
                        id_pregunta, []
                    ),
                }
            )

        return preguntas

    # Bloque CDLform: funcion/metodo get_all; encapsula una operacion del flujo del modulo.
    def get_all(self) -> list[dict[str, Any]]:
        if self._usar_json():
            return self._json_repository.get_all()

        sql = """
        SELECT
            [id_pregunta],
            [clave_pregunta],
            [texto],
            [tipo],
            [obligatoria],
            [activa],
            [orden],
            [version],
            [filtros_contexto_json],
            [fecha_creacion],
            [fecha_actualizacion],
            [fecha_desactivacion],
            [reemplazada_por]
        FROM [dbo].[preguntas]
        ORDER BY [orden], [clave_pregunta], [version];
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return self._mapear_preguntas(conn, rows)

    # Bloque CDLform: funcion/metodo obtener_todas; encapsula una operacion del flujo del modulo.
    def obtener_todas(self) -> list[dict[str, Any]]:
        return self.get_all()

    # Bloque CDLform: funcion/metodo find_by_id; encapsula una operacion del flujo del modulo.
    def find_by_id(self, item_id: str) -> Optional[dict[str, Any]]:
        if self._usar_json():
            return self._json_repository.find_by_id(item_id)

        id_pregunta = self._normalizar_texto(item_id)
        if not id_pregunta:
            return None

        sql = """
        SELECT
            [id_pregunta],
            [clave_pregunta],
            [texto],
            [tipo],
            [obligatoria],
            [activa],
            [orden],
            [version],
            [filtros_contexto_json],
            [fecha_creacion],
            [fecha_actualizacion],
            [fecha_desactivacion],
            [reemplazada_por]
        FROM [dbo].[preguntas]
        WHERE [id_pregunta] = ?;
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_pregunta,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            preguntas = self._mapear_preguntas(conn, rows)
            return preguntas[0] if preguntas else None

    # Bloque CDLform: funcion/metodo obtener_por_id; encapsula una operacion del flujo del modulo.
    def obtener_por_id(self, id_pregunta: str) -> Optional[dict[str, Any]]:
        return self.find_by_id(id_pregunta)

    # Bloque CDLform: funcion/metodo add; encapsula una operacion del flujo del modulo.
    def add(self, item: dict[str, Any]) -> dict[str, Any]:
        if self._usar_json():
            self._json_repository.add(item)
            return item

        id_pregunta = self._normalizar_texto(item.get("id_pregunta"))
        if not id_pregunta:
            raise ValueError("id_pregunta es obligatorio.")

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO [dbo].[preguntas] (
                    [id_pregunta],
                    [clave_pregunta],
                    [texto],
                    [tipo],
                    [obligatoria],
                    [activa],
                    [orden],
                    [version],
                    [filtros_contexto_json],
                    [fecha_creacion],
                    [fecha_actualizacion],
                    [fecha_desactivacion],
                    [reemplazada_por]
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE(?, SYSDATETIME()), COALESCE(?, SYSDATETIME()), ?, ?);
                """,
                (
                    id_pregunta,
                    self._normalizar_texto(item.get("clave_pregunta"))
                    or id_pregunta,
                    self._normalizar_texto(item.get("texto")),
                    self._normalizar_texto(item.get("tipo")),
                    1 if self._normalizar_bool(item.get("obligatoria")) else 0,
                    1 if self._normalizar_bool(item.get("activa")) else 0,
                    self._normalizar_int(item.get("orden")),
                    self._normalizar_int(item.get("version")),
                    self._filtros_a_json(item.get("filtros_contexto")),
                    self._fecha_sql(item.get("fecha_creacion")),
                    self._fecha_sql(item.get("fecha_actualizacion")),
                    self._fecha_sql(item.get("fecha_desactivacion")),
                    self._normalizar_texto(item.get("reemplazada_por")) or None,
                ),
            )
            self._guardar_opciones(cursor, id_pregunta, item)
            conn.commit()

        return item

    # Bloque CDLform: funcion/metodo crear; encapsula una operacion del flujo del modulo.
    def crear(self, pregunta: dict[str, Any]) -> dict[str, Any]:
        self.add(pregunta)
        return pregunta

    # Bloque CDLform: funcion/metodo update_by_id; encapsula una operacion del flujo del modulo.
    def update_by_id(self, item_id: str, new_data: dict[str, Any]) -> bool:
        if self._usar_json():
            return self._json_repository.update_by_id(item_id, new_data)

        id_pregunta = self._normalizar_texto(item_id)
        if not id_pregunta:
            return False

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE [dbo].[preguntas]
                SET
                    [clave_pregunta] = ?,
                    [texto] = ?,
                    [tipo] = ?,
                    [obligatoria] = ?,
                    [activa] = ?,
                    [orden] = ?,
                    [version] = ?,
                    [filtros_contexto_json] = ?,
                    [fecha_creacion] = COALESCE(?, [fecha_creacion]),
                    [fecha_actualizacion] = COALESCE(?, SYSDATETIME()),
                    [fecha_desactivacion] = ?,
                    [reemplazada_por] = ?
                WHERE [id_pregunta] = ?;
                """,
                (
                    self._normalizar_texto(new_data.get("clave_pregunta"))
                    or id_pregunta,
                    self._normalizar_texto(new_data.get("texto")),
                    self._normalizar_texto(new_data.get("tipo")),
                    1 if self._normalizar_bool(new_data.get("obligatoria")) else 0,
                    1 if self._normalizar_bool(new_data.get("activa")) else 0,
                    self._normalizar_int(new_data.get("orden")),
                    self._normalizar_int(new_data.get("version")),
                    self._filtros_a_json(new_data.get("filtros_contexto")),
                    self._fecha_sql(new_data.get("fecha_creacion")),
                    self._fecha_sql(new_data.get("fecha_actualizacion")),
                    self._fecha_sql(new_data.get("fecha_desactivacion")),
                    self._normalizar_texto(new_data.get("reemplazada_por")) or None,
                    id_pregunta,
                ),
            )

            if cursor.rowcount == 0:
                conn.rollback()
                return False

            self._sincronizar_opciones(cursor, id_pregunta, new_data)
            conn.commit()
            return True

    # Bloque CDLform: funcion/metodo actualizar; encapsula una operacion del flujo del modulo.
    def actualizar(self, id_pregunta: str, data: dict[str, Any]) -> Optional[dict]:
        actualizado = self.update_by_id(id_pregunta, data)
        if not actualizado:
            return None
        return self.find_by_id(id_pregunta)

    # Bloque CDLform: funcion/metodo delete_by_id; encapsula una operacion del flujo del modulo.
    def delete_by_id(self, item_id: str) -> bool:
        if self._usar_json():
            return self._json_repository.delete_by_id(item_id)

        id_pregunta = self._normalizar_texto(item_id)
        if not id_pregunta:
            return False

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = ?;",
                (id_pregunta,),
            )
            cursor.execute(
                "DELETE FROM [dbo].[preguntas] WHERE [id_pregunta] = ?;",
                (id_pregunta,),
            )
            eliminado = cursor.rowcount > 0
            conn.commit()
            return eliminado

    # Bloque CDLform: funcion/metodo eliminar; encapsula una operacion del flujo del modulo.
    def eliminar(self, id_pregunta: str) -> bool:
        return self.delete_by_id(id_pregunta)

    # Bloque CDLform: funcion/metodo _guardar_opciones; encapsula una operacion del flujo del modulo.
    def _guardar_opciones(
        self,
        cursor: pyodbc.Cursor,
        id_pregunta: str,
        pregunta: dict[str, Any],
    ) -> None:
        opciones = pregunta.get("opciones_respuesta") or []
        for indice, opcion in enumerate(opciones, start=1):
            if not isinstance(opcion, dict):
                continue

            id_opcion = self._normalizar_texto(opcion.get("id_opcion"))
            valor = self._normalizar_texto(opcion.get("valor"))
            if not id_opcion or not valor:
                continue

            cursor.execute(
                """
                INSERT INTO [dbo].[pregunta_opciones] (
                    [id_pregunta],
                    [id_opcion],
                    [clave_opcion],
                    [valor],
                    [accion_correctiva],
                    [activa],
                    [version],
                    [orden]
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    id_pregunta,
                    id_opcion,
                    self._normalizar_texto(opcion.get("clave_opcion")) or id_opcion,
                    valor,
                    self._normalizar_texto(opcion.get("accion_correctiva")) or None,
                    1 if self._normalizar_bool(opcion.get("activa")) else 0,
                    self._normalizar_int(opcion.get("version")),
                    self._normalizar_int(opcion.get("orden"), indice),
                ),
            )

    # Bloque CDLform: funcion/metodo _sincronizar_opciones; encapsula una operacion del flujo del modulo.
    def _sincronizar_opciones(
        self,
        cursor: pyodbc.Cursor,
        id_pregunta: str,
        pregunta: dict[str, Any],
    ) -> None:
        opciones = pregunta.get("opciones_respuesta") or []
        ids_vigentes: list[str] = []

        for indice, opcion in enumerate(opciones, start=1):
            if not isinstance(opcion, dict):
                continue

            id_opcion = self._normalizar_texto(opcion.get("id_opcion"))
            valor = self._normalizar_texto(opcion.get("valor"))
            if not id_opcion or not valor:
                continue

            ids_vigentes.append(id_opcion)
            cursor.execute(
                """
                UPDATE [dbo].[pregunta_opciones]
                SET
                    [clave_opcion] = ?,
                    [valor] = ?,
                    [accion_correctiva] = ?,
                    [activa] = ?,
                    [version] = ?,
                    [orden] = ?,
                    [fecha_actualizacion] = SYSDATETIME()
                WHERE [id_pregunta] = ?
                  AND [id_opcion] = ?;
                """,
                (
                    self._normalizar_texto(opcion.get("clave_opcion")) or id_opcion,
                    valor,
                    self._normalizar_texto(opcion.get("accion_correctiva")) or None,
                    1 if self._normalizar_bool(opcion.get("activa")) else 0,
                    self._normalizar_int(opcion.get("version")),
                    self._normalizar_int(opcion.get("orden"), indice),
                    id_pregunta,
                    id_opcion,
                ),
            )

            if cursor.rowcount > 0:
                continue

            cursor.execute(
                """
                INSERT INTO [dbo].[pregunta_opciones] (
                    [id_pregunta],
                    [id_opcion],
                    [clave_opcion],
                    [valor],
                    [accion_correctiva],
                    [activa],
                    [version],
                    [orden]
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    id_pregunta,
                    id_opcion,
                    self._normalizar_texto(opcion.get("clave_opcion")) or id_opcion,
                    valor,
                    self._normalizar_texto(opcion.get("accion_correctiva")) or None,
                    1 if self._normalizar_bool(opcion.get("activa")) else 0,
                    self._normalizar_int(opcion.get("version")),
                    self._normalizar_int(opcion.get("orden"), indice),
                ),
            )

        if ids_vigentes:
            placeholders = ", ".join("?" for _ in ids_vigentes)
            cursor.execute(
                f"""
                UPDATE [dbo].[pregunta_opciones]
                SET
                    [activa] = 0,
                    [fecha_actualizacion] = SYSDATETIME()
                WHERE [id_pregunta] = ?
                  AND [id_opcion] NOT IN ({placeholders});
                """,
                tuple([id_pregunta, *ids_vigentes]),
            )
        else:
            cursor.execute(
                """
                UPDATE [dbo].[pregunta_opciones]
                SET
                    [activa] = 0,
                    [fecha_actualizacion] = SYSDATETIME()
                WHERE [id_pregunta] = ?;
                """,
                (id_pregunta,),
            )
