from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from config.settings import SETTINGS
from core.exceptions import BusinessRuleError
from core.validators import require_non_empty_string


class AppLauncher:
    def __init__(self) -> None:
        self.base_dir = SETTINGS.paths.base_dir
        self.main_file = self.base_dir / "main.py"

    def _ensure_main_file_exists(self) -> None:
        if not self.main_file.exists():
            raise BusinessRuleError(
                f"no se encontró el archivo principal de la aplicación en '{self.main_file}'"
            )

    def launch_normal(self) -> subprocess.Popen:
        self._ensure_main_file_exists()

        return subprocess.Popen(
            [sys.executable, str(self.main_file)],
            cwd=str(self.base_dir),
        )

    def launch_auto(
        self,
        op: str,
        area: str,
        maquina: str,
    ) -> subprocess.Popen:
        self._ensure_main_file_exists()

        normalized_op = require_non_empty_string(op, "op")
        normalized_area = require_non_empty_string(area, "area")
        normalized_maquina = require_non_empty_string(maquina, "maquina")

        return subprocess.Popen(
            [
                sys.executable,
                str(self.main_file),
                "--modo",
                "auto",
                "--op",
                normalized_op,
                "--area",
                normalized_area,
                "--maquina",
                normalized_maquina,
            ],
            cwd=str(self.base_dir),
        )