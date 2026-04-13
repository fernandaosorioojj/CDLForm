from __future__ import annotations

from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from models.formulario import (
    ESTADO_EN_APERTURA,
    Formulario,
)
from presenters.formulario_operario_presenter import FormularioOperarioPresenter
from services.forms.formulario_service import FormularioService
from services.forms.pregunta_service import PreguntaService
from services.forms.respuesta_service import RespuestaService
from styles.common import apply_view_style


class AccionCorrectivaDialog(QDialog):
    def __init__(self, accion_correctiva: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Accion correctiva requerida")
        self.setObjectName("accionCorrectivaDialog")
        self.setModal(True)
        self.resize(430, 220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        tarjeta = QFrame()
        tarjeta.setObjectName("dialogCard")
        tarjeta.setProperty("card", "true")
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(20, 18, 20, 18)
        tarjeta_layout.setSpacing(12)

        lbl_intro = QLabel(
            "La opcion seleccionada requiere aplicar la siguiente accion correctiva:"
        )
        lbl_intro.setWordWrap(True)
        lbl_intro.setProperty("role", "dialog-title")
        tarjeta_layout.addWidget(lbl_intro)

        marco = QFrame()
        marco.setObjectName("accionCorrectivaBox")
        marco_layout = QVBoxLayout(marco)
        marco_layout.setContentsMargins(14, 12, 14, 12)

        lbl_accion = QLabel(accion_correctiva or "Sin accion correctiva definida.")
        lbl_accion.setWordWrap(True)
        lbl_accion.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        marco_layout.addWidget(lbl_accion)
        tarjeta_layout.addWidget(marco)

        lbl_cierre = QLabel(
            "Revise esta indicacion antes de continuar con el formulario."
        )
        lbl_cierre.setWordWrap(True)
        lbl_cierre.setProperty("role", "dialog-text")
        tarjeta_layout.addWidget(lbl_cierre)

        tarjeta_layout.addStretch()

        fila = QHBoxLayout()
        fila.addStretch()

        btn = QPushButton("Entendido")
        btn.clicked.connect(self.accept)
        fila.addWidget(btn)

        tarjeta_layout.addLayout(fila)
        layout.addWidget(tarjeta)
        apply_view_style(self, "base.qss", "dialogs.qss", "formulario_operario.qss")


class ConfirmacionEnvioDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Confirmacion de envio")
        self.setObjectName("confirmacionEnvioDialog")
        self.setModal(True)
        self.resize(500, 240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        tarjeta = QFrame()
        tarjeta.setObjectName("dialogCard")
        tarjeta.setProperty("card", "true")
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(20, 18, 20, 18)
        tarjeta_layout.setSpacing(12)

        lbl_titulo = QLabel("Desea enviar el formulario?")
        lbl_titulo.setWordWrap(True)
        lbl_titulo.setProperty("role", "dialog-title")
        tarjeta_layout.addWidget(lbl_titulo)

        lbl_texto = QLabel(
            "Al confirmar el envio, usted declara ser responsable de la correcta "
            "aplicacion de las acciones correctivas y de los resultados derivados "
            "de ellas."
        )
        lbl_texto.setWordWrap(True)
        lbl_texto.setProperty("role", "dialog-text")
        tarjeta_layout.addWidget(lbl_texto)

        self.chk_acepto = QCheckBox("He leido y acepto esta declaracion")
        self.chk_acepto.setObjectName("confirmacionCheck")
        self.chk_acepto.toggled.connect(self._actualizar_estado_confirmar)
        tarjeta_layout.addWidget(self.chk_acepto)

        tarjeta_layout.addStretch()

        fila = QHBoxLayout()
        fila.addStretch()

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setProperty("variant", "secondary")
        self.btn_confirmar = QPushButton("Confirmar")
        self.btn_confirmar.setProperty("variant", "success")
        self.btn_confirmar.setEnabled(False)

        self.btn_cancelar.clicked.connect(self.reject)
        self.btn_confirmar.clicked.connect(self.accept)

        fila.addWidget(self.btn_cancelar)
        fila.addWidget(self.btn_confirmar)
        tarjeta_layout.addLayout(fila)
        layout.addWidget(tarjeta)
        apply_view_style(self, "base.qss", "dialogs.qss", "formulario_operario.qss")

    def _actualizar_estado_confirmar(self, checked: bool) -> None:
        self.btn_confirmar.setEnabled(bool(checked))


class FormularioOperarioView(QWidget):
    qss_files = ("base.qss", "formulario_operario.qss")

    def __init__(
        self,
        formulario: Formulario | None = None,
        operario: str = "",
        contexto: dict[str, Any] | None = None,
        formulario_service: FormularioService | None = None,
        pregunta_service: PreguntaService | None = None,
        respuesta_service: RespuestaService | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.formulario_service = formulario_service or FormularioService()
        self.pregunta_service = pregunta_service or PreguntaService()
        self.respuesta_service = respuesta_service or RespuestaService()
        self.presenter = FormularioOperarioPresenter(
            formulario_service=self.formulario_service,
            pregunta_service=self.pregunta_service,
            respuesta_service=self.respuesta_service,
        )

        self.formulario = self.presenter.resolver_formulario_inicial(
            formulario=formulario,
            contexto=contexto,
        )
        self.operario_seleccionado = self.presenter.normalizar_texto(operario)
        self.preguntas: list[dict[str, Any]] = []
        self.controles_respuesta: list[dict[str, Any]] = []
        self._acciones_correctivas_mostradas: set[str] = set()

        self.setWindowTitle("Formulario Operario")
        self.setObjectName("formularioOperarioView")
        self.resize(980, 720)

        self._configurar_ui()
        apply_view_style(self, *self.qss_files)
        self._cargar_formulario()
        self._cargar_preguntas()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        return FormularioOperarioPresenter.normalizar_texto(valor)

    def _configurar_ui(self) -> None:
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(28, 24, 28, 24)
        self.layout_principal.setSpacing(16)

        self.lbl_titulo = QLabel("Formulario de Operario")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setProperty("role", "title")
        self.layout_principal.addWidget(self.lbl_titulo)

        fila_superior = QHBoxLayout()
        fila_superior.setSpacing(14)

        self.marco_info = QFrame()
        self.marco_info.setProperty("card", "true")
        self.marco_info.setObjectName("infoFormulario")
        self.layout_info = QGridLayout(self.marco_info)
        self.layout_info.setContentsMargins(18, 14, 18, 14)
        self.layout_info.setHorizontalSpacing(12)
        self.layout_info.setVerticalSpacing(8)

        self.lbl_id_formulario = QLabel("-")
        self.lbl_identificador = QLabel("-")
        self.lbl_id_apontamento = QLabel("-")
        self.lbl_fecha = QLabel("-")
        self.lbl_area = QLabel("-")
        self.lbl_maquina = QLabel("-")
        self.lbl_operario = QLabel("-")
        self.lbl_estado = QLabel("-")
        self.lbl_descripcion_op = QLabel("-")
        self.lbl_descripcion_proceso = QLabel("-")

        self._agregar_campo_info(0, 0, "ID Formulario", self.lbl_id_formulario)
        self._agregar_campo_info(0, 2, "OP", self.lbl_identificador)
        self._agregar_campo_info(1, 0, "IdApontamento", self.lbl_id_apontamento)
        self._agregar_campo_info(1, 2, "Fecha", self.lbl_fecha)
        self._agregar_campo_info(2, 0, "Area", self.lbl_area)
        self._agregar_campo_info(2, 2, "Maquina", self.lbl_maquina)
        self._agregar_campo_info(3, 0, "Operario", self.lbl_operario)
        self._agregar_campo_info(3, 2, "Estado", self.lbl_estado)

        fila_superior.addWidget(self.marco_info, 3)

        observacion_card = QFrame()
        observacion_card.setProperty("card", "true")
        observacion_card.setObjectName("observacionFormulario")
        observacion_layout = QVBoxLayout(observacion_card)
        observacion_layout.setContentsMargins(18, 14, 18, 14)
        observacion_layout.setSpacing(8)

        lbl_observacion = QLabel("Observación general")
        lbl_observacion.setProperty("role", "section")

        self.txt_observacion_general = QPlainTextEdit()
        self.txt_observacion_general.setPlaceholderText(
            "Observación general del formulario"
        )
        self.txt_observacion_general.setFixedHeight(88)

        observacion_layout.addWidget(lbl_observacion)
        observacion_layout.addWidget(self.txt_observacion_general)
        fila_superior.addWidget(observacion_card, 2)

        self.layout_principal.addLayout(fila_superior)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("preguntasScroll")

        self.contenedor_preguntas = QWidget()
        self.contenedor_preguntas.setObjectName("contenedorPreguntas")
        self.layout_preguntas = QVBoxLayout(self.contenedor_preguntas)
        self.layout_preguntas.setContentsMargins(0, 0, 0, 0)
        self.layout_preguntas.setSpacing(14)
        self.scroll.setWidget(self.contenedor_preguntas)
        self.layout_principal.addWidget(self.scroll, 1)

        self.layout_botones = QHBoxLayout()
        self.btn_enviar = QPushButton("Enviar")
        self.btn_cancelar = QPushButton("Cancelar")

        self.btn_enviar.clicked.connect(self._enviar_formulario)
        self.btn_cancelar.clicked.connect(self.close)

        self.layout_botones.addStretch()
        self.layout_botones.addWidget(self.btn_enviar)
        self.layout_botones.addWidget(self.btn_cancelar)
        self.layout_principal.addLayout(self.layout_botones)

    def _agregar_campo_info(
        self,
        fila: int,
        columna: int,
        etiqueta: str,
        valor: QLabel,
    ) -> None:
        label = QLabel(f"{etiqueta}:")
        label.setProperty("role", "field-label")
        valor.setProperty("role", "field-value")
        self.layout_info.addWidget(label, fila, columna)
        self.layout_info.addWidget(valor, fila, columna + 1)

    def _cargar_formulario(self) -> None:
        if not self.formulario:
            QMessageBox.information(
                self,
                "Formulario",
                "No hay formularios pendientes para el operario.",
            )
            self.btn_enviar.setEnabled(False)
            return

        self.formulario = self.presenter.preparar_formulario(
            self.formulario,
            self.operario_seleccionado,
        )

        self.lbl_id_formulario.setText(self.formulario.id_formulario)
        self.lbl_identificador.setText(self.formulario.identificador)
        self.lbl_id_apontamento.setText(self.formulario.id_apontamento)
        self.lbl_fecha.setText(self.formulario.fecha_formulario)
        self.lbl_area.setText(self.formulario.area or self.formulario.cod_setor or "-")
        self.lbl_maquina.setText(
            self.formulario.maquina or self.formulario.cod_recurso or "-"
        )
        self.lbl_operario.setText(
            self.formulario.operario or self.operario_seleccionado or "-"
        )
        self.lbl_estado.setText(self.formulario.estado)
        self.lbl_descripcion_op.setText(self.formulario.descripcion_op or "-")
        self.lbl_descripcion_proceso.setText(
            self.formulario.descripcion_proceso or "-"
        )
        self.txt_observacion_general.setPlainText(
            self.formulario.observacion_general or ""
        )

    def _cargar_preguntas(self) -> None:
        while self.layout_preguntas.count():
            item = self.layout_preguntas.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.controles_respuesta.clear()

        if not self.formulario:
            return

        self.preguntas = self._obtener_preguntas_para_formulario()

        if not self.preguntas:
            self.layout_preguntas.addWidget(
                QLabel("No hay preguntas configuradas para este contexto.")
            )
            self.layout_preguntas.addStretch()
            return

        for indice, pregunta in enumerate(self.preguntas, start=1):
            widget = self._crear_bloque_pregunta(indice, pregunta)
            self.layout_preguntas.addWidget(widget)

        self.layout_preguntas.addStretch()

    def _obtener_preguntas_para_formulario(self) -> list[dict[str, Any]]:
        return self.presenter.obtener_preguntas_para_formulario(
            self.formulario,
            self.operario_seleccionado,
        )

    def _crear_bloque_pregunta(
        self, indice: int, pregunta: dict[str, Any]
    ) -> QWidget:
        frame = QFrame()
        frame.setProperty("card", "true")
        frame.setProperty("questionCard", "true")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        texto = self._normalizar_texto(
            pregunta.get("texto")
            or pregunta.get("pregunta")
            or pregunta.get("enunciado")
            or f"Pregunta {indice}"
        )
        obligatoria = self._pregunta_es_obligatoria(pregunta)

        lbl_pregunta = QLabel(f"{indice}. {texto}{' *' if obligatoria else ''}")
        lbl_pregunta.setWordWrap(True)
        lbl_pregunta.setProperty("role", "question")
        layout.addWidget(lbl_pregunta)

        ayuda = self._normalizar_texto(
            pregunta.get("ayuda") or pregunta.get("descripcion")
        )
        if ayuda:
            lbl_ayuda = QLabel(ayuda)
            lbl_ayuda.setWordWrap(True)
            layout.addWidget(lbl_ayuda)

        control_info = self._crear_control_respuesta(pregunta)
        layout.addWidget(control_info["widget"])

        if control_info.get("label_accion_correctiva") is not None:
            layout.addWidget(control_info["label_accion_correctiva"])

        self.controles_respuesta.append(
            {
                "pregunta": pregunta,
                "tipo_control": control_info["tipo_control"],
                "widget": control_info["widget"],
                "meta": control_info.get("meta", {}),
            }
        )

        return frame

    def _crear_control_respuesta(self, pregunta: dict[str, Any]) -> dict[str, Any]:
        tipo = self._normalizar_texto(
            pregunta.get("tipo")
            or pregunta.get("tipo_pregunta")
            or pregunta.get("tipo_respuesta")
            or "texto"
        ).lower()

        if tipo in {"numero", "num", "entero"}:
            widget = QSpinBox()
            widget.setMinimum(0)
            widget.setMaximum(999999999)
            return {"tipo_control": "numero", "widget": widget}

        if tipo in {"textarea", "texto_largo", "observacion"}:
            widget = QPlainTextEdit()
            widget.setFixedHeight(100)
            return {"tipo_control": "texto_largo", "widget": widget}

        if tipo in {"combo", "seleccion", "seleccion_unica", "opcion", "lista"}:
            combo = QComboBox()
            combo.addItem("Seleccione una opcion", "")

            opciones = self._obtener_opciones_pregunta(pregunta)
            for opcion in opciones:
                combo.addItem(opcion["texto"], opcion)

            label_accion = QLabel("")
            label_accion.setWordWrap(True)
            label_accion.setProperty("role", "inline-warning")
            label_accion.hide()

            combo.currentIndexChanged.connect(
                lambda _=None, c=combo, l=label_accion: self._on_combo_changed(c, l)
            )

            return {
                "tipo_control": "combo",
                "widget": combo,
                "meta": {"opciones": opciones},
                "label_accion_correctiva": label_accion,
            }

        if tipo in {"seleccion_multiple", "multiple", "checkbox"}:
            contenedor = QWidget()
            contenedor.setObjectName("opcionesMultiples")
            layout = QVBoxLayout(contenedor)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(8)

            opciones = self._obtener_opciones_pregunta(pregunta)
            checkboxes: list[tuple[QCheckBox, dict[str, str]]] = []

            label_accion = QLabel("")
            label_accion.setWordWrap(True)
            label_accion.setProperty("role", "inline-warning")
            label_accion.hide()

            for opcion in opciones:
                checkbox = QCheckBox(opcion["texto"])
                checkbox.setProperty("optionChoice", "true")
                checkbox.toggled.connect(
                    lambda checked, cb=checkbox, op=opcion, l=label_accion: self._on_checkbox_changed(
                        cb, op, l, checked
                    )
                )
                layout.addWidget(checkbox)
                checkboxes.append((checkbox, opcion))

            return {
                "tipo_control": "seleccion_multiple",
                "widget": contenedor,
                "meta": {"opciones": opciones, "checkboxes": checkboxes},
                "label_accion_correctiva": label_accion,
            }

        if tipo in {"si_no", "booleano", "bool"}:
            contenedor = QWidget()
            layout = QHBoxLayout(contenedor)
            layout.setContentsMargins(0, 0, 0, 0)

            rb_si = QRadioButton("Si")
            rb_no = QRadioButton("No")

            layout.addWidget(rb_si)
            layout.addWidget(rb_no)
            layout.addStretch()

            return {
                "tipo_control": "booleano",
                "widget": contenedor,
                "meta": {"rb_si": rb_si, "rb_no": rb_no},
            }

        widget = QLineEdit()
        return {"tipo_control": "texto", "widget": widget}

    def _obtener_opciones_pregunta(
        self, pregunta: dict[str, Any]
    ) -> list[dict[str, str]]:
        return self.presenter.obtener_opciones_pregunta(pregunta)

    def _pregunta_es_obligatoria(self, pregunta: dict[str, Any]) -> bool:
        return self.presenter.pregunta_es_obligatoria(pregunta)

    def _clave_popup_accion(self, id_pregunta: str, id_opcion: str) -> str:
        return f"{id_pregunta}::{id_opcion}"

    def _mostrar_accion_correctiva(
        self, id_pregunta: str, opcion: dict[str, str]
    ) -> None:
        accion = self._normalizar_texto(opcion.get("accion_correctiva"))
        id_opcion = self._normalizar_texto(opcion.get("id_opcion"))
        if not accion or not id_opcion:
            return

        clave = self._clave_popup_accion(id_pregunta, id_opcion)
        if clave in self._acciones_correctivas_mostradas:
            return

        self._acciones_correctivas_mostradas.add(clave)
        dialog = AccionCorrectivaDialog(accion, self)
        dialog.exec_()

    def _actualizar_label_accion_correctiva(
        self, label: QLabel, acciones: list[str]
    ) -> None:
        acciones_normalizadas = [accion for accion in acciones if accion]
        if not acciones_normalizadas:
            label.clear()
            label.hide()
            return

        label.setText("Accion correctiva: " + " | ".join(acciones_normalizadas))
        label.show()

    def _on_combo_changed(self, combo: QComboBox, label: QLabel) -> None:
        opcion = combo.currentData()
        if not isinstance(opcion, dict):
            self._actualizar_label_accion_correctiva(label, [])
            return

        accion = self._normalizar_texto(opcion.get("accion_correctiva"))
        self._actualizar_label_accion_correctiva(label, [accion] if accion else [])

        if not accion:
            return

        control = self._buscar_control_por_widget(combo)
        if not control:
            return

        id_pregunta = self._normalizar_texto(control["pregunta"].get("id_pregunta"))
        self._mostrar_accion_correctiva(id_pregunta, opcion)

    def _on_checkbox_changed(
        self,
        checkbox: QCheckBox,
        opcion: dict[str, str],
        label: QLabel,
        checked: bool,
    ) -> None:
        control = self._buscar_control_por_widget(checkbox.parentWidget())
        if not control:
            return

        acciones = []
        for item_checkbox, item_opcion in control["meta"].get("checkboxes", []):
            if item_checkbox.isChecked():
                accion = self._normalizar_texto(item_opcion.get("accion_correctiva"))
                if accion:
                    acciones.append(accion)

        self._actualizar_label_accion_correctiva(label, acciones)

        if not checked:
            return

        id_pregunta = self._normalizar_texto(control["pregunta"].get("id_pregunta"))
        self._mostrar_accion_correctiva(id_pregunta, opcion)

    def _buscar_control_por_widget(
        self, widget: QWidget | None
    ) -> dict[str, Any] | None:
        for control in self.controles_respuesta:
            if control["widget"] is widget:
                return control
        return None

    def _extraer_respuestas_control(
        self, control: dict[str, Any]
    ) -> list[dict[str, Any]]:
        tipo_control = control["tipo_control"]
        widget = control["widget"]
        meta = control.get("meta", {})

        if tipo_control == "numero":
            return [
                {
                    "respuesta_texto": None,
                    "respuesta_numero": int(widget.value()),
                    "id_opcion": None,
                    "accion_correctiva_aplicada": None,
                }
            ]

        if tipo_control == "texto_largo":
            texto = self._normalizar_texto(widget.toPlainText())
            if not texto:
                return []
            return [
                {
                    "respuesta_texto": texto,
                    "respuesta_numero": None,
                    "id_opcion": None,
                    "accion_correctiva_aplicada": None,
                }
            ]

        if tipo_control == "combo":
            opcion = widget.currentData()
            if not isinstance(opcion, dict):
                return []
            return [
                {
                    "respuesta_texto": self._normalizar_texto(opcion.get("texto")),
                    "respuesta_numero": None,
                    "id_opcion": self._normalizar_texto(opcion.get("id_opcion")),
                    "accion_correctiva_aplicada": self._normalizar_texto(
                        opcion.get("accion_correctiva")
                    )
                    or None,
                }
            ]

        if tipo_control == "seleccion_multiple":
            respuestas: list[dict[str, Any]] = []
            for item_checkbox, opcion in meta.get("checkboxes", []):
                if not item_checkbox.isChecked():
                    continue
                respuestas.append(
                    {
                        "respuesta_texto": self._normalizar_texto(opcion.get("texto")),
                        "respuesta_numero": None,
                        "id_opcion": self._normalizar_texto(opcion.get("id_opcion")),
                        "accion_correctiva_aplicada": self._normalizar_texto(
                            opcion.get("accion_correctiva")
                        )
                        or None,
                    }
                )
            return respuestas

        if tipo_control == "booleano":
            if meta["rb_si"].isChecked():
                return [
                    {
                        "respuesta_texto": "Si",
                        "respuesta_numero": None,
                        "id_opcion": "SI",
                        "accion_correctiva_aplicada": None,
                    }
                ]
            if meta["rb_no"].isChecked():
                return [
                    {
                        "respuesta_texto": "No",
                        "respuesta_numero": None,
                        "id_opcion": "NO",
                        "accion_correctiva_aplicada": None,
                    }
                ]
            return []

        texto = self._normalizar_texto(widget.text())
        if not texto:
            return []
        return [
            {
                "respuesta_texto": texto,
                "respuesta_numero": None,
                "id_opcion": None,
                "accion_correctiva_aplicada": None,
            }
        ]

    def _validar_respuestas(self) -> tuple[bool, str]:
        return self.presenter.validar_respuestas(
            [
                {
                    "pregunta": control["pregunta"],
                    "respuestas": self._extraer_respuestas_control(control),
                }
                for control in self.controles_respuesta
            ]
        )

    def _confirmar_envio(self) -> bool:
        dialog = ConfirmacionEnvioDialog(self)
        return dialog.exec_() == QDialog.Accepted

    def _enviar_formulario(self) -> None:
        if not self.formulario:
            QMessageBox.warning(self, "Formulario", "No hay un formulario cargado.")
            return

        ok, mensaje = self._validar_respuestas()
        if not ok:
            QMessageBox.warning(self, "Validacion", mensaje)
            return

        if not self._confirmar_envio():
            return

        try:
            self.formulario = self.presenter.guardar_formulario(
                formulario=self.formulario,
                respuestas_por_control=[
                    {
                        "pregunta": control["pregunta"],
                        "respuestas": self._extraer_respuestas_control(control),
                    }
                    for control in self.controles_respuesta
                ],
                observacion_general=self.txt_observacion_general.toPlainText(),
            )

            QMessageBox.information(
                self,
                "Formulario",
                "Formulario enviado correctamente.",
            )
            self.close()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo enviar el formulario.\n\n{exc}",
            )

