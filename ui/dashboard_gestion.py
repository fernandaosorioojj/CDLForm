from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
    QMessageBox,
)

from ui.admin_preguntas import AdminPreguntasView
from ui.reportes import ReportesView


class DashboardGestionView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CDLform - Gestión")
        self.resize(1000, 650)

        self.admin_preguntas_view = None
        self.reportes_view = None
        self.eventos_view = None

        self._init_ui()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(20)
        layout_principal.setContentsMargins(32, 28, 32, 28)

        titulo = QLabel("Panel de Gestión CDLform")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Administración general del sistema de formularios")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)
        layout_principal.addSpacing(10)

        contenedor = QFrame()
        contenedor.setProperty("card", "true")

        grid = QGridLayout(contenedor)
        grid.setSpacing(16)
        grid.setContentsMargins(24, 24, 24, 24)

        btn_preguntas = QPushButton("Administrar Preguntas")
        btn_reportes = QPushButton("Reportes")
        btn_salir = QPushButton("Cerrar sesión")

        btn_reportes.setProperty("variant", "secondary")
        btn_salir.setProperty("variant", "danger")

        btn_preguntas.setMinimumHeight(54)
        btn_reportes.setMinimumHeight(54)
        btn_salir.setMinimumHeight(50)

        btn_preguntas.clicked.connect(self.abrir_admin_preguntas)
        btn_reportes.clicked.connect(self.abrir_reportes)
        btn_salir.clicked.connect(self.close)

        grid.addWidget(btn_preguntas, 0, 0)
        grid.addWidget(btn_reportes, 0, 1)
        grid.addWidget(btn_salir, 1, 0, 1, 2)

        layout_principal.addWidget(contenedor)
        layout_principal.addStretch()

    def abrir_admin_preguntas(self) -> None:
        try:
            self.admin_preguntas_view = AdminPreguntasView()
            self.admin_preguntas_view.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir la administración de preguntas.\n\n{str(e)}",
            )

    def abrir_reportes(self) -> None:
        try:
            self.reportes_view = ReportesView()
            self.reportes_view.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir el módulo de reportes.\n\n{str(e)}",
            )