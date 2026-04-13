from PyQt5.QtWidgets import QWidget

from styles.common import apply_view_style


class BaseWindow(QWidget):
    qss_files: tuple[str, ...] = ("base.qss",)

    def apply_styles(self) -> None:
        apply_view_style(self, *self.qss_files)

