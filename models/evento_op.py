from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class EventoOP:
    id_evento: str
    num_ordem: str
    estado_anterior: str
    estado_nuevo: str
    fecha_evento: str

    id_apontamento: Optional[float] = None
    cod_recurso: Optional[str] = None
    operador: Optional[str] = None
    cod_ativ: Optional[str] = None
    cod_setor: Optional[str] = None
    turno: Optional[int] = None

    dt_producao: Optional[str] = None
    hora_inicio: Optional[str] = None
    hora_fim: Optional[str] = None

    descricao_op: Optional[str] = None
    descricao_processo: Optional[str] = None
    obs: Optional[str] = None

    qtd_produzida: Optional[int] = None
    qtd_planejado: Optional[float] = None
    qtd_perdas: Optional[int] = None
    justificativa_perda: Optional[str] = None

    estacao_origen: Optional[str] = None
    contexto_resuelto: Optional[dict] = None
    id_formulario_generado: Optional[str] = None
    mensaje_error: Optional[str] = None
    procesado: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "EventoOP":
        return EventoOP(
            id_evento=data["id_evento"],
            num_ordem=data["num_ordem"],
            estado_anterior=data["estado_anterior"],
            estado_nuevo=data["estado_nuevo"],
            fecha_evento=data["fecha_evento"],
            id_apontamento=data.get("id_apontamento"),
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
        )