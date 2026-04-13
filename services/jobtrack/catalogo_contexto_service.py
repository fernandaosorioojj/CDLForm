from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.json_manager import JsonManager


class CatalogoContextoService:
    def __init__(
        self,
        storage_dir: str | Path = "storage",
        apontamento_query_service=None,
        usar_sql_catalogos: bool = True,
    ) -> None:
        self.storage_dir = Path(storage_dir)
        self.apontamento_query_service = apontamento_query_service
        self.usar_sql_catalogos = usar_sql_catalogos

    def _obtener_apontamento_query_service(self):
        if self.apontamento_query_service is None:
            from services.jobtrack.apontamento_query_service import ApontamentoQueryService

            self.apontamento_query_service = ApontamentoQueryService(
                catalogo_contexto_service=self
            )

        return self.apontamento_query_service

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

    def _obtener_catalogo_desde_sql(self, nombre_metodo: str) -> list[str]:
        if not self.usar_sql_catalogos:
            return []

        try:
            query_service = self._obtener_apontamento_query_service()
            metodo = getattr(query_service, nombre_metodo)
            resultado = metodo()
            return self._normalizar_lista(resultado)
        except Exception:
            return []

    def listar_cod_recursos(self) -> list[str]:
        valores_sql = self._obtener_catalogo_desde_sql(
            "listar_cod_recursos_disponibles"
        )
        if valores_sql:
            return valores_sql

        data = self._leer_json("cod_recurso.json", [])

        if isinstance(data, list):
            return self._normalizar_lista(data)

        if isinstance(data, dict):
            return self._normalizar_lista(list(data.values()))

        return []

    def listar_cod_recurso(self) -> list[str]:
        return self.listar_cod_recursos()

    def listar_cod_setores(self) -> list[str]:
        valores_sql = self._obtener_catalogo_desde_sql(
            "listar_cod_setores_disponibles"
        )
        if valores_sql:
            return valores_sql

        data = self._leer_json("cod_setor.json", [])

        if isinstance(data, list):
            return self._normalizar_lista(data)

        if isinstance(data, dict):
            return self._normalizar_lista(list(data.values()))

        return []

    def listar_cod_setor(self) -> list[str]:
        return self.listar_cod_setores()

    def listar_turnos(self) -> list[str]:
        valores_sql = self._obtener_catalogo_desde_sql(
            "listar_turnos_disponibles"
        )
        if valores_sql:
            return valores_sql

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
            raise ValueError("La estaciÃ³n no puede venir vacÃ­a.")

        data = self._leer_json("estaciones_recursos.json", {})

        if not isinstance(data, dict):
            raise ValueError(
                "El archivo storage/estaciones_recursos.json debe tener formato objeto JSON."
            )

        codigos = data.get(estacion_normalizada)

        if codigos is None:
            raise ValueError(
                f"No existe homologaciÃ³n de estaciÃ³n a CodRecurso para: "
                f"{estacion_normalizada}"
            )

        if isinstance(codigos, str):
            codigos = [codigos]

        if not isinstance(codigos, list):
            raise ValueError(
                f"La homologaciÃ³n de la estaciÃ³n {estacion_normalizada} debe ser una lista."
            )

        codigos_normalizados = self._normalizar_lista(codigos)

        if not codigos_normalizados:
            raise ValueError(
                f"La estaciÃ³n {estacion_normalizada} no tiene CodRecurso homologado."
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
