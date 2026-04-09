from __future__ import annotations

from PyQt5.QtCore import Qt
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
)

from models.formulario import Formulario
from services.catalogo_contexto_service import CatalogoContextoService
from services.reporte_service import ReporteService
from ui.detalle_formulario import DetalleFormularioView


class ReportesView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.reporte_service = ReporteService()
        self.catalogo_contexto_service = CatalogoContextoService()

        self.formularios: list[Formulario] = []
        self.formularios_filtrados: list[Formulario] = []

        self.setWindowTitle("Reportes")
        self.resize(1500, 820)

        self._init_ui()
        self.cargar_reporte()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(16)

        titulo = QLabel("Reportes de Formularios")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")

        subtitulo = QLabel(
            "Consulta los formularios registrados y abre el detalle para revisar respuestas."
        )
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        panel_filtros = QFrame()
        panel_filtros.setProperty("card", "true")

        layout_filtros = QVBoxLayout(panel_filtros)
        layout_filtros.setContentsMargins(18, 18, 18, 18)
        layout_filtros.setSpacing(12)

        label_filtros = QLabel("Filtros")
        label_filtros.setProperty("role", "section")
        layout_filtros.addWidget(label_filtros)

        filtros_fila_1 = QHBoxLayout()
        filtros_fila_1.setSpacing(10)

        filtros_fila_2 = QHBoxLayout()
        filtros_fila_2.setSpacing(10)

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

        self.combo_cod_ativ = QComboBox()
        self._cargar_combo_con_todos(
            self.combo_cod_ativ,
            self.catalogo_contexto_service.listar_cod_ativ(),
            "CodAtiv: Todos",
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

        filtros_fila_1.addWidget(self.input_identificador)
        filtros_fila_1.addWidget(self.input_operario)
        filtros_fila_1.addWidget(self.combo_cod_setor)
        filtros_fila_1.addWidget(self.combo_cod_recurso)

        filtros_fila_2.addWidget(self.combo_cod_ativ)
        filtros_fila_2.addWidget(self.combo_turno)
        filtros_fila_2.addWidget(self.combo_estado_formulario)

        layout_filtros.addLayout(filtros_fila_1)
        layout_filtros.addLayout(filtros_fila_2)

        botones = QHBoxLayout()
        botones.setSpacing(10)

        self.btn_recargar = QPushButton("Recargar")
        self.btn_recargar.clicked.connect(self.cargar_reporte)

        self.btn_ver_detalle = QPushButton("Ver detalle")
        self.btn_ver_detalle.clicked.connect(self.abrir_detalle)

        self.btn_limpiar = QPushButton("Limpiar filtros")
        self.btn_limpiar.setProperty("variant", "secondary")
        self.btn_limpiar.clicked.connect(self.limpiar_filtros)

        botones.addStretch()
        botones.addWidget(self.btn_recargar)
        botones.addWidget(self.btn_ver_detalle)
        botones.addWidget(self.btn_limpiar)

        layout_filtros.addLayout(botones)
        layout_principal.addWidget(panel_filtros)

        panel_tabla = QFrame()
        panel_tabla.setProperty("card", "true")

        layout_tabla = QVBoxLayout(panel_tabla)
        layout_tabla.setContentsMargins(18, 18, 18, 18)
        layout_tabla.setSpacing(12)

        label_resultados = QLabel("Resultados")
        label_resultados.setProperty("role", "section")
        layout_tabla.addWidget(label_resultados)

        self.tabla_reportes = QTableWidget()
        self.tabla_reportes.setColumnCount(9)
        self.tabla_reportes.setHorizontalHeaderLabels(
            [
                "ID Formulario",
                "Identificador",
                "Operario",
                "CodSetor",
                "CodRecurso",
                "CodAtiv",
                "Turno",
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

        layout_tabla.addWidget(self.tabla_reportes)

        self.label_total = QLabel("Total formularios: 0")
        self.label_total.setAlignment(Qt.AlignRight)
        self.label_total.setProperty("role", "subtitle")
        layout_tabla.addWidget(self.label_total)

        layout_principal.addWidget(panel_tabla, 1)

        self._conectar_filtros()

    def _conectar_filtros(self) -> None:
        self.input_identificador.textChanged.connect(self.cargar_reporte)
        self.input_operario.textChanged.connect(self.cargar_reporte)
        self.combo_cod_setor.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_cod_recurso.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_cod_ativ.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_turno.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_estado_formulario.currentIndexChanged.connect(self.cargar_reporte)

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

    def cargar_reporte(self, *_args) -> None:
        try:
            self.formularios = self.reporte_service.listar_formularios()
            self.formularios_filtrados = self._filtrar_formularios(self.formularios)
            self._ordenar_formularios(self.formularios_filtrados)
            self._cargar_tabla(self.formularios_filtrados)
            self.label_total.setText(
                f"Total formularios: {len(self.formularios_filtrados)}"
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def limpiar_filtros(self) -> None:
        self.input_identificador.clear()
        self.input_operario.clear()

        self.combo_cod_setor.setCurrentIndex(0)
        self.combo_cod_recurso.setCurrentIndex(0)
        self.combo_cod_ativ.setCurrentIndex(0)
        self.combo_turno.setCurrentIndex(0)
        self.combo_estado_formulario.setCurrentIndex(0)

        self.cargar_reporte()

    def _filtrar_formularios(
        self,
        formularios: list[Formulario],
    ) -> list[Formulario]:
        identificador = self.input_identificador.text().strip().lower()
        operario = self.input_operario.text().strip().lower()

        cod_setor = str(self.combo_cod_setor.currentData() or "").strip().lower()
        cod_recurso = str(self.combo_cod_recurso.currentData() or "").strip().lower()
        cod_ativ = str(self.combo_cod_ativ.currentData() or "").strip().lower()
        turno = str(self.combo_turno.currentData() or "").strip().lower()
        estado = str(self.combo_estado_formulario.currentData() or "").strip().lower()

        filtrados: list[Formulario] = []

        for formulario in formularios:
            valor_identificador = (formulario.identificador or "").strip().lower()
            valor_operario = (formulario.operario or "").strip().lower()
            valor_cod_setor = self._obtener_cod_setor(formulario).lower()
            valor_cod_recurso = self._obtener_cod_recurso(formulario).lower()
            valor_cod_ativ = str(formulario.cod_ativ or "").strip().lower()
            valor_turno = str(formulario.turno or "").strip().lower()
            valor_estado = (formulario.estado or "").strip().lower()

            if identificador and identificador not in valor_identificador:
                continue

            if operario and operario not in valor_operario:
                continue

            if cod_setor and cod_setor != valor_cod_setor:
                continue

            if cod_recurso and cod_recurso != valor_cod_recurso:
                continue

            if cod_ativ and cod_ativ != valor_cod_ativ:
                continue

            if turno and turno != valor_turno:
                continue

            if estado and estado != valor_estado:
                continue

            filtrados.append(formulario)

        return filtrados

    def _ordenar_formularios(self, formularios: list[Formulario]) -> None:
        formularios.sort(
            key=lambda formulario: (
                formulario.fecha_formulario or "",
                formulario.id_formulario or "",
            ),
            reverse=True,
        )

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
            self._set_item(row, 5, formulario.cod_ativ)
            self._set_item(row, 6, formulario.turno)
            self._set_item(row, 7, formulario.estado)
            self._set_item(row, 8, formulario.fecha_formulario)

    def _obtener_cod_setor(self, formulario: Formulario) -> str:
        return str(formulario.cod_setor or formulario.area or "").strip()

    def _obtener_cod_recurso(self, formulario: Formulario) -> str:
        return str(formulario.cod_recurso or formulario.maquina or "").strip()

    def _obtener_id_formulario_seleccionado(self) -> str:
        fila = self.tabla_reportes.currentRow()
        if fila < 0:
            return ""

        item = self.tabla_reportes.item(fila, 0)
        if item is None:
            return ""

        return str(item.data(Qt.UserRole) or item.text()).strip()

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