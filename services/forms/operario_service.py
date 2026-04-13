from __future__ import annotations

from typing import Any

from repositories.operario_repository import OperarioRepository


class OperarioService:
    def __init__(
        self,
        operario_repository: OperarioRepository | None = None,
    ) -> None:
        self.operario_repository = operario_repository or OperarioRepository()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @staticmethod
    def _normalizar_lista(valores: Any) -> list[str]:
        if valores is None:
            return []

        if isinstance(valores, list):
            resultado: list[str] = []
            for valor in valores:
                texto = str(valor).strip()
                if texto and texto not in resultado:
                    resultado.append(texto)
            return resultado

        texto = str(valores).strip()
        return [texto] if texto else []

    def _obtener_todos(self) -> list[dict]:
        if hasattr(self.operario_repository, "listar_operarios"):
            return self.operario_repository.listar_operarios()

        if hasattr(self.operario_repository, "list_all"):
            return self.operario_repository.list_all()

        raise AttributeError(
            "OperarioRepository no tiene ni 'listar_operarios' ni 'list_all'."
        )

    def _coincide_contexto(
        self,
        operario: dict,
        cod_recurso: str | None = None,
        cod_setor: str | None = None,
    ) -> bool:
        cod_recurso = self._normalizar_texto(cod_recurso)
        cod_setor = self._normalizar_texto(cod_setor)

        recursos_operario = self._normalizar_lista(
            operario.get("cod_recursos")
            or operario.get("maquinas")
            or operario.get("cod_recurso")
            or operario.get("maquina")
        )

        setores_operario = self._normalizar_lista(
            operario.get("cod_setores")
            or operario.get("areas")
            or operario.get("cod_setor")
            or operario.get("area")
        )

        coincide_recurso = True
        coincide_setor = True

        if cod_recurso and recursos_operario:
            coincide_recurso = cod_recurso in recursos_operario

        if cod_setor and setores_operario:
            coincide_setor = cod_setor in setores_operario

        return coincide_recurso and coincide_setor

    def listar_operarios(
        self,
        solo_activos: bool = True,
        cod_recurso: str | None = None,
        cod_setor: str | None = None,
    ) -> list[dict]:
        operarios = self._obtener_todos()
        resultado: list[dict] = []

        for operario in operarios:
            activo = operario.get("activo", operario.get("activa", True))

            if solo_activos and not bool(activo):
                continue

            if not self._coincide_contexto(
                operario=operario,
                cod_recurso=cod_recurso,
                cod_setor=cod_setor,
            ):
                continue

            resultado.append(operario)

        return resultado

    def obtener_operario_preseleccionado(
        self,
        formulario: dict[str, Any],
    ) -> str:
        return self._normalizar_texto(
            formulario.get("operario") or formulario.get("operador")
        )

    def listar_operarios_para_formulario(
        self,
        formulario: dict[str, Any],
        solo_activos: bool = True,
    ) -> list[dict]:
        operario_preseleccionado = self.obtener_operario_preseleccionado(formulario)

        if operario_preseleccionado:
            return [
                {
                    "id_operario": operario_preseleccionado,
                    "nombre": operario_preseleccionado,
                    "activo": True,
                    "origen": "apontamento",
                }
            ]

        cod_recurso = self._normalizar_texto(
            formulario.get("cod_recurso") or formulario.get("maquina")
        )
        cod_setor = self._normalizar_texto(
            formulario.get("cod_setor") or formulario.get("area")
        )

        return self.listar_operarios(
            solo_activos=solo_activos,
            cod_recurso=cod_recurso,
            cod_setor=cod_setor,
        )

    def listar_nombres_operarios_para_formulario(
        self,
        formulario: dict[str, Any],
        solo_activos: bool = True,
    ) -> list[str]:
        operarios = self.listar_operarios_para_formulario(
            formulario=formulario,
            solo_activos=solo_activos,
        )

        nombres: list[str] = []

        for operario in operarios:
            nombre = self._normalizar_texto(
                operario.get("nombre")
                or operario.get("nombre_operario")
                or operario.get("operario")
                or operario.get("id_operario")
            )

            if nombre and nombre not in nombres:
                nombres.append(nombre)

        return nombres