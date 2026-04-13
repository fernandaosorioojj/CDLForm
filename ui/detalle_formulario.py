from __future__ import annotations

from typing import Any

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

from models.formulario import Formulario
from services.forms.pregunta_service import PreguntaService
from services.reporting.reporte_service import ReporteService
from styles.common import apply_view_style


class DetalleFormularioView(QDialog):
    qss_files = ("base.qss", "dialogs.qss", "detalle_formulario.qss")

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
        self.setObjectName("detalleFormularioView")
        self.resize(960, 640)

        self._configurar_ui()
        apply_view_style(self, *self.qss_files)
        self._cargar_respuestas()

    def _configurar_ui(self) -> None:
        layout = QVBoxLayout(self)

        titulo = QLabel(f"Detalle del formulario {self.formulario.id_formulario}")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setProperty("role", "title")
        layout.addWidget(titulo)

        caja_info = QFrame()
        caja_info.setProperty("card", "true")
        info = QGridLayout(caja_info)
        info.setContentsMargins(18, 14, 18, 14)
        info.setHorizontalSpacing(12)
        info.setVerticalSpacing(8)
        metadata_plantilla = self.reporte_service.obtener_metadata_plantilla_formulario(
            self.formulario
        )
        self._agregar_campo_info(info, 0, 0, "ID Formulario", self.formulario.id_formulario)
        self._agregar_campo_info(info, 0, 2, "OP", self.formulario.identificador)
        self._agregar_campo_info(info, 1, 0, "IdApontamento", self.formulario.id_apontamento)
        self._agregar_campo_info(info, 1, 2, "Fecha", self.formulario.fecha_formulario)
        self._agregar_campo_info(info, 2, 0, "Operario", self.formulario.operario or "-")
        self._agregar_campo_info(info, 2, 2, "Estado", self.formulario.estado or "-")
        self._agregar_campo_info(info, 3, 0, "Área", self.formulario.area or "-")
        self._agregar_campo_info(info, 3, 2, "Máquina", self.formulario.maquina or "-")
        self._agregar_campo_info(
            info,
            4,
            0,
            "Plantilla",
            str(metadata_plantilla.get("clave_plantilla") or "-"),
        )
        self._agregar_campo_info(
            info,
            4,
            2,
            "Versión",
            self.reporte_service.resolver_version_plantilla_formulario(
                self.formulario
            ),
        )
        self._agregar_campo_info(
            info,
            5,
            0,
            "Estado plantilla",
                "Activa actualmente"
                if metadata_plantilla.get("activa")
                else "Histórica",
        )
        self._agregar_campo_info(
            info,
            5,
            2,
            "Observación",
            self.formulario.observacion_general or "-",
        )
        layout.addWidget(caja_info)

        self.tabla_respuestas = QTableWidget()
        self.tabla_respuestas.setColumnCount(9)
        self.tabla_respuestas.setHorizontalHeaderLabels(
            [
                "ID Pregunta",
                "Pregunta",
                "Versión",
                "Estado actual",
                "Respuesta",
                "Opción",
                "Texto opción",
                "Opciones disponibles",
                "Acción correctiva",
            ]
        )
        self.tabla_respuestas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_respuestas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_respuestas.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.tabla_respuestas)

    @staticmethod
    def _agregar_campo_info(
        layout: QGridLayout,
        fila: int,
        columna: int,
        etiqueta: str,
        valor: Any,
    ) -> None:
        label = QLabel(f"{etiqueta}:")
        label.setProperty("role", "field-label")
        value_label = QLabel(str(valor))
        value_label.setProperty("role", "field-value")
        value_label.setWordWrap(True)
        layout.addWidget(label, fila, columna)
        layout.addWidget(value_label, fila, columna + 1)

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
        respuestas = self.reporte_service.obtener_detalle_auditoria_formulario(
            self.formulario
        )

        self.tabla_respuestas.setRowCount(len(respuestas))

        for fila, respuesta in enumerate(respuestas):
            estado_actual = (
                "Activa" if self._valor_respuesta(respuesta, "pregunta_activa") else "Historial"
            )

            self.tabla_respuestas.setItem(
                fila,
                0,
                QTableWidgetItem(str(self._valor_respuesta(respuesta, "id_pregunta", "-"))),
            )
            self.tabla_respuestas.setItem(
                fila,
                1,
                QTableWidgetItem(str(self._valor_respuesta(respuesta, "pregunta", "-"))),
            )
            self.tabla_respuestas.setItem(
                fila,
                2,
                QTableWidgetItem(str(self._valor_respuesta(respuesta, "version_pregunta", "-"))),
            )
            self.tabla_respuestas.setItem(fila, 3, QTableWidgetItem(estado_actual))
            self.tabla_respuestas.setItem(
                fila,
                4,
                QTableWidgetItem(str(self._valor_respuesta(respuesta, "respuesta", "-"))),
            )
            self.tabla_respuestas.setItem(
                fila,
                5,
                QTableWidgetItem(str(self._valor_respuesta(respuesta, "id_opcion", "-") or "-")),
            )
            self.tabla_respuestas.setItem(
                fila,
                6,
                QTableWidgetItem(str(self._valor_respuesta(respuesta, "opcion", "-") or "-")),
            )
            self.tabla_respuestas.setItem(
                fila,
                7,
                QTableWidgetItem(
                    str(self._valor_respuesta(respuesta, "opciones_disponibles", "-") or "-")
                ),
            )
            self.tabla_respuestas.setItem(
                fila,
                8,
                QTableWidgetItem(
                    str(self._valor_respuesta(respuesta, "accion_correctiva", "-") or "-")
                ),
            )

        self.tabla_respuestas.resizeColumnsToContents()
