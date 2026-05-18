"""Definiciones visuales compartidas por la interfaz PyQt.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from utils.style_loader import load_qss_files


# Bloque CDLform: funcion/metodo apply_view_style; encapsula una operacion del flujo del modulo.
def apply_view_style(widget, *qss_files: str) -> None:
    qss = load_qss_files(*qss_files)
    if qss:
        widget.setStyleSheet(qss)

