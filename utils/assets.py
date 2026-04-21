from __future__ import annotations

from config.settings import SETTINGS

ASSETS_DIR = SETTINGS.paths.assets_dir
IMAGES_DIR = ASSETS_DIR / "images"


def image_path(filename: str) -> str:
    return str(IMAGES_DIR / filename)
