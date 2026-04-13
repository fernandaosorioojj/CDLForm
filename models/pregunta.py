from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.enums import TipoPregunta
from core.validators import require_bool, require_non_empty_string
from models.opcion_pregunta import OpcionPregunta


@dataclass(frozen=True)
class Pregunta:
    id_pregunta: str
    texto: str
    tipo: TipoPregunta
    activa: bool = True
    obligatoria: bool = True
    orden: int = 1
    version: int = 1
    clave_pregunta: str = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""
    fecha_desactivacion: str = ""
    reemplazada_por: str = ""

    filtros_contexto: dict[str, list[str]] = field(default_factory=dict)
    opciones_respuesta: list[OpcionPregunta] = field(default_factory=list)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "id_pregunta",
            require_non_empty_string(self.id_pregunta, "id_pregunta"),
        )
        object.__setattr__(
            self,
            "texto",
            require_non_empty_string(self.texto, "texto"),
        )

        if not isinstance(self.tipo, TipoPregunta):
            raise TypeError("tipo debe ser una instancia de TipoPregunta")

        object.__setattr__(self, "activa", require_bool(self.activa, "activa"))
        object.__setattr__(self, "obligatoria", require_bool(self.obligatoria, "obligatoria"))

        if not isinstance(self.orden, int):
            raise TypeError("orden debe ser un entero")
        if self.orden <= 0:
            raise ValueError("orden debe ser mayor que 0")

        if not isinstance(self.version, int):
            raise TypeError("version debe ser un entero")
        if self.version <= 0:
            raise ValueError("version debe ser mayor que 0")

        object.__setattr__(
            self,
            "clave_pregunta",
            self.clave_pregunta.strip() if self.clave_pregunta else self.id_pregunta,
        )
        object.__setattr__(
            self,
            "fecha_creacion",
            self.fecha_creacion.strip() if self.fecha_creacion else "",
        )
        object.__setattr__(
            self,
            "fecha_actualizacion",
            self.fecha_actualizacion.strip() if self.fecha_actualizacion else "",
        )
        object.__setattr__(
            self,
            "fecha_desactivacion",
            self.fecha_desactivacion.strip() if self.fecha_desactivacion else "",
        )
        object.__setattr__(
            self,
            "reemplazada_por",
            self.reemplazada_por.strip() if self.reemplazada_por else "",
        )

        filtros_normalizados: dict[str, list[str]] = {}

        if not isinstance(self.filtros_contexto, dict):
            raise TypeError("filtros_contexto debe ser un diccionario")

        for clave, valores in self.filtros_contexto.items():
            if not isinstance(clave, str) or not clave.strip():
                raise ValueError("cada clave de filtros_contexto debe ser un string no vacío")

            clave_normalizada = self._normalizar_clave_filtro(clave)

            if valores is None:
                filtros_normalizados[clave_normalizada] = []
                continue

            if not isinstance(valores, list):
                raise TypeError(
                    f"el filtro '{clave}' debe contener una lista de strings"
                )

            lista_limpia: list[str] = []
            vistos: set[str] = set()

            for valor in valores:
                if not isinstance(valor, str):
                    raise TypeError(
                        f"el filtro '{clave}' debe contener solo strings"
                    )

                valor_limpio = valor.strip()
                if not valor_limpio:
                    continue

                valor_normalizado = valor_limpio.upper()
                if valor_normalizado not in vistos:
                    vistos.add(valor_normalizado)
                    lista_limpia.append(valor_normalizado)

            filtros_normalizados[clave_normalizada] = lista_limpia

        object.__setattr__(self, "filtros_contexto", filtros_normalizados)

        opciones_normalizadas: list[OpcionPregunta] = []
        for opcion in self.opciones_respuesta:
            if isinstance(opcion, OpcionPregunta):
                opciones_normalizadas.append(opcion)
            elif isinstance(opcion, dict):
                opciones_normalizadas.append(OpcionPregunta.from_dict(opcion))
            else:
                raise TypeError(
                    "opciones_respuesta debe contener instancias de OpcionPregunta o dict"
                )

        object.__setattr__(self, "opciones_respuesta", opciones_normalizadas)

        if self.tipo in {
            TipoPregunta.SI_NO,
            TipoPregunta.SELECCION_UNICA,
            TipoPregunta.SELECCION_MULTIPLE,
        }:
            if not self.opciones_respuesta:
                raise ValueError(
                    "la pregunta debe tener opciones_respuesta para tipo si_no, seleccion_unica o seleccion_multiple"
                )

        if self.tipo in {TipoPregunta.TEXTO, TipoPregunta.NUMERO}:
            if self.opciones_respuesta:
                raise ValueError(
                    "las preguntas de tipo texto o numero no deben tener opciones_respuesta"
                )

    def _normalizar_clave_filtro(self, clave: str) -> str:
        clave_limpia = clave.strip().lower()

        aliases = {
            "codsetor": "cod_setor",
            "cod_setor": "cod_setor",
            "codrecurso": "cod_recurso",
            "cod_recurso": "cod_recurso",
            "tipotrabajo": "tipo_trabajo",
            "tipo_trabajo": "tipo_trabajo",
            "turno": "turno",
        }

        return aliases.get(clave_limpia, clave_limpia)

    def to_dict(self) -> dict:
        return {
            "id_pregunta": self.id_pregunta,
            "texto": self.texto,
            "tipo": self.tipo.value,
            "activa": self.activa,
            "obligatoria": self.obligatoria,
            "orden": self.orden,
            "version": self.version,
            "clave_pregunta": self.clave_pregunta,
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion,
            "fecha_desactivacion": self.fecha_desactivacion,
            "reemplazada_por": self.reemplazada_por,
            "filtros_contexto": self.filtros_contexto,
            "opciones_respuesta": [op.to_dict() for op in self.opciones_respuesta],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Pregunta":
        return cls(
            id_pregunta=data["id_pregunta"],
            texto=data["texto"],
            tipo=TipoPregunta(data["tipo"]),
            activa=data.get("activa", True),
            obligatoria=data.get("obligatoria", True),
            orden=data.get("orden", 1),
            version=data.get("version", 1),
            clave_pregunta=data.get("clave_pregunta", data["id_pregunta"]),
            fecha_creacion=data.get("fecha_creacion", ""),
            fecha_actualizacion=data.get("fecha_actualizacion", ""),
            fecha_desactivacion=data.get("fecha_desactivacion", ""),
            reemplazada_por=data.get("reemplazada_por", ""),
            filtros_contexto=data.get("filtros_contexto", {}),
            opciones_respuesta=data.get("opciones_respuesta", []),
        )
