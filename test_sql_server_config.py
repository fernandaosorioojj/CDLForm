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

from config import sql_server_config


WORKSPACE_TMP = Path(__file__).resolve().parent / ".test_tmp_sql"


@contextmanager
def _temporary_workspace_dir() -> Iterator[Path]:
    WORKSPACE_TMP.mkdir(exist_ok=True)
    tmp_path = WORKSPACE_TMP / f"test-{uuid.uuid4().hex}"
    tmp_path.mkdir()
    try:
        yield tmp_path
    finally:
        shutil.rmtree(tmp_path)


class SqlServerConfigTest(unittest.TestCase):
    def test_build_connection_string_lee_config_local(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "sql_server.local.json"
            config_path.write_text(
                json.dumps(
                    {
                        "server": "SERVIDOR",
                        "database": "BASE",
                        "username": "USUARIO",
                        "password": "CLAVE",
                        "driver": "ODBC Driver 18 for SQL Server",
                        "trust_server_certificate": "yes",
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(sql_server_config, "LOCAL_CONFIG_PATH", config_path):
                connection_string = sql_server_config.build_connection_string()

        self.assertIn("SERVER=SERVIDOR;", connection_string)
        self.assertIn("DATABASE=BASE;", connection_string)
        self.assertIn("UID=USUARIO;", connection_string)
        self.assertIn("PWD=CLAVE;", connection_string)

    def test_variables_entorno_tienen_prioridad_sobre_archivo(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "sql_server.local.json"
            config_path.write_text(
                json.dumps(
                    {
                        "server": "SERVIDOR_ARCHIVO",
                        "database": "BASE_ARCHIVO",
                        "username": "USUARIO_ARCHIVO",
                        "password": "CLAVE_ARCHIVO",
                    }
                ),
                encoding="utf-8",
            )

            env = {
                "CDLFORM_SQL_SERVER": "SERVIDOR_ENV",
                "CDLFORM_SQL_DATABASE": "BASE_ENV",
                "CDLFORM_SQL_USERNAME": "USUARIO_ENV",
                "CDLFORM_SQL_PASSWORD": "CLAVE_ENV",
            }
            with patch.object(sql_server_config, "LOCAL_CONFIG_PATH", config_path):
                with patch.dict(os.environ, env, clear=False):
                    connection_string = sql_server_config.build_connection_string()

        self.assertIn("SERVER=SERVIDOR_ENV;", connection_string)
        self.assertIn("DATABASE=BASE_ENV;", connection_string)
        self.assertIn("UID=USUARIO_ENV;", connection_string)
        self.assertIn("PWD=CLAVE_ENV;", connection_string)

    def test_falla_sin_configuracion_requerida(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            config_path = tmp_dir / "sql_server.local.json"
            env = {
                key: ""
                for key in [
                    "CDLFORM_SQL_SERVER",
                    "CDLFORM_SQL_DATABASE",
                    "CDLFORM_SQL_USERNAME",
                    "CDLFORM_SQL_PASSWORD",
                ]
            }
            with patch.object(sql_server_config, "LOCAL_CONFIG_PATH", config_path):
                with patch.dict(os.environ, env, clear=False):
                    with self.assertRaisesRegex(RuntimeError, "SQL Server"):
                        sql_server_config.build_connection_string()


if __name__ == "__main__":
    unittest.main()
