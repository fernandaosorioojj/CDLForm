"""Coordinacion de apertura de ventanas y formularios pendientes en el cliente operario.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import inspect
from typing import Any, Callable

from PyQt5.QtWidgets import QApplication

from services.forms.formulario_service import FormularioService
from services.forms.pregunta_service import PreguntaService
from services.forms.respuesta_service import RespuestaService
from ui.formulario_operario import FormularioOperarioView


# Bloque CDLform: clase AppLauncher; agrupa estado y comportamiento de esta parte del flujo.
class AppLauncher:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        formulario_service: FormularioService | None = None,
        pregunta_service: PreguntaService | None = None,
        respuesta_service: RespuestaService | None = None,
    ) -> None:
        self.formulario_service = formulario_service or FormularioService()
        self.pregunta_service = pregunta_service or PreguntaService()
        self.respuesta_service = respuesta_service or RespuestaService()
        self._ventanas_abiertas: list[Any] = []

    # Bloque CDLform: funcion/metodo tiene_ventanas_abiertas; encapsula una operacion del flujo del modulo.
    def tiene_ventanas_abiertas(self) -> bool:
        return bool(self._ventanas_abiertas)

    # Bloque CDLform: funcion/metodo _obtener_o_crear_app; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _obtener_o_crear_app() -> tuple[QApplication, bool]:
        app = QApplication.instance()
        if app is not None:
            return app, False

        return QApplication([]), True

    # Bloque CDLform: funcion/metodo _mostrar_view; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _mostrar_view(view: Any) -> None:
        if hasattr(view, "showMaximized"):
            view.showMaximized()
            return

        if hasattr(view, "show"):
            view.show()
            return

        raise ValueError("La vista no tiene mÃ©todos show ni showMaximized.")

    # Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo _obtener_valor_formulario; encapsula una operacion del flujo del modulo.
    @classmethod
    def _obtener_valor_formulario(
        cls,
        formulario: Any,
        clave: str,
        default: Any = None,
    ) -> Any:
        if hasattr(formulario, "get"):
            return formulario.get(clave, default)
        return getattr(formulario, clave, default)

    # Bloque CDLform: funcion/metodo _obtener_operario_formulario; encapsula una operacion del flujo del modulo.
    @classmethod
    def _obtener_operario_formulario(cls, formulario: Any) -> str:
        return cls._normalizar_texto(
            cls._obtener_valor_formulario(formulario, "operario")
            or cls._obtener_valor_formulario(formulario, "operador")
        )

    # Bloque CDLform: funcion/metodo _instanciar_formulario_operario_view; encapsula una operacion del flujo del modulo.
    def _instanciar_formulario_operario_view(
        self,
        formulario: Any,
        on_close: Callable[[dict[str, Any]], None] | None = None,
    ) -> Any:
        operario = self._obtener_operario_formulario(formulario)
        kwargs_disponibles = {
            "formulario": formulario,
            "formulario_service": self.formulario_service,
            "pregunta_service": self.pregunta_service,
            "respuesta_service": self.respuesta_service,
            "operario": operario,
        }

        signature = inspect.signature(FormularioOperarioView.__init__)
        kwargs_aceptados: dict[str, Any] = {}

        for nombre_parametro in list(signature.parameters.keys())[1:]:
            if nombre_parametro in kwargs_disponibles:
                kwargs_aceptados[nombre_parametro] = kwargs_disponibles[
                    nombre_parametro
                ]

        errores: list[str] = []

        try:
            return FormularioOperarioView(**kwargs_aceptados)
        except TypeError as exc:
            errores.append(str(exc))

        intentos = [
            lambda: FormularioOperarioView(formulario=formulario, operario=operario),
            lambda: FormularioOperarioView(formulario),
            lambda: FormularioOperarioView(),
        ]

        for intento in intentos:
            try:
                return intento()
            except TypeError as exc:
                errores.append(str(exc))

        raise RuntimeError(
            "No se pudo instanciar FormularioOperarioView con las firmas probadas. "
            f"Errores detectados: {' | '.join(errores)}"
        )

    # Bloque CDLform: funcion/metodo abrir_formulario_pendiente_operario; encapsula una operacion del flujo del modulo.
    def abrir_formulario_pendiente_operario(
        self,
        formulario: dict[str, Any],
        on_close: Callable[[dict[str, Any]], None] | None = None,
    ) -> dict[str, Any]:
        app, app_creada = self._obtener_o_crear_app()
        view = self._instanciar_formulario_operario_view(
            formulario=formulario,
            on_close=on_close,
        )
        self._ventanas_abiertas.append(view)

        if hasattr(view, "destroyed"):
            view.destroyed.connect(
                lambda *args, ventana=view: self._liberar_ventana(ventana)
            )

        if on_close is not None and hasattr(view, "destroyed"):
            view.destroyed.connect(lambda *args: on_close(formulario))

        self._mostrar_view(view)

        exit_code = None
        if app_creada:
            exit_code = app.exec_()

        return {
            "app_creada": app_creada,
            "exit_code": exit_code,
            "formulario": formulario,
        }

    # Bloque CDLform: funcion/metodo _liberar_ventana; encapsula una operacion del flujo del modulo.
    def _liberar_ventana(self, ventana: Any) -> None:
        if ventana in self._ventanas_abiertas:
            self._ventanas_abiertas.remove(ventana)
