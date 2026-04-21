from __future__ import annotations

import math

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QLinearGradient, QPainter, QRadialGradient
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

        width = max(1, self.width())
        height = max(1, self.height())
        t = self._animation_time

        start_x = width * (-0.10 + 0.10 * math.sin(t * 0.18))
        end_x = width * (1.05 + 0.08 * math.cos(t * 0.16))
        start_y = height * (0.04 + 0.08 * math.cos(t * 0.14))
        end_y = height * (0.96 + 0.07 * math.sin(t * 0.15))

        gradient = QLinearGradient(start_x, start_y, end_x, end_y)
        gradient.setColorAt(0.00, QColor(THEME.gradient_accent))
        gradient.setColorAt(0.30, QColor(THEME.gradient_start))
        gradient.setColorAt(0.66, QColor(THEME.gradient_mid))
        gradient.setColorAt(1.00, QColor(THEME.gradient_end))

        painter.fillRect(self.rect(), gradient)

        halo_accent = QRadialGradient(
            width * (0.18 + 0.18 * math.sin(t * 0.25)),
            height * (0.24 + 0.11 * math.cos(t * 0.21)),
            width * 0.78,
        )
        accent_core = QColor(THEME.gradient_accent)
        accent_core.setAlpha(138)
        halo_accent.setColorAt(0.0, accent_core)
        halo_accent.setColorAt(0.34, QColor(0, 224, 174, 62))
        halo_accent.setColorAt(0.72, QColor(57, 153, 124, 22))
        halo_accent.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(self.rect(), halo_accent)

        halo_green = QRadialGradient(
            width * (0.78 + 0.15 * math.cos(t * 0.20)),
            height * (0.20 + 0.11 * math.sin(t * 0.23)),
            width * 0.74,
        )
        green_core = QColor(THEME.gradient_start)
        green_core.setAlpha(116)
        halo_green.setColorAt(0.0, green_core)
        halo_green.setColorAt(0.38, QColor(57, 153, 124, 54))
        halo_green.setColorAt(0.74, QColor(81, 105, 94, 18))
        halo_green.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(self.rect(), halo_green)

        halo_mid = QRadialGradient(
            width * (0.50 + 0.16 * math.sin(t * 0.18 + 1.2)),
            height * (0.84 + 0.08 * math.cos(t * 0.20)),
            width * 0.98,
        )
        mid_core = QColor(THEME.gradient_mid)
        mid_core.setAlpha(94)
        halo_mid.setColorAt(0.0, mid_core)
        halo_mid.setColorAt(0.32, QColor(81, 105, 94, 46))
        halo_mid.setColorAt(0.58, QColor(255, 255, 255, 34))
        halo_mid.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(self.rect(), halo_mid)

        painter.end()
        super().paintEvent(event)
