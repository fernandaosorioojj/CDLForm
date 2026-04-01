from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pyodbc

from launcher.app_launcher import AppLauncher
from services.catalogo_contexto_service import CatalogoContextoService
from services.evento_op_service import EventoOPService
from services.formulario_service import FormularioService
from services.jobtrack_config_service import JobtrackConfigService


class DisparadorService:
    def __init__(
        self,
        server: str,
        database: str,
        username: str,
        password: str,
        driver: str = "ODBC Driver 17 for SQL Server",
        processed_file: str | Path = "storage/apontamentos_procesados.json",
    ) -> None:
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver

        self.evento_service = EventoOPService()
        self.launcher = AppLauncher()
        self.catalogo_service = CatalogoContextoService()
        self.formulario_service = FormularioService()
        self.jobtrack_config_service = JobtrackConfigService()

        self.processed_file = Path(processed_file)
        self._ensure_processed_file()

    def _ensure_processed_file(self) -> None:
        self.processed_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.processed_file.exists():
            self.processed_file.write_text("[]", encoding="utf-8")

    def _read_processed(self) -> list[dict[str, Any]]:
        try:
            return json.loads(self.processed_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _write_processed(self, data: list[dict[str, Any]]) -> None:
        self.processed_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )

    def ya_procesado(self, id_apontamento: str | int) -> bool:
        id_normalizado = str(id_apontamento).strip()
        registros = self._read_processed()

        return any(
            str(item.get("id_apontamento", "")).strip() == id_normalizado
            for item in registros
        )

    def marcar_como_procesado(self, id_apontamento: str | int, num_ordem: str = "") -> None:
        if self.ya_procesado(id_apontamento):
            return

        registros = self._read_processed()
        registros.append(
            {
                "id_apontamento": str(id_apontamento).strip(),
                "num_ordem": str(num_ordem).strip(),
            }
        )
        self._write_processed(registros)

    def obtener_estacion_actual(self) -> str:
        return self.jobtrack_config_service.obtener_estacion_actual()

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

    def buscar_apontamentos_pendientes(self) -> list[dict[str, Any]]:
        estacion = self.obtener_estacion_actual()

        sql = """
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
          AND [CodRecurso] = ?
        ORDER BY [HoraFim] DESC
        """

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (estacion,))
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

        candidatos: list[dict[str, Any]] = []

        for row in rows:
            registro = dict(zip(columns, row))
            id_apontamento = registro.get("IdApontamento")

            if id_apontamento is None:
                continue

            if self.ya_procesado(id_apontamento):
                continue

            candidatos.append(registro)

        return candidatos

    def homologar_evento_desde_apontamento(self, apontamento: dict[str, Any]) -> dict[str, Any]:
        return {
            "id_evento": str(apontamento.get("IdApontamento", "")).strip(),
            "id_apontamento": str(apontamento.get("IdApontamento", "")).strip(),
            "num_ordem": str(apontamento.get("NumOrdem", "")).strip(),
            "cod_recurso": str(apontamento.get("CodRecurso", "")).strip(),
            "cod_setor": str(apontamento.get("CodSetor", "")).strip(),
            "cod_ativ": str(apontamento.get("CodAtiv", "")).strip(),
            "turno": str(apontamento.get("Turno", "")).strip(),
            "hora_fim": str(apontamento.get("HoraFim", "")).strip(),
            "operador": str(apontamento.get("Operador", "")).strip(),
            "descripcion_op": str(apontamento.get("DescricaoOP", "")).strip(),
            "descripcion_proceso": str(apontamento.get("DescricaoProcesso", "")).strip(),
            "qtd_produzida": apontamento.get("QtdProduzida"),
            "qtd_planejado": apontamento.get("QtdPlanejado"),
            "qtd_perdas": apontamento.get("QtdPerdas"),
            "justificativa_perda": str(apontamento.get("JustificativaPerda", "")).strip(),
        }

    def debe_disparar(self, apontamento: dict[str, Any]) -> bool:
        id_apontamento = str(apontamento.get("IdApontamento", "")).strip()
        hora_fim = str(apontamento.get("HoraFim", "")).strip()
        cod_recurso = str(apontamento.get("CodRecurso", "")).strip()

        if not id_apontamento:
            return False

        if not cod_recurso:
            return False

        if not hora_fim:
            return False

        if hora_fim == "1899-12-30 00:00:00":
            return False

        if hora_fim == "1899-12-30 00:00:00.000":
            return False

        if self.ya_procesado(id_apontamento):
            return False

        return True

    def procesar_apontamento(self, apontamento: dict[str, Any], operario: str = "PENDIENTE") -> dict:
        resultado = {
            "debe_disparar": False,
            "formulario": None,
            "contexto_resuelto": None,
            "mensaje": "",
            "evento_homologado": None,
        }

        if not self.debe_disparar(apontamento):
            resultado["mensaje"] = "El apontamento no cumple condiciones de disparo."
            return resultado

        evento = self.homologar_evento_desde_apontamento(apontamento)
        resultado["evento_homologado"] = evento

        contexto = self.catalogo_service.resolver_contexto(
            cod_setor=evento.get("cod_setor"),
            cod_recurso=evento.get("cod_recurso"),
            cod_ativ=evento.get("cod_ativ"),
            turno=evento.get("turno"),
        )

        resultado["contexto_resuelto"] = contexto

        if not contexto.get("cod_setor"):
            resultado["mensaje"] = "No se pudo homologar el cod_setor del apontamento."
            return resultado

        if not contexto.get("cod_recurso"):
            resultado["mensaje"] = "No se pudo homologar el cod_recurso del apontamento."
            return resultado

        formulario = self.formulario_service.crear_formulario(
            identificador=str(evento.get("num_ordem", "")).strip(),
            operario=operario,
            contexto=contexto,
            evento_origen=str(evento.get("id_evento", "")).strip(),
            estado="pendiente",
        )

        self.marcar_como_procesado(
            id_apontamento=evento.get("id_apontamento", ""),
            num_ordem=evento.get("num_ordem", ""),
        )

        resultado["debe_disparar"] = True
        resultado["formulario"] = formulario.to_dict()
        resultado["mensaje"] = "Formulario generado correctamente desde apontamento."
        return resultado

    def procesar_pendientes(self, operario: str = "PENDIENTE") -> list[dict]:
        pendientes = self.buscar_apontamentos_pendientes()
        resultados: list[dict] = []

        for apontamento in pendientes:
            resultado = self.procesar_apontamento(apontamento, operario=operario)
            resultados.append(resultado)

        return resultados