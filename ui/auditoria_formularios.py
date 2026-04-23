from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from models.plantilla_preguntas import PlantillaPreguntas
from services.forms.plantilla_preguntas_service import PlantillaPreguntasService
from styles.common import apply_view_style
from ui.detalle_plantilla_preguntas import DetallePlantillaPreguntasView


class AuditoriaFormulariosView(QWidget):
    registros_por_pagina = 100
    qss_files = ("base.qss", "auditoria_formularios.qss")

    def __init__(
        self,
        plantilla_service: PlantillaPreguntasService | None = None,
    ) -> None:
        super().__init__()

        self.plantilla_service = plantilla_service or PlantillaPreguntasService()
        self.plantillas: list[PlantillaPreguntas] = []
        self.plantillas_filtradas: list[PlantillaPreguntas] = []
        self.pagina_actual = 0

        self.setWindowTitle("Auditoria de Plantillas")
        self.setObjectName("auditoriaFormulariosView")
        self.resize(1400, 820)

        self._init_ui()
        apply_view_style(self, *self.qss_files)
        self.cargar_plantillas()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(16)

        top_panel = QFrame()
        top_panel.setObjectName("auditoriaTopPanel")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(18, 18, 18, 18)
        top_layout.setSpacing(14)

        header_panel = QFrame()
        header_panel.setObjectName("auditoriaHeader")
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(22, 20, 22, 20)
        header_layout.setSpacing(6)

        eyebrow = QLabel("Gestion")
        eyebrow.setProperty("role", "eyebrow")

        titulo = QLabel("Auditoria de Plantillas")
        titulo.setProperty("role", "title")

        subtitulo = QLabel(
            "Consulta todas las versiones de conjuntos de preguntas por recurso y setor."
        )
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        header_layout.addWidget(eyebrow)
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        top_layout.addWidget(header_panel)

        panel_filtros = QFrame()
        panel_filtros.setProperty("card", "true")
        layout_filtros = QVBoxLayout(panel_filtros)
        layout_filtros.setContentsMargins(14, 12, 14, 12)
        layout_filtros.setSpacing(8)

        fila_filtros = QHBoxLayout()
        fila_filtros.setSpacing(10)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText(
            "Buscar plantilla, recurso, setor o version..."
        )
        self.input_busqueda.textChanged.connect(self.cargar_plantillas_desde_inicio)

        self.combo_estado = QComboBox()
        self.combo_estado.addItem("Estado: Todos", "")
        self.combo_estado.addItem("Activas", "activa")
        self.combo_estado.addItem("Historicas", "historica")
        self.combo_estado.currentIndexChanged.connect(self.cargar_plantillas_desde_inicio)

        self.btn_ver_detalle = QPushButton("Ver detalle")
        self.btn_ver_detalle.clicked.connect(self.abrir_detalle)

        self.btn_recargar = QPushButton("Recargar")
        self.btn_recargar.setProperty("variant", "secondary")
        self.btn_recargar.clicked.connect(self.cargar_plantillas)

        fila_filtros.addWidget(self.input_busqueda, 1)
        fila_filtros.addWidget(self.combo_estado)
        fila_filtros.addWidget(self.btn_ver_detalle)
        fila_filtros.addWidget(self.btn_recargar)

        layout_filtros.addLayout(fila_filtros)
        top_layout.addWidget(panel_filtros)
        layout_principal.addWidget(top_panel)

        panel_tabla = QFrame()
        panel_tabla.setProperty("card", "true")
        layout_tabla = QVBoxLayout(panel_tabla)
        layout_tabla.setContentsMargins(18, 18, 18, 18)
        layout_tabla.setSpacing(12)

        self.tabla_plantillas = QTableWidget()
        self.tabla_plantillas.setColumnCount(8)
        self.tabla_plantillas.setHorizontalHeaderLabels(
            [
                "Plantilla",
                "Version",
                "CodSetor",
                "CodRecurso",
                "Preguntas",
                "Estado",
                "Creada",
                "Desactivada",
            ]
        )
        self.tabla_plantillas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_plantillas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_plantillas.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_plantillas.verticalHeader().setVisible(False)
        self.tabla_plantillas.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tabla_plantillas.horizontalHeader().setStretchLastSection(True)
        self.tabla_plantillas.doubleClicked.connect(self.abrir_detalle)

        layout_tabla.addWidget(self.tabla_plantillas)

        fila_paginacion = QHBoxLayout()
        fila_paginacion.setSpacing(10)

        self.label_total = QLabel("Total versiones: 0")
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

    def cargar_plantillas_desde_inicio(self, *_args) -> None:
        self.pagina_actual = 0
        self.cargar_plantillas()

    def cargar_plantillas(self, *_args) -> None:
        try:
            self.plantillas = self.plantilla_service.repository.listar_plantillas()
            self.plantillas_filtradas = self._filtrar_plantillas(self.plantillas)
            self.plantillas_filtradas.sort(
                key=lambda plantilla: (
                    plantilla.clave_plantilla,
                    plantilla.version,
                ),
                reverse=True,
            )
            self.pagina_actual = min(self.pagina_actual, self._total_paginas() - 1)
            self._cargar_tabla(self._obtener_plantillas_pagina())
            self._actualizar_paginacion()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def _obtener_plantillas_pagina(self) -> list[PlantillaPreguntas]:
        inicio = self.pagina_actual * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina
        return self.plantillas_filtradas[inicio:fin]

    def _total_paginas(self) -> int:
        total = len(self.plantillas_filtradas)
        if total == 0:
            return 1
        return (total - 1) // self.registros_por_pagina + 1

    def _actualizar_paginacion(self) -> None:
        total = len(self.plantillas_filtradas)
        if total == 0:
            self.label_total.setText("Total versiones: 0")
            self.btn_anterior.setEnabled(False)
            self.btn_siguiente.setEnabled(False)
            return

        inicio = self.pagina_actual * self.registros_por_pagina + 1
        fin = min(inicio + self.registros_por_pagina - 1, total)
        self.label_total.setText(f"Versiones {inicio}-{fin} de {total}")
        self.btn_anterior.setEnabled(self.pagina_actual > 0)
        self.btn_siguiente.setEnabled(self.pagina_actual < self._total_paginas() - 1)

    def pagina_anterior(self) -> None:
        if self.pagina_actual <= 0:
            return
        self.pagina_actual -= 1
        self._cargar_tabla(self._obtener_plantillas_pagina())
        self._actualizar_paginacion()

    def pagina_siguiente(self) -> None:
        if self.pagina_actual >= self._total_paginas() - 1:
            return
        self.pagina_actual += 1
        self._cargar_tabla(self._obtener_plantillas_pagina())
        self._actualizar_paginacion()

    def _filtrar_plantillas(
        self,
        plantillas: list[PlantillaPreguntas],
    ) -> list[PlantillaPreguntas]:
        busqueda = self.input_busqueda.text().strip().lower()
        estado = str(self.combo_estado.currentData() or "").strip()

        resultado: list[PlantillaPreguntas] = []
        for plantilla in plantillas:
            if estado == "activa" and not plantilla.activa:
                continue
            if estado == "historica" and plantilla.activa:
                continue

            texto_busqueda = " ".join(
                [
                    plantilla.clave_plantilla,
                    plantilla.id_plantilla,
                    plantilla.cod_setor,
                    plantilla.cod_recurso,
                    str(plantilla.version),
                ]
            ).lower()
            if busqueda and busqueda not in texto_busqueda:
                continue

            resultado.append(plantilla)

        return resultado

    def _cargar_tabla(self, plantillas: list[PlantillaPreguntas]) -> None:
        self.tabla_plantillas.setRowCount(0)

        for plantilla in plantillas:
            row = self.tabla_plantillas.rowCount()
            self.tabla_plantillas.insertRow(row)

            self._set_item(row, 0, plantilla.clave_plantilla, plantilla.id_plantilla)
            self._set_item(row, 1, plantilla.version)
            self._set_item(row, 2, plantilla.cod_setor)
            self._set_item(row, 3, plantilla.cod_recurso)
            self._set_item(row, 4, len(plantilla.items))
            self._set_item(row, 5, "Activa" if plantilla.activa else "Historica")
            self._set_item(row, 6, plantilla.fecha_creacion or "-")
            self._set_item(row, 7, plantilla.fecha_desactivacion or "-")

    def abrir_detalle(self, *_args) -> None:
        id_plantilla = self._obtener_id_plantilla_seleccionada()
        if not id_plantilla:
            QMessageBox.information(
                self,
                "Auditoria",
                "Selecciona una version de plantilla para ver el detalle.",
            )
            return

        plantilla = self.plantilla_service.repository.obtener_por_id(id_plantilla)
        if not plantilla:
            QMessageBox.warning(
                self,
                "Auditoria",
                "No se encontro la plantilla seleccionada.",
            )
            return

        dialogo = DetallePlantillaPreguntasView(
            plantilla=plantilla,
            parent=self,
        )
        dialogo.exec_()

    def _obtener_id_plantilla_seleccionada(self) -> str:
        fila = self.tabla_plantillas.currentRow()
        if fila < 0:
            return ""

        item = self.tabla_plantillas.item(fila, 0)
        if item is None:
            return ""

        return str(item.data(Qt.UserRole) or "").strip()

    def _set_item(
        self,
        row: int,
        column: int,
        value,
        user_data=None,
    ) -> None:
        item = QTableWidgetItem("" if value is None else str(value))
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if column in {1, 4}:
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if user_data is not None:
            item.setData(Qt.UserRole, user_data)

        self.tabla_plantillas.setItem(row, column, item)
