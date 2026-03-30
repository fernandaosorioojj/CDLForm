from __future__ import annotations

from models.disparador_formulario import DisparadorFormulario
from services.disparador_service import DisparadorService


class EventProcessor:
    def __init__(self) -> None:
        self.disparador_service = DisparadorService()

    def process_event(self, id_evento: str) -> DisparadorFormulario:
        return self.disparador_service.process_event(id_evento)

    def process_pending_events(self) -> list[DisparadorFormulario]:
        return self.disparador_service.process_pending_events()