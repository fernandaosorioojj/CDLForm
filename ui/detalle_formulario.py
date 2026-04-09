from __future__ import annotations

from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from models.formulario import Formulario
from services.pregunta_service import PreguntaService
from services.reporte_service import ReporteService


class DetalleFormularioView(QDialog):
    def __init__(
        self,
        formulario: Formulario,
        reporte_service: ReporteService | None = None,
        pregunta_service: PreguntaService | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.formulario = formulario
        self.reporte_service = reporte_service or ReporteService()
        self.pregunta_service = pregunta_service or PreguntaService()

        self.setWindowTitle(f"Detalle Formulario - {self.formulario.id_formulario}")
        self.resize(960, 640)

        self._configurar_ui()
        self._cargar_respuestas()

    def _configurar_ui(self) -> None:
        layout = QVBoxLayout(self)

        titulo = QLabel(f"Detalle del formulario {self.formulario.id_formulario}")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        info = QFormLayout()
        info.addRow("ID Formulario:", QLabel(self.formulario.id_formulario))
        info.addRow("OP:", QLabel(self.formulario.identificador))
        info.addRow("IdApontamento:", QLabel(self.formulario.id_apontamento))
        info.addRow("Fecha:", QLabel(self.formulario.fecha_formulario))
        info.addRow("Operario:", QLabel(self.formulario.operario or "-"))
        info.addRow("Área:", QLabel(self.formulario.area or "-"))
        info.addRow("Máquina:", QLabel(self.formulario.maquina or "-"))
        info.addRow("Estado:", QLabel(self.formulario.estado or "-"))
        info.addRow("Descripción OP:", QLabel(self.formulario.descripcion_op or "-"))
        info.addRow(
            "Descripción proceso:",
            QLabel(self.formulario.descripcion_proceso or "-"),
        )
        info.addRow(
            "Observación general:",
            QLabel(self.formulario.observacion_general or "-"),
        )
        layout.addLayout(info)

        self.tabla_respuestas = QTableWidget()
        self.tabla_respuestas.setColumnCount(4)
        self.tabla_respuestas.setHorizontalHeaderLabels(
            [
                "ID Pregunta",
                "Pregunta",
                "Respuesta",
                "Opción",
            ]
        )
        self.tabla_respuestas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_respuestas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_respuestas.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.tabla_respuestas)

    def _valor_respuesta(self, respuesta: Any, clave: str, default: Any = None) -> Any:
        if isinstance(respuesta, dict):
            return respuesta.get(clave, default)
        return getattr(respuesta, clave, default)

    def _resolver_texto_pregunta(self, id_pregunta: str) -> str:
        id_pregunta = str(id_pregunta).strip()
        if not id_pregunta:
            return "-"

        metodos_directos = [
            "obtener_pregunta_por_id",
            "obtener_pregunta",
        ]

        for nombre in metodos_directos:
            metodo = getattr(self.pregunta_service, nombre, None)
            if callable(metodo):
                try:
                    pregunta = metodo(id_pregunta)
                except Exception:
                    pregunta = None

                if pregunta:
                    if isinstance(pregunta, dict):
                        return str(
                            pregunta.get("texto")
                            or pregunta.get("pregunta")
                            or pregunta.get("enunciado")
                            or id_pregunta
                        ).strip()
                    return str(
                        getattr(pregunta, "texto", "")
                        or getattr(pregunta, "pregunta", "")
                        or getattr(pregunta, "enunciado", "")
                        or id_pregunta
                    ).strip()

        metodo_listar = getattr(self.pregunta_service, "listar_preguntas", None)
        if callable(metodo_listar):
            try:
                preguntas = metodo_listar(solo_activas=False)
            except TypeError:
                preguntas = metodo_listar()
            except Exception:
                preguntas = []

            for pregunta in preguntas:
                if isinstance(pregunta, dict):
                    if str(pregunta.get("id_pregunta", "")).strip() == id_pregunta:
                        return str(
                            pregunta.get("texto")
                            or pregunta.get("pregunta")
                            or pregunta.get("enunciado")
                            or id_pregunta
                        ).strip()

        return id_pregunta

    def _formatear_respuesta(self, respuesta: Any) -> str:
        respuesta_texto = self._valor_respuesta(respuesta, "respuesta_texto")
        respuesta_numero = self._valor_respuesta(respuesta, "respuesta_numero")

        if respuesta_texto not in (None, ""):
            return str(respuesta_texto).strip()

        if respuesta_numero not in (None, ""):
            return str(respuesta_numero).strip()

        return "-"

    def _cargar_respuestas(self) -> None:
        respuestas = self.reporte_service.obtener_respuestas_de_formulario(
            self.formulario.id_formulario
        )

        self.tabla_respuestas.setRowCount(len(respuestas))

        for fila, respuesta in enumerate(respuestas):
            id_pregunta = str(self._valor_respuesta(respuesta, "id_pregunta", "")).strip()
            texto_pregunta = self._resolver_texto_pregunta(id_pregunta)
            texto_respuesta = self._formatear_respuesta(respuesta)
            id_opcion = str(self._valor_respuesta(respuesta, "id_opcion", "") or "").strip()

            self.tabla_respuestas.setItem(fila, 0, QTableWidgetItem(id_pregunta or "-"))
            self.tabla_respuestas.setItem(fila, 1, QTableWidgetItem(texto_pregunta or "-"))
            self.tabla_respuestas.setItem(fila, 2, QTableWidgetItem(texto_respuesta or "-"))
            self.tabla_respuestas.setItem(fila, 3, QTableWidgetItem(id_opcion or "-"))

        self.tabla_respuestas.resizeColumnsToContents()