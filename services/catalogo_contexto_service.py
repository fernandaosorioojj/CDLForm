from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.json_manager import JsonManager


class CatalogoContextoService:
    def __init__(self, storage_dir: str | Path = "storage") -> None:
        self.storage_dir = Path(storage_dir)

    def _leer_json(self, nombre_archivo: str, default: Any) -> Any:
        file_path = self.storage_dir / nombre_archivo
        JsonManager.ensure_file_exists(str(file_path), default)

        data = JsonManager.read_json(str(file_path))

        if data is None:
            return default

        return data

    @staticmethod
    def _normalizar_lista(valores: list[Any]) -> list[str]:
        normalizados: list[str] = []

        for valor in valores:
            valor_normalizado = str(valor).strip()
            if valor_normalizado and valor_normalizado not in normalizados:
                normalizados.append(valor_normalizado)

        return normalizados

    def listar_cod_recursos(self) -> list[str]:
        data = self._leer_json("cod_recurso.json", [])

        if isinstance(data, list):
            return self._normalizar_lista(data)

        if isinstance(data, dict):
            return self._normalizar_lista(list(data.values()))

        return []

    def listar_cod_setores(self) -> list[str]:
        data = self._leer_json("cod_setor.json", [])

        if isinstance(data, list):
            return self._normalizar_lista(data)

        if isinstance(data, dict):
            return self._normalizar_lista(list(data.values()))

        return []

    def listar_cod_ativ(self) -> list[str]:
        data = self._leer_json("cod_ativ.json", [])

        if isinstance(data, list):
            return self._normalizar_lista(data)

        if isinstance(data, dict):
            return self._normalizar_lista(list(data.values()))

        return []

    def listar_turnos(self) -> list[str]:
        data = self._leer_json("turnos.json", [])

        if isinstance(data, list):
            return self._normalizar_lista(data)

        if isinstance(data, dict):
            return self._normalizar_lista(list(data.values()))

        return []

    def listar_tipos_trabajo(self) -> list[str]:
        data = self._leer_json("tipos_trabajo.json", [])

        if isinstance(data, list):
            return self._normalizar_lista(data)

        if isinstance(data, dict):
            return self._normalizar_lista(list(data.values()))

        return []

    def obtener_cod_recursos_por_estacion(self, estacion: str) -> list[str]:
        estacion_normalizada = str(estacion).strip()

        if not estacion_normalizada:
            raise ValueError("La estación no puede venir vacía.")

        data = self._leer_json("estaciones_recursos.json", {})

        if not isinstance(data, dict):
            raise ValueError(
                "El archivo storage/estaciones_recursos.json debe tener formato objeto JSON."
            )

        codigos = data.get(estacion_normalizada)

        if codigos is None:
            raise ValueError(
                f"No existe homologación de estación a CodRecurso para: "
                f"{estacion_normalizada}"
            )

        if isinstance(codigos, str):
            codigos = [codigos]

        if not isinstance(codigos, list):
            raise ValueError(
                f"La homologación de la estación {estacion_normalizada} debe ser una lista."
            )

        codigos_normalizados = self._normalizar_lista(codigos)

        if not codigos_normalizados:
            raise ValueError(
                f"La estación {estacion_normalizada} no tiene CodRecurso homologado."
            )

        return codigos_normalizados

    def homologar_estacion_a_cod_recursos(self, estacion: str) -> list[str]:
        return self.obtener_cod_recursos_por_estacion(estacion)

    def resolver_contexto_desde_estacion(self, estacion: str) -> dict[str, object]:
        estacion_normalizada = str(estacion).strip()

        return {
            "estacion": estacion_normalizada,
            "cod_recursos": self.obtener_cod_recursos_por_estacion(
                estacion_normalizada
            ),
        }

    @staticmethod
    def construir_placeholders_in(cantidad: int) -> str:
        if cantidad <= 0:
            raise ValueError("La cantidad de placeholders debe ser mayor que cero.")

        return ", ".join("?" for _ in range(cantidad))