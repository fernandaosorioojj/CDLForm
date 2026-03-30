from __future__ import annotations

from typing import Optional, List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QComboBox,
    QFrame,
)

from core.exceptions import ValidationError
from services.operario_service import OperarioService
from ui.formulario_operario import FormularioOperarioView


class SeleccionOperarioView(QWidget):
    def __init__(
        self,
        op: str,
        area: str,
        maquina: str,
        evento_origen: Optional[str] = None,
    ):
        super().__init__()

        self.op = op
        self.area = area
        self.maquina = maquina
        self.evento_origen = evento_origen

        self.operario_service = OperarioService()
        self.formulario_view = None
        self.operarios = []

        self.setWindowTitle("Selección de Operario")
        self.resize(700, 350)

        self._init_ui()
        self._cargar_operarios()

    def _init_ui(self) -> None:
        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)

        contenedor = QFrame()
        contenedor_layout = QVBoxLayout(contenedor)
        contenedor_layout.setSpacing(14)

        titulo = QLabel("Selecciona el operario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_seleccion_operario")

        lbl_info = QLabel(
            f"OP: {self.op}\n"
            f"Área: {self.area}\n"
            f"Máquina: {self.maquina}"
        )
        lbl_info.setAlignment(Qt.AlignCenter)

        self.combo_operarios = QComboBox()
        self.combo_operarios.addItem("Seleccione un operario", None)

        fila_botones = QHBoxLayout()

        self.btn_continuar = QPushButton("Continuar")
        self.btn_continuar.clicked.connect(self.continuar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.close)

        fila_botones.addStretch()
        fila_botones.addWidget(self.btn_cancelar)
        fila_botones.addWidget(self.btn_continuar)

        contenedor_layout.addWidget(titulo)
        contenedor_layout.addWidget(lbl_info)
        contenedor_layout.addWidget(self.combo_operarios)
        contenedor_layout.addLayout(fila_botones)

        layout_principal.addWidget(contenedor)

    def _cargar_operarios(self) -> None:
        try:
            self.operarios = self.operario_service.listar_operarios_por_area_y_maquina(
                area=self.area,
                maquina=self.maquina,
                solo_activos=True,
            )

            self.combo_operarios.clear()
            self.combo_operarios.addItem("Seleccione un operario", None)

            for operario in self.operarios:
                self.combo_operarios.addItem(operario.nombre, operario)

            if not self.operarios:
                QMessageBox.information(
                    self,
                    "Sin operarios",
                    "No hay operarios activos disponibles para esta área y máquina.",
                )

        except ValidationError as e:
            QMessageBox.warning(self, "Validación", str(e))
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible cargar los operarios.\n\n{str(e)}",
            )

    def continuar(self) -> None:
        operario = self.combo_operarios.currentData()

        if operario is None:
            QMessageBox.warning(self, "Validación", "Debes seleccionar un operario.")
            return

        try:
            self.formulario_view = FormularioOperarioView(
                op=self.op,
                area=self.area,
                maquina=self.maquina,
                operario=operario.nombre,
                evento_origen=self.evento_origen,
            )
            self.formulario_view.show()
            self.close()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir el formulario del operario.\n\n{str(e)}",
            )