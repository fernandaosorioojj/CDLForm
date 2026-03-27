from __future__ import annotations

import logging
import sys
from pathlib import Path

from config.logging_config import configure_logging
from config.settings import SETTINGS
from core.exceptions import CDLformError
from utils.json_manager import JsonManager

logger = logging.getLogger(__name__)


def initialize_storage() -> None:
    files_to_initialize: dict[Path, list] = {
        SETTINGS.paths.formularios_file: [],
        SETTINGS.paths.respuestas_file: [],
        SETTINGS.paths.preguntas_file: [],
        SETTINGS.paths.eventos_op_file: [],
        SETTINGS.paths.disparadores_file: [],
    }
                                                                                                                                                                                                                                                                                    
    for file_path, default_data in files_to_initialize.items():
        JsonManager.ensure_file_exists(file_path, default_data)


def bootstrap_application() -> None:
    configure_logging()

    logger.info(
        "iniciando aplicación %s versión %s en entorno %s",
        SETTINGS.app_name,
        SETTINGS.app_version,
        SETTINGS.environment,
    )

    initialize_storage()

    logger.info("storage inicializado correctamente")
    logger.info("aplicación lista para continuar con el flujo de ejecución")


def main() -> int:
    try:
        bootstrap_application()
        print(f"{SETTINGS.app_name} iniciado correctamente.")
        return 0

    except CDLformError as exc:
        logging.getLogger(__name__).exception("error controlado de aplicación: %s", exc)
        print(f"error de aplicación: {exc}")
        return 1

    except Exception as exc:
        logging.getLogger(__name__).exception("error no controlado: %s", exc)
        print(f"error inesperado: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())