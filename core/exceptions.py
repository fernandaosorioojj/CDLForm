"""Primitivas de dominio compartidas por modelos y servicios: enums, errores y validaciones.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations


# Base comun para errores propios del dominio CDLform.
class CDLformError(Exception):
    """excepción base del dominio de la aplicación."""


# Usado por validadores, servicios y utilidades cuando un dato de entrada no es valido.
class ValidationError(CDLformError):
    """error para datos inválidos de entrada."""


# Usado por servicios cuando un recurso requerido no existe.
class NotFoundError(CDLformError):
    """error cuando un recurso requerido no existe."""


# Clases no usadas por el flujo actual.
# Se dejan comentadas para no presentar codigo inactivo como parte vigente del dominio.
#
# class RepositoryError(CDLformError):
#     """error al leer o persistir datos."""
#
#
# class DuplicateEntityError(CDLformError):
#     """error cuando se intenta crear un registro duplicado."""
#
#
# class BusinessRuleError(CDLformError):
#     """error cuando una regla de negocio no se cumple."""
#
#
# class ConfigurationError(CDLformError):
#     """error de configuración de la aplicación."""
