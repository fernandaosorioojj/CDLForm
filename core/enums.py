"""Primitivas de dominio compartidas por modelos y servicios: enums, errores y validaciones.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from enum import Enum


# Usado por modelos y servicios para validar los tipos de pregunta configurables.
class TipoPregunta(str, Enum):
    TEXTO = "texto"
    NUMERO = "numero"
    SI_NO = "si_no"
    SELECCION_UNICA = "seleccion_unica"
    SELECCION_MULTIPLE = "seleccion_multiple"


# Clases no usadas por el flujo actual.
# Se dejan comentadas para no presentar codigo inactivo como parte vigente del dominio.
#
# class FormularioEstado(str, Enum):
#     EN_PROGRESO = "en_progreso"
#     COMPLETADO = "completado"
#     CANCELADO = "cancelado"
#
#
# class DisparadorEstado(str, Enum):
#     ABIERTO = "abierto"
#     FALLIDO = "fallido"
#     OMITIDO = "omitido"
#     PROCESADO = "procesado"
#
#
# class EventoEstadoProcesamiento(str, Enum):
#     PENDIENTE = "pendiente"
#     PROCESADO = "procesado"
#
#
# class OrigenEvento(str, Enum):
#     JOBTRACK = "jobtrack"
#     MANUAL = "manual"
#     SISTEMA_EXTERNO = "sistema_externo"
