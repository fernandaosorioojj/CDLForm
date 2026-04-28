from __future__ import annotations

from datetime import datetime
from typing import Any

from models.plantilla_preguntas import PlantillaPreguntaItem, PlantillaPreguntas
from repositories.plantilla_preguntas_repository import PlantillaPreguntasRepository


class PlantillaPreguntasService:
    def __init__(
        self,
        repository: PlantillaPreguntasRepository | None = None,
    ) -> None:
        self.repository = repository or PlantillaPreguntasRepository()

    @staticmethod
    def normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @classmethod
    def normalizar_contexto(cls, valor: Any) -> str:
        return cls.normalizar_texto(valor).upper()

    def obtener_activa(
        self,
        cod_recurso: str,
        cod_setor: str,
    ) -> PlantillaPreguntas | None:
        cod_recurso_normalizado = self.normalizar_contexto(cod_recurso)
        cod_setor_normalizado = self.normalizar_contexto(cod_setor)

        if not cod_recurso_normalizado or not cod_setor_normalizado:
            return None

        return self.repository.obtener_activa(
            cod_recurso=cod_recurso_normalizado,
            cod_setor=cod_setor_normalizado,
        )

    def asegurar_plantilla_contexto(
        self,
        cod_recurso: str,
        cod_setor: str,
        preguntas: list[dict[str, Any]],
    ) -> PlantillaPreguntas | None:
        cod_recurso_normalizado = self.normalizar_contexto(cod_recurso)
        cod_setor_normalizado = self.normalizar_contexto(cod_setor)

        if not cod_recurso_normalizado or not cod_setor_normalizado:
            return None

        preguntas_ordenadas = [
            pregunta
            for pregunta in sorted(
                preguntas,
                key=lambda item: (
                    int(item.get("orden", 9999))
                    if str(item.get("orden", "")).strip().isdigit()
                    else 9999,
                    str(item.get("id_pregunta", "")).strip(),
                ),
            )
            if str(pregunta.get("id_pregunta", "")).strip()
        ]

        if not preguntas_ordenadas:
            return None

        activa_actual = self.obtener_activa(
            cod_recurso=cod_recurso_normalizado,
            cod_setor=cod_setor_normalizado,
        )
        items_deseados = [
            (
                str(pregunta.get("id_pregunta", "")).strip(),
                int(pregunta.get("orden", 1)),
            )
            for pregunta in preguntas_ordenadas
        ]

        if activa_actual:
            items_actuales = [
                (item.id_pregunta, int(item.orden))
                for item in sorted(
                    activa_actual.items,
                    key=lambda item: (int(item.orden), item.id_pregunta),
                )
            ]
            if items_actuales == items_deseados:
                return activa_actual

        return self.crear_nueva_version(
            cod_recurso=cod_recurso_normalizado,
            cod_setor=cod_setor_normalizado,
            preguntas=preguntas_ordenadas,
        )

    def crear_nueva_version(
        self,
        cod_recurso: str,
        cod_setor: str,
        preguntas: list[dict[str, Any]],
    ) -> PlantillaPreguntas | None:
        cod_recurso_normalizado = self.normalizar_contexto(cod_recurso)
        cod_setor_normalizado = self.normalizar_contexto(cod_setor)

        if not cod_recurso_normalizado or not cod_setor_normalizado:
            return None

        clave_plantilla = f"TPL-{cod_setor_normalizado}-{cod_recurso_normalizado}"
        activa_actual = self.repository.obtener_activa(
            cod_recurso=cod_recurso_normalizado,
            cod_setor=cod_setor_normalizado,
        )
        siguiente_version = 1
        ahora = datetime.now().isoformat(timespec="seconds")

        if activa_actual:
            siguiente_version = activa_actual.version + 1
            self.repository.guardar(
                PlantillaPreguntas(
                    id_plantilla=activa_actual.id_plantilla,
                    clave_plantilla=activa_actual.clave_plantilla,
                    cod_recurso=activa_actual.cod_recurso,
                    cod_setor=activa_actual.cod_setor,
                    version=activa_actual.version,
                    activa=False,
                    fecha_creacion=activa_actual.fecha_creacion,
                    fecha_desactivacion=ahora,
                    items=activa_actual.items,
                )
            )

        items = [
            PlantillaPreguntaItem(
                id_pregunta=str(pregunta.get("id_pregunta", "")).strip(),
                orden=int(pregunta.get("orden", 1)),
            )
            for pregunta in preguntas
            if str(pregunta.get("id_pregunta", "")).strip()
        ]

        plantilla = PlantillaPreguntas(
            id_plantilla=f"{clave_plantilla}-V{siguiente_version:03d}",
            clave_plantilla=clave_plantilla,
            cod_recurso=cod_recurso_normalizado,
            cod_setor=cod_setor_normalizado,
            version=siguiente_version,
            activa=True,
            fecha_creacion=ahora,
            items=items,
        )

        return self.repository.guardar(plantilla)
