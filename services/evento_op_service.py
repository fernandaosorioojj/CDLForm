from __future__ import annotations

from typing import Any

from models.evento_op import EventoOP
from repositories.evento_op_repository import EventoOPRepository
from utils.id_generator import generate_id


class EventoOPService:
    def __init__(self) -> None:
        self.repository = EventoOPRepository()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def listar_eventos(self) -> list[dict]:
        return self.repository.get_all()

    def obtener_por_id(self, id_evento: str) -> dict | None:
        id_evento_normalizado = self._normalizar_texto(id_evento)
        if not id_evento_normalizado:
            return None
        return self.repository.find_by_id(id_evento_normalizado)

    def obtener_por_id_apontamento(self, id_apontamento: str | int) -> dict | None:
        id_apontamento_normalizado = self._normalizar_texto(id_apontamento)

        if not id_apontamento_normalizado:
            return None

        for evento in self.repository.get_all():
            if self._normalizar_texto(evento.get("id_apontamento")) == id_apontamento_normalizado:
                return evento

        return None

    def buscar_por_num_ordem(self, num_ordem: str) -> list[dict]:
        num_ordem_normalizada = self._normalizar_texto(num_ordem)

        return [
            evento
            for evento in self.repository.get_all()
            if self._normalizar_texto(evento.get("num_ordem")) == num_ordem_normalizada
        ]

    def obtener_no_procesados(self) -> list[dict]:
        return [
            evento
            for evento in self.repository.get_all()
            if not bool(evento.get("procesado", False))
        ]

    def ya_existe_por_id_apontamento(self, id_apontamento: str | int) -> bool:
        return self.obtener_por_id_apontamento(id_apontamento) is not None

    def registrar_evento_desde_apontamento(
        self,
        id_apontamento: str | int,
        num_ordem: str,
        cod_recurso: str | None = None,
        operador: str | None = None,
        cod_ativ: str | None = None,
        cod_setor: str | None = None,
        turno: str | int | None = None,
        dt_producao: str | None = None,
        hora_inicio: str | None = None,
        hora_fim: str | None = None,
        descricao_op: str | None = None,
        descricao_processo: str | None = None,
        obs: str | None = None,
        qtd_produzida: int | float | None = None,
        qtd_planejado: int | float | None = None,
        qtd_perdas: int | float | None = None,
        justificativa_perda: str | None = None,
        datos_extra: dict[str, Any] | None = None,
    ) -> dict:
        id_apontamento_normalizado = self._normalizar_texto(id_apontamento)
        num_ordem_normalizada = self._normalizar_texto(num_ordem)

        if not id_apontamento_normalizado:
            raise ValueError("id_apontamento es obligatorio.")

        if not num_ordem_normalizada:
            raise ValueError("num_ordem es obligatorio.")

        existente = self.obtener_por_id_apontamento(id_apontamento_normalizado)
        if existente:
            return existente

        payload: dict[str, Any] = {
            "id_evento": generate_id("EVOP", self.repository.get_all(), "id_evento"),
            "id_apontamento": id_apontamento_normalizado,
            "num_ordem": num_ordem_normalizada,
            "cod_recurso": self._normalizar_texto(cod_recurso),
            "operador": self._normalizar_texto(operador),
            "cod_ativ": self._normalizar_texto(cod_ativ),
            "cod_setor": self._normalizar_texto(cod_setor),
            "turno": self._normalizar_texto(turno),
            "dt_producao": self._normalizar_texto(dt_producao),
            "hora_inicio": self._normalizar_texto(hora_inicio),
            "hora_fim": self._normalizar_texto(hora_fim),
            "descricao_op": self._normalizar_texto(descricao_op),
            "descricao_processo": self._normalizar_texto(descricao_processo),
            "obs": self._normalizar_texto(obs),
            "qtd_produzida": qtd_produzida,
            "qtd_planejado": qtd_planejado,
            "qtd_perdas": qtd_perdas,
            "justificativa_perda": self._normalizar_texto(justificativa_perda),
            "procesado": False,
        }

        if datos_extra:
            payload.update(datos_extra)

        try:
            evento = EventoOP(**payload)
            data = evento.to_dict()
        except Exception:
            data = payload

        self.repository.add(data)
        return data

    def marcar_como_procesado(self, id_evento: str) -> bool:
        evento = self.obtener_por_id(id_evento)
        if not evento:
            return False

        evento["procesado"] = True
        self.repository.update_by_id(id_evento, evento)
        return True

    def marcar_por_id_apontamento_como_procesado(self, id_apontamento: str | int) -> bool:
        evento = self.obtener_por_id_apontamento(id_apontamento)
        if not evento:
            return False

        id_evento = self._normalizar_texto(evento.get("id_evento"))
        if not id_evento:
            return False

        evento["procesado"] = True
        self.repository.update_by_id(id_evento, evento)
        return True

    def actualizar_evento(self, id_evento: str, cambios: dict[str, Any]) -> bool:
        evento = self.obtener_por_id(id_evento)
        if not evento:
            return False

        evento.update(cambios)
        self.repository.update_by_id(id_evento, evento)
        return True