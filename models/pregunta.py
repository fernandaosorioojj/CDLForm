from __future__ import annotations

from dataclasses import dataclass, field

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

        filtros_normalizados: dict[str, list[str]] = {}

        if not isinstance(self.filtros_contexto, dict):
            raise TypeError("filtros_contexto debe ser un diccionario")

        for clave, valores in self.filtros_contexto.items():
            if not isinstance(clave, str) or not clave.strip():
                raise ValueError("cada clave de filtros_contexto debe ser un string no vacío")

            if valores is None:
                filtros_normalizados[clave.strip()] = []
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

                valor_upper = valor_limpio.upper()
                if valor_upper not in vistos:
                    vistos.add(valor_upper)
                    lista_limpia.append(valor_limpio)

            filtros_normalizados[clave.strip()] = lista_limpia

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

        if self.tipo in {TipoPregunta.SI_NO, TipoPregunta.SELECCION_UNICA}:
            if not self.opciones_respuesta:
                raise ValueError(
                    "la pregunta debe tener opciones_respuesta para tipo si_no o seleccion_unica"
                )

        if self.tipo in {TipoPregunta.TEXTO, TipoPregunta.NUMERO}:
            if self.opciones_respuesta:
                raise ValueError(
                    "las preguntas de tipo texto o numero no deben tener opciones_respuesta"
                )

    def to_dict(self) -> dict:
        return {
            "id_pregunta": self.id_pregunta,
            "texto": self.texto,
            "tipo": self.tipo.value,
            "activa": self.activa,
            "obligatoria": self.obligatoria,
            "orden": self.orden,
            "filtros_contexto": self.filtros_contexto,
            "opciones_respuesta": [op.to_dict() for op in self.opciones_respuesta],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pregunta":
        return cls(
            id_pregunta=data["id_pregunta"],
            texto=data["texto"],
            tipo=TipoPregunta(data["tipo"]),
            activa=data.get("activa", True),
            obligatoria=data.get("obligatoria", True),
            orden=data.get("orden", 1),
            filtros_contexto=data.get("filtros_contexto", {}),
            opciones_respuesta=data.get("opciones_respuesta", []),
        )