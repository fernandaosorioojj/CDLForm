from __future__ import annotations

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget

from styles.theme import THEME

from styles.common import apply_view_style


class BaseWindow(QWidget):
    qss_files: tuple[str, ...] = ("base.qss",)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("animatedBackground", True)
        self._animation_time = 0.0
        self._gradient_timer = QTimer(self)
        self._gradient_timer.setInterval(36)
        self._gradient_timer.timeout.connect(self._advance_gradient)
        self._gradient_timer.start()

    def apply_styles(self) -> None:
        apply_view_style(self, *self.qss_files)

    def _advance_gradient(self) -> None:
        self._animation_time += 0.010
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(THEME.bg_app))

        painter.end()
        super().paintEvent(event)
