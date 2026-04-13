from __future__ import annotations

import inspect
from typing import Any

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
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
        layout_principal.setContentsMargins(28, 28, 28, 28)

        contenedor = CardFrame()
        layout = QVBoxLayout(contenedor)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Seleccion de operario")
        titulo.setProperty("role", "title")
        layout.addWidget(titulo)

        self.lbl_info = QLabel(self._build_info_text())
        self.lbl_info.setWordWrap(True)
        layout.addWidget(self.lbl_info)

        self.combo_operarios = QComboBox()
        layout.addWidget(self.combo_operarios)

        self.btn_continuar = QPushButton("Continuar")
        self.btn_continuar.clicked.connect(self.continuar)
        layout.addWidget(self.btn_continuar)

        layout_principal.addWidget(contenedor)

    def _build_info_text(self) -> str:
        return self.presenter.construir_info_formulario(self.formulario)

    def cargar_operarios(self) -> None:
        self.combo_operarios.clear()

        try:
            operarios = self.presenter.listar_operarios_para_formulario(
                formulario=self.formulario,
                solo_activos=True,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudieron cargar los operarios.\n{exc}",
            )
            return

        for operario in operarios:
            nombre = self.presenter.obtener_nombre_operario(operario)

            if not nombre:
                continue

            self.combo_operarios.addItem(nombre, nombre)

        if self.combo_operarios.count() == 0:
            QMessageBox.warning(
                self,
                "Operarios",
                "No se encontraron operarios para este formulario.",
            )
            return

        if self.combo_operarios.count() == 1:
            QTimer.singleShot(0, self.continuar)

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
        operario = self.combo_operarios.currentData()
        if operario is None:
            operario = self.combo_operarios.currentText()

        try:
            operario = self.presenter.validar_operario_seleccionado(operario)
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

