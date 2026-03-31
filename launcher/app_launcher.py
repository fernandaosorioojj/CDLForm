import sys
from PyQt5.QtWidgets import QApplication

from ui.seleccion_operario import SeleccionOperarioView


class AppLauncher:
    def lanzar_formulario(self, evento: dict) -> None:
        app = QApplication.instance()
        debe_crear_app = app is None

        if debe_crear_app:
            app = QApplication(sys.argv)

        ventana = SeleccionOperarioView(evento=evento)
        ventana.showMaximized()

        if debe_crear_app:
            app.exec_()