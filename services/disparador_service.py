from __future__ import annotations

from typing import Any

from launcher.app_launcher import AppLauncher
from services.formulario_service import FormularioService


class DisparadorService:
    def __init__(
        self,
        formulario_service: FormularioService | None = None,
        app_launcher: AppLauncher | None = None,
    ) -> None:
        self.formulario_service = formulario_service or FormularioService()
        self.app_launcher = app_launcher or AppLauncher(
            formulario_service=self.formulario_service
        )
        self._formularios_en_apertura: set[str] = set()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def _liberar_formulario_en_apertura(self, formulario: dict[str, Any]) -> None:
        id_formulario = self._normalizar_texto(formulario.get("id_formulario"))

        if id_formulario in self._formularios_en_apertura:
            self._formularios_en_apertura.remove(id_formulario)

        formulario_actual = self.formulario_service.obtener_formulario_por_id(
            id_formulario
        )

        if not formulario_actual:
            return

        estado_actual = self._normalizar_texto(formulario_actual.get("estado"))

        if estado_actual == "en_apertura":
            self.formulario_service.marcar_formulario_pendiente_operario(id_formulario)

    def listar_formularios_pendientes_operario(self) -> list[dict]:
        return self.formulario_service.listar_formularios_pendientes_operario()

    def obtener_siguiente_formulario_pendiente(self) -> dict | None:
        for formulario in self.listar_formularios_pendientes_operario():
            id_formulario = self._normalizar_texto(formulario.get("id_formulario"))
            if id_formulario not in self._formularios_en_apertura:
                return formulario

        return None

    def disparar_siguiente_formulario_pendiente(self) -> dict[str, Any]:
        formulario = self.obtener_siguiente_formulario_pendiente()

        if not formulario:
            return {
                "se_abrio": False,
                "motivo": "sin_formularios_pendientes",
                "formulario": None,
            }

        id_formulario = self._normalizar_texto(formulario.get("id_formulario"))
        self._formularios_en_apertura.add(id_formulario)
        self.formulario_service.marcar_formulario_en_apertura(id_formulario)

        try:
            resultado_lanzamiento = self.app_launcher.abrir_formulario_pendiente_operario(
                formulario=formulario,
                on_close=self._liberar_formulario_en_apertura,
            )

            return {
                "se_abrio": True,
                "motivo": "formulario_lanzado",
                "formulario": self.formulario_service.obtener_formulario_por_id(
                    id_formulario
                ),
                "resultado_lanzamiento": resultado_lanzamiento,
            }

        except Exception:
            self._liberar_formulario_en_apertura(formulario)
            raise

    def procesar_formularios_pendientes(self, maximo: int = 1) -> dict[str, Any]:
        abiertos: list[dict[str, Any]] = []
        maximo_normalizado = max(1, int(maximo))

        for _ in range(maximo_normalizado):
            resultado = self.disparar_siguiente_formulario_pendiente()

            if not resultado["se_abrio"]:
                break

            abiertos.append(resultado)

        return {
            "total_abiertos": len(abiertos),
            "formularios_abiertos": abiertos,
        }