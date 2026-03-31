from __future__ import annotations

from pathlib import Path
import unicodedata

from utils.json_manager import JsonManager


class CatalogoContextoService:
    def __init__(self) -> None:
        self.base_path = Path("storage")

    def listar_cod_setor(self) -> list[str]:
        return self._leer_catalogo("cod_setor.json")

    def listar_cod_recurso(self) -> list[str]:
        return self._leer_catalogo("cod_recurso.json")

    def listar_cod_ativ(self) -> list[str]:
        return self._leer_catalogo("cod_ativ.json")

    def listar_turnos(self) -> list[str]:
        return self._leer_catalogo("turnos.json")

    def listar_tipos_trabajo(self) -> list[str]:
        return self._leer_catalogo("tipos_trabajo.json")

    def resolver_contexto(
        self,
        cod_setor: str | None = None,
        cod_recurso: str | None = None,
        cod_ativ: str | None = None,
        turno: str | int | None = None,
    ) -> dict:
        return {
            "cod_setor": self._resolver_valor_catalogo("cod_setor.json", cod_setor),
            "cod_recurso": self._resolver_valor_catalogo("cod_recurso.json", cod_recurso),
            "cod_ativ": self._resolver_valor_catalogo("cod_ativ.json", cod_ativ),
            "turno": self._resolver_valor_catalogo("turnos.json", turno),
            "tipo_trabajo": self._resolver_tipo_trabajo(cod_ativ),
        }

    def _resolver_tipo_trabajo(self, cod_ativ: str | None) -> str:
        valor = str(cod_ativ or "").strip()
        if not valor:
            return ""

        tipos = self._leer_catalogo("tipos_trabajo.json")
        valor_normalizado = self._normalizar(valor)

        for item in tipos:
            if self._normalizar(item) == valor_normalizado:
                return item

        return ""

    def _resolver_valor_catalogo(self, filename: str, valor_entrada: str | int | None) -> str:
        valor_entrada = str(valor_entrada or "").strip()
        if not valor_entrada:
            return ""

        catalogo = self._leer_catalogo(filename)
        valor_normalizado = self._normalizar(valor_entrada)

        for item in catalogo:
            if self._normalizar(item) == valor_normalizado:
                return item

        return ""

    def _leer_catalogo(self, filename: str) -> list[str]:
        file_path = self.base_path / filename
        JsonManager.ensure_file_exists(str(file_path), [])

        data = JsonManager.read_json(str(file_path))
        if not isinstance(data, list):
            return []

        valores: list[str] = []
        vistos: set[str] = set()

        for item in data:
            valor = str(item).strip()
            if not valor:
                continue

            clave = self._normalizar(valor)
            if clave not in vistos:
                vistos.add(clave)
                valores.append(valor)

        return valores

    def _normalizar(self, valor: str) -> str:
        valor = str(valor).strip().lower()
        valor = unicodedata.normalize("NFKD", valor)
        valor = "".join(c for c in valor if not unicodedata.combining(c))
        valor = " ".join(valor.split())
        return valor