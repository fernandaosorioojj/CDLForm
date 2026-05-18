"""Capa presenter que conecta vistas PyQt con servicios de negocio.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from typing import Any

from repositories.usuario_gestion_repository import UsuarioGestionRepository
from services.security.auth_service import AuthService


# Bloque CDLform: clase UsuariosGestionPresenter; agrupa estado y comportamiento de esta parte del flujo.
class UsuariosGestionPresenter:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        usuario_repository: UsuarioGestionRepository | None = None,
    ) -> None:
        self.usuario_repository = usuario_repository or UsuarioGestionRepository()

    # Bloque CDLform: funcion/metodo normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo listar_usuarios; encapsula una operacion del flujo del modulo.
    def listar_usuarios(self) -> list[dict[str, Any]]:
        return self.usuario_repository.listar_usuarios()

    # Bloque CDLform: funcion/metodo crear_o_actualizar_usuario; encapsula una operacion del flujo del modulo.
    def crear_o_actualizar_usuario(
        self,
        usuario: str,
        password: str,
        rol: str = "gestion",
        activo: bool = True,
    ) -> str:
        usuario_normalizado = self.normalizar_texto(usuario)
        password_limpio = str(password or "")
        if not usuario_normalizado:
            raise ValueError("El usuario es obligatorio.")
        if not password_limpio:
            raise ValueError("La contrasena es obligatoria.")

        password_hash = AuthService.generar_password_hash(password_limpio)
        self.usuario_repository.guardar_usuario(
            usuario=usuario_normalizado,
            password_hash=password_hash,
            rol=rol,
            activo=activo,
        )
        return "Usuario guardado correctamente."

    # Bloque CDLform: funcion/metodo cambiar_password; encapsula una operacion del flujo del modulo.
    def cambiar_password(self, usuario: str, password: str) -> str:
        usuario_normalizado = self.normalizar_texto(usuario)
        password_limpio = str(password or "")
        if not usuario_normalizado:
            raise ValueError("Selecciona un usuario primero.")
        if not password_limpio:
            raise ValueError("La nueva contrasena es obligatoria.")

        password_hash = AuthService.generar_password_hash(password_limpio)
        self.usuario_repository.cambiar_password(
            usuario=usuario_normalizado,
            password_hash=password_hash,
        )
        return "Contrasena actualizada correctamente."

    # Bloque CDLform: funcion/metodo actualizar_activo; encapsula una operacion del flujo del modulo.
    def actualizar_activo(self, usuario: str, activo: bool) -> str:
        usuario_normalizado = self.normalizar_texto(usuario)
        if not usuario_normalizado:
            raise ValueError("Selecciona un usuario primero.")

        self.usuario_repository.actualizar_activo(usuario_normalizado, activo)
        return "Estado del usuario actualizado correctamente."

    # Bloque CDLform: funcion/metodo actualizar_rol; encapsula una operacion del flujo del modulo.
    def actualizar_rol(self, usuario: str, rol: str) -> str:
        usuario_normalizado = self.normalizar_texto(usuario)
        if not usuario_normalizado:
            raise ValueError("Selecciona un usuario primero.")

        self.usuario_repository.actualizar_rol(usuario_normalizado, rol)
        return "Rol actualizado correctamente."
