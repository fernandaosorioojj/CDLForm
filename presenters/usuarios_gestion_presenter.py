from __future__ import annotations

from typing import Any

from repositories.usuario_gestion_repository import UsuarioGestionRepository
from services.security.auth_service import AuthService


class UsuariosGestionPresenter:
    def __init__(
        self,
        usuario_repository: UsuarioGestionRepository | None = None,
    ) -> None:
        self.usuario_repository = usuario_repository or UsuarioGestionRepository()

    @staticmethod
    def normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def listar_usuarios(self) -> list[dict[str, Any]]:
        return self.usuario_repository.listar_usuarios()

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

    def actualizar_activo(self, usuario: str, activo: bool) -> str:
        usuario_normalizado = self.normalizar_texto(usuario)
        if not usuario_normalizado:
            raise ValueError("Selecciona un usuario primero.")

        self.usuario_repository.actualizar_activo(usuario_normalizado, activo)
        return "Estado del usuario actualizado correctamente."

    def actualizar_rol(self, usuario: str, rol: str) -> str:
        usuario_normalizado = self.normalizar_texto(usuario)
        if not usuario_normalizado:
            raise ValueError("Selecciona un usuario primero.")

        self.usuario_repository.actualizar_rol(usuario_normalizado, rol)
        return "Rol actualizado correctamente."
