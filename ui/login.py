"""Vistas PyQt que componen las pantallas de gestion y operario.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from presenters.login_presenter import LoginPresenter
from services.security.auth_service import AuthService
from ui.dashboard_gestion import DashboardGestionView
from widgets.base_window import BaseWindow
from widgets.card_frame import CardFrame
from widgets.asset_image import AssetImage


# Bloque CDLform: clase LoginView; agrupa estado y comportamiento de esta parte del flujo.
class LoginView(BaseWindow):
    qss_files = ("base.qss", "login.qss")

    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self) -> None:
        super().__init__()

        self.auth_service = AuthService()
        self.presenter = LoginPresenter(self.auth_service)
        self.dashboard_gestion = None

        self.setObjectName("loginView")
        self.setWindowTitle("CDLform - Gestion")
        self.resize(820, 440)

        self._init_ui()
        self.apply_styles()

    # Bloque CDLform: funcion/metodo _init_ui; encapsula una operacion del flujo del modulo.
    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)
        layout_principal.setContentsMargins(32, 32, 32, 32)

        shell = QFrame()
        shell.setObjectName("loginShell")
        shell_layout = QHBoxLayout(shell)
        shell_layout.setSpacing(18)
        shell_layout.setContentsMargins(10, 10, 10, 10)

        visual = QFrame()
        visual.setObjectName("loginVisual")
        visual.setProperty("visualPanel", "true")
        visual_layout = QVBoxLayout(visual)
        visual_layout.setSpacing(14)
        visual_layout.setContentsMargins(28, 28, 28, 28)

        logo = AssetImage("cdl-logo.svg", width=96, height=96)
        logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        visual_eyebrow = QLabel("Bienvenida")
        visual_eyebrow.setProperty("role", "eyebrow")

        visual_titulo = QLabel("CDLform")
        visual_titulo.setProperty("role", "title")

        visual_subtitulo = QLabel(
            "Gestiona formularios, auditorias y reportes desde un espacio mas claro y ordenado."
        )
        visual_subtitulo.setWordWrap(True)
        visual_subtitulo.setProperty("role", "subtitle")

        ilustracion = AssetImage("workflow-illustration.svg", width=280, height=190)

        visual_layout.addWidget(logo)
        visual_layout.addWidget(visual_eyebrow)
        visual_layout.addWidget(visual_titulo)
        visual_layout.addWidget(visual_subtitulo)
        visual_layout.addStretch()
        visual_layout.addWidget(ilustracion)

        contenedor = CardFrame()
        contenedor.setObjectName("loginCard")
        contenedor.setMaximumWidth(380)

        layout = QVBoxLayout(contenedor)
        layout.setSpacing(12)
        layout.setContentsMargins(28, 28, 28, 28)

        eyebrow = QLabel("Acceso")
        eyebrow.setAlignment(Qt.AlignCenter)
        eyebrow.setProperty("role", "eyebrow")

        titulo = QLabel("Ingreso Gestion")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Entra al tablero para revisar actividad, reportes y seguimiento.")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Usuario")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contrasena")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_ingresar = QPushButton("Ingresar")
        self.btn_ingresar.clicked.connect(self.iniciar_sesion)

        layout.addWidget(eyebrow)
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(10)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_password)
        layout.addSpacing(10)
        layout.addWidget(self.btn_ingresar)

        shell_layout.addWidget(visual, 1)
        shell_layout.addWidget(contenedor, 1)
        layout_principal.addWidget(shell)

    # Bloque CDLform: funcion/metodo iniciar_sesion; encapsula una operacion del flujo del modulo.
    def iniciar_sesion(self) -> None:
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()

        valido, mensaje = self.presenter.validar_credenciales_ingresadas(
            usuario,
            password,
        )
        if not valido:
            QMessageBox.warning(
                self,
                "Validacion",
                mensaje,
            )
            return

        try:
            sesion = self.presenter.autenticar_usuario(usuario, password)
            if sesion:
                self.dashboard_gestion = DashboardGestionView(
                    usuario=sesion.get("usuario", usuario),
                    rol=sesion.get("rol", "gestion"),
                )
                self.dashboard_gestion.show()
                self.close()
                return
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error de configuracion",
                f"No fue posible validar el acceso de Gestion.\n\n{exc}",
            )
            return

        QMessageBox.warning(
            self,
            "Acceso denegado",
            "Usuario o contrasena incorrectos.",
        )

