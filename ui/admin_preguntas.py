from __future__ import annotations

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
    QSpinBox,
    QFormLayout,
    QAbstractItemView,
    QFrame,
    QScrollArea,
    QSizePolicy,
)

from services.catalogo_contexto_service import CatalogoContextoService
from services.pregunta_service import PreguntaService


class AdminPreguntasView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.catalogo_contexto_service = CatalogoContextoService()
        self.pregunta_service = PreguntaService()
        self.id_pregunta_en_edicion: str | None = None

        self.setWindowTitle("Administración de Preguntas")
        self.resize(1380, 820)

        self._init_ui()
        self.cargar_preguntas()

    def _init_ui(self) -> None:
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(18, 18, 18, 18)
        layout_principal.setSpacing(18)

        panel_izquierdo = QFrame()
        panel_izquierdo.setMinimumWidth(360)
        panel_izquierdo.setMaximumWidth(430)
        panel_izquierdo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout_izquierdo = QVBoxLayout(panel_izquierdo)
        layout_izquierdo.setContentsMargins(16, 16, 16, 16)
        layout_izquierdo.setSpacing(12)

        titulo = QLabel("Gestión de Preguntas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText(
            "Buscar por texto, tipo o filtros de contexto..."
        )
        self.input_busqueda.textChanged.connect(self.filtrar_preguntas)

        label_lista = QLabel("Listado de preguntas")

        self.lista_preguntas = QListWidget()
        self.lista_preguntas.itemClicked.connect(self.cargar_pregunta_seleccionada)
        self.lista_preguntas.setMinimumHeight(540)

        layout_izquierdo.addWidget(titulo)
        layout_izquierdo.addWidget(self.input_busqueda)
        layout_izquierdo.addWidget(label_lista)
        layout_izquierdo.addWidget(self.lista_preguntas, 1)

        panel_derecho = QFrame()
        layout_derecho_externo = QVBoxLayout(panel_derecho)
        layout_derecho_externo.setContentsMargins(16, 16, 16, 16)
        layout_derecho_externo.setSpacing(12)

        titulo_form = QLabel("Configuración de pregunta")
        titulo_form.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout_derecho_externo.addWidget(titulo_form)

        self.scroll_form = QScrollArea()
        self.scroll_form.setWidgetResizable(True)
        self.scroll_form.setFrameShape(QFrame.NoFrame)

        self.form_container = QWidget()
        self.scroll_form.setWidget(self.form_container)

        form_wrapper = QVBoxLayout(self.form_container)
        form_wrapper.setContentsMargins(6, 6, 6, 6)
        form_wrapper.setSpacing(18)

        bloque_basico = QFrame()
        layout_basico = QFormLayout(bloque_basico)
        layout_basico.setContentsMargins(14, 14, 14, 14)
        layout_basico.setSpacing(12)
        layout_basico.setLabelAlignment(Qt.AlignLeft)
        layout_basico.setFormAlignment(Qt.AlignTop)

        self.input_texto = QLineEdit()

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["texto", "numero", "seleccion_unica"])
        self.combo_tipo.currentTextChanged.connect(self._actualizar_estado_opciones)

        self.spin_orden = QSpinBox()
        self.spin_orden.setMinimum(1)
        self.spin_orden.setMaximum(9999)
        self.spin_orden.setValue(1)

        checks_layout = QHBoxLayout()
        checks_layout.setSpacing(18)

        self.check_obligatoria = QCheckBox("Obligatoria")
        self.check_obligatoria.setChecked(True)

        self.check_activa = QCheckBox("Activa")
        self.check_activa.setChecked(True)

        checks_layout.addWidget(self.check_obligatoria)
        checks_layout.addWidget(self.check_activa)
        checks_layout.addStretch()

        checks_widget = QWidget()
        checks_widget.setLayout(checks_layout)

        layout_basico.addRow("Texto:", self.input_texto)
        layout_basico.addRow("Tipo:", self.combo_tipo)
        layout_basico.addRow("Orden:", self.spin_orden)
        layout_basico.addRow("Estado:", checks_widget)

        bloque_contexto = QFrame()
        layout_contexto = QVBoxLayout(bloque_contexto)
        layout_contexto.setContentsMargins(14, 14, 14, 14)
        layout_contexto.setSpacing(12)

        label_contexto = QLabel("Filtros de contexto")
        label_contexto.setStyleSheet("font-weight: bold;")

        contexto_fila_1 = QHBoxLayout()
        contexto_fila_1.setSpacing(12)

        contexto_fila_2 = QHBoxLayout()
        contexto_fila_2.setSpacing(12)

        self.lista_cod_setor = self._crear_lista_multiseleccion(
            self.catalogo_contexto_service.listar_cod_setor()
        )
        self.lista_cod_recurso = self._crear_lista_multiseleccion(
            self.catalogo_contexto_service.listar_cod_recurso()
        )
        self.lista_turno = self._crear_lista_multiseleccion(
            self.catalogo_contexto_service.listar_turnos()
        )

        contexto_fila_1.addWidget(self._crear_bloque_lista("CodSetor", self.lista_cod_setor))
        contexto_fila_1.addWidget(self._crear_bloque_lista("CodRecurso", self.lista_cod_recurso))
        contexto_fila_1.addWidget(self._crear_bloque_lista("Turno", self.lista_turno))
        contexto_fila_1.addStretch()

        layout_contexto.addWidget(label_contexto)
        layout_contexto.addLayout(contexto_fila_1)
        layout_contexto.addLayout(contexto_fila_2)

        self.panel_opciones = QFrame()
        layout_opciones = QVBoxLayout(self.panel_opciones)
        layout_opciones.setContentsMargins(14, 14, 14, 14)
        layout_opciones.setSpacing(12)

        label_opciones = QLabel("Opciones de respuesta")
        label_opciones.setStyleSheet("font-weight: bold;")

        self.label_info_opciones = QLabel("")
        self.label_info_opciones.setWordWrap(True)

        fila_opcion = QHBoxLayout()
        fila_opcion.setSpacing(10)

        self.input_opcion_valor = QLineEdit()
        self.input_opcion_valor.setPlaceholderText("Valor de la opción")

        self.input_opcion_accion = QLineEdit()
        self.input_opcion_accion.setPlaceholderText("Acción correctiva (opcional)")

        self.btn_agregar_opcion = QPushButton("Agregar opción")
        self.btn_agregar_opcion.clicked.connect(self.agregar_opcion)

        fila_opcion.addWidget(self.input_opcion_valor, 2)
        fila_opcion.addWidget(self.input_opcion_accion, 3)
        fila_opcion.addWidget(self.btn_agregar_opcion, 1)

        self.lista_opciones = QListWidget()
        self.lista_opciones.setMinimumHeight(180)
        self.lista_opciones.setMaximumHeight(220)

        fila_botones_opciones = QHBoxLayout()
        fila_botones_opciones.setSpacing(10)

        self.btn_eliminar_opcion = QPushButton("Eliminar opción")
        self.btn_eliminar_opcion.clicked.connect(self.eliminar_opcion_seleccionada)

        self.btn_limpiar_opciones = QPushButton("Limpiar opciones")
        self.btn_limpiar_opciones.clicked.connect(self.limpiar_opciones)

        fila_botones_opciones.addStretch()
        fila_botones_opciones.addWidget(self.btn_limpiar_opciones)
        fila_botones_opciones.addWidget(self.btn_eliminar_opcion)

        layout_opciones.addWidget(label_opciones)
        layout_opciones.addWidget(self.label_info_opciones)
        layout_opciones.addLayout(fila_opcion)
        layout_opciones.addWidget(self.lista_opciones)
        layout_opciones.addLayout(fila_botones_opciones)

        form_wrapper.addWidget(bloque_basico)
        form_wrapper.addWidget(bloque_contexto)
        form_wrapper.addWidget(self.panel_opciones)
        form_wrapper.addStretch()

        layout_derecho_externo.addWidget(self.scroll_form, 1)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_pregunta)

        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_nuevo.clicked.connect(self.limpiar_formulario)

        self.btn_desactivar = QPushButton("Desactivar")
        self.btn_desactivar.clicked.connect(self.desactivar_pregunta)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_pregunta)

        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_guardar)
        botones_layout.addWidget(self.btn_nuevo)
        botones_layout.addWidget(self.btn_desactivar)
        botones_layout.addWidget(self.btn_eliminar)

        layout_derecho_externo.addLayout(botones_layout)

        layout_principal.addWidget(panel_izquierdo, 0)
        layout_principal.addWidget(panel_derecho, 1)

        self._actualizar_estado_opciones()

    def _crear_lista_multiseleccion(self, valores: list[str]) -> QListWidget:
        lista = QListWidget()
        lista.setSelectionMode(QAbstractItemView.MultiSelection)
        lista.setMinimumHeight(130)
        lista.setMaximumHeight(170)

        for valor in valores:
            item = QListWidgetItem(valor)
            lista.addItem(item)

        return lista

    def _crear_bloque_lista(self, titulo: str, lista: QListWidget) -> QWidget:
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(titulo)
        label.setStyleSheet("font-weight: 600;")

        layout.addWidget(label)
        layout.addWidget(lista)
        return contenedor

    def cargar_preguntas(self) -> None:
        self.lista_preguntas.clear()
        preguntas = self.pregunta_service.listar_preguntas(solo_activas=False)

        for pregunta in preguntas:
            texto = pregunta.get("texto", "")
            tipo = pregunta.get("tipo", "")
            orden = pregunta.get("orden", 0)
            activa = "Activa" if pregunta.get("activa", True) else "Inactiva"

            filtros = pregunta.get("filtros_contexto", {})
            resumen_filtros = self._resumen_filtros_contexto(filtros)

            item_texto = f"[{orden}] {texto} - ({tipo}) - {activa}"
            if resumen_filtros:
                item_texto += f" | {resumen_filtros}"

            item = QListWidgetItem(item_texto)
            item.setData(Qt.UserRole, pregunta)
            self.lista_preguntas.addItem(item)

    def filtrar_preguntas(self) -> None:
        texto_busqueda = self.input_busqueda.text().strip().lower()

        for i in range(self.lista_preguntas.count()):
            item = self.lista_preguntas.item(i)
            pregunta = item.data(Qt.UserRole) or {}

            texto = str(pregunta.get("texto", "")).strip().lower()
            tipo = str(pregunta.get("tipo", "")).strip().lower()
            estado = "activa" if pregunta.get("activa", True) else "inactiva"

            filtros = pregunta.get("filtros_contexto", {})
            valores_filtros: list[str] = []
            for valores in filtros.values():
                if isinstance(valores, list):
                    valores_filtros.extend(str(valor).strip().lower() for valor in valores)

            universo_busqueda = " ".join(
                [texto, tipo, estado, " ".join(valores_filtros), item.text().lower()]
            )

            item.setHidden(texto_busqueda not in universo_busqueda)

    def cargar_pregunta_seleccionada(self, item: QListWidgetItem) -> None:
        pregunta = item.data(Qt.UserRole)
        self.id_pregunta_en_edicion = pregunta.get("id_pregunta")

        self.input_texto.setText(pregunta.get("texto", ""))
        tipo_actual = pregunta.get("tipo", "texto")
        if tipo_actual == "si_no":
            tipo_actual = "seleccion_unica"
        self.combo_tipo.setCurrentText(tipo_actual)
        self.spin_orden.setValue(pregunta.get("orden", 1))
        self.check_obligatoria.setChecked(pregunta.get("obligatoria", True))
        self.check_activa.setChecked(pregunta.get("activa", True))

        filtros = pregunta.get("filtros_contexto", {})
        self._seleccionar_valores_lista(self.lista_cod_setor, filtros.get("cod_setor", []))
        self._seleccionar_valores_lista(self.lista_cod_recurso, filtros.get("cod_recurso", []))
        self._seleccionar_valores_lista(self.lista_turno, filtros.get("turno", []))

        self._cargar_opciones_en_lista(pregunta.get("opciones_respuesta", []))
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

        self._limpiar_seleccion_lista(self.lista_cod_setor)
        self._limpiar_seleccion_lista(self.lista_cod_recurso)
        self._limpiar_seleccion_lista(self.lista_turno)

        self.input_opcion_valor.clear()
        self.input_opcion_accion.clear()
        self.lista_opciones.clear()
        self._actualizar_estado_opciones()

    def agregar_opcion(self) -> None:
        tipo = self.combo_tipo.currentText().strip().lower()

        if tipo != "seleccion_unica":
            return

        valor = self.input_opcion_valor.text().strip()
        accion_correctiva = self.input_opcion_accion.text().strip()

        if not valor:
            QMessageBox.warning(self, "Atención", "Debes ingresar un valor para la opción.")
            return

        if self._existe_valor_opcion(valor):
            QMessageBox.warning(self, "Atención", "Ya existe una opción con ese valor.")
            return

        self._agregar_item_opcion(
            {
                "id_opcion": "",
                "valor": valor,
                "accion_correctiva": accion_correctiva,
            }
        )

        self.input_opcion_valor.clear()
        self.input_opcion_accion.clear()
        self.input_opcion_valor.setFocus()

    def eliminar_opcion_seleccionada(self) -> None:
        item = self.lista_opciones.currentItem()
        if item is None:
            QMessageBox.warning(self, "Atención", "Selecciona una opción primero.")
            return

        self.lista_opciones.takeItem(self.lista_opciones.row(item))

    def limpiar_opciones(self) -> None:
        self.lista_opciones.clear()
        self.input_opcion_valor.clear()
        self.input_opcion_accion.clear()

    def _actualizar_estado_opciones(self) -> None:
        tipo = self.combo_tipo.currentText().strip().lower()
        requiere_opciones = tipo == "seleccion_unica"

        self.panel_opciones.setVisible(requiere_opciones)

        if not requiere_opciones:
            self.label_info_opciones.setText(
                "Este tipo de pregunta no requiere opciones configurables."
            )
            self.input_opcion_valor.clear()
            self.input_opcion_accion.clear()
            self.lista_opciones.clear()
            self.input_opcion_valor.setEnabled(False)
            self.input_opcion_accion.setEnabled(False)
            self.btn_agregar_opcion.setEnabled(False)
            self.btn_eliminar_opcion.setEnabled(False)
            self.btn_limpiar_opciones.setEnabled(False)
            return

        self.label_info_opciones.setText(
            "Agrega opciones desde los campos inferiores. "
            "Cada opción puede tener una acción correctiva opcional."
        )
        self.input_opcion_valor.setEnabled(True)
        self.input_opcion_accion.setEnabled(True)
        self.btn_agregar_opcion.setEnabled(True)
        self.btn_eliminar_opcion.setEnabled(True)
        self.btn_limpiar_opciones.setEnabled(True)

    def _construir_filtros_contexto(self) -> dict[str, list[str]]:
        filtros: dict[str, list[str]] = {}

        cod_setor = self._obtener_valores_seleccionados(self.lista_cod_setor)
        cod_recurso = self._obtener_valores_seleccionados(self.lista_cod_recurso)
        turno = self._obtener_valores_seleccionados(self.lista_turno)

        if cod_setor:
            filtros["cod_setor"] = cod_setor
        if cod_recurso:
            filtros["cod_recurso"] = cod_recurso
        if turno:
            filtros["turno"] = turno

        return filtros

    def _construir_opciones_respuesta(self) -> list[dict]:
        tipo = self.combo_tipo.currentText().strip().lower()

        if tipo != "seleccion_unica":
            return []

        opciones: list[dict] = []

        for indice in range(self.lista_opciones.count()):
            item = self.lista_opciones.item(indice)
            data = item.data(Qt.UserRole) or {}

            valor = str(data.get("valor", "")).strip()
            accion_correctiva = str(data.get("accion_correctiva", "")).strip()

            if not valor:
                raise ValueError("Cada opción debe tener un valor válido.")

            opciones.append(
                {
                    "id_opcion": f"OPC-{indice + 1:03d}",
                    "valor": valor,
                    "accion_correctiva": accion_correctiva,
                }
            )

        if not opciones:
            raise ValueError(
                "Debes ingresar opciones_respuesta para preguntas de tipo seleccion_unica."
            )

        return opciones

    def _obtener_valores_seleccionados(self, lista: QListWidget) -> list[str]:
        valores: list[str] = []
        for item in lista.selectedItems():
            texto = item.text().strip()
            if texto:
                valores.append(texto)
        return valores

    def _seleccionar_valores_lista(self, lista: QListWidget, valores: list[str]) -> None:
        valores_normalizados = {str(valor).strip().upper() for valor in valores}

        for i in range(lista.count()):
            item = lista.item(i)
            item.setSelected(item.text().strip().upper() in valores_normalizados)

    def _limpiar_seleccion_lista(self, lista: QListWidget) -> None:
        for i in range(lista.count()):
            item = lista.item(i)
            item.setSelected(False)

    def _agregar_item_opcion(self, opcion: dict) -> None:
        valor = str(opcion.get("valor", "")).strip()
        accion_correctiva = str(opcion.get("accion_correctiva", "")).strip()

        texto = valor
        if accion_correctiva:
            texto += f" | Acción correctiva: {accion_correctiva}"

        item = QListWidgetItem(texto)
        item.setData(
            Qt.UserRole,
            {
                "id_opcion": str(opcion.get("id_opcion", "")).strip(),
                "valor": valor,
                "accion_correctiva": accion_correctiva,
            },
        )
        self.lista_opciones.addItem(item)

    def _cargar_opciones_en_lista(self, opciones: list[dict]) -> None:
        self.lista_opciones.clear()

        for opcion in opciones:
            if not isinstance(opcion, dict):
                continue

            self._agregar_item_opcion(opcion)

    def _obtener_opciones_actuales(self) -> list[dict]:
        opciones: list[dict] = []

        for i in range(self.lista_opciones.count()):
            item = self.lista_opciones.item(i)
            data = item.data(Qt.UserRole) or {}
            opciones.append(data)

        return opciones

    def _existe_valor_opcion(self, valor: str) -> bool:
        valor_normalizado = valor.strip().upper()

        for opcion in self._obtener_opciones_actuales():
            actual = str(opcion.get("valor", "")).strip().upper()
            if actual == valor_normalizado:
                return True

        return False

    def _resumen_filtros_contexto(self, filtros: dict) -> str:
        if not isinstance(filtros, dict) or not filtros:
            return ""

        partes: list[str] = []

        etiquetas = {
            "cod_setor": "Setor",
            "cod_recurso": "Recurso",
            "turno": "Turno",
        }

        for clave, etiqueta in etiquetas.items():
            valores = filtros.get(clave, [])
            if not valores:
                continue

            texto_valores = ", ".join(
                str(valor).strip() for valor in valores if str(valor).strip()
            )
            if texto_valores:
                partes.append(f"{etiqueta}: {texto_valores}")

        return " | ".join(partes)