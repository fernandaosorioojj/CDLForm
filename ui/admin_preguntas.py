from __future__ import annotations

import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QComboBox,
    QCheckBox,
    QTextEdit,
    QSpinBox,
    QFormLayout,
)

from services.pregunta_service import PreguntaService


class AdminPreguntasView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.pregunta_service = PreguntaService()
        self.id_pregunta_en_edicion: str | None = None

        self.setWindowTitle("Administración de Preguntas")
        self.resize(1200, 700)

        self._init_ui()
        self.cargar_preguntas()

    def _init_ui(self) -> None:
        layout_principal = QHBoxLayout(self)

        panel_izquierdo = QVBoxLayout()
        panel_derecho = QVBoxLayout()

        titulo = QLabel("Gestión de Preguntas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por texto de pregunta...")
        self.input_busqueda.textChanged.connect(self.filtrar_preguntas)

        self.lista_preguntas = QListWidget()
        self.lista_preguntas.itemClicked.connect(self.cargar_pregunta_seleccionada)

        panel_izquierdo.addWidget(titulo)
        panel_izquierdo.addWidget(self.input_busqueda)
        panel_izquierdo.addWidget(self.lista_preguntas)

        form_layout = QFormLayout()

        self.input_texto = QLineEdit()
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["texto", "numero", "si_no", "seleccion_unica"])
        self.combo_tipo.currentTextChanged.connect(self._actualizar_estado_opciones)

        self.check_obligatoria = QCheckBox("Obligatoria")
        self.check_obligatoria.setChecked(True)

        self.check_activa = QCheckBox("Activa")
        self.check_activa.setChecked(True)

        self.spin_orden = QSpinBox()
        self.spin_orden.setMinimum(1)
        self.spin_orden.setMaximum(9999)
        self.spin_orden.setValue(1)

        self.input_cod_setor = QLineEdit()
        self.input_cod_setor.setPlaceholderText("Ej: LAM, COR, CAL")

        self.input_cod_recurso = QLineEdit()
        self.input_cod_recurso.setPlaceholderText("Ej: RC-01, RC-02")

        self.input_cod_ativ = QLineEdit()
        self.input_cod_ativ.setPlaceholderText("Ej: ATIV-10, PROC-20")

        self.input_turno = QLineEdit()
        self.input_turno.setPlaceholderText("Ej: DIA, NOCHE")

        self.input_tipo_trabajo = QLineEdit()
        self.input_tipo_trabajo.setPlaceholderText("Ej: MONTAJE, AJUSTE")

        self.input_opciones = QTextEdit()
        self.input_opciones.setPlaceholderText(
            "Para si_no o seleccion_unica.\n"
            "Una opción por línea en formato:\n"
            "valor|accion_correctiva\n\n"
            "Ejemplo:\n"
            "Sí|\n"
            "No|Revisar ajuste antes de continuar."
        )
        self.input_opciones.setFixedHeight(180)

        form_layout.addRow("Texto:", self.input_texto)
        form_layout.addRow("Tipo:", self.combo_tipo)
        form_layout.addRow("Orden:", self.spin_orden)
        form_layout.addRow("", self.check_obligatoria)
        form_layout.addRow("", self.check_activa)
        form_layout.addRow("Filtro CodSetor:", self.input_cod_setor)
        form_layout.addRow("Filtro CodRecurso:", self.input_cod_recurso)
        form_layout.addRow("Filtro CodAtiv:", self.input_cod_ativ)
        form_layout.addRow("Filtro Turno:", self.input_turno)
        form_layout.addRow("Filtro TipoTrabajo:", self.input_tipo_trabajo)
        form_layout.addRow("Opciones:", self.input_opciones)

        botones_layout = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_pregunta)

        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_nuevo.clicked.connect(self.limpiar_formulario)

        self.btn_desactivar = QPushButton("Desactivar")
        self.btn_desactivar.clicked.connect(self.desactivar_pregunta)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_pregunta)

        botones_layout.addWidget(self.btn_guardar)
        botones_layout.addWidget(self.btn_nuevo)
        botones_layout.addWidget(self.btn_desactivar)
        botones_layout.addWidget(self.btn_eliminar)

        panel_derecho.addLayout(form_layout)
        panel_derecho.addLayout(botones_layout)

        layout_principal.addLayout(panel_izquierdo, 1)
        layout_principal.addLayout(panel_derecho, 1)

        self._actualizar_estado_opciones()

    def cargar_preguntas(self) -> None:
        self.lista_preguntas.clear()
        preguntas = self.pregunta_service.listar_preguntas(solo_activas=False)

        for pregunta in preguntas:
            texto = pregunta.get("texto", "")
            tipo = pregunta.get("tipo", "")
            orden = pregunta.get("orden", 0)
            activa = "Activa" if pregunta.get("activa", True) else "Inactiva"

            item_texto = f"[{orden}] {texto} - ({tipo}) - {activa}"
            item = QListWidgetItem(item_texto)
            item.setData(Qt.UserRole, pregunta)
            self.lista_preguntas.addItem(item)

    def filtrar_preguntas(self) -> None:
        texto_busqueda = self.input_busqueda.text().strip().lower()

        for i in range(self.lista_preguntas.count()):
            item = self.lista_preguntas.item(i)
            visible = texto_busqueda in item.text().lower()
            item.setHidden(not visible)

    def cargar_pregunta_seleccionada(self, item: QListWidgetItem) -> None:
        pregunta = item.data(Qt.UserRole)
        self.id_pregunta_en_edicion = pregunta.get("id_pregunta")

        self.input_texto.setText(pregunta.get("texto", ""))
        self.combo_tipo.setCurrentText(pregunta.get("tipo", "texto"))
        self.spin_orden.setValue(pregunta.get("orden", 1))
        self.check_obligatoria.setChecked(pregunta.get("obligatoria", True))
        self.check_activa.setChecked(pregunta.get("activa", True))

        filtros = pregunta.get("filtros_contexto", {})
        self.input_cod_setor.setText(", ".join(filtros.get("cod_setor", [])))
        self.input_cod_recurso.setText(", ".join(filtros.get("cod_recurso", [])))
        self.input_cod_ativ.setText(", ".join(filtros.get("cod_ativ", [])))
        self.input_turno.setText(", ".join(filtros.get("turno", [])))
        self.input_tipo_trabajo.setText(", ".join(filtros.get("tipo_trabajo", [])))

        opciones = pregunta.get("opciones_respuesta", [])
        lineas: list[str] = []

        for opcion in opciones:
            valor = opcion.get("valor", "")
            accion_correctiva = opcion.get("accion_correctiva", "")
            lineas.append(f"{valor}|{accion_correctiva}")

        self.input_opciones.setPlainText("\n".join(lineas))
        self._actualizar_estado_opciones()

    def guardar_pregunta(self) -> None:
        try:
            texto = self.input_texto.text().strip()
            tipo = self.combo_tipo.currentText().strip()
            orden = self.spin_orden.value()
            obligatoria = self.check_obligatoria.isChecked()
            activa = self.check_activa.isChecked()

            filtros_contexto = self._construir_filtros_contexto()
            opciones_respuesta = self._construir_opciones_respuesta()

            if not texto:
                raise ValueError("El texto de la pregunta es obligatorio.")

            if self.id_pregunta_en_edicion:
                self.pregunta_service.actualizar_pregunta(
                    id_pregunta=self.id_pregunta_en_edicion,
                    texto=texto,
                    tipo=tipo,
                    obligatoria=obligatoria,
                    activa=activa,
                    orden=orden,
                    filtros_contexto=filtros_contexto,
                    opciones_respuesta=opciones_respuesta,
                )
                QMessageBox.information(self, "Éxito", "Pregunta actualizada correctamente.")
            else:
                self.pregunta_service.crear_pregunta(
                    texto=texto,
                    tipo=tipo,
                    obligatoria=obligatoria,
                    activa=activa,
                    orden=orden,
                    filtros_contexto=filtros_contexto,
                    opciones_respuesta=opciones_respuesta,
                )
                QMessageBox.information(self, "Éxito", "Pregunta creada correctamente.")

            self.limpiar_formulario()
            self.cargar_preguntas()

        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def desactivar_pregunta(self) -> None:
        if not self.id_pregunta_en_edicion:
            QMessageBox.warning(self, "Atención", "Selecciona una pregunta primero.")
            return

        try:
            self.pregunta_service.desactivar_pregunta(self.id_pregunta_en_edicion)
            QMessageBox.information(self, "Éxito", "Pregunta desactivada correctamente.")
            self.limpiar_formulario()
            self.cargar_preguntas()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def eliminar_pregunta(self) -> None:
        if not self.id_pregunta_en_edicion:
            QMessageBox.warning(self, "Atención", "Selecciona una pregunta primero.")
            return

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar esta pregunta?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmacion != QMessageBox.Yes:
            return

        try:
            self.pregunta_service.eliminar_pregunta(self.id_pregunta_en_edicion)
            QMessageBox.information(self, "Éxito", "Pregunta eliminada correctamente.")
            self.limpiar_formulario()
            self.cargar_preguntas()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def limpiar_formulario(self) -> None:
        self.id_pregunta_en_edicion = None
        self.input_texto.clear()
        self.combo_tipo.setCurrentText("texto")
        self.spin_orden.setValue(1)
        self.check_obligatoria.setChecked(True)
        self.check_activa.setChecked(True)

        self.input_cod_setor.clear()
        self.input_cod_recurso.clear()
        self.input_cod_ativ.clear()
        self.input_turno.clear()
        self.input_tipo_trabajo.clear()

        self.input_opciones.clear()
        self._actualizar_estado_opciones()

    def _actualizar_estado_opciones(self) -> None:
        tipo = self.combo_tipo.currentText().strip().lower()
        requiere_opciones = tipo in {"si_no", "seleccion_unica"}

        self.input_opciones.setEnabled(requiere_opciones)

        if not requiere_opciones:
            self.input_opciones.setPlainText("")

    def _construir_filtros_contexto(self) -> dict[str, list[str]]:
        filtros: dict[str, list[str]] = {}

        cod_setor = self._parse_lista_simple(self.input_cod_setor.text())
        cod_recurso = self._parse_lista_simple(self.input_cod_recurso.text())
        cod_ativ = self._parse_lista_simple(self.input_cod_ativ.text())
        turno = self._parse_lista_simple(self.input_turno.text())
        tipo_trabajo = self._parse_lista_simple(self.input_tipo_trabajo.text())

        if cod_setor:
            filtros["cod_setor"] = cod_setor
        if cod_recurso:
            filtros["cod_recurso"] = cod_recurso
        if cod_ativ:
            filtros["cod_ativ"] = cod_ativ
        if turno:
            filtros["turno"] = turno
        if tipo_trabajo:
            filtros["tipo_trabajo"] = tipo_trabajo

        return filtros

    def _construir_opciones_respuesta(self) -> list[dict]:
        tipo = self.combo_tipo.currentText().strip().lower()

        if tipo not in {"si_no", "seleccion_unica"}:
            return []

        texto_opciones = self.input_opciones.toPlainText().strip()
        if not texto_opciones:
            raise ValueError(
                "Debes ingresar opciones_respuesta para preguntas de tipo si_no o seleccion_unica."
            )

        opciones: list[dict] = []

        for linea in texto_opciones.splitlines():
            linea = linea.strip()
            if not linea:
                continue

            if "|" in linea:
                valor, accion_correctiva = linea.split("|", 1)
            else:
                valor, accion_correctiva = linea, ""

            valor = valor.strip()
            accion_correctiva = accion_correctiva.strip()

            if not valor:
                raise ValueError("Cada opción debe tener un valor válido.")

            opciones.append(
                {
                    "valor": valor,
                    "accion_correctiva": accion_correctiva,
                }
            )

        if not opciones:
            raise ValueError("Debes ingresar al menos una opción válida.")

        return opciones

    def _parse_lista_simple(self, texto: str) -> list[str]:
        valores: list[str] = []
        vistos: set[str] = set()

        for parte in texto.split(","):
            valor = parte.strip()
            if not valor:
                continue

            clave = valor.upper()
            if clave not in vistos:
                vistos.add(clave)
                valores.append(valor)

        return valores