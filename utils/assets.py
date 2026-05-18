"""Utilidades transversales de fechas, IDs, assets, JSON y estilos.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from config.settings import SETTINGS

ASSETS_DIR = SETTINGS.paths.assets_dir
IMAGES_DIR = ASSETS_DIR / "images"


# Bloque CDLform: funcion/metodo image_path; encapsula una operacion del flujo del modulo.
def image_path(filename: str) -> str:
    return str(IMAGES_DIR / filename)
