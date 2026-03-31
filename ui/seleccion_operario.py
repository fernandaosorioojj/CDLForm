from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QMessageBox
)
from PyQt5.QtCore import Qt

from services.formulario_service import FormularioService
from services.operario_service import OperarioService
from ui.formulario_operario import FormularioOperarioView


class SeleccionOperarioView(QWidget):
    def __init__(self, evento: dict | None = None):
        super().__init__()
        self.evento = evento or {}
        self.operario_service = OperarioService()
        self.formulario_service = FormularioService()
        self.formulario_view = None

        self.setWindowTitle("Selección de Operario")
        self.init_ui()
        self.cargar_operarios()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        titulo = QLabel("Seleccione Operario")
        titulo.setAlignment(Qt.AlignCenter)

        self.label_contexto = QLabel(self.obtener_texto_contexto())
        self.label_contexto.setAlignment(Qt.AlignCenter)
        self.label_contexto.setWordWrap(True)

        self.combo_operarios = QComboBox()
        self.combo_operarios.addItem("Seleccione un operario", None)

        btn_continuar = QPushButton("Continuar")
        btn_continuar.clicked.connect(self.continuar)

        layout.addWidget(titulo)
        layout.addWidget(self.label_contexto)
        layout.addWidget(self.combo_operarios)
        layout.addWidget(btn_continuar)

        self.setLayout(layout)

    def obtener_texto_contexto(self) -> str:
        num_ordem = self.evento.get("num_ordem", "")
        contexto_resuelto = self.evento.get("contexto_resuelto") or {}

        cod_setor = contexto_resuelto.get("cod_setor") or self.evento.get("cod_setor", "")
        cod_recurso = contexto_resuelto.get("cod_recurso") or self.evento.get("cod_recurso", "")
        cod_ativ = contexto_resuelto.get("cod_ativ") or self.evento.get("cod_ativ", "")
        turno = contexto_resuelto.get("turno") or self.evento.get("turno", "")
        descricao_processo = self.evento.get("descricao_processo", "")

        partes = []

        if num_ordem:
            partes.append(f"Identificador: {num_ordem}")
        if cod_setor:
            partes.append(f"Setor: {cod_setor}")
        if cod_recurso:
            partes.append(f"Recurso: {cod_recurso}")
        if cod_ativ:
            partes.append(f"Actividad: {cod_ativ}")
        if turno:
            partes.append(f"Turno: {turno}")
        if descricao_processo:
            partes.append(f"Proceso: {descricao_processo}")

        return " | ".join(partes) if partes else "Sin contexto de evento."

    def cargar_operarios(self) -> None:
        try:
            operarios = self.operario_service.listar_operarios()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudieron cargar los operarios.\n{e}"
            )
            return

        for operario in operarios:
            nombre = operario.get("nombre", "Sin nombre")
            self.combo_operarios.addItem(nombre, operario)

    def _obtener_formulario_pendiente(self):
        formularios = self.formulario_service.listar_formularios_por_estado("pendiente")
        evento_id = str(self.evento.get("id_evento", "")).strip()
        identificador = str(self.evento.get("num_ordem", "")).strip()

        for formulario in formularios:
            if evento_id and str(formulario.evento_origen or "").strip() == evento_id:
                return formulario

        for formulario in formularios:
            if identificador and str(formulario.identificador).strip() == identificador:
                return formulario

        return None

    def continuar(self) -> None:
        operario = self.combo_operarios.currentData()

        if not operario:
            QMessageBox.warning(self, "Atención", "Debes seleccionar un operario.")
            return

        formulario = self._obtener_formulario_pendiente()

        if formulario is None:
            QMessageBox.warning(
                self,
                "Atención",
                "No se encontró un formulario pendiente para este evento."
            )
            return

        nombre_operario = str(operario.get("nombre", "")).strip()
        id_operario = str(operario.get("id_operario", "")).strip()

        try:
            formulario_actualizado = self.formulario_service.asignar_operario(
                formulario.id_formulario,
                nombre_operario
            )

            contexto = {
                "id_formulario": formulario_actualizado.id_formulario,
                "identificador": formulario_actualizado.identificador,
                "id_operario": id_operario,
                "operario": nombre_operario,
                "cod_setor": formulario_actualizado.cod_setor,
                "cod_recurso": formulario_actualizado.cod_recurso,
                "cod_ativ": formulario_actualizado.cod_ativ,
                "turno": formulario_actualizado.turno,
                "tipo_trabajo": formulario_actualizado.tipo_trabajo,
                "evento_origen": formulario_actualizado.evento_origen,
                "estado": formulario_actualizado.estado,
                "evento": self.evento,
            }

            self.formulario_view = FormularioOperarioView(
                operario=operario,
                contexto=contexto
            )
            self.formulario_view.showMaximized()
            self.close()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo asignar el operario al formulario.\n{e}"
            )