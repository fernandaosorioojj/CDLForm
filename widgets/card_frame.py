"""Widgets PyQt reutilizables para construir pantallas.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from PyQt5.QtWidgets import QFrame


# Bloque CDLform: clase CardFrame; agrupa estado y comportamiento de esta parte del flujo.
class CardFrame(QFrame):
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setProperty("card", "true")

