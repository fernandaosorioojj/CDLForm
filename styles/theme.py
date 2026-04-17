from dataclasses import dataclass


@dataclass(frozen=True)
class AppTheme:
    bg_app: str = "#eef4f1"
    bg_card: str = "#ffffff"
    bg_input: str = "#f7fbf8"
    bg_button: str = "#163d34"
    bg_button_hover: str = "#0f2f28"
    bg_button_secondary: str = "#e2eee8"
    bg_button_secondary_hover: str = "#d2e3dc"
    bg_button_danger: str = "#d8574d"
    bg_button_danger_hover: str = "#bd443b"
    bg_button_success: str = "#2e9f68"
    bg_button_success_hover: str = "#238553"
    bg_warning_soft: str = "#fff4c7"
    border_warning: str = "#b88700"

    text_primary: str = "#17231f"
    text_secondary: str = "#5f736b"
    text_heading: str = "#163d34"
    text_on_app: str = "#17231f"
    text_on_app_accent: str = "#5f736b"
    text_on_button: str = "#ffffff"
    border: str = "#d9e5df"
    border_input: str = "#b8ccc2"
    focus: str = "#42b883"

    radius_sm: int = 8
    radius_md: int = 8
    radius_lg: int = 8

    font_family: str = "Segoe UI"
    font_size_base: int = 14
    font_size_title: int = 28
    font_size_section: int = 18


THEME = AppTheme()
