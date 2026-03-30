from __future__ import annotations

from core.enums import (
    DisparadorEstado,
    EventoEstadoProcesamiento,
)
from core.exceptions import BusinessRuleError, NotFoundError
from models.disparador_formulario import DisparadorFormulario
from models.evento_op import EventoOP
from repositories.disparador_formulario_repository import (
    DisparadorFormularioRepository,
)
from services.evento_op_service import EventoOPService
from services.formulario_service import FormularioService
from utils.datetime_utils import DateTimeUtils
from utils.id_generator import IdGenerator


class DisparadorService:
    def __init__(self) -> None:
        self.repository = DisparadorFormularioRepository()
        self.evento_service = EventoOPService()
        self.formulario_service = FormularioService()

    def list_all(self) -> list[DisparadorFormulario]:
        return self.repository.list_all()

    def get_by_id(self, id_disparador: str) -> DisparadorFormulario:
        return self.repository.get_by_id(id_disparador)

    def get_by_evento(self, id_evento: str) -> list[DisparadorFormulario]:
        return self.repository.get_by_evento(id_evento)

    def get_by_op(self, op: str) -> list[DisparadorFormulario]:
        return self.repository.get_by_op(op)

    def get_by_estado(
        self,
        estado_disparo: DisparadorEstado,
    ) -> list[DisparadorFormulario]:
        return self.repository.get_by_estado(estado_disparo)

    def _next_id(self) -> str:
        next_number = len(self.repository.list_all()) + 1
        return IdGenerator.generate("DISP", next_number)

    def _create_record(
        self,
        id_evento: str,
        op: str,
        estado_disparo: DisparadorEstado,
        mensaje: str | None = None,
    ) -> DisparadorFormulario:
        disparador = DisparadorFormulario(
            id_disparador=self._next_id(),
            id_evento=id_evento,
            op=op,
            fecha_disparo=DateTimeUtils.now_as_string(),
            estado_disparo=estado_disparo,
            mensaje=mensaje,
        )

        self.repository.add(disparador)
        return disparador

    def process_event(self, id_evento: str) -> DisparadorFormulario:
        evento = self.evento_service.get_by_id(id_evento)

        if evento.estado_procesamiento == EventoEstadoProcesamiento.PROCESADO:
            raise BusinessRuleError(
                f"el evento '{id_evento}' ya fue procesado previamente"
            )

        if self.get_by_evento(id_evento):
            raise BusinessRuleError(
                f"ya existe al menos un disparador asociado al evento '{id_evento}'"
            )

        if not self.evento_service.is_trigger_status(evento.estado_nuevo):
            disparador = self._create_record(
                id_evento=evento.id_evento,
                op=evento.op,
                estado_disparo=DisparadorEstado.OMITIDO,
                mensaje=(
                    f"el estado '{evento.estado_nuevo}' no corresponde a un estado disparador"
                ),
            )

            self.evento_service.mark_as_processed(evento.id_evento)
            return disparador

        try:
            formulario = self.formulario_service.create_from_event(
                op=evento.op,
                area=evento.area,
                maquina=evento.maquina,
                id_evento_origen=evento.id_evento,
                origen_disparo=evento.origen,
                fecha=evento.fecha_evento,
            )

            disparador = self._create_record(
                id_evento=evento.id_evento,
                op=evento.op,
                estado_disparo=DisparadorEstado.PROCESADO,
                mensaje=(
                    f"formulario '{formulario.id_formulario}' generado correctamente"
                ),
            )

            self.evento_service.mark_as_processed(evento.id_evento)
            return disparador

        except Exception as exc:
            return self._create_record(
                id_evento=evento.id_evento,
                op=evento.op,
                estado_disparo=DisparadorEstado.FALLIDO,
                mensaje=str(exc),
            )

    def process_pending_events(self) -> list[DisparadorFormulario]:
        resultados: list[DisparadorFormulario] = []

        for evento in self.evento_service.get_pending_events():
            resultado = self.process_event(evento.id_evento)
            resultados.append(resultado)

        return resultados

    def delete(self, id_disparador: str) -> None:
        self.repository.delete(id_disparador)

    def ensure_exists(self, id_disparador: str) -> None:
        try:
            self.repository.get_by_id(id_disparador)
        except NotFoundError as exc:
            raise NotFoundError(
                f"no existe un disparador con id '{id_disparador}'"
            ) from exc