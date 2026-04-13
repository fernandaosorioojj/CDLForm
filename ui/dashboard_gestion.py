from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from presenters.dashboard_gestion_presenter import DashboardGestionPresenter
from widgets.base_window import BaseWindow
from widgets.card_frame import CardFrame


class DashboardGestionView(BaseWindow):
    qss_files = ("base.qss", "dashboard_gestion.qss")

    def __init__(self) -> None:
        super().__init__()

        self.presenter = DashboardGestionPresenter()
        self.admin_preguntas_view = None
        self.reportes_view = None
        self.auditoria_formularios_view = None
        self.eventos_view = None

        self.setObjectName("dashboardGestionView")
        self.setWindowTitle("CDLform - Gestion")
        self.resize(1000, 650)

        self._init_ui()
        self.apply_styles()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(20)
        layout_principal.setContentsMargins(32, 28, 32, 28)

        titulo = QLabel("Panel de Gestion CDLform")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Administracion general del sistema de formularios")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)
        layout_principal.addSpacing(10)

        contenedor = CardFrame()
        grid = QGridLayout(contenedor)
        grid.setSpacing(16)
        grid.setContentsMargins(24, 24, 24, 24)

        btn_preguntas = QPushButton("Administrar Preguntas")
        btn_reportes = QPushButton("Reportes")
        btn_auditoria = QPushButton("Auditoria de Plantillas")
        btn_salir = QPushButton("Cerrar sesion")

        btn_salir.setProperty("variant", "danger")

        btn_preguntas.setMinimumHeight(54)
        btn_reportes.setMinimumHeight(54)
        btn_auditoria.setMinimumHeight(54)
        btn_salir.setMinimumHeight(50)

        btn_preguntas.clicked.connect(self.abrir_admin_preguntas)
        btn_reportes.clicked.connect(self.abrir_reportes)
        btn_auditoria.clicked.connect(self.abrir_auditoria_formularios)
        btn_salir.clicked.connect(self.close)

        grid.addWidget(btn_preguntas, 0, 0)
        grid.addWidget(btn_reportes, 0, 1)
        grid.addWidget(btn_auditoria, 1, 0, 1, 2)
        grid.addWidget(btn_salir, 2, 0, 1, 2)

        layout_principal.addWidget(contenedor)
        layout_principal.addStretch()

    def abrir_admin_preguntas(self) -> None:
        try:
            self.admin_preguntas_view = self.presenter.crear_admin_preguntas_view()
            self.admin_preguntas_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir la administracion de preguntas.\n\n{exc}",
            )

    def abrir_reportes(self) -> None:
        try:
            self.reportes_view = self.presenter.crear_reportes_view()
            self.reportes_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir el modulo de reportes.\n\n{exc}",
            )

    def abrir_auditoria_formularios(self) -> None:
        try:
            self.auditoria_formularios_view = (
                self.presenter.crear_auditoria_formularios_view()
            )
            self.auditoria_formularios_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir la auditoria de formularios.\n\n{exc}",
            )
