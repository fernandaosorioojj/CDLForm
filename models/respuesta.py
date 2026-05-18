"""Modelos de dominio usados para transportar formularios, preguntas, opciones y respuestas.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


# Bloque CDLform: clase Respuesta; agrupa estado y comportamiento de esta parte del flujo.
@dataclass
class Respuesta:
    id_respuesta: str
    id_formulario: str
    id_pregunta: str
    respuesta_texto: Optional[str] = None
    respuesta_numero: Optional[int] = None
    id_opcion: Optional[str] = None
    accion_correctiva_aplicada: Optional[str] = None
    fecha_creacion: str = ""

    # Bloque CDLform: funcion/metodo __post_init__; encapsula una operacion del flujo del modulo.
    def __post_init__(self) -> None:
        self.id_respuesta = str(self.id_respuesta).strip()
        self.id_formulario = str(self.id_formulario).strip()
        self.id_pregunta = str(self.id_pregunta).strip()

        if self.respuesta_texto is not None:
            self.respuesta_texto = str(self.respuesta_texto).strip()

        if self.id_opcion is not None:
            self.id_opcion = str(self.id_opcion).strip()

        if self.accion_correctiva_aplicada is not None:
            self.accion_correctiva_aplicada = str(
                self.accion_correctiva_aplicada
            ).strip()
        self.fecha_creacion = str(self.fecha_creacion or "").strip()

        if not self.id_respuesta:
            raise ValueError("id_respuesta es obligatorio.")

        if not self.id_formulario:
            raise ValueError("id_formulario es obligatorio.")

        if not self.id_pregunta:
            raise ValueError("id_pregunta es obligatorio.")

    # Bloque CDLform: funcion/metodo to_dict; encapsula una operacion del flujo del modulo.
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_respuesta": self.id_respuesta,
            "id_formulario": self.id_formulario,
            "id_pregunta": self.id_pregunta,
            "respuesta_texto": self.respuesta_texto,
            "respuesta_numero": self.respuesta_numero,
            "id_opcion": self.id_opcion,
            "accion_correctiva_aplicada": self.accion_correctiva_aplicada,
            "fecha_creacion": self.fecha_creacion,
        }

    # Bloque CDLform: funcion/metodo from_dict; encapsula una operacion del flujo del modulo.
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Respuesta":
        if not isinstance(data, dict):
            raise ValueError("Los datos de la respuesta deben venir en formato dict.")

        return cls(
            id_respuesta=data.get("id_respuesta", ""),
            id_formulario=data.get("id_formulario", ""),
            id_pregunta=data.get("id_pregunta", ""),
            respuesta_texto=data.get("respuesta_texto"),
            respuesta_numero=data.get("respuesta_numero"),
            id_opcion=data.get("id_opcion"),
            accion_correctiva_aplicada=data.get("accion_correctiva_aplicada"),
            fecha_creacion=data.get("fecha_creacion", ""),
        )
