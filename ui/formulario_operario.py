from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QMessageBox,
    QScrollArea,
    QFrame,
)

from services.formulario_service import FormularioService
from services.pregunta_service import PreguntaService
from services.respuesta_service import RespuestaService


class FormularioOperarioView(QWidget):
    def __init__(self, operario: dict | None = None, contexto: dict | None = None) -> None:
        super().__init__()

        self.operario = operario or {}
        self.contexto = contexto or {}

        self.formulario_service = FormularioService()
        self.pregunta_service = PreguntaService()
        self.respuesta_service = RespuestaService()

        self.preguntas_widgets: list[tuple[dict, QWidget]] = []

        self.setWindowTitle("Formulario Operario")
        self.resize(1200, 800)

        self._init_ui()
        self.cargar_preguntas()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)

        titulo = QLabel("Formulario de Operario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        subtitulo = QLabel(self._build_contexto_texto())
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        cabecera = QHBoxLayout()

        self.input_identificador = QLineEdit()
        self.input_identificador.setPlaceholderText("Identificador / OP / referencia")

        identificador_inicial = (
            self.contexto.get("identificador")
            or self.contexto.get("num_ordem")
            or ""
        )
        self.input_identificador.setText(str(identificador_inicial).strip())

        cabecera.addWidget(QLabel("Identificador:"))
        cabecera.addWidget(self.input_identificador)

        layout_principal.addLayout(cabecera)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.contenedor_preguntas = QWidget()
        self.layout_preguntas = QVBoxLayout(self.contenedor_preguntas)
        self.layout_preguntas.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.contenedor_preguntas)
        layout_principal.addWidget(self.scroll_area)

        botones = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar formulario")
        self.btn_guardar.clicked.connect(self.guardar_formulario)

        self.btn_recargar = QPushButton("Recargar preguntas")
        self.btn_recargar.clicked.connect(self.cargar_preguntas)

        botones.addStretch()
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_guardar)

        layout_principal.addLayout(botones)

    def _build_contexto_texto(self) -> str:
        partes: list[str] = []

        nombre_operario = self.operario.get("nombre") or self.operario.get("nombre_operario")
        if nombre_operario:
            partes.append(f"Operario: {nombre_operario}")

        identificador = self.contexto.get("identificador")
        if identificador:
            partes.append(f"Identificador: {identificador}")

        etiquetas = {
            "cod_setor": "Setor",
            "cod_recurso": "Recurso",
            "cod_ativ": "Actividad",
            "turno": "Turno",
            "tipo_trabajo": "Tipo trabajo",
        }

        for clave, etiqueta in etiquetas.items():
            valor = self.contexto.get(clave)
            if valor:
                partes.append(f"{etiqueta}: {valor}")

        if not partes:
            return "Sin contexto operativo cargado."

        return " | ".join(partes)

    def _construir_contexto_preguntas(self) -> dict:
        return {
            "cod_setor": self.contexto.get("cod_setor"),
            "cod_recurso": self.contexto.get("cod_recurso"),
            "cod_ativ": self.contexto.get("cod_ativ"),
            "turno": self.contexto.get("turno"),
            "tipo_trabajo": self.contexto.get("tipo_trabajo"),
        }

    def cargar_preguntas(self) -> None:
        self._limpiar_preguntas_ui()
        self.preguntas_widgets.clear()

        try:
            contexto = self._construir_contexto_preguntas()
            preguntas = self.pregunta_service.listar_preguntas_para_contexto(contexto)

            if not preguntas:
                aviso = QLabel("No hay preguntas configuradas para este contexto.")
                aviso.setAlignment(Qt.AlignCenter)
                self.layout_preguntas.addWidget(aviso)
                return

            for pregunta in preguntas:
                frame = QFrame()
                frame.setFrameShape(QFrame.StyledPanel)

                layout = QVBoxLayout(frame)

                texto = pregunta.get("texto", "")
                obligatoria = pregunta.get("obligatoria", True)

                label = QLabel(
                    f"{pregunta.get('orden', 0)}. {texto}"
                    + (" *" if obligatoria else "")
                )
                label.setWordWrap(True)
                label.setStyleSheet("font-size: 14px; font-weight: bold;")

                layout.addWidget(label)

                widget_respuesta = self._crear_widget_respuesta(pregunta)
                layout.addWidget(widget_respuesta)

                self.layout_preguntas.addWidget(frame)
                self.preguntas_widgets.append((pregunta, widget_respuesta))

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudieron cargar las preguntas.\n{exc}"
            )

    def _crear_widget_respuesta(self, pregunta: dict) -> QWidget:
        tipo = pregunta.get("tipo", "texto")
        opciones = pregunta.get("opciones_respuesta", [])

        if tipo == "texto":
            widget = QTextEdit()
            widget.setFixedHeight(90)
            return widget

        if tipo == "numero":
            widget = QSpinBox()
            widget.setMinimum(0)
            widget.setMaximum(999999999)
            return widget

        if tipo in {"si_no", "seleccion_unica"}:
            combo = QComboBox()
            combo.addItem("-- Seleccionar --", None)

            for opcion in opciones:
                combo.addItem(opcion.get("valor", ""), opcion)

            return combo

        fallback = QLineEdit()
        return fallback

    def guardar_formulario(self) -> None:
        try:
            identificador = self.input_identificador.text().strip()
            if not identificador:
                raise ValueError("El identificador es obligatorio.")

            id_formulario_existente = str(self.contexto.get("id_formulario", "")).strip()
            if not id_formulario_existente:
                raise ValueError("No se encontró el formulario pendiente asociado al evento.")

            respuestas = []
            for pregunta, widget in self.preguntas_widgets:
                respuesta = self._obtener_respuesta_widget(pregunta, widget)
                respuestas.append(respuesta)

            self._validar_respuestas_obligatorias(respuestas)

            for respuesta in respuestas:
                self.respuesta_service.crear_respuesta(
                    id_formulario=id_formulario_existente,
                    id_pregunta=respuesta["id_pregunta"],
                    respuesta_texto=respuesta.get("respuesta_texto"),
                    respuesta_numero=respuesta.get("respuesta_numero"),
                    id_opcion=respuesta.get("id_opcion"),
                    accion_correctiva_aplicada=respuesta.get("accion_correctiva_aplicada", ""),
                )

            self.formulario_service.actualizar_estado_formulario(
                id_formulario_existente,
                "completado",
            )

            QMessageBox.information(self, "Éxito", "Formulario guardado correctamente.")
            self.close()

        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def _obtener_respuesta_widget(self, pregunta: dict, widget: QWidget) -> dict:
        tipo = pregunta.get("tipo", "texto")

        resultado = {
            "id_pregunta": pregunta.get("id_pregunta"),
            "respuesta_texto": None,
            "respuesta_numero": None,
            "id_opcion": None,
            "accion_correctiva_aplicada": "",
            "obligatoria": pregunta.get("obligatoria", True),
            "texto_pregunta": pregunta.get("texto", ""),
        }

        if tipo == "texto":
            resultado["respuesta_texto"] = widget.toPlainText().strip()
            return resultado

        if tipo == "numero":
            resultado["respuesta_numero"] = widget.value()
            return resultado

        if tipo in {"si_no", "seleccion_unica"}:
            data = widget.currentData()
            if data:
                resultado["id_opcion"] = data.get("id_opcion")
                resultado["respuesta_texto"] = data.get("valor", "")
                resultado["accion_correctiva_aplicada"] = data.get("accion_correctiva", "")
            return resultado

        if isinstance(widget, QLineEdit):
            resultado["respuesta_texto"] = widget.text().strip()

        return resultado

    def _validar_respuestas_obligatorias(self, respuestas: list[dict]) -> None:
        for respuesta in respuestas:
            if not respuesta.get("obligatoria", True):
                continue

            if respuesta.get("respuesta_texto"):
                continue

            if respuesta.get("respuesta_numero") is not None:
                continue

            if respuesta.get("id_opcion"):
                continue

            raise ValueError(
                f"Debes responder la pregunta obligatoria: {respuesta.get('texto_pregunta', '')}"
            )

    def _limpiar_preguntas_ui(self) -> None:
        while self.layout_preguntas.count():
            item = self.layout_preguntas.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()