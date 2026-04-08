from __future__ import annotations

from enum import Enum


class FormularioEstado(str, Enum):
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class DisparadorEstado(str, Enum):
    ABIERTO = "abierto"
    FALLIDO = "fallido"
    OMITIDO = "omitido"
    PROCESADO = "procesado"


class EventoEstadoProcesamiento(str, Enum):
    PENDIENTE = "pendiente"
    PROCESADO = "procesado"


class OrigenEvento(str, Enum):
    JOBTRACK = "jobtrack"
    MANUAL = "manual"
    SISTEMA_EXTERNO = "sistema_externo"


class TipoPregunta(str, Enum):
    TEXTO = "texto"
    NUMERO = "numero"
    SI_NO = "si_no"
    SELECCION_UNICA = "seleccion_unica"
    SELECCION_MULTIPLE = "seleccion_multiple"