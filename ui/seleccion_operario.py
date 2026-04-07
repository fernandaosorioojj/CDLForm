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
    QWidget,
)

from services.formulario_service import FormularioService
from services.operario_service import OperarioService
from services.pregunta_service import PreguntaService
from services.respuesta_service import RespuestaService
from ui.formulario_operario import FormularioOperarioView


class SeleccionOperarioView(QWidget):
    def __init__(
        self,
        formulario: dict[str, Any] | None = None,
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
        self.on_close = on_close

        self.formulario = self._resolver_formulario(formulario, id_formulario)
        self.formulario_operario_view = None

        self.setWindowTitle("Selección de operario")
        self.resize(520, 220)

        self.lbl_info = QLabel(self._build_info_text())
        self.combo_operarios = QComboBox()
        self.btn_continuar = QPushButton("Continuar")

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_info)
        layout.addWidget(self.combo_operarios)
        layout.addWidget(self.btn_continuar)
        self.setLayout(layout)

        self.btn_continuar.clicked.connect(self.continuar)

        self.cargar_operarios()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def _resolver_formulario(
        self,
        formulario: dict[str, Any] | None,
        id_formulario: str | None,
    ) -> dict[str, Any]:
        if formulario is not None:
            return formulario

        if id_formulario:
            encontrado = self.formulario_service.obtener_formulario_por_id(id_formulario)
            if encontrado:
                return encontrado

        raise ValueError("No se pudo resolver el formulario para la selección de operario.")

    def _build_info_text(self) -> str:
        identificador = self._normalizar_texto(
            self.formulario.get("identificador")
        )
        maquina = self._normalizar_texto(
            self.formulario.get("maquina") or self.formulario.get("cod_recurso")
        )
        area = self._normalizar_texto(
            self.formulario.get("area") or self.formulario.get("cod_setor")
        )

        return (
            f"Formulario: {self._normalizar_texto(self.formulario.get('id_formulario'))}\n"
            f"Identificador: {identificador}\n"
            f"Máquina: {maquina}\n"
            f"Área: {area}"
        )

    def cargar_operarios(self) -> None:
        self.combo_operarios.clear()

        try:
            operarios = self.operario_service.listar_operarios_para_formulario(
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
            nombre = self._normalizar_texto(
                operario.get("nombre")
                or operario.get("nombre_operario")
                or operario.get("operario")
                or operario.get("id_operario")
            )

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
            "id_formulario": self.formulario.get("id_formulario"),
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
            lambda: FormularioOperarioView(self.formulario.get("id_formulario")),
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

        operario = self._normalizar_texto(operario)

        if not operario:
            QMessageBox.warning(
                self,
                "Operario",
                "Debe seleccionar un operario.",
            )
            return

        id_formulario = self._normalizar_texto(self.formulario.get("id_formulario"))
        self.formulario_service.asignar_operario(id_formulario, operario)
        self.formulario = self.formulario_service.obtener_formulario_por_id(id_formulario)

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