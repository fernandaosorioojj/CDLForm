from __future__ import annotations

from typing import Any

from services.disparador_service import DisparadorService
from services.jobtrack_config_service import JobtrackConfigService


class EventProcessor:
    def __init__(
        self,
        server: str,
        database: str,
        username: str,
        password: str,
        driver: str = "ODBC Driver 18 for SQL Server",
        processed_file: str = "storage/apontamentos_procesados.json",
    ) -> None:
        self.jobtrack_config_service = JobtrackConfigService()
        self.disparador_service = DisparadorService(
            server=server,
            database=database,
            username=username,
            password=password,
            driver=driver,
            processed_file=processed_file,
        )

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @staticmethod
    def _obtener_primero(payload: dict[str, Any], *claves: str) -> Any:
        for clave in claves:
            if clave in payload and payload[clave] is not None:
                return payload[clave]
        return None

    def obtener_estacion_actual(self) -> str:
        return self.jobtrack_config_service.obtener_estacion_actual()

    def normalizar_evento_externo(self, payload: dict[str, Any]) -> dict[str, Any]:
        estacion_actual = self.obtener_estacion_actual()

        id_apontamento = self._obtener_primero(
            payload,
            "IdApontamento",
            "id_apontamento",
            "idApontamento",
            "id_evento",
            "IdEvento",
        )

        num_ordem = self._obtener_primero(
            payload,
            "NumOrdem",
            "num_ordem",
            "numOrdem",
            "op",
            "identificador",
        )

        cod_recurso = self._obtener_primero(
            payload,
            "CodRecurso",
            "cod_recurso",
            "codRecurso",
            "estacion",
            "Estacao",
        )

        cod_setor = self._obtener_primero(
            payload,
            "CodSetor",
            "cod_setor",
            "codSetor",
        )

        cod_ativ = self._obtener_primero(
            payload,
            "CodAtiv",
            "cod_ativ",
            "codAtiv",
        )

        turno = self._obtener_primero(
            payload,
            "Turno",
            "turno",
        )

        hora_fim = self._obtener_primero(
            payload,
            "HoraFim",
            "hora_fim",
            "horaFim",
            "fecha_fin",
            "dt_fim",
        )

        operador = self._obtener_primero(
            payload,
            "Operador",
            "operador",
        )

        descricao_op = self._obtener_primero(
            payload,
            "DescricaoOP",
            "descricao_op",
            "descripcion_op",
        )

        descricao_processo = self._obtener_primero(
            payload,
            "DescricaoProcesso",
            "descricao_processo",
            "descripcion_proceso",
        )

        qtd_produzida = self._obtener_primero(
            payload,
            "QtdProduzida",
            "qtd_produzida",
        )

        qtd_planejado = self._obtener_primero(
            payload,
            "QtdPlanejado",
            "qtd_planejado",
        )

        qtd_perdas = self._obtener_primero(
            payload,
            "QtdPerdas",
            "qtd_perdas",
        )

        justificativa_perda = self._obtener_primero(
            payload,
            "JustificativaPerda",
            "justificativa_perda",
        )

        evento_normalizado = {
            "id_evento": self._normalizar_texto(id_apontamento),
            "id_apontamento": self._normalizar_texto(id_apontamento),
            "num_ordem": self._normalizar_texto(num_ordem),
            "cod_recurso": self._normalizar_texto(cod_recurso) or estacion_actual,
            "cod_setor": self._normalizar_texto(cod_setor),
            "cod_ativ": self._normalizar_texto(cod_ativ),
            "turno": self._normalizar_texto(turno),
            "hora_fim": self._normalizar_texto(hora_fim),
            "operador": self._normalizar_texto(operador),
            "descripcion_op": self._normalizar_texto(descricao_op),
            "descripcion_proceso": self._normalizar_texto(descricao_processo),
            "qtd_produzida": qtd_produzida,
            "qtd_planejado": qtd_planejado,
            "qtd_perdas": qtd_perdas,
            "justificativa_perda": self._normalizar_texto(justificativa_perda),
            "estacion_actual": self._normalizar_texto(estacion_actual),
        }

        return evento_normalizado

    def convertir_evento_a_apontamento(self, evento: dict[str, Any]) -> dict[str, Any]:
        return {
            "IdApontamento": evento.get("id_apontamento", ""),
            "NumOrdem": evento.get("num_ordem", ""),
            "CodRecurso": evento.get("cod_recurso", ""),
            "CodSetor": evento.get("cod_setor", ""),
            "CodAtiv": evento.get("cod_ativ", ""),
            "Turno": evento.get("turno", ""),
            "HoraFim": evento.get("hora_fim", ""),
            "Operador": evento.get("operador", ""),
            "DescricaoOP": evento.get("descripcion_op", ""),
            "DescricaoProcesso": evento.get("descripcion_proceso", ""),
            "QtdProduzida": evento.get("qtd_produzida"),
            "QtdPlanejado": evento.get("qtd_planejado"),
            "QtdPerdas": evento.get("qtd_perdas"),
            "JustificativaPerda": evento.get("justificativa_perda", ""),
        }

    def procesar_evento_externo(
        self,
        payload: dict[str, Any],
        operario: str = "PENDIENTE",
    ) -> dict[str, Any]:
        evento_normalizado = self.normalizar_evento_externo(payload)
        apontamento = self.convertir_evento_a_apontamento(evento_normalizado)

        resultado = self.disparador_service.procesar_apontamento(
            apontamento,
            operario=operario,
        )

        resultado["evento_normalizado"] = evento_normalizado
        return resultado