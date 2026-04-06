from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class EventoOP:
    id_evento: str
    id_apontamento: str
    num_ordem: str

    cod_recurso: str | None = None
    operador: str | None = None
    cod_ativ: str | None = None
    cod_setor: str | None = None
    turno: str | None = None

    dt_producao: str | None = None
    hora_inicio: str | None = None
    hora_fim: str | None = None

    descricao_op: str | None = None
    descricao_processo: str | None = None
    obs: str | None = None

    qtd_produzida: int | float | None = None
    qtd_planejado: int | float | None = None
    qtd_perdas: int | float | None = None
    justificativa_perda: str | None = None

    estacao_origen: str | None = None
    contexto_resuelto: dict[str, Any] | None = None
    id_formulario_generado: str | None = None
    mensaje_error: str | None = None
    procesado: bool = False

    estado_anterior: str | None = None
    estado_nuevo: str | None = None
    fecha_evento: str | None = None

    def __post_init__(self) -> None:
        self.id_evento = str(self.id_evento).strip()
        self.id_apontamento = str(self.id_apontamento).strip()
        self.num_ordem = str(self.num_ordem).strip()

        if not self.id_evento:
            raise ValueError("id_evento es obligatorio.")

        if not self.id_apontamento:
            raise ValueError("id_apontamento es obligatorio.")

        if not self.num_ordem:
            raise ValueError("num_ordem es obligatorio.")

        self.cod_recurso = self._normalizar_opcional(self.cod_recurso)
        self.operador = self._normalizar_opcional(self.operador)
        self.cod_ativ = self._normalizar_opcional(self.cod_ativ)
        self.cod_setor = self._normalizar_opcional(self.cod_setor)
        self.turno = self._normalizar_opcional(self.turno)

        self.dt_producao = self._normalizar_opcional(self.dt_producao)
        self.hora_inicio = self._normalizar_opcional(self.hora_inicio)
        self.hora_fim = self._normalizar_opcional(self.hora_fim)

        self.descricao_op = self._normalizar_opcional(self.descricao_op)
        self.descricao_processo = self._normalizar_opcional(self.descricao_processo)
        self.obs = self._normalizar_opcional(self.obs)

        self.justificativa_perda = self._normalizar_opcional(self.justificativa_perda)

        self.estacao_origen = self._normalizar_opcional(self.estacao_origen)
        self.id_formulario_generado = self._normalizar_opcional(self.id_formulario_generado)
        self.mensaje_error = self._normalizar_opcional(self.mensaje_error)

        self.estado_anterior = self._normalizar_opcional(self.estado_anterior)
        self.estado_nuevo = self._normalizar_opcional(self.estado_nuevo)
        self.fecha_evento = self._normalizar_opcional(self.fecha_evento)

        if self.contexto_resuelto is not None and not isinstance(self.contexto_resuelto, dict):
            raise ValueError("contexto_resuelto debe ser un diccionario o None.")

        self.procesado = bool(self.procesado)

    @staticmethod
    def _normalizar_opcional(valor: Any) -> str | None:
        if valor is None:
            return None

        valor_normalizado = str(valor).strip()
        return valor_normalizado or None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "EventoOP":
        return EventoOP(
            id_evento=data["id_evento"],
            id_apontamento=str(
                data.get("id_apontamento")
                or data.get("id_evento")
                or ""
            ).strip(),
            num_ordem=data["num_ordem"],
            cod_recurso=data.get("cod_recurso"),
            operador=data.get("operador"),
            cod_ativ=data.get("cod_ativ"),
            cod_setor=data.get("cod_setor"),
            turno=data.get("turno"),
            dt_producao=data.get("dt_producao"),
            hora_inicio=data.get("hora_inicio"),
            hora_fim=data.get("hora_fim"),
            descricao_op=data.get("descricao_op"),
            descricao_processo=data.get("descricao_processo"),
            obs=data.get("obs"),
            qtd_produzida=data.get("qtd_produzida"),
            qtd_planejado=data.get("qtd_planejado"),
            qtd_perdas=data.get("qtd_perdas"),
            justificativa_perda=data.get("justificativa_perda"),
            estacao_origen=data.get("estacao_origen"),
            contexto_resuelto=data.get("contexto_resuelto"),
            id_formulario_generado=data.get("id_formulario_generado"),
            mensaje_error=data.get("mensaje_error"),
            procesado=data.get("procesado", False),
            estado_anterior=data.get("estado_anterior"),
            estado_nuevo=data.get("estado_nuevo"),
            fecha_evento=data.get("fecha_evento"),
        )