from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from models.plantilla_preguntas import PlantillaPreguntas
from services.forms.pregunta_service import PreguntaService
from styles.common import apply_view_style


class DetallePlantillaPreguntasView(QDialog):
    qss_files = ("base.qss", "dialogs.qss", "detalle_plantilla_preguntas.qss")

    def __init__(
        self,
        plantilla: PlantillaPreguntas,
        pregunta_service: PreguntaService | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.plantilla = plantilla
        self.pregunta_service = pregunta_service or PreguntaService()

        self.setWindowTitle(
            f"Detalle plantilla {self.plantilla.clave_plantilla} v{self.plantilla.version}"
        )
        self.setObjectName("detallePlantillaPreguntasView")
        self.resize(1100, 650)

        self._configurar_ui()
        apply_view_style(self, *self.qss_files)
        self._cargar_preguntas()

    def _configurar_ui(self) -> None:
        layout = QVBoxLayout(self)

        titulo = QLabel(
            f"{self.plantilla.clave_plantilla} - version {self.plantilla.version}"
        )
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")
        layout.addWidget(titulo)

        caja_info = QFrame()
        caja_info.setProperty("card", "true")

        info = QGridLayout(caja_info)
        info.setContentsMargins(18, 14, 18, 14)
        info.setHorizontalSpacing(12)
        info.setVerticalSpacing(8)

        self._agregar_campo_info(info, 0, 0, "ID tecnico", self.plantilla.id_plantilla)
        self._agregar_campo_info(info, 0, 2, "Version", self.plantilla.version)
        self._agregar_campo_info(info, 1, 0, "CodSetor", self.plantilla.cod_setor)
        self._agregar_campo_info(info, 1, 2, "CodRecurso", self.plantilla.cod_recurso)
        self._agregar_campo_info(
            info,
            2,
            0,
            "Estado",
            "Activa" if self.plantilla.activa else "Historica",
        )
        self._agregar_campo_info(info, 2, 2, "Preguntas", len(self.plantilla.items))
        self._agregar_campo_info(
            info,
            3,
            0,
            "Creacion",
            self.plantilla.fecha_creacion or "-",
        )
        self._agregar_campo_info(
            info,
            3,
            2,
            "Desactivacion",
            self.plantilla.fecha_desactivacion or "-",
        )

        layout.addWidget(caja_info)

        self.tabla_preguntas = QTableWidget()
        self.tabla_preguntas.setColumnCount(9)
        self.tabla_preguntas.setHorizontalHeaderLabels(
            [
                "Orden",
                "ID Pregunta",
                "Version pregunta",
                "Estado en plantilla",
                "Estado actual",
                "Texto",
                "Tipo",
                "Obligatoria",
                "Opciones",
            ]
        )
        self.tabla_preguntas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_preguntas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_preguntas.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabla_preguntas)

    @staticmethod
    def _agregar_campo_info(
        layout: QGridLayout,
        fila: int,
        columna: int,
        etiqueta: str,
        valor,
    ) -> None:
        label = QLabel(f"{etiqueta}:")
        label.setProperty("role", "field-label")
        value_label = QLabel(str(valor))
        value_label.setProperty("role", "field-value")
        value_label.setWordWrap(True)
        layout.addWidget(label, fila, columna)
        layout.addWidget(value_label, fila, columna + 1)

    def _cargar_preguntas(self) -> None:
        preguntas_por_id = {
            pregunta.get("id_pregunta"): pregunta
            for pregunta in self.pregunta_service.listar_preguntas(solo_activas=False)
        }

        self.tabla_preguntas.setRowCount(len(self.plantilla.items))

        for fila, item in enumerate(self.plantilla.items):
            pregunta = preguntas_por_id.get(item.id_pregunta, {})
            self._set_item(fila, 0, item.orden)
            self._set_item(fila, 1, item.id_pregunta)
            self._set_item(fila, 2, pregunta.get("version", "-"))
            self._set_item(fila, 3, "Activa en esta plantilla")
            self._set_item(
                fila,
                4,
                "Activa actualmente" if pregunta.get("activa", False) else "Historica",
            )
            self._set_item(fila, 5, pregunta.get("texto", "-"))
            self._set_item(fila, 6, pregunta.get("tipo", "-"))
            self._set_item(
                fila,
                7,
                "Si" if pregunta.get("obligatoria", False) else "No",
            )
            self._set_item(fila, 8, self._formatear_opciones(pregunta))

        self.tabla_preguntas.resizeColumnsToContents()

    def _set_item(self, row: int, column: int, value) -> None:
        item = QTableWidgetItem("" if value is None else str(value))
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tabla_preguntas.setItem(row, column, item)

    @staticmethod
    def _formatear_opciones(pregunta: dict) -> str:
        opciones = []
        for opcion in pregunta.get("opciones_respuesta", []):
            if not isinstance(opcion, dict):
                continue
            valor = str(opcion.get("valor") or "").strip()
            accion = str(opcion.get("accion_correctiva") or "").strip()
            if accion:
                valor = f"{valor} -> {accion}"
            if valor:
                opciones.append(valor)

        return "; ".join(opciones) or "-"
