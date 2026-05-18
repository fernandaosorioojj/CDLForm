"""Servicios de autenticacion, usuarios y hashes de acceso gestion.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import json
import hashlib
import hmac
import os
import secrets
from pathlib import Path

from config.settings import SETTINGS
from repositories.usuario_gestion_repository import UsuarioGestionRepository


HASH_ALGORITHM = "pbkdf2_sha256"
HASH_ITERATIONS = 260000
ROL_ADMIN = "admin"
ROL_GESTION = "gestion"


# Bloque CDLform: clase AuthService; agrupa estado y comportamiento de esta parte del flujo.
class AuthService:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        config_path: Path | None = None,
        usuario_gestion_repository: UsuarioGestionRepository | None = None,
    ) -> None:
        self.config_path = config_path or self._resolver_config_path(
            SETTINGS.paths.gestion_login_file,
            SETTINGS.paths.bundled_config_dir / "gestion_login.json",
        )
        self.legacy_config_path = self._resolver_config_path(
            SETTINGS.paths.admin_login_file,
            SETTINGS.paths.bundled_config_dir / "admin_login.json",
        )
        self.usuario_gestion_repository = (
            usuario_gestion_repository or UsuarioGestionRepository()
        )

    # Bloque CDLform: funcion/metodo _resolver_config_path; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _resolver_config_path(path_local: Path, path_bundled: Path) -> Path:
        if path_local.exists():
            return path_local
        return path_bundled

    # Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_texto(valor: object) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo normalizar_rol; encapsula una operacion del flujo del modulo.
    @classmethod
    def normalizar_rol(cls, valor: object) -> str:
        rol = cls._normalizar_texto(valor).lower()
        if rol in {ROL_ADMIN, ROL_GESTION}:
            return rol
        return ROL_GESTION

    # Bloque CDLform: funcion/metodo generar_password_hash; encapsula una operacion del flujo del modulo.
    @staticmethod
    def generar_password_hash(password: str) -> str:
        password_limpio = str(password or "")
        if not password_limpio:
            raise ValueError("password no puede venir vacio.")

        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password_limpio.encode("utf-8"),
            salt.encode("utf-8"),
            HASH_ITERATIONS,
        ).hex()
        return f"{HASH_ALGORITHM}${HASH_ITERATIONS}${salt}${digest}"

    # Bloque CDLform: funcion/metodo _validar_password_hash; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _validar_password_hash(password: str, password_hash: str) -> bool:
        partes = str(password_hash or "").split("$")
        if len(partes) != 4:
            return False

        algoritmo, iteraciones_raw, salt, digest_esperado = partes
        if algoritmo != HASH_ALGORITHM:
            return False

        try:
            iteraciones = int(iteraciones_raw)
        except ValueError:
            return False

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            str(password or "").encode("utf-8"),
            salt.encode("utf-8"),
            iteraciones,
        ).hex()
        return hmac.compare_digest(digest, digest_esperado)

    # Bloque CDLform: funcion/metodo _leer_credenciales_desde_entorno; encapsula una operacion del flujo del modulo.
    def _leer_credenciales_desde_entorno(self) -> dict[str, str] | None:
        # FALLBACK VIGENTE:
        # Solo se usa si SQL no entrega usuario activo. No es la fuente principal
        # de credenciales en el flujo actual de gestion.
        usuario = self._normalizar_texto(os.getenv("CDLFORM_GESTION_USER"))
        password_hash = self._normalizar_texto(
            os.getenv("CDLFORM_GESTION_PASSWORD_HASH")
        )

        if not usuario or not password_hash:
            usuario = self._normalizar_texto(os.getenv("CDLFORM_ADMIN_USER"))
            password_hash = self._normalizar_texto(
                os.getenv("CDLFORM_ADMIN_PASSWORD_HASH")
            )

        if usuario and password_hash:
            return {
                "usuario": usuario,
                "password_hash": password_hash,
                "rol": ROL_ADMIN,
            }

        return None

    # Bloque CDLform: funcion/metodo _leer_credenciales_desde_archivo; encapsula una operacion del flujo del modulo.
    def _leer_credenciales_desde_archivo(
        self,
        config_path: Path,
    ) -> dict[str, str] | None:
        # FALLBACK VIGENTE:
        # Lee gestion_login.json/admin_login.json para continuidad, pero la ruta
        # objetivo en produccion es usuarios_gestion en SQL Server.
        if not config_path.exists():
            return None

        data = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(
                f"El archivo de login {config_path} debe contener un objeto JSON."
            )

        usuario = self._normalizar_texto(data.get("usuario"))
        password_hash = self._normalizar_texto(data.get("password_hash"))
        rol = self.normalizar_rol(data.get("rol") or ROL_ADMIN)

        if usuario and password_hash:
            return {
                "usuario": usuario,
                "password_hash": password_hash,
                "rol": rol,
            }

        raise ValueError(
            f"El archivo de login {config_path} debe incluir "
            "'usuario' y 'password_hash'."
        )

    # Bloque CDLform: funcion/metodo obtener_credenciales_gestion; encapsula una operacion del flujo del modulo.
    def obtener_credenciales_gestion(self) -> dict[str, str]:
        credenciales_entorno = self._leer_credenciales_desde_entorno()
        if credenciales_entorno:
            return credenciales_entorno

        credenciales_archivo = self._leer_credenciales_desde_archivo(
            self.config_path
        )
        if credenciales_archivo:
            return credenciales_archivo

        credenciales_archivo = self._leer_credenciales_desde_archivo(
            self.legacy_config_path
        )
        if credenciales_archivo:
            return credenciales_archivo

        raise RuntimeError(
            "No hay credenciales de Gestion configuradas. "
            "Defina CDLFORM_GESTION_USER/CDLFORM_GESTION_PASSWORD_HASH o cree "
            f"{self.config_path}."
        )

    # Bloque CDLform: funcion/metodo obtener_credenciales_gestion_sql; encapsula una operacion del flujo del modulo.
    def obtener_credenciales_gestion_sql(
        self,
        usuario: str,
    ) -> dict[str, str] | None:
        # FLUJO ACTUAL:
        # SQL Server es la fuente principal de autenticacion de gestion.
        try:
            return self.usuario_gestion_repository.obtener_usuario_activo(usuario)
        except Exception:
            return None

    # Bloque CDLform: funcion/metodo obtener_credenciales_admin; encapsula una operacion del flujo del modulo.
    def obtener_credenciales_admin(self) -> dict[str, str]:
        # LEGACY:
        # Se conserva por compatibilidad con codigo antiguo que distinguia admin
        # de gestion por archivo. Hoy ambos pasan por obtener_credenciales_gestion().
        return self.obtener_credenciales_gestion()

    # Bloque CDLform: funcion/metodo autenticar_usuario; encapsula una operacion del flujo del modulo.
    def autenticar_usuario(self, usuario: str, password: str) -> dict[str, str] | None:
        usuario_ingresado = self._normalizar_texto(usuario)
        password_ingresado = self._normalizar_texto(password)

        if not usuario_ingresado or not password_ingresado:
            return None

        origen_sql = True
        credenciales = self.obtener_credenciales_gestion_sql(usuario_ingresado)
        if not credenciales:
            origen_sql = False
            credenciales = self.obtener_credenciales_gestion()

        usuario_configurado = self._normalizar_texto(credenciales.get("usuario"))
        password_hash_configurado = self._normalizar_texto(
            credenciales.get("password_hash")
        )
        rol = self.normalizar_rol(credenciales.get("rol"))

        if (
            usuario_ingresado == usuario_configurado
            and self._validar_password_hash(
                password_ingresado,
                password_hash_configurado,
            )
        ):
            if not origen_sql:
                self._sincronizar_credenciales_fallback_a_sql(
                    usuario=usuario_configurado,
                    password_hash=password_hash_configurado,
                    rol=rol,
                )
            return {
                "usuario": usuario_configurado,
                "rol": rol,
            }

        return None

    # Bloque CDLform: funcion/metodo _sincronizar_credenciales_fallback_a_sql; encapsula una operacion del flujo del modulo.
    def _sincronizar_credenciales_fallback_a_sql(
        self,
        usuario: str,
        password_hash: str,
        rol: str,
    ) -> None:
        # MIGRACION SUAVE:
        # Si el fallback JSON/env funciono, intenta dejar el usuario en SQL para
        # que el siguiente inicio use la ruta principal.
        try:
            self.usuario_gestion_repository.guardar_usuario(
                usuario=usuario,
                password_hash=password_hash,
                rol=self.normalizar_rol(rol or ROL_ADMIN),
                activo=True,
            )
        except Exception:
            return

    # Bloque CDLform: funcion/metodo validar_login; encapsula una operacion del flujo del modulo.
    def validar_login(self, usuario: str, password: str) -> bool:
        return self.autenticar_usuario(usuario, password) is not None
