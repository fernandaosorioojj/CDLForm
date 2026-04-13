from dataclasses import dataclass


@dataclass(frozen=True)
class AppTheme:
    bg_app: str = "#65706D"
    bg_card: str = "#ffffff"
    bg_input: str = "#ffffff"
    bg_button: str = "#2CB833"
    bg_button_hover: str = "#23962a"
    bg_button_secondary: str = "#70C2AF"
    bg_button_secondary_hover: str = "#5dad9a"
    bg_button_danger: str = "#c94b4b"
    bg_button_danger_hover: str = "#ad3f3f"
    bg_button_success: str = "#2CB833"
    bg_button_success_hover: str = "#23962a"
    bg_warning_soft: str = "#FBFF0D"
    border_warning: str = "#d6d900"

    text_primary: str = "#1d2825"
    text_secondary: str = "#65706D"
    text_heading: str = "#1f5f36"
    text_on_app: str = "#ffffff"
    text_on_app_accent: str = "#d7f8dc"
    text_on_button: str = "#ffffff"
    border: str = "#d9e1de"
    border_input: str = "#b8c8c2"
    focus: str = "#70C2AF"

    radius_sm: int = 8
    radius_md: int = 8
    radius_lg: int = 8

    font_family: str = "Segoe UI"
    font_size_base: int = 14
    font_size_title: int = 26
    font_size_section: int = 18


THEME = AppTheme()
