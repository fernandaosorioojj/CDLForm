from __future__ import annotations


class CDLformError(Exception):
    """excepción base del dominio de la aplicación."""


class ValidationError(CDLformError):
    """error para datos inválidos de entrada."""


class RepositoryError(CDLformError):
    """error al leer o persistir datos."""


class NotFoundError(CDLformError):
    """error cuando un recurso requerido no existe."""


class DuplicateEntityError(CDLformError):
    """error cuando se intenta crear un registro duplicado."""


class BusinessRuleError(CDLformError):
    """error cuando una regla de negocio no se cumple."""


class ConfigurationError(CDLformError):
    """error de configuración de la aplicación."""