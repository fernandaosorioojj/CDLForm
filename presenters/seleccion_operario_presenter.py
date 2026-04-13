from __future__ import annotations

from typing import Any

from models.formulario import Formulario
from services.forms.formulario_service import FormularioService
from services.forms.operario_service import OperarioService


class SeleccionOperarioPresenter:
    def __init__(
        self,
        formulario_service: FormularioService | None = None,
        operario_service: OperarioService | None = None,
    ) -> None:
        self.formulario_service = formulario_service or FormularioService()
        self.operario_service = operario_service or OperarioService()

    @staticmethod
    def normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def resolver_formulario(
        self,
        formulario: Formulario | None,
        id_formulario: str | None,
    ) -> Formulario:
        if formulario is not None:
            return formulario

        id_normalizado = self.normalizar_texto(id_formulario)
        if id_normalizado:
            encontrado = self.formulario_service.obtener_formulario_por_id(
                id_normalizado
            )
            if encontrado:
                return encontrado

        raise ValueError("No se pudo resolver el formulario para la seleccion de operario.")

    def construir_info_formulario(self, formulario: Formulario) -> str:
        identificador = self.normalizar_texto(formulario.identificador)
        maquina = self.normalizar_texto(formulario.maquina or formulario.cod_recurso)
        area = self.normalizar_texto(formulario.area or formulario.cod_setor)

        return (
            f"Formulario: {self.normalizar_texto(formulario.id_formulario)}\n"
            f"Identificador: {identificador}\n"
            f"Maquina: {maquina}\n"
            f"Area: {area}"
        )

    def listar_operarios_para_formulario(
        self,
        formulario: Formulario,
        solo_activos: bool = True,
    ) -> list[dict[str, Any]]:
        return self.operario_service.listar_operarios_para_formulario(
            formulario=formulario,
            solo_activos=solo_activos,
        )

    def obtener_nombre_operario(self, operario: dict[str, Any]) -> str:
        return self.normalizar_texto(
            operario.get("nombre")
            or operario.get("nombre_operario")
            or operario.get("operario")
            or operario.get("id_operario")
        )

    def validar_operario_seleccionado(self, operario: Any) -> str:
        operario_normalizado = self.normalizar_texto(operario)
        if not operario_normalizado:
            raise ValueError("Debe seleccionar un operario.")
        return operario_normalizado

    def asignar_operario(
        self,
        formulario: Formulario,
        operario: str,
    ) -> Formulario:
        id_formulario = self.normalizar_texto(formulario.id_formulario)
        self.formulario_service.asignar_operario(id_formulario, operario)
        actualizado = self.formulario_service.obtener_formulario_por_id(id_formulario)
        return actualizado or formulario

