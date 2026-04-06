from pathlib import Path

from PyQt5.QtWidgets import QApplication
from ui.formulario_operario import FormularioOperarioView


def cargar_estilos(app: QApplication) -> None:
    ruta_estilos = Path("assets/styles.qss")

    if not ruta_estilos.exists():
        print(f"No se encontró la hoja de estilos: {ruta_estilos}")
        return

    app.setStyleSheet(ruta_estilos.read_text(encoding="utf-8"))


app = QApplication([])

cargar_estilos(app)

operario = {
    "id_operario": "OPR-001",
    "nombre": "Operario Prueba",
}

contexto = {
    "id_formulario": "FORM-0001",
    "identificador": "FLE37858",
    "num_ordem": "FLE37858",
    "cod_setor": "SETOR-01",
    "cod_recurso": "REC-01",
    "cod_ativ": "ATIV-01",
    "turno": "1",
    "tipo_trabajo": "Produccion",
}

ventana = FormularioOperarioView(operario=operario, contexto=contexto)
ventana.show()

app.exec_()