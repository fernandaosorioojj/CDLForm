from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from utils.assets import image_path


class AssetImage(QLabel):
    def __init__(
        self,
        filename: str,
        width: int = 220,
        height: int = 160,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._source = QPixmap(image_path(filename))
        self._target_width = width
        self._target_height = height

        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(width, height)
        self.setMaximumHeight(height)
        self.setProperty("assetImage", "true")

        if self._source.isNull():
            self.setText("")
            return

        self._refresh_pixmap()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._refresh_pixmap()

    def _refresh_pixmap(self) -> None:
        if self._source.isNull():
            return

        width = min(self.width() or self._target_width, self._target_width)
        height = min(self.height() or self._target_height, self._target_height)
        self.setPixmap(
            self._source.scaled(
                width,
                height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )
