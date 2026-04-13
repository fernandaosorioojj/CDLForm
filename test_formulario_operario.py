from PyQt5.QtWidgets import QApplication

from services.forms.formulario_service import FormularioService
from ui.formulario_operario import FormularioOperarioView
from utils.style_loader import load_qss_files


def cargar_estilos(app: QApplication) -> None:
    app.setStyleSheet(load_qss_files("base.qss", "formulario_operario.qss"))


app = QApplication([])

cargar_estilos(app)
formulario_service = FormularioService()

operario = {
    "id_operario": "OPR-001",
    "nombre": "Operario Prueba",
}

contexto = {
    # No enviamos id_formulario para que la vista use este contexto de prueba
    # y no reemplace los valores con un formulario persistido en storage.
    "identificador": "TEST-UTECO-001",
    "num_ordem": "TEST-UTECO-001",
    "id_apontamento": "TEST-0001",
    "fecha_formulario": "2026-04-10",
    "cod_setor": "IMP_HUEGO",
    "cod_recurso": "UTECO",
    "turno": "3",
    "tipo_trabajo": "Produccion",
    "estado": "en_apertura",
    "descripcion_op": "OP de prueba",
    "descripcion_proceso": "Proceso de prueba",
    "estacion": "ESTACION-76",
}

formulario = formulario_service.obtener_siguiente_formulario_pendiente_operario()

ventana = FormularioOperarioView(
    formulario=formulario,
    operario=operario["nombre"],
    contexto=contexto,
)
ventana.show()

app.exec_()
