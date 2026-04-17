from __future__ import annotations

import inspect
from typing import Any

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.formulario import Formulario
from presenters.seleccion_operario_presenter import SeleccionOperarioPresenter
from services.forms.formulario_service import FormularioService
from services.forms.operario_service import OperarioService
from services.forms.pregunta_service import PreguntaService
from services.forms.respuesta_service import RespuestaService
from ui.formulario_operario import FormularioOperarioView
from widgets.base_window import BaseWindow
from widgets.card_frame import CardFrame


class SeleccionOperarioView(BaseWindow):
    qss_files = ("base.qss", "seleccion_operario.qss")

    def __init__(
        self,
        formulario: Formulario | None = None,
        id_formulario: str | None = None,
        formulario_service: FormularioService | None = None,
        operario_service: OperarioService | None = None,
        pregunta_service: PreguntaService | None = None,
        respuesta_service: RespuestaService | None = None,
        on_close=None,
    ) -> None:
        super().__init__()

        self.formulario_service = formulario_service or FormularioService()
        self.operario_service = operario_service or OperarioService()
        self.pregunta_service = pregunta_service or PreguntaService()
        self.respuesta_service = respuesta_service or RespuestaService()
        self.presenter = SeleccionOperarioPresenter(
            formulario_service=self.formulario_service,
            operario_service=self.operario_service,
        )
        self.on_close = on_close

        self.formulario = self.presenter.resolver_formulario(formulario, id_formulario)
        self.formulario_operario_view = None
        self.operarios_disponibles: list[str] = []

        self.setObjectName("seleccionOperarioView")
        self.setWindowTitle("Seleccion de operario")
        self.resize(520, 260)

        self._init_ui()
        self.apply_styles()
        self.cargar_operarios()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        return SeleccionOperarioPresenter.normalizar_texto(valor)

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(32, 28, 32, 28)
        layout_principal.setSpacing(16)

        titulo = QLabel("Seleccion de Operario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Busca y selecciona un operador registrado para continuar.")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        panel_info = CardFrame()
        panel_info.setObjectName("infoFormularioSeleccion")
        panel_info.setMaximumWidth(860)

        info_layout = QGridLayout(panel_info)
        info_layout.setContentsMargins(18, 14, 18, 14)
        info_layout.setHorizontalSpacing(14)
        info_layout.setVerticalSpacing(8)

        self._agregar_campo_info(info_layout, 0, 0, "Formulario", self.formulario.id_formulario)
        self._agregar_campo_info(info_layout, 0, 2, "Identificador", self.formulario.identificador)
        self._agregar_campo_info(info_layout, 1, 0, "Maquina", self.formulario.maquina or self.formulario.cod_recurso)
        self._agregar_campo_info(info_layout, 1, 2, "Area", self.formulario.area or self.formulario.cod_setor)

        layout_principal.addWidget(panel_info, 0, Qt.AlignHCenter)

        contenedor = CardFrame()
        contenedor.setObjectName("selectorOperario")
        contenedor.setMaximumWidth(860)

        contenido_layout = QVBoxLayout(contenedor)
        contenido_layout.setContentsMargins(18, 18, 18, 18)
        contenido_layout.setSpacing(12)

        self.lbl_error_operarios = QLabel("")
        self.lbl_error_operarios.setWordWrap(True)
        self.lbl_error_operarios.setProperty("role", "inline-warning")
        self.lbl_error_operarios.hide()
        contenido_layout.addWidget(self.lbl_error_operarios)

        self.input_busqueda_operario = QLineEdit()
        self.input_busqueda_operario.setPlaceholderText(
            "Filtrar por nombre o numero..."
        )
        self.input_busqueda_operario.textChanged.connect(self._filtrar_operarios)
        contenido_layout.addWidget(self.input_busqueda_operario)

        self.lista_operarios = QListWidget()
        self.lista_operarios.setSelectionMode(QAbstractItemView.SingleSelection)
        self.lista_operarios.itemSelectionChanged.connect(
            self._actualizar_estado_continuar
        )
        contenido_layout.addWidget(
            self._crear_bloque_lista("Operadores registrados", self.lista_operarios)
        )

        self.btn_continuar = QPushButton("Continuar")
        self.btn_continuar.clicked.connect(self.continuar)
        contenido_layout.addWidget(self.btn_continuar)

        layout_principal.addWidget(contenedor, 0, Qt.AlignHCenter)
        layout_principal.addStretch()

    @staticmethod
    def _agregar_campo_info(
        layout: QGridLayout,
        fila: int,
        columna: int,
        etiqueta: str,
        valor: Any,
    ) -> None:
        label = QLabel(f"{etiqueta}:")
        label.setProperty("role", "field-label")
        value_label = QLabel(str(valor or "-"))
        value_label.setProperty("role", "field-value")
        value_label.setWordWrap(True)
        layout.addWidget(label, fila, columna)
        layout.addWidget(value_label, fila, columna + 1)

    def _build_info_text(self) -> str:
        return self.presenter.construir_info_formulario(self.formulario)

    def cargar_operarios(self) -> None:
        self.lista_operarios.clear()
        self.operarios_disponibles.clear()
        self.lbl_error_operarios.clear()
        self.lbl_error_operarios.hide()
        self.btn_continuar.setEnabled(False)

        try:
            operarios = self.presenter.listar_operarios_para_formulario(
                formulario=self.formulario,
                solo_activos=True,
            )
        except Exception as exc:
            self.lbl_error_operarios.setText(
                "No se pudieron cargar los operadores desde Apontamentos. "
                f"Revise la conexion SQL.\n{exc}"
            )
            self.lbl_error_operarios.show()
            return

        for operario in operarios:
            nombre = self.presenter.obtener_nombre_operario(operario)

            if not nombre:
                continue

            if nombre not in self.operarios_disponibles:
                self.operarios_disponibles.append(nombre)

        self._filtrar_operarios("")

        if self.lista_operarios.count() == 0:
            self.lbl_error_operarios.setText(
                "No se encontraron operadores registrados en Apontamentos."
            )
            self.lbl_error_operarios.show()
            return

        if self.lista_operarios.count() == 1:
            self.lista_operarios.setCurrentRow(0)
            QTimer.singleShot(0, self.continuar)

    def _crear_bloque_lista(self, titulo: str, lista: QListWidget) -> QWidget:
        contenedor = QFrame()
        contenedor.setProperty("card", "true")
        contenedor.setProperty("compactCard", "true")

        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        label = QLabel(titulo)
        label.setProperty("role", "section")

        layout.addWidget(label)
        layout.addWidget(lista)
        return contenedor

    def _filtrar_operarios(self, texto: str) -> None:
        texto_normalizado = self._normalizar_texto(texto).lower()
        seleccion_actual = self._obtener_operario_seleccionado()

        filtrados = [
            operario
            for operario in self.operarios_disponibles
            if not texto_normalizado or texto_normalizado in operario.lower()
        ]

        self.lista_operarios.blockSignals(True)
        self.lista_operarios.clear()
        for operario in filtrados:
            item = QListWidgetItem(operario)
            item.setData(Qt.UserRole, operario)
            self.lista_operarios.addItem(item)

        if seleccion_actual in filtrados:
            self.lista_operarios.setCurrentRow(filtrados.index(seleccion_actual))

        self.lista_operarios.blockSignals(False)
        self._actualizar_estado_continuar()

    def _obtener_operario_seleccionado(self) -> str:
        items = self.lista_operarios.selectedItems()
        if not items:
            return ""
        return self._normalizar_texto(items[0].data(Qt.UserRole) or items[0].text())

    def _actualizar_estado_continuar(self) -> None:
        self.btn_continuar.setEnabled(bool(self._obtener_operario_seleccionado()))

    def _normalizar_operario_listado(self, valor: str) -> str:
        return self._normalizar_texto(valor).casefold()

    def _operario_existe_en_listado(self, operario: str) -> bool:
        operario_normalizado = self._normalizar_operario_listado(operario)
        return any(
            self._normalizar_operario_listado(disponible) == operario_normalizado
            for disponible in self.operarios_disponibles
        )

    def _instanciar_formulario_operario_view(self, operario: str) -> Any:
        kwargs_disponibles = {
            "formulario": self.formulario,
            "id_formulario": self.formulario.id_formulario,
            "formulario_service": self.formulario_service,
            "pregunta_service": self.pregunta_service,
            "respuesta_service": self.respuesta_service,
            "operario": operario,
        }

        signature = inspect.signature(FormularioOperarioView.__init__)
        kwargs_aceptados: dict[str, Any] = {}

        for nombre_parametro in list(signature.parameters.keys())[1:]:
            if nombre_parametro in kwargs_disponibles:
                kwargs_aceptados[nombre_parametro] = kwargs_disponibles[
                    nombre_parametro
                ]

        errores: list[str] = []

        try:
            return FormularioOperarioView(**kwargs_aceptados)
        except TypeError as exc:
            errores.append(str(exc))

        intentos = [
            lambda: FormularioOperarioView(self.formulario, operario),
            lambda: FormularioOperarioView(self.formulario),
            lambda: FormularioOperarioView(
                contexto={"id_formulario": self.formulario.id_formulario}
            ),
            lambda: FormularioOperarioView(),
        ]

        for intento in intentos:
            try:
                return intento()
            except TypeError as exc:
                errores.append(str(exc))

        raise RuntimeError(
            "No se pudo instanciar FormularioOperarioView con las firmas probadas. "
            f"Errores detectados: {' | '.join(errores)}"
        )

    def continuar(self) -> None:
        operario = self._obtener_operario_seleccionado()

        try:
            operario = self.presenter.validar_operario_seleccionado(operario)
            if not self._operario_existe_en_listado(operario):
                raise ValueError(
                    "Debe seleccionar un operario existente del listado."
                )
            self.formulario = self.presenter.asignar_operario(self.formulario, operario)
        except ValueError as exc:
            QMessageBox.warning(self, "Operario", str(exc))
            return

        self.formulario_operario_view = self._instanciar_formulario_operario_view(
            operario=operario,
        )

        if hasattr(self.formulario_operario_view, "destroyed"):
            self.formulario_operario_view.destroyed.connect(self.close)

        if hasattr(self.formulario_operario_view, "showMaximized"):
            self.formulario_operario_view.showMaximized()
        else:
            self.formulario_operario_view.show()

        self.hide()

