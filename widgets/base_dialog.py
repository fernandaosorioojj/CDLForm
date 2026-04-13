from PyQt5.QtWidgets import QDialog

from styles.common import apply_view_style


class BaseDialog(QDialog):
    qss_files: tuple[str, ...] = ("base.qss", "dialogs.qss")

    def apply_styles(self) -> None:
        apply_view_style(self, *self.qss_files)

