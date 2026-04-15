from __future__ import annotations

import json
import hashlib
import hmac
import os
import secrets
from pathlib import Path

from config.settings import SETTINGS


HASH_ALGORITHM = "pbkdf2_sha256"
HASH_ITERATIONS = 260000


class AuthService:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or (SETTINGS.paths.config_dir / "gestion_login.json")
        self.legacy_config_path = SETTINGS.paths.config_dir / "admin_login.json"

    @staticmethod
    def _normalizar_texto(valor: object) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @staticmethod
    def generar_password_hash(password: str) -> str:
        password_limpio = str(password or "")
        if not password_limpio:
            raise ValueError("password no puede venir vacio.")

        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password_limpio.encode("utf-8"),
            salt.encode("utf-8"),
            HASH_ITERATIONS,
        ).hex()
        return f"{HASH_ALGORITHM}${HASH_ITERATIONS}${salt}${digest}"

    @staticmethod
    def _validar_password_hash(password: str, password_hash: str) -> bool:
        partes = str(password_hash or "").split("$")
        if len(partes) != 4:
            return False

        algoritmo, iteraciones_raw, salt, digest_esperado = partes
        if algoritmo != HASH_ALGORITHM:
            return False

        try:
            iteraciones = int(iteraciones_raw)
        except ValueError:
            return False

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            str(password or "").encode("utf-8"),
            salt.encode("utf-8"),
            iteraciones,
        ).hex()
        return hmac.compare_digest(digest, digest_esperado)

    def _leer_credenciales_desde_entorno(self) -> dict[str, str] | None:
        usuario = self._normalizar_texto(os.getenv("CDLFORM_GESTION_USER"))
        password_hash = self._normalizar_texto(
            os.getenv("CDLFORM_GESTION_PASSWORD_HASH")
        )

        if not usuario or not password_hash:
            usuario = self._normalizar_texto(os.getenv("CDLFORM_ADMIN_USER"))
            password_hash = self._normalizar_texto(
                os.getenv("CDLFORM_ADMIN_PASSWORD_HASH")
            )

        if usuario and password_hash:
            return {
                "usuario": usuario,
                "password_hash": password_hash,
            }

        return None

    def _leer_credenciales_desde_archivo(
        self,
        config_path: Path,
    ) -> dict[str, str] | None:
        if not config_path.exists():
            return None

        data = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(
                f"El archivo de login {config_path} debe contener un objeto JSON."
            )

        usuario = self._normalizar_texto(data.get("usuario"))
        password_hash = self._normalizar_texto(data.get("password_hash"))

        if usuario and password_hash:
            return {
                "usuario": usuario,
                "password_hash": password_hash,
            }

        raise ValueError(
            f"El archivo de login {config_path} debe incluir "
            "'usuario' y 'password_hash'."
        )

    def obtener_credenciales_gestion(self) -> dict[str, str]:
        credenciales_entorno = self._leer_credenciales_desde_entorno()
        if credenciales_entorno:
            return credenciales_entorno

        credenciales_archivo = self._leer_credenciales_desde_archivo(
            self.config_path
        )
        if credenciales_archivo:
            return credenciales_archivo

        credenciales_archivo = self._leer_credenciales_desde_archivo(
            self.legacy_config_path
        )
        if credenciales_archivo:
            return credenciales_archivo

        raise RuntimeError(
            "No hay credenciales de Gestion configuradas. "
            "Defina CDLFORM_GESTION_USER/CDLFORM_GESTION_PASSWORD_HASH o cree "
            "config/gestion_login.json."
        )

    def obtener_credenciales_admin(self) -> dict[str, str]:
        return self.obtener_credenciales_gestion()

    def validar_login(self, usuario: str, password: str) -> bool:
        usuario_ingresado = self._normalizar_texto(usuario)
        password_ingresado = self._normalizar_texto(password)

        if not usuario_ingresado or not password_ingresado:
            return False

        credenciales = self.obtener_credenciales_gestion()
        usuario_configurado = self._normalizar_texto(credenciales.get("usuario"))
        password_hash_configurado = self._normalizar_texto(
            credenciales.get("password_hash")
        )

        return (
            usuario_ingresado == usuario_configurado
            and self._validar_password_hash(
                password_ingresado,
                password_hash_configurado,
            )
        )
