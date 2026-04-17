from __future__ import annotations

from pathlib import Path


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
IMAGES_DIR = ASSETS_DIR / "images"


def image_path(filename: str) -> str:
    return str(IMAGES_DIR / filename)
