from __future__ import annotations

from pathlib import Path

from models.plantilla_preguntas import PlantillaPreguntas
from repositories.base_repository import BaseRepository
from utils.json_manager import JsonManager


class PlantillaPreguntasRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = Path(file_path or "storage/plantillas_preguntas.json")
        super().__init__(self.file_path)

    def listar_plantillas(self) -> list[PlantillaPreguntas]:
        return [
            PlantillaPreguntas.from_dict(item)
            for item in self.get_all()
        ]

    def obtener_por_id(self, id_plantilla: str) -> PlantillaPreguntas | None:
        id_normalizado = str(id_plantilla).strip()

        for plantilla in self.listar_plantillas():
            if plantilla.id_plantilla == id_normalizado:
                return plantilla

        return None

    def obtener_activa(
        self,
        cod_recurso: str,
        cod_setor: str,
    ) -> PlantillaPreguntas | None:
        cod_recurso_normalizado = str(cod_recurso or "").strip().upper()
        cod_setor_normalizado = str(cod_setor or "").strip().upper()

        candidatas = [
            plantilla
            for plantilla in self.listar_plantillas()
            if plantilla.activa
            and plantilla.cod_recurso == cod_recurso_normalizado
            and plantilla.cod_setor == cod_setor_normalizado
        ]

        if not candidatas:
            return None

        return sorted(
            candidatas,
            key=lambda plantilla: plantilla.version,
            reverse=True,
        )[0]

    def listar_por_contexto(
        self,
        cod_recurso: str,
        cod_setor: str,
    ) -> list[PlantillaPreguntas]:
        cod_recurso_normalizado = str(cod_recurso or "").strip().upper()
        cod_setor_normalizado = str(cod_setor or "").strip().upper()

        return sorted(
            [
                plantilla
                for plantilla in self.listar_plantillas()
                if plantilla.cod_recurso == cod_recurso_normalizado
                and plantilla.cod_setor == cod_setor_normalizado
            ],
            key=lambda plantilla: plantilla.version,
        )

    def guardar(self, plantilla: PlantillaPreguntas) -> PlantillaPreguntas:
        plantillas = self.listar_plantillas()

        for indice, actual in enumerate(plantillas):
            if actual.id_plantilla == plantilla.id_plantilla:
                plantillas[indice] = plantilla
                self._guardar_todas(plantillas)
                return plantilla

        plantillas.append(plantilla)
        self._guardar_todas(plantillas)
        return plantilla

    def _guardar_todas(self, plantillas: list[PlantillaPreguntas]) -> None:
        JsonManager.write_json(
            str(self.file_path),
            [plantilla.to_dict() for plantilla in plantillas],
        )
