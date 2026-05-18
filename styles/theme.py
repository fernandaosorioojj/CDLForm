"""Definiciones visuales compartidas por la interfaz PyQt.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from dataclasses import dataclass


# Bloque CDLform: clase AppTheme; agrupa estado y comportamiento de esta parte del flujo.
@dataclass(frozen=True)
class AppTheme:
    bg_app: str = "#FFFFFF"
    bg_card: str = "#FFFFFF"
    bg_input: str = "#FFFFFF"
    bg_button: str = "#05095C"
    bg_button_hover: str = "#9AB3E6"
    bg_button_secondary: str = "#9AB3E6"
    bg_button_secondary_hover: str = "#E8D34F"
    bg_button_danger: str = "#8F8F8F"
    bg_button_danger_hover: str = "#05095C"
    bg_button_success: str = "#E8D34F"
    bg_button_success_hover: str = "#9AB3E6"
    bg_warning_soft: str = "#E8D34F"
    border_warning: str = "#E8D34F"

    text_primary: str = "#05095C"
    text_secondary: str = "#8F8F8F"
    text_heading: str = "#05095C"
    text_on_app: str = "#05095C"
    text_on_app_accent: str = "#8F8F8F"
    text_on_button: str = "#FFFFFF"
    border: str = "#9AB3E6"
    border_input: str = "#9AB3E6"
    focus: str = "#E8D34F"
    # LEGACY / NO FLUJO VISUAL ACTUAL:
    # Valores conservados para compatibilidad con QSS antiguos. El tema vigente
    # usa fondo blanco y no aplica gradientes.
    gradient_start: str = "#FFFFFF"
    gradient_mid: str = "#FFFFFF"
    gradient_end: str = "#FFFFFF"
    gradient_accent: str = "#E8D34F"

    radius_sm: int = 8
    radius_md: int = 8
    radius_lg: int = 8

    font_family: str = "Trebuchet MS"
    font_size_base: int = 14
    font_size_title: int = 28
    font_size_section: int = 18


THEME = AppTheme()
