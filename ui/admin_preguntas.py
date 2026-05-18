"""Vistas PyQt que componen las pantallas de gestion y operario.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

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
    QStackedWidget,
)

from presenters.admin_preguntas_presenter import AdminPreguntasPresenter
from services.jobtrack.catalogo_contexto_service import CatalogoContextoService
from services.forms.pregunta_service import PreguntaService
from styles.common import apply_view_style


# Bloque CDLform: clase AdminPreguntasView; agrupa estado y comportamiento de esta parte del flujo.
class AdminPreguntasView(QWidget):
    qss_files = ("base.qss", "admin_preguntas.qss")

    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self) -> None:
        super().__init__()

        self.catalogo_contexto_service = CatalogoContextoService()
        self.pregunta_service = PreguntaService()
        self.presenter = AdminPreguntasPresenter(self.pregunta_service)
        self.id_pregunta_en_edicion: str | None = None
        self.paso_actual = 0
        self.etiquetas_pasos: list[QLabel] = []

        self.setWindowTitle("Administración de Preguntas")
        self.setObjectName("adminPreguntasView")
        self.resize(1380, 820)

        self._init_ui()
        apply_view_style(self, *self.qss_files)
        self.cargar_preguntas()

    # Bloque CDLform: funcion/metodo _init_ui; encapsula una operacion del flujo del modulo.
    def _init_ui(self) -> None:
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(24, 24, 24, 24)
        layout_raiz.setSpacing(18)

        top_panel = QFrame()
        top_panel.setObjectName("adminTopPanel")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(18, 18, 18, 18)
        top_layout.setSpacing(14)

        header_panel = QFrame()
        header_panel.setObjectName("adminHeader")
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(22, 20, 22, 20)
        header_layout.setSpacing(6)

        eyebrow = QLabel("Gestion")
        eyebrow.setProperty("role", "eyebrow")

        titulo_superior = QLabel("Gestion de Preguntas")
        titulo_superior.setProperty("role", "title")

        subtitulo_superior = QLabel(
            "Crea, edita y organiza las preguntas del formulario dinamico."
        )
        subtitulo_superior.setWordWrap(True)
        subtitulo_superior.setProperty("role", "subtitle")

        header_layout.addWidget(eyebrow)
        header_layout.addWidget(titulo_superior)
        header_layout.addWidget(subtitulo_superior)
        top_layout.addWidget(header_panel)
        layout_raiz.addWidget(top_panel)

        layout_principal = QHBoxLayout()
        layout_principal.setSpacing(18)

        panel_izquierdo = QFrame()
        panel_izquierdo.setObjectName("adminSidebar")
        panel_izquierdo.setProperty("card", "true")
        panel_izquierdo.setMinimumWidth(360)
        panel_izquierdo.setMaximumWidth(430)
        panel_izquierdo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        layout_izquierdo = QVBoxLayout(panel_izquierdo)
        layout_izquierdo.setContentsMargins(18, 18, 18, 18)
        layout_izquierdo.setSpacing(12)

        titulo = QLabel("Gestión de Preguntas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")

        subtitulo = QLabel("Crea, edita y organiza las preguntas del formulario dinámico.")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")
        titulo.hide()
        subtitulo.hide()

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setObjectName("adminSidebarSearch")
        self.input_busqueda.setPlaceholderText(
            "Buscar por texto, tipo o filtros de contexto..."
        )
        self.input_busqueda.textChanged.connect(self.filtrar_preguntas)

        label_lista = QLabel("Listado de preguntas")
        label_lista.setObjectName("adminSidebarLabel")
        label_lista.setProperty("role", "section")

        self.lista_preguntas = QListWidget()
        self.lista_preguntas.setObjectName("adminSidebarList")
        self.lista_preguntas.itemClicked.connect(self.cargar_pregunta_seleccionada)
        self.lista_preguntas.setMinimumHeight(540)

        layout_izquierdo.addWidget(titulo)
        layout_izquierdo.addWidget(subtitulo)
        layout_izquierdo.addSpacing(6)
        layout_izquierdo.addWidget(self.input_busqueda)
        layout_izquierdo.addWidget(label_lista)
        layout_izquierdo.addWidget(self.lista_preguntas, 1)

        panel_derecho = QFrame()
        panel_derecho.setProperty("card", "true")

        layout_derecho_externo = QVBoxLayout(panel_derecho)
        layout_derecho_externo.setContentsMargins(18, 18, 18, 18)
        layout_derecho_externo.setSpacing(12)

        titulo_form = QLabel("Configuración de pregunta")
        titulo_form.setProperty("role", "section")
        layout_derecho_externo.addWidget(titulo_form)

        pasos_layout = QHBoxLayout()
        pasos_layout.setSpacing(8)
        for texto_paso in ("1. Datos", "2. Contexto", "3. Opciones", "4. Resumen"):
            etiqueta_paso = QLabel(texto_paso)
            etiqueta_paso.setObjectName("adminPasoFlujo")
            etiqueta_paso.setAlignment(Qt.AlignCenter)
            self.etiquetas_pasos.append(etiqueta_paso)
            pasos_layout.addWidget(etiqueta_paso)
        layout_derecho_externo.addLayout(pasos_layout)

        self.scroll_form = QScrollArea()
        self.scroll_form.setWidgetResizable(True)
        self.scroll_form.setFrameShape(QFrame.NoFrame)

        self.form_container = QWidget()
        self.scroll_form.setWidget(self.form_container)

        form_wrapper = QVBoxLayout(self.form_container)
        form_wrapper.setContentsMargins(6, 6, 6, 6)
        form_wrapper.setSpacing(18)

        self.stack_fases = QStackedWidget()

        bloque_basico = QFrame()
        bloque_basico.setProperty("card", "true")
        bloque_basico.setObjectName("bloqueBasicoPregunta")

        layout_basico = QFormLayout(bloque_basico)
        layout_basico.setContentsMargins(14, 14, 14, 14)
        layout_basico.setSpacing(12)
        layout_basico.setLabelAlignment(Qt.AlignLeft)
        layout_basico.setFormAlignment(Qt.AlignTop)

        self.input_texto = QLineEdit()

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(
            ["texto", "numero", "seleccion_unica", "seleccion_multiple"]
        )
        self.combo_tipo.currentTextChanged.connect(self._actualizar_estado_opciones)

        self.spin_orden = QSpinBox()
        self.spin_orden.setMinimum(1)
        self.spin_orden.setMaximum(9999)
        self.spin_orden.setValue(1)

        checks_layout = QHBoxLayout()
        checks_layout.setSpacing(18)

        self.check_obligatoria = QCheckBox("Obligatoria")
        self.check_obligatoria.setChecked(True)
        self.check_obligatoria.setProperty("chip", "true")

        self.check_activa = QCheckBox("Activa")
        self.check_activa.setChecked(True)
        self.check_activa.setProperty("chip", "true")

        checks_layout.addWidget(self.check_obligatoria)
        checks_layout.addWidget(self.check_activa)
        checks_layout.addStretch()

        checks_widget = QWidget()
        checks_widget.setObjectName("estadoPregunta")
        checks_widget.setLayout(checks_layout)

        layout_basico.addRow("Texto:", self.input_texto)
        layout_basico.addRow("Tipo:", self.combo_tipo)
        layout_basico.addRow("Orden:", self.spin_orden)
        layout_basico.addRow("Estado:", checks_widget)

        bloque_contexto = QFrame()
        bloque_contexto.setProperty("card", "true")
        bloque_contexto.setObjectName("bloqueContextoPregunta")

        layout_contexto = QVBoxLayout(bloque_contexto)
        layout_contexto.setContentsMargins(14, 14, 14, 14)
        layout_contexto.setSpacing(12)

        label_contexto = QLabel("Filtros de contexto")
        label_contexto.setProperty("role", "section")

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
        self.panel_opciones.setProperty("card", "true")
        self.panel_opciones.setObjectName("panelOpcionesPregunta")

        layout_opciones = QVBoxLayout(self.panel_opciones)
        layout_opciones.setContentsMargins(14, 14, 14, 14)
        layout_opciones.setSpacing(12)

        label_opciones = QLabel("Opciones de respuesta")
        label_opciones.setProperty("role", "section")

        self.label_info_opciones = QLabel("")
        self.label_info_opciones.setWordWrap(True)
        self.label_info_opciones.setProperty("role", "subtitle")

        fila_opcion = QHBoxLayout()
        fila_opcion.setSpacing(10)

        self.input_opcion_valor = QLineEdit()
        self.input_opcion_valor.setPlaceholderText("Valor de la opción")

        self.input_opcion_accion = QLineEdit()
        self.input_opcion_accion.setPlaceholderText("Acción correctiva (opcional)")

        self.btn_agregar_opcion = QPushButton("Agregar opción")
        self.btn_agregar_opcion.setProperty("variant", "secondary")
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
        self.btn_eliminar_opcion.setProperty("variant", "danger")
        self.btn_eliminar_opcion.clicked.connect(self.eliminar_opcion_seleccionada)

        self.btn_limpiar_opciones = QPushButton("Limpiar opciones")
        self.btn_limpiar_opciones.setProperty("variant", "secondary")
        self.btn_limpiar_opciones.clicked.connect(self.limpiar_opciones)

        fila_botones_opciones.addStretch()
        fila_botones_opciones.addWidget(self.btn_limpiar_opciones)
        fila_botones_opciones.addWidget(self.btn_eliminar_opcion)

        layout_opciones.addWidget(label_opciones)
        layout_opciones.addWidget(self.label_info_opciones)
        layout_opciones.addLayout(fila_opcion)
        layout_opciones.addWidget(self.lista_opciones)
        layout_opciones.addLayout(fila_botones_opciones)

        self.label_sin_opciones = QLabel("")
        self.label_sin_opciones.setWordWrap(True)
        self.label_sin_opciones.setProperty("role", "subtitle")

        self.label_resumen_confirmacion = QLabel("")
        self.label_resumen_confirmacion.setWordWrap(True)
        self.label_resumen_confirmacion.setObjectName("adminResumenConfirmacion")
        self.label_resumen_confirmacion.setAlignment(Qt.AlignJustify | Qt.AlignTop)

        fase_datos = self._crear_fase_flujo(bloque_basico)
        fase_contexto = self._crear_fase_flujo(bloque_contexto)
        fase_opciones = QWidget()
        fase_opciones_layout = QVBoxLayout(fase_opciones)
        fase_opciones_layout.setContentsMargins(0, 0, 0, 0)
        fase_opciones_layout.setSpacing(12)
        fase_opciones_layout.addWidget(self.panel_opciones)
        fase_opciones_layout.addWidget(self.label_sin_opciones)
        fase_opciones_layout.addStretch()

        fase_resumen = QWidget()
        fase_resumen_layout = QVBoxLayout(fase_resumen)
        fase_resumen_layout.setContentsMargins(0, 0, 0, 0)
        fase_resumen_layout.setSpacing(12)
        fase_resumen_layout.addWidget(self.label_resumen_confirmacion)
        fase_resumen_layout.addStretch()

        self.stack_fases.addWidget(fase_datos)
        self.stack_fases.addWidget(fase_contexto)
        self.stack_fases.addWidget(fase_opciones)
        self.stack_fases.addWidget(fase_resumen)

        form_wrapper.addWidget(self.stack_fases)
        form_wrapper.addStretch()

        layout_derecho_externo.addWidget(self.scroll_form, 1)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        self.btn_atras = QPushButton("Back")
        self.btn_atras.setProperty("variant", "secondary")
        self.btn_atras.clicked.connect(self.paso_anterior)

        self.btn_siguiente = QPushButton("Siguiente")
        self.btn_siguiente.setProperty("variant", "secondary")
        self.btn_siguiente.clicked.connect(self.paso_siguiente)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setProperty("variant", "success")
        self.btn_guardar.clicked.connect(self.guardar_pregunta)

        self.btn_nuevo = QPushButton("Limpiar")
        self.btn_nuevo.setProperty("variant", "secondary")
        self.btn_nuevo.clicked.connect(self.limpiar_formulario)

        self.btn_eliminar = QPushButton("Enviar a historial")
        self.btn_eliminar.setProperty("variant", "danger")
        self.btn_eliminar.clicked.connect(self.eliminar_pregunta)

        botones_layout.addWidget(self.btn_atras)
        botones_layout.addWidget(self.btn_siguiente)
        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_nuevo)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_guardar)

        layout_derecho_externo.addLayout(botones_layout)

        layout_principal.addWidget(panel_izquierdo, 0)
        layout_principal.addWidget(panel_derecho, 1)
        layout_raiz.addLayout(layout_principal, 1)

        self._actualizar_estado_opciones()
        self._ir_a_paso(0)

    # Bloque CDLform: funcion/metodo _crear_fase_flujo; encapsula una operacion del flujo del modulo.
    def _crear_fase_flujo(self, contenido: QWidget) -> QWidget:
        fase = QWidget()
        layout = QVBoxLayout(fase)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(contenido)
        layout.addStretch()
        return fase

    # Bloque CDLform: funcion/metodo _crear_lista_multiseleccion; encapsula una operacion del flujo del modulo.
    def _crear_lista_multiseleccion(self, valores: list[str]) -> QListWidget:
        lista = QListWidget()
        lista.setSelectionMode(QAbstractItemView.MultiSelection)
        lista.setMinimumHeight(130)
        lista.setMaximumHeight(170)

        for valor in valores:
            item = QListWidgetItem(valor)
            lista.addItem(item)

        return lista

    # Bloque CDLform: funcion/metodo _crear_bloque_lista; encapsula una operacion del flujo del modulo.
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

    # Bloque CDLform: funcion/metodo cargar_preguntas; encapsula una operacion del flujo del modulo.
    def cargar_preguntas(self) -> None:
        self.lista_preguntas.clear()
        preguntas = self.presenter.listar_preguntas()

        for pregunta in preguntas:
            item_texto = self.presenter.construir_item_lista_pregunta(pregunta)
            item = QListWidgetItem(item_texto)
            item.setData(Qt.UserRole, pregunta)
            self.lista_preguntas.addItem(item)

    # Bloque CDLform: funcion/metodo filtrar_preguntas; encapsula una operacion del flujo del modulo.
    def filtrar_preguntas(self) -> None:
        texto_busqueda = self.input_busqueda.text().strip().lower()

        for i in range(self.lista_preguntas.count()):
            item = self.lista_preguntas.item(i)
            pregunta = item.data(Qt.UserRole) or {}

            coincide = self.presenter.coincide_filtro_busqueda(
                pregunta,
                item.text(),
                texto_busqueda,
            )
            item.setHidden(not coincide)

    # Bloque CDLform: funcion/metodo cargar_pregunta_seleccionada; encapsula una operacion del flujo del modulo.
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
        self._ir_a_paso(0)

    # Bloque CDLform: funcion/metodo guardar_pregunta; encapsula una operacion del flujo del modulo.
    def guardar_pregunta(self) -> None:
        if self.paso_actual < self.stack_fases.count() - 1:
            self.paso_siguiente()
            return

        try:
            payload = self._construir_payload_desde_formulario()
            mensaje = self.presenter.guardar_pregunta(
                self.id_pregunta_en_edicion,
                payload,
            )
            QMessageBox.information(self, "Éxito", mensaje)

            self.limpiar_formulario()
            self.cargar_preguntas()

        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    # Bloque CDLform: funcion/metodo eliminar_pregunta; encapsula una operacion del flujo del modulo.
    def eliminar_pregunta(self) -> None:
        if not self.id_pregunta_en_edicion:
            QMessageBox.warning(self, "Atención", "Selecciona una pregunta primero.")
            return

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Seguro que deseas desactivar esta pregunta y conservarla en el historial?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmacion != QMessageBox.Yes:
            return

        try:
            mensaje = self.presenter.eliminar_pregunta(self.id_pregunta_en_edicion)
            QMessageBox.information(self, "Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_preguntas()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    # Bloque CDLform: funcion/metodo limpiar_formulario; encapsula una operacion del flujo del modulo.
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
        self._ir_a_paso(0)

    # Bloque CDLform: funcion/metodo paso_anterior; encapsula una operacion del flujo del modulo.
    def paso_anterior(self) -> None:
        self._ir_a_paso(self.paso_actual - 1)

    # Bloque CDLform: funcion/metodo paso_siguiente; encapsula una operacion del flujo del modulo.
    def paso_siguiente(self) -> None:
        if not self._validar_paso_actual():
            return
        self._ir_a_paso(self.paso_actual + 1)

    # Bloque CDLform: funcion/metodo _ir_a_paso; encapsula una operacion del flujo del modulo.
    def _ir_a_paso(self, indice: int) -> None:
        if not hasattr(self, "stack_fases"):
            return

        indice_limitado = max(0, min(indice, self.stack_fases.count() - 1))
        self.paso_actual = indice_limitado
        self.stack_fases.setCurrentIndex(indice_limitado)
        self._actualizar_resumen_confirmacion()
        self._actualizar_navegacion_fases()

    # Bloque CDLform: funcion/metodo _validar_paso_actual; encapsula una operacion del flujo del modulo.
    def _validar_paso_actual(self) -> bool:
        try:
            if self.paso_actual == 0 and not self.input_texto.text().strip():
                raise ValueError("El texto de la pregunta es obligatorio.")

            if self.paso_actual == 2:
                self._construir_payload_desde_formulario()
        except Exception as exc:
            QMessageBox.warning(self, "AtenciÃ³n", str(exc))
            return False

        return True

    # Bloque CDLform: funcion/metodo _actualizar_navegacion_fases; encapsula una operacion del flujo del modulo.
    def _actualizar_navegacion_fases(self) -> None:
        total_pasos = self.stack_fases.count()
        es_ultimo_paso = self.paso_actual == total_pasos - 1

        self.btn_atras.setEnabled(self.paso_actual > 0)
        self.btn_siguiente.setVisible(not es_ultimo_paso)
        self.btn_guardar.setVisible(es_ultimo_paso)
        self.btn_eliminar.setVisible(es_ultimo_paso)
        self.btn_eliminar.setEnabled(bool(self.id_pregunta_en_edicion))

        for indice, etiqueta in enumerate(self.etiquetas_pasos):
            etiqueta.setProperty("estado", "actual" if indice == self.paso_actual else "")
            etiqueta.style().unpolish(etiqueta)
            etiqueta.style().polish(etiqueta)

    # Bloque CDLform: funcion/metodo _actualizar_resumen_confirmacion; encapsula una operacion del flujo del modulo.
    def _actualizar_resumen_confirmacion(self) -> None:
        if not hasattr(self, "label_resumen_confirmacion"):
            return

        filtros = self._construir_filtros_contexto()
        resumen_filtros = self._resumen_filtros_contexto(filtros) or "Sin filtros"
        tipo = self.combo_tipo.currentText().strip()
        cantidad_opciones = len(self._obtener_opciones_actuales())
        estado = "Activa" if self.check_activa.isChecked() else "Inactiva"
        obligatoria = "Obligatoria" if self.check_obligatoria.isChecked() else "Opcional"

        self.label_resumen_confirmacion.setText(
            "<h2>Resumen antes de guardar</h2>"
            "<p><b>Texto</b><br>"
            f"{self.input_texto.text().strip() or '-'}</p>"
            "<p><b>Tipo</b><br>"
            f"{tipo}</p>"
            "<p><b>Orden</b><br>"
            f"{self.spin_orden.value()}</p>"
            "<p><b>Estado</b><br>"
            f"{estado} | {obligatoria}</p>"
            "<p><b>Contexto</b><br>"
            f"{resumen_filtros}</p>"
            "<p><b>Opciones configuradas</b><br>"
            f"{cantidad_opciones}</p>"
        )

    # Bloque CDLform: funcion/metodo agregar_opcion; encapsula una operacion del flujo del modulo.
    def agregar_opcion(self) -> None:
        tipo = self.combo_tipo.currentText().strip().lower()

        if not self.presenter.requiere_opciones(tipo):
            return

        valor = self.input_opcion_valor.text().strip()
        accion_correctiva = self.input_opcion_accion.text().strip()

        try:
            if self._existe_valor_opcion(valor):
                raise ValueError("Ya existe una opción con ese valor.")

            opcion = self.presenter.construir_opcion_temporal(
                valor,
                accion_correctiva,
            )
            self._agregar_item_opcion(opcion)
        except ValueError as exc:
            QMessageBox.warning(self, "Atención", str(exc))
            return

        self.input_opcion_valor.clear()
        self.input_opcion_accion.clear()
        self.input_opcion_valor.setFocus()
        self._actualizar_resumen_confirmacion()

    # Bloque CDLform: funcion/metodo eliminar_opcion_seleccionada; encapsula una operacion del flujo del modulo.
    def eliminar_opcion_seleccionada(self) -> None:
        item = self.lista_opciones.currentItem()
        if item is None:
            QMessageBox.warning(self, "Atención", "Selecciona una opción primero.")
            return

        self.lista_opciones.takeItem(self.lista_opciones.row(item))
        self._actualizar_resumen_confirmacion()

    # Bloque CDLform: funcion/metodo limpiar_opciones; encapsula una operacion del flujo del modulo.
    def limpiar_opciones(self) -> None:
        self.lista_opciones.clear()
        self.input_opcion_valor.clear()
        self.input_opcion_accion.clear()
        self._actualizar_resumen_confirmacion()

    # Bloque CDLform: funcion/metodo _actualizar_estado_opciones; encapsula una operacion del flujo del modulo.
    def _actualizar_estado_opciones(self) -> None:
        tipo = self.combo_tipo.currentText().strip().lower()
        requiere_opciones = self.presenter.requiere_opciones(tipo)

        self.panel_opciones.setVisible(requiere_opciones)

        if not requiere_opciones:
            self.label_info_opciones.setText(self.presenter.mensaje_opciones(tipo))
            if hasattr(self, "label_sin_opciones"):
                self.label_sin_opciones.setText(self.presenter.mensaje_opciones(tipo))
                self.label_sin_opciones.setVisible(True)
            self.input_opcion_valor.clear()
            self.input_opcion_accion.clear()
            self.lista_opciones.clear()
            self.input_opcion_valor.setEnabled(False)
            self.input_opcion_accion.setEnabled(False)
            self.btn_agregar_opcion.setEnabled(False)
            self.btn_eliminar_opcion.setEnabled(False)
            self.btn_limpiar_opciones.setEnabled(False)
            self._actualizar_resumen_confirmacion()
            return

        self.label_info_opciones.setText(self.presenter.mensaje_opciones(tipo))
        if hasattr(self, "label_sin_opciones"):
            self.label_sin_opciones.clear()
            self.label_sin_opciones.setVisible(False)

        self.input_opcion_valor.setEnabled(True)
        self.input_opcion_accion.setEnabled(True)
        self.btn_agregar_opcion.setEnabled(True)
        self.btn_eliminar_opcion.setEnabled(True)
        self.btn_limpiar_opciones.setEnabled(True)
        self._actualizar_resumen_confirmacion()

    # Bloque CDLform: funcion/metodo _construir_payload_desde_formulario; encapsula una operacion del flujo del modulo.
    def _construir_payload_desde_formulario(self) -> dict:
        return self.presenter.construir_payload_pregunta(
            texto=self.input_texto.text().strip(),
            tipo=self.combo_tipo.currentText().strip(),
            obligatoria=self.check_obligatoria.isChecked(),
            activa=self.check_activa.isChecked(),
            orden=self.spin_orden.value(),
            filtros_contexto=self._construir_filtros_contexto(),
            opciones_respuesta=self._construir_opciones_respuesta(),
        )

    # Bloque CDLform: funcion/metodo _construir_filtros_contexto; encapsula una operacion del flujo del modulo.
    def _construir_filtros_contexto(self) -> dict[str, list[str]]:
        cod_setor = self._obtener_valores_seleccionados(self.lista_cod_setor)
        cod_recurso = self._obtener_valores_seleccionados(self.lista_cod_recurso)
        turno = self._obtener_valores_seleccionados(self.lista_turno)
        return self.presenter.construir_filtros_contexto(
            cod_setor,
            cod_recurso,
            turno,
        )

    # Bloque CDLform: funcion/metodo _construir_opciones_respuesta; encapsula una operacion del flujo del modulo.
    def _construir_opciones_respuesta(self) -> list[dict]:
        return self.presenter.construir_opciones_respuesta(
            self.combo_tipo.currentText().strip().lower(),
            self._obtener_opciones_actuales(),
        )

    # Bloque CDLform: funcion/metodo _obtener_valores_seleccionados; encapsula una operacion del flujo del modulo.
    def _obtener_valores_seleccionados(self, lista: QListWidget) -> list[str]:
        valores: list[str] = []
        for item in lista.selectedItems():
            texto = item.text().strip()
            if texto:
                valores.append(texto)
        return valores

    # Bloque CDLform: funcion/metodo _seleccionar_valores_lista; encapsula una operacion del flujo del modulo.
    def _seleccionar_valores_lista(self, lista: QListWidget, valores: list[str]) -> None:
        valores_normalizados = {str(valor).strip().upper() for valor in valores}

        for i in range(lista.count()):
            item = lista.item(i)
            item.setSelected(item.text().strip().upper() in valores_normalizados)

    # Bloque CDLform: funcion/metodo _limpiar_seleccion_lista; encapsula una operacion del flujo del modulo.
    def _limpiar_seleccion_lista(self, lista: QListWidget) -> None:
        for i in range(lista.count()):
            item = lista.item(i)
            item.setSelected(False)

    # Bloque CDLform: funcion/metodo _agregar_item_opcion; encapsula una operacion del flujo del modulo.
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

    # Bloque CDLform: funcion/metodo _cargar_opciones_en_lista; encapsula una operacion del flujo del modulo.
    def _cargar_opciones_en_lista(self, opciones: list[dict]) -> None:
        self.lista_opciones.clear()

        for opcion in opciones:
            if not isinstance(opcion, dict):
                continue

            self._agregar_item_opcion(opcion)

    # Bloque CDLform: funcion/metodo _obtener_opciones_actuales; encapsula una operacion del flujo del modulo.
    def _obtener_opciones_actuales(self) -> list[dict]:
        opciones: list[dict] = []

        for i in range(self.lista_opciones.count()):
            item = self.lista_opciones.item(i)
            data = item.data(Qt.UserRole) or {}
            opciones.append(data)

        return opciones

    # Bloque CDLform: funcion/metodo _existe_valor_opcion; encapsula una operacion del flujo del modulo.
    def _existe_valor_opcion(self, valor: str) -> bool:
        return self.presenter.existe_valor_opcion(
            valor,
            self._obtener_opciones_actuales(),
        )

    # Bloque CDLform: funcion/metodo _resumen_filtros_contexto; encapsula una operacion del flujo del modulo.
    def _resumen_filtros_contexto(self, filtros: dict) -> str:
        return self.presenter.resumen_filtros_contexto(filtros)

