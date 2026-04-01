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
)

from services.catalogo_contexto_service import CatalogoContextoService
from services.reporte_service import ReporteService


class ReportesView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.reporte_service = ReporteService()
        self.catalogo_contexto_service = CatalogoContextoService()

        self.setWindowTitle("Reportes")
        self.resize(1500, 820)

        self._init_ui()
        self.cargar_reporte()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)

        titulo = QLabel("Reportes de Formularios")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout_principal.addWidget(titulo)

        filtros_fila_1 = QHBoxLayout()
        filtros_fila_2 = QHBoxLayout()

        self.input_identificador = QLineEdit()
        self.input_identificador.setPlaceholderText("Buscar identificador...")

        self.input_operario = QLineEdit()
        self.input_operario.setPlaceholderText("Buscar operario...")

        self.input_texto_pregunta = QLineEdit()
        self.input_texto_pregunta.setPlaceholderText("Buscar texto de pregunta...")

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

        self.combo_tipo_trabajo = QComboBox()
        self._cargar_combo_con_todos(
            self.combo_tipo_trabajo,
            self.catalogo_contexto_service.listar_tipos_trabajo(),
            "TipoTrabajo: Todos",
        )

        self.combo_estado_formulario = QComboBox()
        self.combo_estado_formulario.addItem("Estado: Todos", "")
        self.combo_estado_formulario.addItem("Pendiente", "pendiente")
        self.combo_estado_formulario.addItem("Completado", "completado")

        self.combo_con_accion_correctiva = QComboBox()
        self.combo_con_accion_correctiva.addItem("Acción correctiva: Todas", "")
        self.combo_con_accion_correctiva.addItem("Con acción correctiva", "SI")
        self.combo_con_accion_correctiva.addItem("Sin acción correctiva", "NO")

        filtros_fila_1.addWidget(self.input_identificador)
        filtros_fila_1.addWidget(self.input_operario)
        filtros_fila_1.addWidget(self.combo_cod_setor)
        filtros_fila_1.addWidget(self.combo_cod_recurso)
        filtros_fila_1.addWidget(self.combo_cod_ativ)

        filtros_fila_2.addWidget(self.combo_turno)
        filtros_fila_2.addWidget(self.combo_tipo_trabajo)
        filtros_fila_2.addWidget(self.combo_estado_formulario)
        filtros_fila_2.addWidget(self.input_texto_pregunta)
        filtros_fila_2.addWidget(self.combo_con_accion_correctiva)

        layout_principal.addLayout(filtros_fila_1)
        layout_principal.addLayout(filtros_fila_2)

        botones = QHBoxLayout()

        self.btn_limpiar = QPushButton("Limpiar filtros")
        self.btn_limpiar.clicked.connect(self.limpiar_filtros)

        botones.addStretch()
        botones.addWidget(self.btn_limpiar)

        layout_principal.addLayout(botones)

        self.tabla_reportes = QTableWidget()
        self.tabla_reportes.setColumnCount(14)
        self.tabla_reportes.setHorizontalHeaderLabels(
            [
                "Identificador",
                "Operario",
                "CodSetor",
                "CodRecurso",
                "CodAtiv",
                "Turno",
                "TipoTrabajo",
                "Estado",
                "Pregunta",
                "Tipo Pregunta",
                "Respuesta Texto",
                "Respuesta Número",
                "Id Opción",
                "Acción Correctiva",
            ]
        )
        self.tabla_reportes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_reportes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_reportes.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_reportes.verticalHeader().setVisible(False)
        self.tabla_reportes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout_principal.addWidget(self.tabla_reportes)

        self.label_total = QLabel("Total registros: 0")
        self.label_total.setAlignment(Qt.AlignRight)
        layout_principal.addWidget(self.label_total)

        self._conectar_filtros()

    def _conectar_filtros(self) -> None:
        self.input_identificador.textChanged.connect(self.cargar_reporte)
        self.input_operario.textChanged.connect(self.cargar_reporte)
        self.input_texto_pregunta.textChanged.connect(self.cargar_reporte)

        self.combo_cod_setor.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_cod_recurso.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_cod_ativ.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_turno.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_tipo_trabajo.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_estado_formulario.currentIndexChanged.connect(self.cargar_reporte)
        self.combo_con_accion_correctiva.currentIndexChanged.connect(self.cargar_reporte)

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

    def cargar_reporte(self) -> None:
        try:
            filtros = self._obtener_filtros()
            filas = self.reporte_service.generar_reporte(filtros)

            self.tabla_reportes.setRowCount(0)

            for fila in filas:
                row = self.tabla_reportes.rowCount()
                self.tabla_reportes.insertRow(row)

                self._set_item(row, 0, fila.get("identificador", ""))
                self._set_item(row, 1, fila.get("operario", ""))
                self._set_item(row, 2, fila.get("cod_setor", ""))
                self._set_item(row, 3, fila.get("cod_recurso", ""))
                self._set_item(row, 4, fila.get("cod_ativ", ""))
                self._set_item(row, 5, fila.get("turno", ""))
                self._set_item(row, 6, fila.get("tipo_trabajo", ""))
                self._set_item(row, 7, fila.get("estado_formulario", ""))
                self._set_item(row, 8, fila.get("texto_pregunta", ""))
                self._set_item(row, 9, fila.get("tipo_pregunta", ""))
                self._set_item(row, 10, self._resolver_respuesta_texto(fila))
                self._set_item(row, 11, self._resolver_respuesta_numero(fila))
                self._set_item(row, 12, fila.get("id_opcion", ""))
                self._set_item(row, 13, fila.get("accion_correctiva_aplicada", ""))

            self.label_total.setText(f"Total registros: {len(filas)}")

        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def limpiar_filtros(self) -> None:
        self.input_identificador.clear()
        self.input_operario.clear()
        self.input_texto_pregunta.clear()

        self.combo_cod_setor.setCurrentIndex(0)
        self.combo_cod_recurso.setCurrentIndex(0)
        self.combo_cod_ativ.setCurrentIndex(0)
        self.combo_turno.setCurrentIndex(0)
        self.combo_tipo_trabajo.setCurrentIndex(0)
        self.combo_estado_formulario.setCurrentIndex(0)
        self.combo_con_accion_correctiva.setCurrentIndex(0)

    def _obtener_filtros(self) -> dict:
        filtros: dict[str, str] = {}

        if self.input_identificador.text().strip():
            filtros["identificador"] = self.input_identificador.text().strip()

        if self.input_operario.text().strip():
            filtros["operario"] = self.input_operario.text().strip()

        valor_cod_setor = self.combo_cod_setor.currentData()
        if valor_cod_setor:
            filtros["cod_setor"] = valor_cod_setor

        valor_cod_recurso = self.combo_cod_recurso.currentData()
        if valor_cod_recurso:
            filtros["cod_recurso"] = valor_cod_recurso

        valor_cod_ativ = self.combo_cod_ativ.currentData()
        if valor_cod_ativ:
            filtros["cod_ativ"] = valor_cod_ativ

        valor_turno = self.combo_turno.currentData()
        if valor_turno:
            filtros["turno"] = valor_turno

        valor_tipo_trabajo = self.combo_tipo_trabajo.currentData()
        if valor_tipo_trabajo:
            filtros["tipo_trabajo"] = valor_tipo_trabajo

        valor_estado = self.combo_estado_formulario.currentData()
        if valor_estado:
            filtros["estado_formulario"] = valor_estado

        if self.input_texto_pregunta.text().strip():
            filtros["texto_pregunta"] = self.input_texto_pregunta.text().strip()

        valor_accion = self.combo_con_accion_correctiva.currentData()
        if valor_accion:
            filtros["con_accion_correctiva"] = valor_accion

        return filtros

    def _resolver_respuesta_texto(self, fila: dict) -> str:
        valor = fila.get("respuesta_texto")
        if valor is None:
            return ""
        return str(valor)

    def _resolver_respuesta_numero(self, fila: dict) -> str:
        valor = fila.get("respuesta_numero")
        if valor is None:
            return ""
        return str(valor)

    def _set_item(self, row: int, column: int, value) -> None:
        texto = "" if value is None else str(value)
        item = QTableWidgetItem(texto)
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tabla_reportes.setItem(row, column, item)