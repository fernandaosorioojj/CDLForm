from dataclasses import dataclass


@dataclass(frozen=True)
class AppTheme:
    bg_app: str = "#D1CDC2"
    bg_card: str = "#ffffff"
    bg_input: str = "#FFFFFF"
    bg_button: str = "#DEDEDE"
    bg_button_hover: str = "#CFCFCF"
    bg_button_secondary: str = "#DEDEDE"
    bg_button_secondary_hover: str = "#CFCFCF"
    bg_button_danger: str = "#d8574d"
    bg_button_danger_hover: str = "#bd443b"
    bg_button_success: str = "#B5E2FF"
    bg_button_success_hover: str = "#A6D7F6"
    bg_warning_soft: str = "#FCE3FF"
    border_warning: str = "#D7C3E3"

    text_primary: str = "#33485D"
    text_secondary: str = "#6C7A8C"
    text_heading: str = "#44586F"
    text_on_app: str = "#33485D"
    text_on_app_accent: str = "#6C7A8C"
    text_on_button: str = "#4F6278"
    border: str = "#D9E4EF"
    border_input: str = "#CCD9E6"
    focus: str = "#B5E2FF"
    gradient_start: str = "#D1CDC2"
    gradient_mid: str = "#D1CDC2"
    gradient_end: str = "#D1CDC2"
    gradient_accent: str = "#D1CDC2"

    radius_sm: int = 8
    radius_md: int = 8
    radius_lg: int = 8

    font_family: str = "Trebuchet MS"
    font_size_base: int = 14
    font_size_title: int = 28
    font_size_section: int = 18


THEME = AppTheme()
