from __future__ import annotations

import json
import os
import shutil
import unittest
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from services.security.auth_service import AuthService


WORKSPACE_TMP = Path(__file__).resolve().parent / ".test_tmp_auth"
LOGIN_ENV_KEYS = [
    "CDLFORM_GESTION_USER",
    "CDLFORM_GESTION_PASSWORD_HASH",
    "CDLFORM_ADMIN_USER",
    "CDLFORM_ADMIN_PASSWORD_HASH",
]


@contextmanager
def _temporary_workspace_dir() -> Iterator[Path]:
    WORKSPACE_TMP.mkdir(exist_ok=True)
    tmp_path = WORKSPACE_TMP / f"test-{uuid.uuid4().hex}"
    tmp_path.mkdir()
    try:
        yield tmp_path
    finally:
        shutil.rmtree(tmp_path)


class AuthServiceTest(unittest.TestCase):
    def _env_limpio(self, valores: dict[str, str] | None = None) -> dict[str, str]:
        env = {key: "" for key in LOGIN_ENV_KEYS}
        if valores:
            env.update(valores)
        return env

    def test_validar_login_con_hash_desde_archivo(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "gestion_login.json"
            config_path.write_text(
                json.dumps(
                    {
                        "usuario": "gestion",
                        "password_hash": AuthService.generar_password_hash("clave"),
                    }
                ),
                encoding="utf-8",
            )
            service = AuthService(config_path=config_path)

            with patch.dict(os.environ, self._env_limpio(), clear=False):
                self.assertTrue(service.validar_login("gestion", "clave"))
                self.assertFalse(service.validar_login("gestion", "otra"))
                self.assertFalse(service.validar_login("otro", "clave"))

    def test_validar_login_con_hash_desde_entorno(self) -> None:
        env = self._env_limpio(
            {
                "CDLFORM_GESTION_USER": "gestion_env",
                "CDLFORM_GESTION_PASSWORD_HASH": AuthService.generar_password_hash(
                    "clave_env"
                ),
            }
        )

        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "gestion_login.json"
            service = AuthService(config_path=config_path)
            with patch.dict(os.environ, env, clear=False):
                self.assertTrue(service.validar_login("gestion_env", "clave_env"))
                self.assertFalse(service.validar_login("gestion_env", "clave"))

    def test_validar_login_mantiene_entorno_legacy_admin(self) -> None:
        env = self._env_limpio(
            {
                "CDLFORM_ADMIN_USER": "admin_env",
                "CDLFORM_ADMIN_PASSWORD_HASH": AuthService.generar_password_hash(
                    "clave_admin"
                ),
            }
        )

        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "gestion_login.json"
            service = AuthService(config_path=config_path)
            with patch.dict(os.environ, env, clear=False):
                self.assertTrue(service.validar_login("admin_env", "clave_admin"))

    def test_archivo_login_rechaza_password_plano(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "gestion_login.json"
            config_path.write_text(
                json.dumps({"usuario": "gestion", "password": "1234"}),
                encoding="utf-8",
            )
            service = AuthService(config_path=config_path)

            with self.assertRaisesRegex(ValueError, "password_hash"):
                service.obtener_credenciales_admin()

    def test_falla_sin_configuracion(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "gestion_login.json"
            service = AuthService(config_path=config_path)
            service.legacy_config_path = tmp_dir / "admin_login.json"
            env = self._env_limpio()

            with patch.dict(os.environ, env, clear=False):
                with self.assertRaisesRegex(RuntimeError, "Gestion"):
                    service.obtener_credenciales_gestion()


if __name__ == "__main__":
    unittest.main()
