from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
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


class LoginView(BaseWindow):
    qss_files = ("base.qss", "login.qss")

    def __init__(self) -> None:
        super().__init__()

        self.auth_service = AuthService()
        self.presenter = LoginPresenter(self.auth_service)
        self.dashboard_gestion = None

        self.setObjectName("loginView")
        self.setWindowTitle("CDLform - Gestion")
        self.resize(500, 320)

        self._init_ui()
        self.apply_styles()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)
        layout_principal.setContentsMargins(32, 32, 32, 32)

        contenedor = CardFrame()
        contenedor.setMaximumWidth(380)

        layout = QVBoxLayout(contenedor)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Ingreso Gestion")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Accede al panel de administracion del sistema.")
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

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(8)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_password)
        layout.addSpacing(8)
        layout.addWidget(self.btn_ingresar)

        layout_principal.addWidget(contenedor)

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
            if self.presenter.iniciar_sesion(usuario, password):
                self.dashboard_gestion = DashboardGestionView()
                self.dashboard_gestion.show()
                self.close()
                return
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error de configuracion",
                f"No fue posible validar el acceso administrativo.\n\n{exc}",
            )
            return

        QMessageBox.warning(
            self,
            "Acceso denegado",
            "Usuario o contrasena incorrectos.",
        )

