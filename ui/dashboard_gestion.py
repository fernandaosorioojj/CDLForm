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


class DashboardGestionView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CDLform - Gestión")
        self.resize(1000, 650)

        self.admin_preguntas_view = None
        self.admin_operarios_view = None
        self.formularios_view = None
        self.reportes_view = None
        self.eventos_view = None

        self._init_ui()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(20)

        titulo = QLabel("Panel de Gestión CDLform")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_dashboard")

        subtitulo = QLabel("Administración general del sistema de formularios")
        subtitulo.setAlignment(Qt.AlignCenter)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        contenedor = QFrame()
        grid = QGridLayout(contenedor)
        grid.setSpacing(15)

        btn_preguntas = QPushButton("Administrar Preguntas")
        btn_operarios = QPushButton("Administrar Operarios")
        btn_formularios = QPushButton("Ver Formularios")
        btn_reportes = QPushButton("Reportes")
        btn_eventos = QPushButton("Eventos / Disparadores")
        btn_salir = QPushButton("Cerrar sesión")

        btn_preguntas.clicked.connect(self.abrir_admin_preguntas)
        btn_operarios.clicked.connect(self.abrir_admin_operarios)
        btn_formularios.clicked.connect(self.abrir_formularios)
        btn_reportes.clicked.connect(self.abrir_reportes)
        btn_eventos.clicked.connect(self.abrir_eventos)
        btn_salir.clicked.connect(self.close)

        grid.addWidget(btn_preguntas, 0, 0)
        grid.addWidget(btn_operarios, 0, 1)
        grid.addWidget(btn_formularios, 1, 0)
        grid.addWidget(btn_reportes, 1, 1)
        grid.addWidget(btn_eventos, 2, 0, 1, 2)
        grid.addWidget(btn_salir, 3, 0, 1, 2)

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

    def abrir_admin_operarios(self) -> None:
        QMessageBox.information(
            self,
            "Pendiente",
            "Aquí se conectará la administración de operarios.",
        )

    def abrir_formularios(self) -> None:
        QMessageBox.information(
            self,
            "Pendiente",
            "Aquí se conectará la visualización de formularios.",
        )

    def abrir_reportes(self) -> None:
        QMessageBox.information(
            self,
            "Pendiente",
            "Aquí se conectará el módulo de reportes.",
        )

    def abrir_eventos(self) -> None:
        QMessageBox.information(
            self,
            "Pendiente",
            "Aquí se conectará el módulo de eventos y disparadores.",
        )