"""Coordinacion de apertura de ventanas y formularios pendientes en el cliente operario.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt5.QtCore import QObject, QTimer

from launcher.app_launcher import AppLauncher
from services.workflows.disparador_service import DisparadorService

LOGGER = logging.getLogger(__name__)


# Bloque CDLform: clase PendingFormCoordinator; agrupa estado y comportamiento de esta parte del flujo.
class PendingFormCoordinator(QObject):
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        formulario_launcher: AppLauncher | None = None,
        disparador_service: DisparadorService | None = None,
        interval_ms: int = 15000,
    ) -> None:
        super().__init__()
        self.formulario_launcher = formulario_launcher or AppLauncher()
        self.disparador_service = disparador_service or DisparadorService()
        self.interval_ms = max(1000, int(interval_ms))

        self._timer = QTimer(self)
        self._timer.setInterval(self.interval_ms)
        self._timer.timeout.connect(self.revisar_pendientes)
        self._revisando = False
        self.ultimo_resultado: dict[str, Any] | None = None

    # Bloque CDLform: funcion/metodo iniciar; encapsula una operacion del flujo del modulo.
    def iniciar(self, revisar_inmediatamente: bool = True) -> None:
        if not self._timer.isActive():
            self._timer.start()

        if revisar_inmediatamente:
            QTimer.singleShot(0, self.revisar_pendientes)

    # Bloque CDLform: funcion/metodo detener; encapsula una operacion del flujo del modulo.
    def detener(self) -> None:
        if self._timer.isActive():
            self._timer.stop()

    # Bloque CDLform: funcion/metodo revisar_pendientes; encapsula una operacion del flujo del modulo.
    def revisar_pendientes(self) -> dict[str, Any]:
        if self._revisando:
            return self.ultimo_resultado or {
                "se_preparo": False,
                "motivo": "revision_en_curso",
                "formulario": None,
            }

        if self.formulario_launcher.tiene_ventanas_abiertas():
            self.ultimo_resultado = {
                "se_preparo": False,
                "motivo": "ventana_activa",
                "formulario": None,
            }
            return self.ultimo_resultado

        self._revisando = True

        try:
            try:
                resultado = self.disparador_service.preparar_siguiente_formulario_pendiente()
            except Exception as exc:
                LOGGER.exception("No fue posible revisar formularios pendientes.")
                resultado = {
                    "se_preparo": False,
                    "motivo": "error_revision",
                    "formulario": None,
                    "error": str(exc),
                }
            self.ultimo_resultado = resultado

            formulario = resultado.get("formulario")
            if resultado.get("se_preparo") and formulario is not None:
                self.formulario_launcher.abrir_formulario_pendiente_operario(
                    formulario=formulario,
                    on_close=self.disparador_service.liberar_formulario_en_apertura,
                )

            return resultado
        finally:
            self._revisando = False
