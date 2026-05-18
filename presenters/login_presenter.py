"""Capa presenter que conecta vistas PyQt con servicios de negocio.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from services.security.auth_service import AuthService


# Bloque CDLform: clase LoginPresenter; agrupa estado y comportamiento de esta parte del flujo.
class LoginPresenter:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, auth_service: AuthService | None = None) -> None:
        self.auth_service = auth_service or AuthService()

    # Bloque CDLform: funcion/metodo normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def normalizar_texto(valor: object) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo validar_credenciales_ingresadas; encapsula una operacion del flujo del modulo.
    def validar_credenciales_ingresadas(
        self,
        usuario: str,
        password: str,
    ) -> tuple[bool, str]:
        if not self.normalizar_texto(usuario) or not self.normalizar_texto(password):
            return False, "Debes ingresar usuario y contrasena."
        return True, ""

    # Bloque CDLform: funcion/metodo iniciar_sesion; encapsula una operacion del flujo del modulo.
    def iniciar_sesion(self, usuario: str, password: str) -> bool:
        return self.auth_service.validar_login(usuario, password)

    # Bloque CDLform: funcion/metodo autenticar_usuario; encapsula una operacion del flujo del modulo.
    def autenticar_usuario(self, usuario: str, password: str) -> dict[str, str] | None:
        return self.auth_service.autenticar_usuario(usuario, password)


