from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame,
)

from ui.dashboard_gestion import DashboardGestionView


class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CDLform - Gestión")
        self.resize(500, 320)

        self.dashboard_gestion = None

        self._init_ui()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)

        contenedor = QFrame()
        contenedor.setMaximumWidth(380)

        layout = QVBoxLayout(contenedor)
        layout.setSpacing(12)

        titulo = QLabel("Ingreso Gestión")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_login")

        subtitulo = QLabel("Acceso para administración y gestión de formularios")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Usuario")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_ingresar = QPushButton("Ingresar")
        self.btn_ingresar.clicked.connect(self.iniciar_sesion)

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_ingresar)

        layout_principal.addWidget(contenedor)

    def iniciar_sesion(self) -> None:
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()

        if not usuario or not password:
            QMessageBox.warning(self, "Validación", "Debes ingresar usuario y contraseña.")
            return

        # Login temporal de desarrollo
        if usuario == "admin" and password == "1234":
            self.dashboard_gestion = DashboardGestionView()
            self.dashboard_gestion.show()
            self.close()
            return

        QMessageBox.warning(
            self,
            "Acceso denegado",
            "Usuario o contraseña incorrectos.\n\nCredenciales temporales:\nUsuario: admin\nContraseña: 1234",
        )