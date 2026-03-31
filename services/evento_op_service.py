from models.evento_op import EventoOP
from repositories.evento_op_repository import EventoOPRepository
from utils.id_generator import generate_id


class EventoOPService:
    def __init__(self) -> None:
        self.repository = EventoOPRepository()

    def crear_evento(
        self,
        num_ordem: str,
        estado_anterior: str,
        estado_nuevo: str,
        fecha_evento: str,
        id_apontamento: float | None = None,
        cod_recurso: str | None = None,
        operador: str | None = None,
        cod_ativ: str | None = None,
        cod_setor: str | None = None,
        turno: int | None = None,
        dt_producao: str | None = None,
        hora_inicio: str | None = None,
        hora_fim: str | None = None,
        descricao_op: str | None = None,
        descricao_processo: str | None = None,
        obs: str | None = None,
        qtd_produzida: int | None = None,
        qtd_planejado: float | None = None,
        qtd_perdas: int | None = None,
        justificativa_perda: str | None = None,
    ) -> dict:
        if not num_ordem or not str(num_ordem).strip():
            raise ValueError("num_ordem es obligatorio.")

        if not estado_nuevo or not str(estado_nuevo).strip():
            raise ValueError("estado_nuevo es obligatorio.")

        evento = EventoOP(
            id_evento=generate_id("EVOP", self.repository.get_all(), "id_evento"),
            num_ordem=str(num_ordem).strip(),
            estado_anterior=str(estado_anterior or "").strip(),
            estado_nuevo=str(estado_nuevo).strip(),
            fecha_evento=str(fecha_evento or "").strip(),
            id_apontamento=id_apontamento,
            cod_recurso=cod_recurso,
            operador=operador,
            cod_ativ=cod_ativ,
            cod_setor=cod_setor,
            turno=turno,
            dt_producao=dt_producao,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            descricao_op=descricao_op,
            descricao_processo=descricao_processo,
            obs=obs,
            qtd_produzida=qtd_produzida,
            qtd_planejado=qtd_planejado,
            qtd_perdas=qtd_perdas,
            justificativa_perda=justificativa_perda,
            procesado=False,
        )

        self.repository.add(evento.to_dict())
        return evento.to_dict()

    def listar_eventos(self) -> list[dict]:
        return self.repository.get_all()

    def buscar_por_num_ordem(self, num_ordem: str) -> list[dict]:
        return [
            evento
            for evento in self.repository.get_all()
            if str(evento.get("num_ordem", "")).strip() == str(num_ordem).strip()
        ]

    def obtener_no_procesados(self) -> list[dict]:
        return [
            evento
            for evento in self.repository.get_all()
            if not evento.get("procesado", False)
        ]

    def obtener_por_id(self, id_evento: str) -> dict | None:
        return self.repository.find_by_id(id_evento)

    def marcar_como_procesado(self, id_evento: str) -> bool:
        evento = self.obtener_por_id(id_evento)
        if not evento:
            return False

        evento["procesado"] = True
        self.repository.update_by_id(id_evento, evento)
        return True

    def ya_existe_evento_equivalente(
        self,
        num_ordem: str,
        estado_anterior: str,
        estado_nuevo: str,
        fecha_evento: str | None = None,
    ) -> bool:
        for evento in self.repository.get_all():
            mismo_evento = (
                str(evento.get("num_ordem", "")).strip() == str(num_ordem).strip()
                and str(evento.get("estado_anterior", "")).strip() == str(estado_anterior).strip()
                and str(evento.get("estado_nuevo", "")).strip() == str(estado_nuevo).strip()
            )

            if not mismo_evento:
                continue

            if fecha_evento is None:
                return True

            if str(evento.get("fecha_evento", "")).strip() == str(fecha_evento).strip():
                return True

        return False

    def actualizar_evento(self, id_evento: str, cambios: dict) -> bool:
        evento = self.obtener_por_id(id_evento)
        if not evento:
            return False

        evento.update(cambios)
        self.repository.update_by_id(id_evento, evento)
        return True