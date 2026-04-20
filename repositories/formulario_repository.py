from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

import pyodbc

from config.sql_server_config import build_connection_string
from models.formulario import Formulario
from repositories.base_repository import BaseRepository
from utils.json_manager import JsonManager


class FormularioRepository:
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = Path(file_path) if file_path else None
        self._json_repository = BaseRepository(self.file_path) if self.file_path else None

    def _usar_json(self) -> bool:
        return self._json_repository is not None

    def _connect(self) -> pyodbc.Connection:
        return pyodbc.connect(build_connection_string())

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @staticmethod
    def _normalizar_id_apontamento(valor: Any) -> str:
        texto = str(valor or "").strip()
        if not texto:
            raise ValueError("El IdApontamento no puede venir vacio.")

        try:
            numero = float(texto)
            if numero.is_integer():
                return str(int(numero))
        except ValueError:
            pass

        return texto

    @staticmethod
    def _serializar_fecha(valor: Any) -> str:
        if valor is None:
            return ""
        if isinstance(valor, datetime):
            return valor.isoformat(timespec="seconds")
        if isinstance(valor, date):
            return valor.isoformat()
        return str(valor).strip()

    @staticmethod
    def _fecha_sql(valor: Any) -> Any:
        texto = str(valor or "").strip()
        if not texto:
            return None
        return texto.replace("T", " ")

    @staticmethod
    def _rows_to_dicts(
        cursor: pyodbc.Cursor,
        rows: list[pyodbc.Row],
    ) -> list[dict[str, Any]]:
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, row)) for row in rows]

    def _leer_todos_crudos(self) -> list[dict[str, Any]]:
        if self._usar_json():
            return self._json_repository.get_all()

        sql = """
        SELECT
            [id_formulario],
            [id_apontamento],
            [identificador],
            [fecha_formulario],
            [cod_recurso],
            [cod_setor],
            [turno],
            [hora_fim],
            [operador_apontamento],
            [supervisor_apontamento],
            [operario_formulario],
            [estacion],
            [evento_origen],
            [estado],
            [descripcion_op],
            [descripcion_proceso],
            [observacion_general],
            [fecha_creacion],
            [fecha_actualizacion],
            [id_plantilla_preguntas],
            [version_plantilla_preguntas]
        FROM [dbo].[formularios_operario];
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return self._rows_to_dicts(cursor, cursor.fetchall())

    def _guardar_todos(self, formularios: list[Formulario]) -> None:
        if not self.file_path:
            raise RuntimeError("No hay archivo JSON configurado para guardar.")

        JsonManager.write_json(
            str(self.file_path),
            [formulario.to_dict() for formulario in formularios],
        )

    def _formulario_desde_row(self, row: dict[str, Any]) -> Formulario:
        operario = self._normalizar_texto(row.get("operario_formulario"))
        if not operario:
            operario = self._normalizar_texto(row.get("operador_apontamento"))

        return Formulario(
            id_formulario=self._normalizar_texto(row.get("id_formulario")),
            identificador=self._normalizar_texto(row.get("identificador")),
            id_apontamento=self._normalizar_id_apontamento(row.get("id_apontamento")),
            fecha_formulario=self._serializar_fecha(row.get("fecha_formulario")),
            area=self._normalizar_texto(row.get("cod_setor")),
            maquina=self._normalizar_texto(row.get("cod_recurso")),
            cod_recurso=self._normalizar_texto(row.get("cod_recurso")),
            cod_setor=self._normalizar_texto(row.get("cod_setor")),
            turno=row.get("turno"),
            hora_fim=self._serializar_fecha(row.get("hora_fim")),
            operario=operario,
            supervisor_apontamento=self._normalizar_texto(
                row.get("supervisor_apontamento")
            ),
            estacion=self._normalizar_texto(row.get("estacion")),
            evento_origen=self._normalizar_texto(row.get("evento_origen")),
            estado=self._normalizar_texto(row.get("estado")),
            descripcion_op=self._normalizar_texto(row.get("descripcion_op")),
            descripcion_proceso=self._normalizar_texto(
                row.get("descripcion_proceso")
            ),
            observacion_general=self._normalizar_texto(
                row.get("observacion_general")
            ),
            fecha_creacion=self._serializar_fecha(row.get("fecha_creacion")),
            fecha_actualizacion=self._serializar_fecha(row.get("fecha_actualizacion")),
            id_plantilla_preguntas=self._normalizar_texto(
                row.get("id_plantilla_preguntas")
            ),
            version_plantilla_preguntas=int(
                row.get("version_plantilla_preguntas") or 0
            ),
        )

    def listar_formularios(self) -> list[Formulario]:
        if self._usar_json():
            return [
                Formulario.from_dict(item)
                for item in self._leer_todos_crudos()
            ]

        return [
            self._formulario_desde_row(item)
            for item in self._leer_todos_crudos()
        ]

    def obtener_por_id(self, id_formulario: str) -> Formulario | None:
        id_normalizado = str(id_formulario).strip()
        if not id_normalizado:
            return None

        if self._usar_json():
            for formulario in self.listar_formularios():
                if formulario.id_formulario == id_normalizado:
                    return formulario
            return None

        sql = """
        SELECT
            [id_formulario],
            [id_apontamento],
            [identificador],
            [fecha_formulario],
            [cod_recurso],
            [cod_setor],
            [turno],
            [hora_fim],
            [operador_apontamento],
            [supervisor_apontamento],
            [operario_formulario],
            [estacion],
            [evento_origen],
            [estado],
            [descripcion_op],
            [descripcion_proceso],
            [observacion_general],
            [fecha_creacion],
            [fecha_actualizacion],
            [id_plantilla_preguntas],
            [version_plantilla_preguntas]
        FROM [dbo].[formularios_operario]
        WHERE [id_formulario] = ?;
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return self._formulario_desde_row(rows[0]) if rows else None

    def obtener_por_id_apontamento(self, id_apontamento: str) -> Formulario | None:
        id_normalizado = self._normalizar_id_apontamento(id_apontamento)

        if self._usar_json():
            for formulario in self.listar_formularios():
                if formulario.id_apontamento == id_normalizado:
                    return formulario
            return None

        sql = """
        SELECT
            [id_formulario],
            [id_apontamento],
            [identificador],
            [fecha_formulario],
            [cod_recurso],
            [cod_setor],
            [turno],
            [hora_fim],
            [operador_apontamento],
            [supervisor_apontamento],
            [operario_formulario],
            [estacion],
            [evento_origen],
            [estado],
            [descripcion_op],
            [descripcion_proceso],
            [observacion_general],
            [fecha_creacion],
            [fecha_actualizacion],
            [id_plantilla_preguntas],
            [version_plantilla_preguntas]
        FROM [dbo].[formularios_operario]
        WHERE [id_apontamento] = ?;
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return self._formulario_desde_row(rows[0]) if rows else None

    def listar_por_estado(self, estado: str) -> list[Formulario]:
        estado_normalizado = str(estado).strip()
        if not estado_normalizado:
            return []

        if self._usar_json():
            return [
                formulario
                for formulario in self.listar_formularios()
                if formulario.estado == estado_normalizado
            ]

        sql = """
        SELECT
            [id_formulario],
            [id_apontamento],
            [identificador],
            [fecha_formulario],
            [cod_recurso],
            [cod_setor],
            [turno],
            [hora_fim],
            [operador_apontamento],
            [supervisor_apontamento],
            [operario_formulario],
            [estacion],
            [evento_origen],
            [estado],
            [descripcion_op],
            [descripcion_proceso],
            [observacion_general],
            [fecha_creacion],
            [fecha_actualizacion],
            [id_plantilla_preguntas],
            [version_plantilla_preguntas]
        FROM [dbo].[formularios_operario]
        WHERE [estado] = ?;
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (estado_normalizado,))
            rows = self._rows_to_dicts(cursor, cursor.fetchall())
            return [self._formulario_desde_row(row) for row in rows]

    def guardar(self, formulario: Formulario) -> Formulario:
        if self._usar_json():
            formularios = self.listar_formularios()

            for indice, actual in enumerate(formularios):
                if actual.id_formulario == formulario.id_formulario:
                    formularios[indice] = formulario
                    self._guardar_todos(formularios)
                    return formulario

            formularios.append(formulario)
            self._guardar_todos(formularios)
            return formulario

        with self._connect() as conn:
            cursor = conn.cursor()
            self._guardar_sql(cursor, formulario)
            conn.commit()

        return formulario

    def add_formulario(self, formulario: Formulario) -> Formulario:
        if self.obtener_por_id(formulario.id_formulario):
            raise ValueError(
                f"Ya existe un formulario con id {formulario.id_formulario}."
            )
        return self.guardar(formulario)

    def actualizar_formulario(
        self,
        id_formulario: str,
        cambios: dict,
    ) -> Formulario | None:
        formulario = self.obtener_por_id(id_formulario)
        if not formulario:
            return None

        formulario.actualizar(cambios)
        return self.guardar(formulario)

    def _guardar_sql(
        self,
        cursor: pyodbc.Cursor,
        formulario: Formulario,
    ) -> None:
        id_apontamento = self._normalizar_id_apontamento(formulario.id_apontamento)
        identificador = self._normalizar_texto(formulario.identificador)
        cod_recurso = self._normalizar_texto(formulario.cod_recurso or formulario.maquina)
        cod_setor = self._normalizar_texto(formulario.cod_setor or formulario.area)

        cursor.execute(
            """
            UPDATE [dbo].[formularios_operario]
            SET
                [id_apontamento] = ?,
                [identificador] = ?,
                [num_ordem] = ?,
                [fecha_formulario] = ?,
                [cod_recurso] = ?,
                [cod_setor] = ?,
                [turno] = ?,
                [hora_fim] = ?,
                [supervisor_apontamento] = ?,
                [operario_formulario] = ?,
                [estacion] = ?,
                [evento_origen] = ?,
                [estado] = ?,
                [descripcion_op] = ?,
                [descripcion_proceso] = ?,
                [observacion_general] = ?,
                [id_plantilla_preguntas] = ?,
                [version_plantilla_preguntas] = ?,
                [fecha_creacion] = COALESCE(?, [fecha_creacion]),
                [fecha_actualizacion] = COALESCE(?, SYSDATETIME())
            WHERE [id_formulario] = ?;
            """,
            (
                id_apontamento,
                identificador,
                identificador,
                self._fecha_sql(formulario.fecha_formulario),
                cod_recurso,
                cod_setor,
                formulario.turno,
                self._fecha_sql(formulario.hora_fim),
                self._normalizar_texto(formulario.supervisor_apontamento) or None,
                self._normalizar_texto(formulario.operario) or None,
                self._normalizar_texto(formulario.estacion) or None,
                self._normalizar_texto(formulario.evento_origen) or None,
                self._normalizar_texto(formulario.estado),
                self._normalizar_texto(formulario.descripcion_op) or None,
                self._normalizar_texto(formulario.descripcion_proceso) or None,
                self._normalizar_texto(formulario.observacion_general) or None,
                self._normalizar_texto(formulario.id_plantilla_preguntas),
                int(formulario.version_plantilla_preguntas or 0),
                self._fecha_sql(formulario.fecha_creacion),
                self._fecha_sql(formulario.fecha_actualizacion),
                formulario.id_formulario,
            ),
        )

        if cursor.rowcount > 0:
            return

        cursor.execute(
            """
            INSERT INTO [dbo].[formularios_operario] (
                [id_formulario],
                [id_apontamento],
                [identificador],
                [num_ordem],
                [fecha_formulario],
                [cod_recurso],
                [cod_setor],
                [turno],
                [hora_fim],
                [supervisor_apontamento],
                [operario_formulario],
                [estacion],
                [evento_origen],
                [estado],
                [descripcion_op],
                [descripcion_proceso],
                [observacion_general],
                [id_plantilla_preguntas],
                [version_plantilla_preguntas],
                [fecha_creacion],
                [fecha_actualizacion]
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE(?, SYSDATETIME()), COALESCE(?, SYSDATETIME()));
            """,
            (
                formulario.id_formulario,
                id_apontamento,
                identificador,
                identificador,
                self._fecha_sql(formulario.fecha_formulario),
                cod_recurso,
                cod_setor,
                formulario.turno,
                self._fecha_sql(formulario.hora_fim),
                self._normalizar_texto(formulario.supervisor_apontamento) or None,
                self._normalizar_texto(formulario.operario) or None,
                self._normalizar_texto(formulario.estacion) or None,
                self._normalizar_texto(formulario.evento_origen) or None,
                self._normalizar_texto(formulario.estado),
                self._normalizar_texto(formulario.descripcion_op) or None,
                self._normalizar_texto(formulario.descripcion_proceso) or None,
                self._normalizar_texto(formulario.observacion_general) or None,
                self._normalizar_texto(formulario.id_plantilla_preguntas),
                int(formulario.version_plantilla_preguntas or 0),
                self._fecha_sql(formulario.fecha_creacion),
                self._fecha_sql(formulario.fecha_actualizacion),
            ),
        )
