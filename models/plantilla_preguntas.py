from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _normalizar_texto(valor: Any) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


@dataclass(frozen=True)
class PlantillaPreguntaItem:
    id_pregunta: str
    orden: int = 1

    def __post_init__(self) -> None:
        id_pregunta = _normalizar_texto(self.id_pregunta)
        if not id_pregunta:
            raise ValueError("id_pregunta es obligatorio")

        if not isinstance(self.orden, int):
            raise TypeError("orden debe ser un entero")
        if self.orden <= 0:
            raise ValueError("orden debe ser mayor que 0")

        object.__setattr__(self, "id_pregunta", id_pregunta)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_pregunta": self.id_pregunta,
            "orden": self.orden,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlantillaPreguntaItem":
        return cls(
            id_pregunta=data.get("id_pregunta", ""),
            orden=int(data.get("orden", 1)),
        )


@dataclass(frozen=True)
class PlantillaPreguntas:
    id_plantilla: str
    cod_recurso: str
    cod_setor: str
    version: int
    clave_plantilla: str = ""
    activa: bool = True
    fecha_creacion: str = ""
    fecha_desactivacion: str = ""
    items: list[PlantillaPreguntaItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        id_plantilla = _normalizar_texto(self.id_plantilla)
        cod_recurso = _normalizar_texto(self.cod_recurso).upper()
        cod_setor = _normalizar_texto(self.cod_setor).upper()
        clave_plantilla = _normalizar_texto(self.clave_plantilla)

        if not id_plantilla:
            raise ValueError("id_plantilla es obligatorio")
        if not cod_recurso:
            raise ValueError("cod_recurso es obligatorio")
        if not cod_setor:
            raise ValueError("cod_setor es obligatorio")

        if not isinstance(self.version, int):
            raise TypeError("version debe ser un entero")
        if self.version <= 0:
            raise ValueError("version debe ser mayor que 0")

        if not isinstance(self.activa, bool):
            raise TypeError("activa debe ser booleano")

        items_normalizados: list[PlantillaPreguntaItem] = []
        for item in self.items:
            if isinstance(item, PlantillaPreguntaItem):
                items_normalizados.append(item)
            elif isinstance(item, dict):
                items_normalizados.append(PlantillaPreguntaItem.from_dict(item))
            else:
                raise TypeError("items debe contener PlantillaPreguntaItem o dict")

        object.__setattr__(self, "id_plantilla", id_plantilla)
        object.__setattr__(
            self,
            "clave_plantilla",
            clave_plantilla or f"TPL-{cod_setor}-{cod_recurso}",
        )
        object.__setattr__(self, "cod_recurso", cod_recurso)
        object.__setattr__(self, "cod_setor", cod_setor)
        object.__setattr__(
            self,
            "fecha_creacion",
            _normalizar_texto(self.fecha_creacion),
        )
        object.__setattr__(
            self,
            "fecha_desactivacion",
            _normalizar_texto(self.fecha_desactivacion),
        )
        object.__setattr__(self, "items", items_normalizados)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_plantilla": self.id_plantilla,
            "clave_plantilla": self.clave_plantilla,
            "cod_recurso": self.cod_recurso,
            "cod_setor": self.cod_setor,
            "version": self.version,
            "activa": self.activa,
            "fecha_creacion": self.fecha_creacion,
            "fecha_desactivacion": self.fecha_desactivacion,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlantillaPreguntas":
        return cls(
            id_plantilla=data.get("id_plantilla", ""),
            clave_plantilla=data.get("clave_plantilla", ""),
            cod_recurso=data.get("cod_recurso", ""),
            cod_setor=data.get("cod_setor", ""),
            version=int(data.get("version", 1)),
            activa=data.get("activa", True),
            fecha_creacion=data.get("fecha_creacion", ""),
            fecha_desactivacion=data.get("fecha_desactivacion", ""),
            items=data.get("items", []),
        )
