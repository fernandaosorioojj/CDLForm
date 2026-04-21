from __future__ import annotations

from typing import Any

from services.forms.formulario_service import FormularioService


class DisparadorService:
    def __init__(
        self,
        formulario_service: FormularioService | None = None,
    ) -> None:
        self.formulario_service = formulario_service or FormularioService()
        self._formularios_en_apertura: set[str] = set()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def liberar_formulario_en_apertura(self, formulario: dict[str, Any]) -> None:
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
            self.formulario_service.marcar_formulario_pendiente_operario(
                id_formulario
            )

    def listar_formularios_pendientes_operario(self) -> list[dict]:
        return self.formulario_service.listar_formularios_pendientes_operario()

    def obtener_siguiente_formulario_pendiente(self) -> dict | None:
        for formulario in self.listar_formularios_pendientes_operario():
            id_formulario = self._normalizar_texto(formulario.get("id_formulario"))
            if id_formulario not in self._formularios_en_apertura:
                return formulario

        return None

    def preparar_siguiente_formulario_pendiente(self) -> dict[str, Any]:
        formulario = self.obtener_siguiente_formulario_pendiente()

        if not formulario:
            return {
                "se_preparo": False,
                "motivo": "sin_formularios_pendientes",
                "formulario": None,
            }

        return self.preparar_formulario_pendiente(formulario)

    def preparar_formulario_pendiente(
        self,
        formulario: dict[str, Any],
    ) -> dict[str, Any]:
        id_formulario = self._normalizar_texto(formulario.get("id_formulario"))
        self._formularios_en_apertura.add(id_formulario)
        self.formulario_service.marcar_formulario_en_apertura(id_formulario)

        try:
            return {
                "se_preparo": True,
                "motivo": "formulario_preparado",
                "formulario": self.formulario_service.obtener_formulario_por_id(
                    id_formulario
                ),
            }

        except Exception:
            self.liberar_formulario_en_apertura(formulario)
            raise

    def procesar_formularios_pendientes(self, maximo: int = 1) -> dict[str, Any]:
        preparados: list[dict[str, Any]] = []
        maximo_normalizado = max(1, int(maximo))

        for _ in range(maximo_normalizado):
            resultado = self.preparar_siguiente_formulario_pendiente()

            if not resultado["se_preparo"]:
                break

            preparados.append(resultado)

        return {
            "total_preparados": len(preparados),
            "formularios_preparados": preparados,
        }
