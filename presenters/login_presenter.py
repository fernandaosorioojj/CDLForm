from __future__ import annotations

from services.security.auth_service import AuthService


class LoginPresenter:
    def __init__(self, auth_service: AuthService | None = None) -> None:
        self.auth_service = auth_service or AuthService()

    @staticmethod
    def normalizar_texto(valor: object) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def validar_credenciales_ingresadas(
        self,
        usuario: str,
        password: str,
    ) -> tuple[bool, str]:
        if not self.normalizar_texto(usuario) or not self.normalizar_texto(password):
            return False, "Debes ingresar usuario y contrasena."
        return True, ""

    def iniciar_sesion(self, usuario: str, password: str) -> bool:
        return self.auth_service.validar_login(usuario, password)


