from __future__ import annotations

from pathlib import Path
from string import Template

from styles.theme import THEME


def _theme_mapping() -> dict[str, object]:
    return {
        "bg_app": THEME.bg_app,
        "bg_card": THEME.bg_card,
        "bg_input": THEME.bg_input,
        "bg_button": THEME.bg_button,
        "bg_button_hover": THEME.bg_button_hover,
        "bg_button_secondary": THEME.bg_button_secondary,
        "bg_button_secondary_hover": THEME.bg_button_secondary_hover,
        "bg_button_danger": THEME.bg_button_danger,
        "bg_button_danger_hover": THEME.bg_button_danger_hover,
        "bg_button_success": THEME.bg_button_success,
        "bg_button_success_hover": THEME.bg_button_success_hover,
        "bg_warning_soft": THEME.bg_warning_soft,
        "border_warning": THEME.border_warning,
        "text_primary": THEME.text_primary,
        "text_secondary": THEME.text_secondary,
        "text_heading": THEME.text_heading,
        "text_on_app": THEME.text_on_app,
        "text_on_app_accent": THEME.text_on_app_accent,
        "text_on_button": THEME.text_on_button,
        "border": THEME.border,
        "border_input": THEME.border_input,
        "focus": THEME.focus,
        "radius_sm": THEME.radius_sm,
        "radius_md": THEME.radius_md,
        "radius_lg": THEME.radius_lg,
        "font_family": THEME.font_family,
        "font_size_base": THEME.font_size_base,
        "font_size_title": THEME.font_size_title,
        "font_size_section": THEME.font_size_section,
    }


def load_qss_files(*filenames: str) -> str:
    base_dir = Path(__file__).resolve().parent.parent
    styles_dir = base_dir / "styles"
    partes: list[str] = []

    for filename in filenames:
        if not filename:
            continue

        qss_path = styles_dir / filename
        if not qss_path.exists():
            continue

        content = qss_path.read_text(encoding="utf-8")
        partes.append(Template(content).safe_substitute(_theme_mapping()))

    return "\n\n".join(partes)
