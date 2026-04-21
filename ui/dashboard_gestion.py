from __future__ import annotations

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from presenters.dashboard_gestion_presenter import DashboardGestionPresenter
from utils.assets import image_path
from widgets.base_window import BaseWindow
from widgets.asset_image import AssetImage


class DashboardGestionView(BaseWindow):
    qss_files = ("base.qss", "dashboard_gestion.qss")

    def __init__(self) -> None:
        super().__init__()

        self.presenter = DashboardGestionPresenter()
        self.admin_preguntas_view = None
        self.reportes_view = None
        self.auditoria_formularios_view = None
        self.acciones_correctivas_view = None
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

        encabezado = QFrame()
        encabezado.setProperty("visualPanel", "true")
        encabezado_layout = QHBoxLayout(encabezado)
        encabezado_layout.setContentsMargins(24, 22, 24, 22)
        encabezado_layout.setSpacing(24)

        textos = QVBoxLayout()
        textos.setSpacing(8)

        eyebrow = QLabel("Centro de gestion")
        eyebrow.setProperty("role", "eyebrow")

        titulo = QLabel("Panel de Gestion CDLform")
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Administracion general del sistema de formularios")
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        textos.addWidget(eyebrow)
        textos.addWidget(titulo)
        textos.addWidget(subtitulo)
        textos.addStretch()

        encabezado_layout.addLayout(textos, 1)
        encabezado_layout.addWidget(AssetImage("workflow-illustration.svg", 260, 150))

        layout_principal.addWidget(encabezado)

        contenedor = QFrame()
        contenedor.setObjectName("dashboardActions")
        grid = QGridLayout(contenedor)
        grid.setSpacing(16)
        grid.setContentsMargins(0, 0, 0, 0)

        btn_preguntas = self._crear_tarjeta_accion(
            texto="Administrar Preguntas",
            icono="icon-questions.svg",
            accent="accent",
        )
        btn_reportes = self._crear_tarjeta_accion(
            texto="Reportes",
            icono="icon-reports.svg",
            accent="light",
        )
        btn_acciones = self._crear_tarjeta_accion(
            texto="Acciones Correctivas",
            icono="icon-corrective.svg",
            accent="mid",
        )
        btn_auditoria = self._crear_tarjeta_accion(
            texto="Auditoria de Plantillas",
            icono="icon-audit.svg",
            accent="soft",
        )
        btn_salir = self._crear_tarjeta_accion(
            texto="Cerrar sesion",
            icono="icon-audit.svg",
            accent="danger",
        )

        btn_preguntas.clicked.connect(self.abrir_admin_preguntas)
        btn_reportes.clicked.connect(self.abrir_reportes)
        btn_acciones.clicked.connect(self.abrir_acciones_correctivas)
        btn_auditoria.clicked.connect(self.abrir_auditoria_formularios)
        btn_salir.clicked.connect(self.close)

        grid.addWidget(btn_preguntas, 0, 0)
        grid.addWidget(btn_reportes, 0, 1)
        grid.addWidget(btn_acciones, 1, 0)
        grid.addWidget(btn_auditoria, 1, 1)
        grid.addWidget(btn_salir, 2, 0, 1, 2)

        layout_principal.addWidget(contenedor)
        layout_principal.addStretch()

    def _crear_tarjeta_accion(
        self,
        *,
        texto: str,
        icono: str,
        accent: str,
    ) -> QPushButton:
        boton = QPushButton(texto)
        boton.setProperty("dashboardTile", True)
        boton.setProperty("tileAccent", accent)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setIcon(QIcon(image_path(icono)))
        boton.setIconSize(QSize(30, 30))
        boton.setMinimumHeight(118)

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(28)
        sombra.setOffset(0, 10)
        sombra.setColor(Qt.black)
        boton.setGraphicsEffect(sombra)

        return boton

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

    def abrir_acciones_correctivas(self) -> None:
        try:
            self.acciones_correctivas_view = (
                self.presenter.crear_acciones_correctivas_view()
            )
            self.acciones_correctivas_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir las acciones correctivas.\n\n{exc}",
            )
