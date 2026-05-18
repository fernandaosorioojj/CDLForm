"""Vistas PyQt que componen las pantallas de gestion y operario.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from datetime import datetime

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QHeaderView,
    QFrame,
    QDateEdit,
    QCheckBox,
)

from models.formulario import Formulario
from services.jobtrack.catalogo_contexto_service import CatalogoContextoService
from services.reporting.reporte_service import ReporteService
from styles.common import apply_view_style
from ui.detalle_formulario import DetalleFormularioView


# Bloque CDLform: clase ReportesView; agrupa estado y comportamiento de esta parte del flujo.
class ReportesView(QWidget):
    registros_por_pagina = 100
    qss_files = ("base.qss", "reportes.qss")
    window_title = "Reportes"
    title_text = "Reportes de Formularios"
    subtitle_text = (
        "Consulta los formularios registrados y abre el detalle para revisar respuestas."
    )
    detail_button_text = "Ver detalle"

    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self) -> None:
        super().__init__()

        self.reporte_service = ReporteService()
        self.catalogo_contexto_service = CatalogoContextoService()

        self.formularios: list[Formulario] = []
        self.formularios_filtrados: list[Formulario] = []
        self.pagina_actual = 0

        self.setWindowTitle(self.window_title)
        self.setObjectName("reportesView")
        self.resize(1500, 820)

        self._init_ui()
        apply_view_style(self, *self.qss_files)
        self.cargar_reporte()

    # Bloque CDLform: funcion/metodo _init_ui; encapsula una operacion del flujo del modulo.
    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(18)

        top_panel = QFrame()
        top_panel.setObjectName("reportesTopPanel")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(18, 18, 18, 18)
        top_layout.setSpacing(14)

        header_panel = QFrame()
        header_panel.setObjectName("reportesHeader")
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(22, 20, 22, 20)
        header_layout.setSpacing(6)

        eyebrow = QLabel("Gestion")
        eyebrow.setProperty("role", "eyebrow")

        titulo = QLabel(self.title_text)
        titulo.setProperty("role", "title")

        subtitulo = QLabel(self.subtitle_text)
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        header_layout.addWidget(eyebrow)
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        top_layout.addWidget(header_panel)

        panel_filtros = QFrame()
        panel_filtros.setObjectName("reportesFiltros")
        panel_filtros.setProperty("card", "true")

        layout_filtros = QHBoxLayout(panel_filtros)
        layout_filtros.setContentsMargins(18, 16, 18, 16)
        layout_filtros.setSpacing(14)

        filtros_fila_1 = QHBoxLayout()
        filtros_fila_1.setSpacing(10)

        self.input_identificador = QLineEdit()
        self.input_identificador.setPlaceholderText("Buscar identificador...")

        self.input_operario = QLineEdit()
        self.input_operario.setPlaceholderText("Buscar operario...")

        self.combo_cod_setor = QComboBox()
        self._cargar_combo_con_todos(
            self.combo_cod_setor,
            self.catalogo_contexto_service.listar_cod_setor(),
            "CodSetor: Todos",
        )

        self.combo_cod_recurso = QComboBox()
        self._cargar_combo_con_todos(
            self.combo_cod_recurso,
            self.catalogo_contexto_service.listar_cod_recurso(),
            "CodRecurso: Todos",
        )

        self.combo_turno = QComboBox()
        self._cargar_combo_con_todos(
            self.combo_turno,
            self.catalogo_contexto_service.listar_turnos(),
            "Turno: Todos",
        )

        self.combo_estado_formulario = QComboBox()
        self.combo_estado_formulario.addItem("Estado: Todos", "")
        self.combo_estado_formulario.addItem("En apertura", "en_apertura")
        self.combo_estado_formulario.addItem("Pendiente operario", "pendiente_operario")
        self.combo_estado_formulario.addItem("Completado", "completado")
        self.combo_estado_formulario.addItem("Cancelado", "cancelado")

        self.check_fecha_desde = QCheckBox("Desde")
        self.check_fecha_hasta = QCheckBox("Hasta")

        self.input_fecha_desde = QDateEdit()
        self.input_fecha_desde.setCalendarPopup(True)
        self.input_fecha_desde.setDisplayFormat("dd/MM/yyyy")
        self.input_fecha_desde.setDate(QDate.currentDate().addMonths(-1))
        self.input_fecha_desde.setEnabled(False)

        self.input_fecha_hasta = QDateEdit()
        self.input_fecha_hasta.setCalendarPopup(True)
        self.input_fecha_hasta.setDisplayFormat("dd/MM/yyyy")
        self.input_fecha_hasta.setDate(QDate.currentDate())
        self.input_fecha_hasta.setEnabled(False)

        filtros_fila_1.addWidget(self.input_identificador)
        filtros_fila_1.addWidget(self.input_operario)
        filtros_fila_1.addWidget(self.combo_cod_setor)
        filtros_fila_1.addWidget(self.combo_cod_recurso)
        filtros_fila_1.addWidget(self.combo_turno)
        filtros_fila_1.addWidget(self.combo_estado_formulario)
        filtros_fila_1.addWidget(self.check_fecha_desde)
        filtros_fila_1.addWidget(self.input_fecha_desde)
        filtros_fila_1.addWidget(self.check_fecha_hasta)
        filtros_fila_1.addWidget(self.input_fecha_hasta)

        layout_filtros.addLayout(filtros_fila_1, 1)

        botones = QHBoxLayout()
        botones.setSpacing(10)

        self.btn_recargar = QPushButton("Recargar")
        self.btn_recargar.clicked.connect(self.cargar_reporte)

        self.btn_ver_detalle = QPushButton(self.detail_button_text)
        self.btn_ver_detalle.clicked.connect(self.abrir_detalle)

        self.btn_limpiar = QPushButton("Limpiar filtros")
        self.btn_limpiar.setProperty("variant", "secondary")
        self.btn_limpiar.clicked.connect(self.limpiar_filtros)

        botones.addStretch()
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_ver_detalle)
        botones.addWidget(self.btn_limpiar)

        layout_filtros.addLayout(botones)
        top_layout.addWidget(panel_filtros)
        layout_principal.addWidget(top_panel)

        panel_tabla = QFrame()
        panel_tabla.setObjectName("reportesTablaPanel")
        panel_tabla.setProperty("card", "true")

        layout_tabla = QVBoxLayout(panel_tabla)
        layout_tabla.setContentsMargins(20, 20, 20, 20)
        layout_tabla.setSpacing(14)

        label_resultados = QLabel("Resultados")
        label_resultados.setProperty("role", "section")
        layout_tabla.addWidget(label_resultados)

        self.tabla_reportes = QTableWidget()
        self._configurar_tabla()

        layout_tabla.addWidget(self.tabla_reportes)

        fila_paginacion = QHBoxLayout()
        fila_paginacion.setSpacing(10)

        self.label_total = QLabel("Total formularios: 0")
        self.label_total.setAlignment(Qt.AlignLeft)
        self.label_total.setProperty("role", "subtitle")

        self.btn_anterior = QPushButton("Anterior")
        self.btn_anterior.setProperty("variant", "secondary")
        self.btn_anterior.clicked.connect(self.pagina_anterior)

        self.btn_siguiente = QPushButton("Siguiente")
        self.btn_siguiente.setProperty("variant", "secondary")
        self.btn_siguiente.clicked.connect(self.pagina_siguiente)

        fila_paginacion.addWidget(self.label_total, 1)
        fila_paginacion.addWidget(self.btn_anterior)
        fila_paginacion.addWidget(self.btn_siguiente)
        layout_tabla.addLayout(fila_paginacion)

        layout_principal.addWidget(panel_tabla, 1)

        self._conectar_filtros()

    # Bloque CDLform: funcion/metodo _configurar_tabla; encapsula una operacion del flujo del modulo.
    def _configurar_tabla(self) -> None:
        self.tabla_reportes.setColumnCount(9)
        self.tabla_reportes.setHorizontalHeaderLabels(
            [
                "ID Formulario",
                "Identificador",
                "Operario",
                "CodSetor",
                "CodRecurso",
                "Turno",
                "Version plantilla",
                "Estado",
                "Fecha",
            ]
        )
        self.tabla_reportes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_reportes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_reportes.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_reportes.verticalHeader().setVisible(False)
        self.tabla_reportes.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tabla_reportes.horizontalHeader().setStretchLastSection(True)
        self.tabla_reportes.doubleClicked.connect(self.abrir_detalle)

    # Bloque CDLform: funcion/metodo _conectar_filtros; encapsula una operacion del flujo del modulo.
    def _conectar_filtros(self) -> None:
        self.input_identificador.textChanged.connect(self.cargar_reporte_desde_inicio)
        self.input_operario.textChanged.connect(self.cargar_reporte_desde_inicio)
        self.combo_cod_setor.currentIndexChanged.connect(self.cargar_reporte_desde_inicio)
        self.combo_cod_recurso.currentIndexChanged.connect(self.cargar_reporte_desde_inicio)
        self.combo_turno.currentIndexChanged.connect(self.cargar_reporte_desde_inicio)
        self.combo_estado_formulario.currentIndexChanged.connect(self.cargar_reporte_desde_inicio)
        self.check_fecha_desde.toggled.connect(self._cambiar_uso_fecha_desde)
        self.check_fecha_hasta.toggled.connect(self._cambiar_uso_fecha_hasta)
        self.input_fecha_desde.dateChanged.connect(self.cargar_reporte_desde_inicio)
        self.input_fecha_hasta.dateChanged.connect(self.cargar_reporte_desde_inicio)

    # Bloque CDLform: funcion/metodo _cargar_combo_con_todos; encapsula una operacion del flujo del modulo.
    def _cargar_combo_con_todos(
        self,
        combo: QComboBox,
        valores: list[str],
        texto_todos: str,
    ) -> None:
        combo.addItem(texto_todos, "")

        for valor in valores:
            valor_limpio = str(valor).strip()
            if valor_limpio:
                combo.addItem(valor_limpio, valor_limpio)

    # Bloque CDLform: funcion/metodo cargar_reporte_desde_inicio; encapsula una operacion del flujo del modulo.
    def cargar_reporte_desde_inicio(self, *_args) -> None:
        self.pagina_actual = 0
        self.cargar_reporte()

    # Bloque CDLform: funcion/metodo cargar_reporte; encapsula una operacion del flujo del modulo.
    def cargar_reporte(self, *_args) -> None:
        try:
            self.formularios = self.reporte_service.listar_formularios()
            self.formularios_filtrados = self._filtrar_formularios(self.formularios)
            self._ordenar_formularios(self.formularios_filtrados)
            self.pagina_actual = min(self.pagina_actual, self._total_paginas() - 1)
            self._cargar_tabla(self._obtener_formularios_pagina())
            self._actualizar_paginacion()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    # Bloque CDLform: funcion/metodo limpiar_filtros; encapsula una operacion del flujo del modulo.
    def limpiar_filtros(self) -> None:
        self.input_identificador.clear()
        self.input_operario.clear()

        self.combo_cod_setor.setCurrentIndex(0)
        self.combo_cod_recurso.setCurrentIndex(0)
        self.combo_turno.setCurrentIndex(0)
        self.combo_estado_formulario.setCurrentIndex(0)
        self.check_fecha_desde.setChecked(False)
        self.check_fecha_hasta.setChecked(False)
        self.input_fecha_desde.setDate(QDate.currentDate().addMonths(-1))
        self.input_fecha_hasta.setDate(QDate.currentDate())

        self.cargar_reporte_desde_inicio()

    # Bloque CDLform: funcion/metodo _obtener_formularios_pagina; encapsula una operacion del flujo del modulo.
    def _obtener_formularios_pagina(self) -> list[Formulario]:
        inicio = self.pagina_actual * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina
        return self.formularios_filtrados[inicio:fin]

    # Bloque CDLform: funcion/metodo _total_paginas; encapsula una operacion del flujo del modulo.
    def _total_paginas(self) -> int:
        total = len(self.formularios_filtrados)
        if total == 0:
            return 1
        return (total - 1) // self.registros_por_pagina + 1

    # Bloque CDLform: funcion/metodo _actualizar_paginacion; encapsula una operacion del flujo del modulo.
    def _actualizar_paginacion(self) -> None:
        total = len(self.formularios_filtrados)
        if total == 0:
            self.label_total.setText("Total formularios: 0")
            self.btn_anterior.setEnabled(False)
            self.btn_siguiente.setEnabled(False)
            return

        inicio = self.pagina_actual * self.registros_por_pagina + 1
        fin = min(inicio + self.registros_por_pagina - 1, total)
        self.label_total.setText(
            f"Formularios {inicio}-{fin} de {total}"
        )
        self.btn_anterior.setEnabled(self.pagina_actual > 0)
        self.btn_siguiente.setEnabled(self.pagina_actual < self._total_paginas() - 1)

    # Bloque CDLform: funcion/metodo pagina_anterior; encapsula una operacion del flujo del modulo.
    def pagina_anterior(self) -> None:
        if self.pagina_actual <= 0:
            return
        self.pagina_actual -= 1
        self._cargar_tabla(self._obtener_formularios_pagina())
        self._actualizar_paginacion()

    # Bloque CDLform: funcion/metodo pagina_siguiente; encapsula una operacion del flujo del modulo.
    def pagina_siguiente(self) -> None:
        if self.pagina_actual >= self._total_paginas() - 1:
            return
        self.pagina_actual += 1
        self._cargar_tabla(self._obtener_formularios_pagina())
        self._actualizar_paginacion()

    # Bloque CDLform: funcion/metodo _filtrar_formularios; encapsula una operacion del flujo del modulo.
    def _filtrar_formularios(
        self,
        formularios: list[Formulario],
    ) -> list[Formulario]:
        identificador = self.input_identificador.text().strip().lower()
        operario = self.input_operario.text().strip().lower()

        cod_setor = str(self.combo_cod_setor.currentData() or "").strip().lower()
        cod_recurso = str(self.combo_cod_recurso.currentData() or "").strip().lower()
        turno = str(self.combo_turno.currentData() or "").strip().lower()
        estado = str(self.combo_estado_formulario.currentData() or "").strip().lower()
        fecha_desde = (
            self.input_fecha_desde.date().toPyDate()
            if self.check_fecha_desde.isChecked()
            else None
        )
        fecha_hasta = (
            self.input_fecha_hasta.date().toPyDate()
            if self.check_fecha_hasta.isChecked()
            else None
        )

        filtrados: list[Formulario] = []

        for formulario in formularios:
            valor_identificador = (formulario.identificador or "").strip().lower()
            valor_operario = (formulario.operario or "").strip().lower()
            valor_cod_setor = self._obtener_cod_setor(formulario).lower()
            valor_cod_recurso = self._obtener_cod_recurso(formulario).lower()
            valor_turno = str(formulario.turno or "").strip().lower()
            valor_estado = (formulario.estado or "").strip().lower()
            valor_fecha = self._coerce_fecha(formulario.fecha_formulario)

            if identificador and identificador not in valor_identificador:
                continue

            if operario and operario not in valor_operario:
                continue

            if cod_setor and cod_setor != valor_cod_setor:
                continue

            if cod_recurso and cod_recurso != valor_cod_recurso:
                continue

            if turno and turno != valor_turno:
                continue

            if estado and estado != valor_estado:
                continue

            if fecha_desde is not None:
                if valor_fecha is None or valor_fecha.date() < fecha_desde:
                    continue

            if fecha_hasta is not None:
                if valor_fecha is None or valor_fecha.date() > fecha_hasta:
                    continue

            filtrados.append(formulario)

        return filtrados

    # Bloque CDLform: funcion/metodo _cambiar_uso_fecha_desde; encapsula una operacion del flujo del modulo.
    def _cambiar_uso_fecha_desde(self, checked: bool) -> None:
        self.input_fecha_desde.setEnabled(checked)
        self.cargar_reporte_desde_inicio()

    # Bloque CDLform: funcion/metodo _cambiar_uso_fecha_hasta; encapsula una operacion del flujo del modulo.
    def _cambiar_uso_fecha_hasta(self, checked: bool) -> None:
        self.input_fecha_hasta.setEnabled(checked)
        self.cargar_reporte_desde_inicio()

    # Bloque CDLform: funcion/metodo _coerce_fecha; encapsula una operacion del flujo del modulo.
    def _coerce_fecha(self, valor) -> datetime | None:
        texto = str(valor or "").strip()
        if not texto:
            return None

        candidatos = [
            texto,
            texto.replace("Z", "+00:00"),
            texto.replace(" ", "T"),
        ]
        for candidato in candidatos:
            try:
                return datetime.fromisoformat(candidato)
            except ValueError:
                continue

        formatos = (
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M",
        )
        for formato in formatos:
            try:
                return datetime.strptime(texto, formato)
            except ValueError:
                continue

        return None

    # Bloque CDLform: funcion/metodo _ordenar_formularios; encapsula una operacion del flujo del modulo.
    def _ordenar_formularios(self, formularios: list[Formulario]) -> None:
        formularios.sort(
            key=lambda formulario: (
                formulario.fecha_formulario or "",
                formulario.id_formulario or "",
            ),
            reverse=True,
        )

    # Bloque CDLform: funcion/metodo _cargar_tabla; encapsula una operacion del flujo del modulo.
    def _cargar_tabla(self, formularios: list[Formulario]) -> None:
        self.tabla_reportes.setRowCount(0)

        for formulario in formularios:
            row = self.tabla_reportes.rowCount()
            self.tabla_reportes.insertRow(row)

            self._set_item(row, 0, formulario.id_formulario, formulario.id_formulario)
            self._set_item(row, 1, formulario.identificador)
            self._set_item(row, 2, formulario.operario)
            self._set_item(row, 3, self._obtener_cod_setor(formulario))
            self._set_item(row, 4, self._obtener_cod_recurso(formulario))
            self._set_item(row, 5, formulario.turno)
            self._set_item(
                row,
                6,
                self.reporte_service.resolver_version_plantilla_formulario(
                    formulario
                ),
            )
            self._set_item(row, 7, formulario.estado)
            self._set_item(row, 8, formulario.fecha_formulario)

    # Bloque CDLform: funcion/metodo _obtener_cod_setor; encapsula una operacion del flujo del modulo.
    def _obtener_cod_setor(self, formulario: Formulario) -> str:
        return str(formulario.cod_setor or formulario.area or "").strip()

    # Bloque CDLform: funcion/metodo _obtener_cod_recurso; encapsula una operacion del flujo del modulo.
    def _obtener_cod_recurso(self, formulario: Formulario) -> str:
        return str(formulario.cod_recurso or formulario.maquina or "").strip()

    # Bloque CDLform: funcion/metodo _obtener_id_formulario_seleccionado; encapsula una operacion del flujo del modulo.
    def _obtener_id_formulario_seleccionado(self) -> str:
        fila = self.tabla_reportes.currentRow()
        if fila < 0:
            return ""

        item = self.tabla_reportes.item(fila, 0)
        if item is None:
            return ""

        return str(item.data(Qt.UserRole) or item.text()).strip()

    # Bloque CDLform: funcion/metodo abrir_detalle; encapsula una operacion del flujo del modulo.
    def abrir_detalle(self, *_args) -> None:
        id_formulario = self._obtener_id_formulario_seleccionado()
        if not id_formulario:
            QMessageBox.information(
                self,
                "Reportes",
                "Selecciona un formulario para ver el detalle.",
            )
            return

        formulario = self.reporte_service.obtener_formulario(id_formulario)
        if not formulario:
            QMessageBox.warning(
                self,
                "Reportes",
                "No se encontró el formulario seleccionado.",
            )
            return

        dialogo = DetalleFormularioView(
            formulario=formulario,
            reporte_service=self.reporte_service,
            parent=self,
        )
        dialogo.exec_()

    # Bloque CDLform: funcion/metodo _set_item; encapsula una operacion del flujo del modulo.
    def _set_item(
        self,
        row: int,
        column: int,
        value,
        user_data=None,
    ) -> None:
        texto = "" if value is None else str(value)
        item = QTableWidgetItem(texto)
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        if user_data is not None:
            item.setData(Qt.UserRole, user_data)

        self.tabla_reportes.setItem(row, column, item)
