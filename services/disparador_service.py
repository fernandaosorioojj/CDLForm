from __future__ import annotations

from typing import Any

from services.apontamento_procesado_service import ApontamentoProcesadoService
from services.apontamento_query_service import ApontamentoQueryService
from services.catalogo_contexto_service import CatalogoContextoService
from services.formulario_service import FormularioService
from services.jobtrack_config_service import JobtrackConfigService


class DisparadorService:
    def __init__(
        self,
        server: str,
        database: str,
        username: str,
        password: str,
        driver: str = "ODBC Driver 18 for SQL Server",
        processed_file: str = "storage/apontamentos_procesados.json",
    ) -> None:
        self.catalogo_service = CatalogoContextoService()
        self.formulario_service = FormularioService()
        self.jobtrack_config_service = JobtrackConfigService()

        self.apontamento_query_service = ApontamentoQueryService(
            server=server,
            database=database,
            username=username,
            password=password,
            driver=driver,
        )

        self.apontamento_procesado_service = ApontamentoProcesadoService(
            processed_file=processed_file,
        )

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def obtener_estacion_actual(self) -> str:
        return self.jobtrack_config_service.obtener_estacion_actual()

    def buscar_apontamentos_pendientes(self) -> list[dict[str, Any]]:
        estacion = self.obtener_estacion_actual()

        if not estacion:
            return []

        ids_procesados = self.apontamento_procesado_service.listar_ids_procesados()

        return self.apontamento_query_service.buscar_apontamentos_pendientes(
            estacion=estacion,
            ids_excluidos=ids_procesados,
        )

    def homologar_evento_desde_apontamento(self, apontamento: dict[str, Any]) -> dict[str, Any]:
        return {
            "id_evento": self._normalizar_texto(apontamento.get("IdApontamento")),
            "id_apontamento": self._normalizar_texto(apontamento.get("IdApontamento")),
            "num_ordem": self._normalizar_texto(apontamento.get("NumOrdem")),
            "cod_recurso": self._normalizar_texto(apontamento.get("CodRecurso")),
            "cod_setor": self._normalizar_texto(apontamento.get("CodSetor")),
            "cod_ativ": self._normalizar_texto(apontamento.get("CodAtiv")),
            "turno": self._normalizar_texto(apontamento.get("Turno")),
            "hora_fim": self._normalizar_texto(apontamento.get("HoraFim")),
            "operador": self._normalizar_texto(apontamento.get("Operador")),
            "descripcion_op": self._normalizar_texto(apontamento.get("DescricaoOP")),
            "descripcion_proceso": self._normalizar_texto(apontamento.get("DescricaoProcesso")),
            "qtd_produzida": apontamento.get("QtdProduzida"),
            "qtd_planejado": apontamento.get("QtdPlanejado"),
            "qtd_perdas": apontamento.get("QtdPerdas"),
            "justificativa_perda": self._normalizar_texto(apontamento.get("JustificativaPerda")),
        }

    def debe_disparar(self, apontamento: dict[str, Any]) -> bool:
        id_apontamento = self._normalizar_texto(apontamento.get("IdApontamento"))
        hora_fim = self._normalizar_texto(apontamento.get("HoraFim"))
        cod_recurso = self._normalizar_texto(apontamento.get("CodRecurso"))

        if not id_apontamento:
            return False

        if not cod_recurso:
            return False

        if not hora_fim:
            return False

        if hora_fim in {"1899-12-30 00:00:00", "1899-12-30 00:00:00.000"}:
            return False

        if self.apontamento_procesado_service.ya_procesado(id_apontamento):
            return False

        return True

    def procesar_apontamento(
        self,
        apontamento: dict[str, Any],
        operario: str = "PENDIENTE",
    ) -> dict[str, Any]:
        resultado: dict[str, Any] = {
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

        identificador = self._normalizar_texto(evento.get("num_ordem"))

        if not identificador:
            resultado["mensaje"] = "El apontamento no trae num_ordem para generar el formulario."
            return resultado

        formulario = self.formulario_service.crear_formulario(
            identificador=identificador,
            operario=operario,
            contexto=contexto,
            evento_origen=self._normalizar_texto(evento.get("id_evento")),
            estado="pendiente",
        )

        self.apontamento_procesado_service.marcar_como_procesado(
            id_apontamento=evento.get("id_apontamento", ""),
            num_ordem=evento.get("num_ordem", ""),
            datos_extra={
                "cod_recurso": evento.get("cod_recurso", ""),
                "turno": evento.get("turno", ""),
                "hora_fim": evento.get("hora_fim", ""),
            },
        )

        resultado["debe_disparar"] = True
        resultado["formulario"] = formulario.to_dict()
        resultado["mensaje"] = "Formulario generado correctamente desde apontamento."
        return resultado

    def procesar_pendientes(self, operario: str = "PENDIENTE") -> list[dict[str, Any]]:
        pendientes = self.buscar_apontamentos_pendientes()
        resultados: list[dict[str, Any]] = []

        for apontamento in pendientes:
            resultado = self.procesar_apontamento(apontamento, operario=operario)
            resultados.append(resultado)

        return resultados