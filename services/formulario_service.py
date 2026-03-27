from __future__ import annotations

from core.enums import FormularioEstado, OrigenEvento
from core.exceptions import BusinessRuleError, NotFoundError
from models.formulario import Formulario
from repositories.formulario_repository import FormularioRepository
from utils.datetime_utils import DateTimeUtils
from utils.id_generator import IdGenerator


class FormularioService:
    def __init__(self) -> None:
        self.repository = FormularioRepository()

    def list_all(self) -> list[Formulario]:
        return self.repository.list_all()

    def get_by_id(self, id_formulario: str) -> Formulario:
        return self.repository.get_by_id(id_formulario)

    def get_by_op(self, op: str) -> list[Formulario]:
        return self.repository.get_by_op(op)

    def create_from_event(
        self,
        op: str,
        area: str,
        maquina: str,
        id_evento_origen: str,
        origen_disparo: OrigenEvento = OrigenEvento.JOBTRACK,
        fecha: str | None = None,
    ) -> Formulario:
        formularios_existentes = self.repository.list_all()
        next_number = len(formularios_existentes) + 1
        id_formulario = IdGenerator.generate("FORM", next_number)

        if self.repository.get_by_evento_origen(id_evento_origen):
            raise BusinessRuleError(
                f"ya existe un formulario asociado al evento '{id_evento_origen}'"
            )

        fecha_formulario = (
            DateTimeUtils.normalize_datetime_string(fecha, "fecha")
            if fecha is not None
            else DateTimeUtils.now_as_string()
        )

        formulario = Formulario(
            id_formulario=id_formulario,
            op=op,
            area=area,
            maquina=maquina,
            fecha=fecha_formulario,
            estado_formulario=FormularioEstado.PENDIENTE,
            id_evento_origen=id_evento_origen,
            origen_disparo=origen_disparo,
        )

        self.repository.add(formulario)
        return formulario

    def update_estado(
        self,
        id_formulario: str,
        nuevo_estado: FormularioEstado,
    ) -> Formulario:
        formulario_actual = self.repository.get_by_id(id_formulario)

        if not isinstance(nuevo_estado, FormularioEstado):
            raise TypeError("nuevo_estado debe ser una instancia de FormularioEstado")

        formulario_actualizado = Formulario(
            id_formulario=formulario_actual.id_formulario,
            op=formulario_actual.op,
            area=formulario_actual.area,
            maquina=formulario_actual.maquina,
            fecha=formulario_actual.fecha,
            estado_formulario=nuevo_estado,
            id_evento_origen=formulario_actual.id_evento_origen,
            origen_disparo=formulario_actual.origen_disparo,
        )

        self.repository.update(formulario_actualizado)
        return formulario_actualizado

    def mark_as_in_progress(self, id_formulario: str) -> Formulario:
        return self.update_estado(id_formulario, FormularioEstado.EN_PROCESO)

    def mark_as_completed(self, id_formulario: str) -> Formulario:
        return self.update_estado(id_formulario, FormularioEstado.COMPLETADO)

    def mark_as_annulled(self, id_formulario: str) -> Formulario:
        return self.update_estado(id_formulario, FormularioEstado.ANULADO)

    def delete(self, id_formulario: str) -> None:
        self.repository.delete(id_formulario)

    def ensure_exists(self, id_formulario: str) -> None:
        try:
            self.repository.get_by_id(id_formulario)
        except NotFoundError as exc:
            raise NotFoundError(
                f"no existe un formulario con id '{id_formulario}'"
            ) from exc