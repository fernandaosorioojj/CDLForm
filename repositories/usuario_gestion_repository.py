"""Acceso a datos SQL Server para entidades del dominio CDLform.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from typing import Any

import pyodbc

from database.sql_connection import get_sql_connection


# Bloque CDLform: clase UsuarioGestionRepository; agrupa estado y comportamiento de esta parte del flujo.
class UsuarioGestionRepository:
    # Bloque CDLform: funcion/metodo _connect; encapsula una operacion del flujo del modulo.
    def _connect(self) -> pyodbc.Connection:
        return get_sql_connection()

    # Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo _rows_to_dicts; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _rows_to_dicts(
        cursor: pyodbc.Cursor,
        rows: list[pyodbc.Row],
    ) -> list[dict[str, Any]]:
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    # Bloque CDLform: funcion/metodo obtener_usuario_activo; encapsula una operacion del flujo del modulo.
    def obtener_usuario_activo(self, usuario: str) -> dict[str, str] | None:
        self.ensure_schema()
        usuario_normalizado = self._normalizar_texto(usuario)
        if not usuario_normalizado:
            return None

        sql = """
        SELECT TOP (1)
            [usuario],
            [password_hash],
            [rol]
        FROM [dbo].[usuarios_gestion]
        WHERE [usuario] = ?
          AND [activo] = 1;
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (usuario_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())

        if not rows:
            return None

        row = rows[0]
        usuario_encontrado = self._normalizar_texto(row.get("usuario"))
        password_hash = self._normalizar_texto(row.get("password_hash"))
        rol = self._normalizar_rol(row.get("rol"))
        if not usuario_encontrado or not password_hash:
            return None

        return {
            "usuario": usuario_encontrado,
            "password_hash": password_hash,
            "rol": rol,
        }

    # Bloque CDLform: funcion/metodo ensure_schema; encapsula una operacion del flujo del modulo.
    def ensure_schema(self) -> None:
        sql = """
        IF OBJECT_ID(N'[dbo].[usuarios_gestion]', N'U') IS NULL
        BEGIN
            CREATE TABLE [dbo].[usuarios_gestion] (
                [id_usuario] INT IDENTITY(1,1) NOT NULL,
                [usuario] NVARCHAR(100) NOT NULL,
                [password_hash] NVARCHAR(300) NOT NULL,
                [rol] NVARCHAR(50) NOT NULL CONSTRAINT [DF_usuarios_gestion_rol] DEFAULT (N'gestion'),
                [activo] BIT NOT NULL CONSTRAINT [DF_usuarios_gestion_activo] DEFAULT (1),
                [fecha_creacion] DATETIME2(0) NOT NULL CONSTRAINT [DF_usuarios_gestion_fecha_creacion] DEFAULT (SYSDATETIME()),
                [fecha_actualizacion] DATETIME2(0) NOT NULL CONSTRAINT [DF_usuarios_gestion_fecha_actualizacion] DEFAULT (SYSDATETIME()),
                CONSTRAINT [PK_usuarios_gestion] PRIMARY KEY CLUSTERED ([id_usuario]),
                CONSTRAINT [UX_usuarios_gestion_usuario] UNIQUE ([usuario])
            );
        END;

        IF COL_LENGTH(N'[dbo].[usuarios_gestion]', N'rol') IS NULL
        BEGIN
            ALTER TABLE [dbo].[usuarios_gestion]
            ADD [rol] NVARCHAR(50) NOT NULL
                CONSTRAINT [DF_usuarios_gestion_rol] DEFAULT (N'gestion')
                WITH VALUES;
        END;
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

    # Bloque CDLform: funcion/metodo listar_usuarios; encapsula una operacion del flujo del modulo.
    def listar_usuarios(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        sql = """
        SELECT
            [id_usuario],
            [usuario],
            [rol],
            [activo],
            [fecha_creacion],
            [fecha_actualizacion]
        FROM [dbo].[usuarios_gestion]
        ORDER BY [usuario];
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return self._rows_to_dicts(cursor, cursor.fetchall())

    # Bloque CDLform: funcion/metodo guardar_usuario; encapsula una operacion del flujo del modulo.
    def guardar_usuario(
        self,
        usuario: str,
        password_hash: str,
        rol: str = "gestion",
        activo: bool = True,
    ) -> None:
        self.ensure_schema()
        usuario_normalizado = self._normalizar_texto(usuario)
        password_hash_normalizado = self._normalizar_texto(password_hash)
        rol_normalizado = self._normalizar_rol(rol)
        if not usuario_normalizado:
            raise ValueError("El usuario es obligatorio.")
        if not password_hash_normalizado:
            raise ValueError("El password_hash es obligatorio.")

        sql = """
        MERGE [dbo].[usuarios_gestion] AS target
        USING (
            SELECT
                ? AS [usuario],
                ? AS [password_hash],
                ? AS [rol],
                ? AS [activo]
        ) AS source
        ON target.[usuario] = source.[usuario]
        WHEN MATCHED THEN
            UPDATE SET
                [password_hash] = source.[password_hash],
                [rol] = source.[rol],
                [activo] = source.[activo],
                [fecha_actualizacion] = SYSDATETIME()
        WHEN NOT MATCHED THEN
            INSERT ([usuario], [password_hash], [rol], [activo])
            VALUES (source.[usuario], source.[password_hash], source.[rol], source.[activo]);
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    usuario_normalizado,
                    password_hash_normalizado,
                    rol_normalizado,
                    1 if activo else 0,
                ),
            )
            conn.commit()

    # Bloque CDLform: funcion/metodo cambiar_password; encapsula una operacion del flujo del modulo.
    def cambiar_password(self, usuario: str, password_hash: str) -> None:
        self.ensure_schema()
        usuario_normalizado = self._normalizar_texto(usuario)
        password_hash_normalizado = self._normalizar_texto(password_hash)
        if not usuario_normalizado:
            raise ValueError("El usuario es obligatorio.")
        if not password_hash_normalizado:
            raise ValueError("El password_hash es obligatorio.")

        sql = """
        UPDATE [dbo].[usuarios_gestion]
        SET
            [password_hash] = ?,
            [fecha_actualizacion] = SYSDATETIME()
        WHERE [usuario] = ?;
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (password_hash_normalizado, usuario_normalizado))
            if cursor.rowcount <= 0:
                raise ValueError(f"No existe el usuario {usuario_normalizado}.")
            conn.commit()

    # Bloque CDLform: funcion/metodo actualizar_activo; encapsula una operacion del flujo del modulo.
    def actualizar_activo(self, usuario: str, activo: bool) -> None:
        self.ensure_schema()
        usuario_normalizado = self._normalizar_texto(usuario)
        if not usuario_normalizado:
            raise ValueError("El usuario es obligatorio.")

        sql = """
        UPDATE [dbo].[usuarios_gestion]
        SET
            [activo] = ?,
            [fecha_actualizacion] = SYSDATETIME()
        WHERE [usuario] = ?;
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (1 if activo else 0, usuario_normalizado))
            if cursor.rowcount <= 0:
                raise ValueError(f"No existe el usuario {usuario_normalizado}.")
            conn.commit()

    # Bloque CDLform: funcion/metodo _normalizar_rol; encapsula una operacion del flujo del modulo.
    @classmethod
    def _normalizar_rol(cls, valor: Any) -> str:
        rol = cls._normalizar_texto(valor).lower()
        if rol in {"admin", "gestion"}:
            return rol
        return "gestion"

    # Bloque CDLform: funcion/metodo actualizar_rol; encapsula una operacion del flujo del modulo.
    def actualizar_rol(self, usuario: str, rol: str) -> None:
        self.ensure_schema()
        usuario_normalizado = self._normalizar_texto(usuario)
        rol_normalizado = self._normalizar_rol(rol)
        if not usuario_normalizado:
            raise ValueError("El usuario es obligatorio.")

        sql = """
        UPDATE [dbo].[usuarios_gestion]
        SET
            [rol] = ?,
            [fecha_actualizacion] = SYSDATETIME()
        WHERE [usuario] = ?;
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (rol_normalizado, usuario_normalizado))
            if cursor.rowcount <= 0:
                raise ValueError(f"No existe el usuario {usuario_normalizado}.")
            conn.commit()
