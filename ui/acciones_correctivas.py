"""Vistas PyQt que componen las pantallas de gestion y operario.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from typing import Any

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

from services.jobtrack.catalogo_contexto_service import CatalogoContextoService
from services.reporting.reporte_service import ReporteService
from styles.common import apply_view_style
from ui.detalle_formulario import DetalleFormularioView


# Bloque CDLform: clase AccionesCorrectivasView; agrupa estado y comportamiento de esta parte del flujo.
class AccionesCorrectivasView(QWidget):
    registros_por_pagina = 100
    qss_files = ("base.qss", "acciones_correctivas.qss")

    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        reporte_service: ReporteService | None = None,
        catalogo_contexto_service: CatalogoContextoService | None = None,
    ) -> None:
        super().__init__()

        self.reporte_service = reporte_service or ReporteService()
        self.catalogo_contexto_service = (
            catalogo_contexto_service or CatalogoContextoService()
        )
        self.acciones: list[dict[str, Any]] = []
        self.acciones_filtradas: list[dict[str, Any]] = []
        self.pagina_actual = 0
        self.incluir_supervisores_sql = False

        self.setWindowTitle("Acciones Correctivas")
        self.setObjectName("accionesCorrectivasView")
        self.resize(1500, 820)

        self._init_ui()
        apply_view_style(self, *self.qss_files)
        self.cargar_acciones()

    # Bloque CDLform: funcion/metodo _init_ui; encapsula una operacion del flujo del modulo.
    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 24, 24, 24)
        layout_principal.setSpacing(16)

        top_panel = QFrame()
        top_panel.setObjectName("accionesTopPanel")
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(18, 18, 18, 18)
        top_layout.setSpacing(14)

        header_panel = QFrame()
        header_panel.setObjectName("accionesHeader")
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(22, 20, 22, 20)
        header_layout.setSpacing(6)

        eyebrow = QLabel("Gestion")
        eyebrow.setProperty("role", "eyebrow")

        titulo = QLabel("Acciones Correctivas")
        titulo.setProperty("role", "title")

        subtitulo = QLabel(
            "Revisa las respuestas que generaron una indicacion correctiva."
        )
        subtitulo.setWordWrap(True)
        subtitulo.setProperty("role", "subtitle")

        header_layout.addWidget(eyebrow)
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        top_layout.addWidget(header_panel)

        panel_filtros = QFrame()
        panel_filtros.setProperty("card", "true")
        layout_filtros = QHBoxLayout(panel_filtros)
        layout_filtros.setContentsMargins(14, 12, 14, 12)
        layout_filtros.setSpacing(10)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText(
            "Buscar OP, operario, pregunta o accion..."
        )
        self.input_busqueda.textChanged.connect(self.cargar_acciones_desde_inicio)

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

        self.combo_estado = QComboBox()
        self.combo_estado.addItem("Estado: Todos", "")
        self.combo_estado.addItem("En apertura", "en_apertura")
        self.combo_estado.addItem("Pendiente operario", "pendiente_operario")
        self.combo_estado.addItem("Completado", "completado")
        self.combo_estado.addItem("Cancelado", "cancelado")

        self.btn_ver_formulario = QPushButton("Ver formulario")
        self.btn_ver_formulario.clicked.connect(self.abrir_detalle_formulario)

        self.btn_supervisores = QPushButton("Cargar supervisores")
        self.btn_supervisores.setProperty("variant", "secondary")
        self.btn_supervisores.clicked.connect(self.cargar_supervisores)

        self.btn_recargar = QPushButton("Recargar")
        self.btn_recargar.setProperty("variant", "secondary")
        self.btn_recargar.clicked.connect(self.cargar_acciones)

        layout_filtros.addWidget(self.input_busqueda, 1)
        layout_filtros.addWidget(self.combo_cod_setor)
        layout_filtros.addWidget(self.combo_cod_recurso)
        layout_filtros.addWidget(self.combo_estado)
        layout_filtros.addWidget(self.btn_ver_formulario)
        layout_filtros.addWidget(self.btn_supervisores)
        layout_filtros.addWidget(self.btn_recargar)

        self.combo_cod_setor.currentIndexChanged.connect(self.cargar_acciones_desde_inicio)
        self.combo_cod_recurso.currentIndexChanged.connect(self.cargar_acciones_desde_inicio)
        self.combo_estado.currentIndexChanged.connect(self.cargar_acciones_desde_inicio)

        top_layout.addWidget(panel_filtros)
        layout_principal.addWidget(top_panel)

        panel_tabla = QFrame()
        panel_tabla.setProperty("card", "true")
        layout_tabla = QVBoxLayout(panel_tabla)
        layout_tabla.setContentsMargins(18, 18, 18, 18)
        layout_tabla.setSpacing(12)

        self.tabla_acciones = QTableWidget()
        self.tabla_acciones.setColumnCount(12)
        self.tabla_acciones.setHorizontalHeaderLabels(
            [
                "Formulario",
                "OP",
                "Operario",
                "Supervisor",
                "CodSetor",
                "CodRecurso",
                "Fecha",
                "Estado",
                "Pregunta",
                "Respuesta",
                "Opcion",
                "Accion correctiva",
            ]
        )
        self.tabla_acciones.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_acciones.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_acciones.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_acciones.verticalHeader().setVisible(False)
        self.tabla_acciones.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tabla_acciones.horizontalHeader().setStretchLastSection(True)
        self.tabla_acciones.doubleClicked.connect(self.abrir_detalle_formulario)

        layout_tabla.addWidget(self.tabla_acciones)

        fila_paginacion = QHBoxLayout()
        fila_paginacion.setSpacing(10)

        self.label_total = QLabel("Total acciones correctivas: 0")
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

    # Bloque CDLform: funcion/metodo cargar_acciones_desde_inicio; encapsula una operacion del flujo del modulo.
    def cargar_acciones_desde_inicio(self, *_args) -> None:
        self.pagina_actual = 0
        self.cargar_acciones()

    # Bloque CDLform: funcion/metodo cargar_acciones; encapsula una operacion del flujo del modulo.
    def cargar_acciones(self, *_args) -> None:
        try:
            self.acciones = self.reporte_service.listar_acciones_correctivas(
                incluir_supervisor_sql=self.incluir_supervisores_sql,
            )
            self.acciones_filtradas = self._filtrar_acciones(self.acciones)
            self.pagina_actual = min(self.pagina_actual, self._total_paginas() - 1)
            self._cargar_tabla(self._obtener_acciones_pagina())
            self._actualizar_paginacion()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    # Bloque CDLform: funcion/metodo cargar_supervisores; encapsula una operacion del flujo del modulo.
    def cargar_supervisores(self) -> None:
        self.incluir_supervisores_sql = True
        self.cargar_acciones_desde_inicio()

    # Bloque CDLform: funcion/metodo _obtener_acciones_pagina; encapsula una operacion del flujo del modulo.
    def _obtener_acciones_pagina(self) -> list[dict[str, Any]]:
        inicio = self.pagina_actual * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina
        return self.acciones_filtradas[inicio:fin]

    # Bloque CDLform: funcion/metodo _total_paginas; encapsula una operacion del flujo del modulo.
    def _total_paginas(self) -> int:
        total = len(self.acciones_filtradas)
        if total == 0:
            return 1
        return (total - 1) // self.registros_por_pagina + 1

    # Bloque CDLform: funcion/metodo _actualizar_paginacion; encapsula una operacion del flujo del modulo.
    def _actualizar_paginacion(self) -> None:
        total = len(self.acciones_filtradas)
        if total == 0:
            self.label_total.setText("Total acciones correctivas: 0")
            self.btn_anterior.setEnabled(False)
            self.btn_siguiente.setEnabled(False)
            return

        inicio = self.pagina_actual * self.registros_por_pagina + 1
        fin = min(inicio + self.registros_por_pagina - 1, total)
        self.label_total.setText(
            f"Acciones correctivas {inicio}-{fin} de {total}"
        )
        self.btn_anterior.setEnabled(self.pagina_actual > 0)
        self.btn_siguiente.setEnabled(self.pagina_actual < self._total_paginas() - 1)

    # Bloque CDLform: funcion/metodo pagina_anterior; encapsula una operacion del flujo del modulo.
    def pagina_anterior(self) -> None:
        if self.pagina_actual <= 0:
            return
        self.pagina_actual -= 1
        self._cargar_tabla(self._obtener_acciones_pagina())
        self._actualizar_paginacion()

    # Bloque CDLform: funcion/metodo pagina_siguiente; encapsula una operacion del flujo del modulo.
    def pagina_siguiente(self) -> None:
        if self.pagina_actual >= self._total_paginas() - 1:
            return
        self.pagina_actual += 1
        self._cargar_tabla(self._obtener_acciones_pagina())
        self._actualizar_paginacion()

    # Bloque CDLform: funcion/metodo _filtrar_acciones; encapsula una operacion del flujo del modulo.
    def _filtrar_acciones(
        self,
        acciones: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        busqueda = self.input_busqueda.text().strip().lower()
        cod_setor = str(self.combo_cod_setor.currentData() or "").strip().lower()
        cod_recurso = str(self.combo_cod_recurso.currentData() or "").strip().lower()
        estado = str(self.combo_estado.currentData() or "").strip().lower()

        filtradas: list[dict[str, Any]] = []
        for accion in acciones:
            texto_busqueda = " ".join(
                [
                    str(accion.get("id_formulario") or ""),
                    str(accion.get("identificador") or ""),
                    str(accion.get("id_apontamento") or ""),
                    str(accion.get("operario") or ""),
                    str(accion.get("supervisor") or ""),
                    str(accion.get("pregunta") or ""),
                    str(accion.get("respuesta") or ""),
                    str(accion.get("opcion") or ""),
                    str(accion.get("accion_correctiva") or ""),
                ]
            ).lower()

            if busqueda and busqueda not in texto_busqueda:
                continue

            if cod_setor and cod_setor != str(accion.get("cod_setor") or "").lower():
                continue

            if cod_recurso and cod_recurso != str(
                accion.get("cod_recurso") or ""
            ).lower():
                continue

            if estado and estado != str(accion.get("estado") or "").lower():
                continue

            filtradas.append(accion)

        return filtradas

    # Bloque CDLform: funcion/metodo _cargar_tabla; encapsula una operacion del flujo del modulo.
    def _cargar_tabla(self, acciones: list[dict[str, Any]]) -> None:
        self.tabla_acciones.setRowCount(0)

        for accion in acciones:
            row = self.tabla_acciones.rowCount()
            self.tabla_acciones.insertRow(row)

            self._set_item(row, 0, accion.get("id_formulario"), accion)
            self._set_item(row, 1, accion.get("identificador"))
            self._set_item(row, 2, accion.get("operario"))
            self._set_item(row, 3, accion.get("supervisor"))
            self._set_item(row, 4, accion.get("cod_setor"))
            self._set_item(row, 5, accion.get("cod_recurso"))
            self._set_item(row, 6, accion.get("fecha_formulario"))
            self._set_item(row, 7, accion.get("estado"))
            self._set_item(row, 8, accion.get("pregunta"))
            self._set_item(row, 9, accion.get("respuesta"))
            self._set_item(row, 10, accion.get("opcion") or accion.get("id_opcion"))
            self._set_item(row, 11, accion.get("accion_correctiva"))

    # Bloque CDLform: funcion/metodo _obtener_accion_seleccionada; encapsula una operacion del flujo del modulo.
    def _obtener_accion_seleccionada(self) -> dict[str, Any] | None:
        fila = self.tabla_acciones.currentRow()
        if fila < 0:
            return None

        item = self.tabla_acciones.item(fila, 0)
        if item is None:
            return None

        accion = item.data(Qt.UserRole)
        return accion if isinstance(accion, dict) else None

    # Bloque CDLform: funcion/metodo abrir_detalle_formulario; encapsula una operacion del flujo del modulo.
    def abrir_detalle_formulario(self, *_args) -> None:
        accion = self._obtener_accion_seleccionada()
        if not accion:
            QMessageBox.information(
                self,
                "Acciones correctivas",
                "Selecciona una accion correctiva para abrir el formulario.",
            )
            return

        id_formulario = str(accion.get("id_formulario") or "").strip()
        formulario = self.reporte_service.obtener_formulario(id_formulario)
        if not formulario:
            QMessageBox.warning(
                self,
                "Acciones correctivas",
                "No se encontro el formulario asociado.",
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

        self.tabla_acciones.setItem(row, column, item)
