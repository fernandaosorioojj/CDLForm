"""Widgets PyQt reutilizables para construir pantallas.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget

from styles.theme import THEME

from styles.common import apply_view_style


# Bloque CDLform: clase BaseWindow; agrupa estado y comportamiento de esta parte del flujo.
class BaseWindow(QWidget):
    qss_files: tuple[str, ...] = ("base.qss",)

    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    # Bloque CDLform: funcion/metodo apply_styles; encapsula una operacion del flujo del modulo.
    def apply_styles(self) -> None:
        apply_view_style(self, *self.qss_files)

    # Bloque CDLform: funcion/metodo paintEvent; encapsula una operacion del flujo del modulo.
    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(THEME.bg_app))

        painter.end()
        super().paintEvent(event)
