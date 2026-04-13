from __future__ import annotations

import json
import os
from pathlib import Path

from config.settings import SETTINGS


class AuthService:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or (SETTINGS.paths.config_dir / "admin_login.json")

    @staticmethod
    def _normalizar_texto(valor: object) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def _leer_credenciales_desde_entorno(self) -> tuple[str, str] | None:
        usuario = self._normalizar_texto(os.getenv("CDLFORM_ADMIN_USER"))
        password = self._normalizar_texto(os.getenv("CDLFORM_ADMIN_PASSWORD"))

        if usuario and password:
            return usuario, password

        return None

    def _leer_credenciales_desde_archivo(self) -> tuple[str, str] | None:
        if not self.config_path.exists():
            return None

        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(
                f"El archivo de login {self.config_path} debe contener un objeto JSON."
            )

        usuario = self._normalizar_texto(data.get("usuario"))
        password = self._normalizar_texto(data.get("password"))

        if usuario and password:
            return usuario, password

        raise ValueError(
            f"El archivo de login {self.config_path} debe incluir 'usuario' y 'password'."
        )

    def obtener_credenciales_admin(self) -> tuple[str, str]:
        credenciales_entorno = self._leer_credenciales_desde_entorno()
        if credenciales_entorno:
            return credenciales_entorno

        credenciales_archivo = self._leer_credenciales_desde_archivo()
        if credenciales_archivo:
            return credenciales_archivo

        raise RuntimeError(
            "No hay credenciales administrativas configuradas. "
            "Defina CDLFORM_ADMIN_USER/CDLFORM_ADMIN_PASSWORD o cree config/admin_login.json."
        )

    def validar_login(self, usuario: str, password: str) -> bool:
        usuario_ingresado = self._normalizar_texto(usuario)
        password_ingresado = self._normalizar_texto(password)

        if not usuario_ingresado or not password_ingresado:
            return False

        usuario_configurado, password_configurado = self.obtener_credenciales_admin()
        return (
            usuario_ingresado == usuario_configurado
            and password_ingresado == password_configurado
        )
