from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ApontamentoProcesadoService:
    def __init__(self, processed_file: str | Path = "storage/apontamentos_procesados.json") -> None:
        self.processed_file = Path(processed_file)
        self._ensure_processed_file()

    def _ensure_processed_file(self) -> None:
        self.processed_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.processed_file.exists():
            self.processed_file.write_text("[]", encoding="utf-8")

    def _read_processed(self) -> list[dict[str, Any]]:
        try:
            data = json.loads(self.processed_file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
            return []
        except Exception:
            return []

    def _write_processed(self, data: list[dict[str, Any]]) -> None:
        self.processed_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )

    def listar_registros(self) -> list[dict[str, Any]]:
        return self._read_processed()

    def listar_ids_procesados(self) -> set[str]:
        registros = self._read_processed()
        return {
            str(item.get("id_apontamento", "")).strip()
            for item in registros
            if str(item.get("id_apontamento", "")).strip()
        }

    def ya_procesado(self, id_apontamento: str | int) -> bool:
        id_normalizado = str(id_apontamento).strip()
        if not id_normalizado:
            return False

        return id_normalizado in self.listar_ids_procesados()

    def marcar_como_procesado(
        self,
        id_apontamento: str | int,
        num_ordem: str = "",
        datos_extra: dict[str, Any] | None = None,
    ) -> None:
        id_normalizado = str(id_apontamento).strip()

        if not id_normalizado:
            return

        if self.ya_procesado(id_normalizado):
            return

        registros = self._read_processed()

        nuevo_registro: dict[str, Any] = {
            "id_apontamento": id_normalizado,
            "num_ordem": str(num_ordem).strip(),
        }

        if datos_extra:
            nuevo_registro.update(datos_extra)

        registros.append(nuevo_registro)
        self._write_processed(registros)