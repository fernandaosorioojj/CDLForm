"""Vistas PyQt que componen las pantallas de gestion y operario.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from presenters.usuarios_gestion_presenter import UsuariosGestionPresenter
from styles.common import apply_view_style


# Bloque CDLform: clase UsuariosGestionView; agrupa estado y comportamiento de esta parte del flujo.
class UsuariosGestionView(QWidget):
    qss_files = ("base.qss", "usuarios_gestion.qss")

    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        presenter: UsuariosGestionPresenter | None = None,
    ) -> None:
        super().__init__()

        self.presenter = presenter or UsuariosGestionPresenter()
        self.usuario_seleccionado = ""

        self.setWindowTitle("Administracion de Usuarios")
        self.setObjectName("usuariosGestionView")
        self.resize(1100, 720)

        self._init_ui()
        apply_view_style(self, *self.qss_files)
        self.cargar_usuarios()

    # Bloque CDLform: funcion/metodo _init_ui; encapsula una operacion del flujo del modulo.
    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(16)

        top_panel = QFrame()
        top_panel.setObjectName("usuariosTopPanel")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(18, 18, 18, 18)
        top_layout.setSpacing(14)

        header_panel = QFrame()
        header_panel.setObjectName("usuariosHeader")
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(22, 20, 22, 20)
        header_layout.setSpacing(6)

        eyebrow = QLabel("Gestion")
        eyebrow.setProperty("role", "eyebrow")

        titulo = QLabel("Administracion de Usuarios")
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Crea usuarios de gestion y actualiza sus credenciales.")
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        header_layout.addWidget(eyebrow)
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        top_layout.addWidget(header_panel)
        layout_principal.addWidget(top_panel)

        contenido = QHBoxLayout()
        contenido.setSpacing(16)

        panel_form = QFrame()
        panel_form.setProperty("card", "true")
        panel_form.setMaximumWidth(380)
        form_layout = QVBoxLayout(panel_form)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(12)

        label_form = QLabel("Credenciales")
        label_form.setProperty("role", "section")

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Usuario")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contrasena")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.input_password_confirmacion = QLineEdit()
        self.input_password_confirmacion.setPlaceholderText("Confirmar contrasena")
        self.input_password_confirmacion.setEchoMode(QLineEdit.Password)

        self.check_activo = QCheckBox("Activo")
        self.check_activo.setChecked(True)

        self.combo_rol = QComboBox()
        self.combo_rol.addItem("Admin", "admin")
        self.combo_rol.addItem("Gestion", "gestion")
        self.combo_rol.setCurrentIndex(1)

        self.btn_guardar = QPushButton("Crear / actualizar")
        self.btn_guardar.clicked.connect(self.guardar_usuario)

        self.btn_actualizar_rol = QPushButton("Actualizar rol")
        self.btn_actualizar_rol.setProperty("variant", "secondary")
        self.btn_actualizar_rol.clicked.connect(self.actualizar_rol)

        self.btn_cambiar_password = QPushButton("Cambiar contrasena")
        self.btn_cambiar_password.setProperty("variant", "secondary")
        self.btn_cambiar_password.clicked.connect(self.cambiar_password)

        self.btn_activar = QPushButton("Activar")
        self.btn_activar.setProperty("variant", "secondary")
        self.btn_activar.clicked.connect(lambda: self.actualizar_activo(True))

        self.btn_desactivar = QPushButton("Desactivar")
        self.btn_desactivar.setProperty("variant", "danger")
        self.btn_desactivar.clicked.connect(lambda: self.actualizar_activo(False))

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setProperty("variant", "secondary")
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)

        form_layout.addWidget(label_form)
        form_layout.addWidget(self.input_usuario)
        form_layout.addWidget(self.input_password)
        form_layout.addWidget(self.input_password_confirmacion)
        form_layout.addWidget(self.combo_rol)
        form_layout.addWidget(self.check_activo)
        form_layout.addSpacing(8)
        form_layout.addWidget(self.btn_guardar)
        form_layout.addWidget(self.btn_cambiar_password)
        form_layout.addWidget(self.btn_actualizar_rol)
        form_layout.addWidget(self.btn_activar)
        form_layout.addWidget(self.btn_desactivar)
        form_layout.addWidget(self.btn_limpiar)
        form_layout.addStretch()

        panel_tabla = QFrame()
        panel_tabla.setProperty("card", "true")
        tabla_layout = QVBoxLayout(panel_tabla)
        tabla_layout.setContentsMargins(18, 18, 18, 18)
        tabla_layout.setSpacing(12)

        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(6)
        self.tabla_usuarios.setHorizontalHeaderLabels(
            [
                "ID",
                "Usuario",
                "Rol",
                "Estado",
                "Creado",
                "Actualizado",
            ]
        )
        self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_usuarios.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_usuarios.verticalHeader().setVisible(False)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tabla_usuarios.horizontalHeader().setStretchLastSection(True)
        self.tabla_usuarios.itemSelectionChanged.connect(self.cargar_seleccion)

        self.label_total = QLabel("Usuarios: 0")
        self.label_total.setProperty("role", "subtitle")

        self.btn_recargar = QPushButton("Recargar")
        self.btn_recargar.setProperty("variant", "secondary")
        self.btn_recargar.clicked.connect(self.cargar_usuarios)

        fila_total = QHBoxLayout()
        fila_total.addWidget(self.label_total, 1)
        fila_total.addWidget(self.btn_recargar)

        tabla_layout.addWidget(self.tabla_usuarios)
        tabla_layout.addLayout(fila_total)

        contenido.addWidget(panel_form, 0)
        contenido.addWidget(panel_tabla, 1)
        layout_principal.addLayout(contenido, 1)

    # Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo cargar_usuarios; encapsula una operacion del flujo del modulo.
    def cargar_usuarios(self) -> None:
        try:
            usuarios = self.presenter.listar_usuarios()
            self._cargar_tabla(usuarios)
            self.label_total.setText(f"Usuarios: {len(usuarios)}")
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    # Bloque CDLform: funcion/metodo _cargar_tabla; encapsula una operacion del flujo del modulo.
    def _cargar_tabla(self, usuarios: list[dict[str, Any]]) -> None:
        self.tabla_usuarios.setRowCount(0)

        for usuario in usuarios:
            row = self.tabla_usuarios.rowCount()
            self.tabla_usuarios.insertRow(row)
            self._set_item(row, 0, usuario.get("id_usuario"), usuario)
            self._set_item(row, 1, usuario.get("usuario"))
            self._set_item(row, 2, usuario.get("rol") or "gestion")
            self._set_item(row, 3, "Activo" if usuario.get("activo") else "Inactivo")
            self._set_item(row, 4, usuario.get("fecha_creacion"))
            self._set_item(row, 5, usuario.get("fecha_actualizacion"))

    # Bloque CDLform: funcion/metodo cargar_seleccion; encapsula una operacion del flujo del modulo.
    def cargar_seleccion(self) -> None:
        usuario = self._obtener_usuario_seleccionado()
        self.usuario_seleccionado = usuario.get("usuario", "") if usuario else ""
        self.input_usuario.setText(self.usuario_seleccionado)
        self.check_activo.setChecked(bool(usuario.get("activo")) if usuario else True)
        self._seleccionar_rol(usuario.get("rol") if usuario else "gestion")
        self.input_password.clear()
        self.input_password_confirmacion.clear()

    # Bloque CDLform: funcion/metodo guardar_usuario; encapsula una operacion del flujo del modulo.
    def guardar_usuario(self) -> None:
        try:
            usuario = self.input_usuario.text().strip()
            password = self._obtener_password_validado()
            mensaje = self.presenter.crear_o_actualizar_usuario(
                usuario=usuario,
                password=password,
                rol=str(self.combo_rol.currentData() or "gestion"),
                activo=self.check_activo.isChecked(),
            )
            QMessageBox.information(self, "Usuarios", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        except Exception as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))

    # Bloque CDLform: funcion/metodo actualizar_rol; encapsula una operacion del flujo del modulo.
    def actualizar_rol(self) -> None:
        try:
            usuario = self.input_usuario.text().strip() or self.usuario_seleccionado
            mensaje = self.presenter.actualizar_rol(
                usuario,
                str(self.combo_rol.currentData() or "gestion"),
            )
            QMessageBox.information(self, "Usuarios", mensaje)
            self.cargar_usuarios()
        except Exception as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))

    # Bloque CDLform: funcion/metodo cambiar_password; encapsula una operacion del flujo del modulo.
    def cambiar_password(self) -> None:
        try:
            usuario = self.input_usuario.text().strip() or self.usuario_seleccionado
            password = self._obtener_password_validado()
            mensaje = self.presenter.cambiar_password(usuario, password)
            QMessageBox.information(self, "Usuarios", mensaje)
            self.input_password.clear()
            self.input_password_confirmacion.clear()
            self.cargar_usuarios()
        except Exception as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))

    # Bloque CDLform: funcion/metodo actualizar_activo; encapsula una operacion del flujo del modulo.
    def actualizar_activo(self, activo: bool) -> None:
        try:
            usuario = self.input_usuario.text().strip() or self.usuario_seleccionado
            mensaje = self.presenter.actualizar_activo(usuario, activo)
            QMessageBox.information(self, "Usuarios", mensaje)
            self.cargar_usuarios()
        except Exception as exc:
            QMessageBox.warning(self, "Usuarios", str(exc))

    # Bloque CDLform: funcion/metodo limpiar_formulario; encapsula una operacion del flujo del modulo.
    def limpiar_formulario(self) -> None:
        self.usuario_seleccionado = ""
        self.input_usuario.clear()
        self.input_password.clear()
        self.input_password_confirmacion.clear()
        self.combo_rol.setCurrentIndex(1)
        self.check_activo.setChecked(True)
        self.tabla_usuarios.clearSelection()

    # Bloque CDLform: funcion/metodo _seleccionar_rol; encapsula una operacion del flujo del modulo.
    def _seleccionar_rol(self, rol: Any) -> None:
        rol_normalizado = self._normalizar_texto(rol).lower() or "gestion"
        for indice in range(self.combo_rol.count()):
            if self.combo_rol.itemData(indice) == rol_normalizado:
                self.combo_rol.setCurrentIndex(indice)
                return
        self.combo_rol.setCurrentIndex(1)

    # Bloque CDLform: funcion/metodo _obtener_password_validado; encapsula una operacion del flujo del modulo.
    def _obtener_password_validado(self) -> str:
        password = self.input_password.text()
        confirmacion = self.input_password_confirmacion.text()
        if password != confirmacion:
            raise ValueError("Las contrasenas no coinciden.")
        return password

    # Bloque CDLform: funcion/metodo _obtener_usuario_seleccionado; encapsula una operacion del flujo del modulo.
    def _obtener_usuario_seleccionado(self) -> dict[str, Any] | None:
        fila = self.tabla_usuarios.currentRow()
        if fila < 0:
            return None

        item = self.tabla_usuarios.item(fila, 0)
        if item is None:
            return None

        data = item.data(Qt.UserRole)
        return data if isinstance(data, dict) else None

    # Bloque CDLform: funcion/metodo _set_item; encapsula una operacion del flujo del modulo.
    def _set_item(
        self,
        row: int,
        column: int,
        value: Any,
        user_data: Any = None,
    ) -> None:
        item = QTableWidgetItem("" if value is None else str(value))
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if user_data is not None:
            item.setData(Qt.UserRole, user_data)
        self.tabla_usuarios.setItem(row, column, item)
