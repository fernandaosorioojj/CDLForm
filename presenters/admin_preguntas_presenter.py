"""Capa presenter que conecta vistas PyQt con servicios de negocio.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from typing import Any

from services.forms.pregunta_service import PreguntaService


# Bloque CDLform: clase AdminPreguntasPresenter; agrupa estado y comportamiento de esta parte del flujo.
class AdminPreguntasPresenter:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, pregunta_service: PreguntaService | None = None) -> None:
        self.pregunta_service = pregunta_service or PreguntaService()

    # Bloque CDLform: funcion/metodo normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo listar_preguntas; encapsula una operacion del flujo del modulo.
    def listar_preguntas(self) -> list[dict[str, Any]]:
        return self.pregunta_service.listar_preguntas(solo_activas=False)

    # Bloque CDLform: funcion/metodo resumen_filtros_contexto; encapsula una operacion del flujo del modulo.
    def resumen_filtros_contexto(self, filtros: dict[str, Any]) -> str:
        if not isinstance(filtros, dict) or not filtros:
            return ""

        partes: list[str] = []
        etiquetas = {
            "cod_setor": "Setor",
            "cod_recurso": "Recurso",
            "turno": "Turno",
        }

        for clave, etiqueta in etiquetas.items():
            valores = filtros.get(clave, [])
            if not valores:
                continue

            texto_valores = ", ".join(
                self.normalizar_texto(valor) for valor in valores if self.normalizar_texto(valor)
            )
            if texto_valores:
                partes.append(f"{etiqueta}: {texto_valores}")

        return " | ".join(partes)

    # Bloque CDLform: funcion/metodo construir_item_lista_pregunta; encapsula una operacion del flujo del modulo.
    def construir_item_lista_pregunta(self, pregunta: dict[str, Any]) -> str:
        texto = pregunta.get("texto", "")
        tipo = pregunta.get("tipo", "")
        orden = pregunta.get("orden", 0)
        activa = "Activa" if pregunta.get("activa", True) else "Inactiva"
        version = pregunta.get("version", 1)

        resumen_filtros = self.resumen_filtros_contexto(
            pregunta.get("filtros_contexto", {})
        )

        item_texto = f"[{orden}] v{version} {texto} - ({tipo}) - {activa}"
        if resumen_filtros:
            item_texto += f" | {resumen_filtros}"
        return item_texto

    # Bloque CDLform: funcion/metodo coincide_filtro_busqueda; encapsula una operacion del flujo del modulo.
    def coincide_filtro_busqueda(
        self,
        pregunta: dict[str, Any],
        item_texto: str,
        texto_busqueda: str,
    ) -> bool:
        texto = self.normalizar_texto(pregunta.get("texto")).lower()
        tipo = self.normalizar_texto(pregunta.get("tipo")).lower()
        estado = "activa" if pregunta.get("activa", True) else "inactiva"

        filtros = pregunta.get("filtros_contexto", {})
        valores_filtros: list[str] = []
        for valores in filtros.values():
            if isinstance(valores, list):
                valores_filtros.extend(
                    self.normalizar_texto(valor).lower()
                    for valor in valores
                    if self.normalizar_texto(valor)
                )

        universo_busqueda = " ".join(
            [texto, tipo, estado, " ".join(valores_filtros), item_texto.lower()]
        )
        return texto_busqueda in universo_busqueda

    # Bloque CDLform: funcion/metodo construir_filtros_contexto; encapsula una operacion del flujo del modulo.
    def construir_filtros_contexto(
        self,
        cod_setor: list[str],
        cod_recurso: list[str],
        turno: list[str],
    ) -> dict[str, list[str]]:
        filtros: dict[str, list[str]] = {}
        if cod_setor:
            filtros["cod_setor"] = cod_setor
        if cod_recurso:
            filtros["cod_recurso"] = cod_recurso
        if turno:
            filtros["turno"] = turno
        return filtros

    # Bloque CDLform: funcion/metodo construir_opciones_respuesta; encapsula una operacion del flujo del modulo.
    def construir_opciones_respuesta(
        self,
        tipo: str,
        opciones_actuales: list[dict[str, Any]],
    ) -> list[dict[str, str]]:
        tipo_normalizado = self.normalizar_texto(tipo).lower()
        if tipo_normalizado not in {"seleccion_unica", "seleccion_multiple"}:
            return []

        opciones: list[dict[str, str]] = []

        for indice, data in enumerate(opciones_actuales, start=1):
            valor = self.normalizar_texto(data.get("valor"))
            accion_correctiva = self.normalizar_texto(data.get("accion_correctiva"))

            if not valor:
                raise ValueError("Cada opcion debe tener un valor valido.")

            opciones.append(
                {
                    "id_opcion": f"OPC-{indice:03d}",
                    "valor": valor,
                    "accion_correctiva": accion_correctiva,
                }
            )

        if not opciones:
            raise ValueError(
                "Debes ingresar opciones de respuesta para preguntas de seleccion."
            )

        return opciones

    # Bloque CDLform: funcion/metodo construir_payload_pregunta; encapsula una operacion del flujo del modulo.
    def construir_payload_pregunta(
        self,
        *,
        texto: str,
        tipo: str,
        obligatoria: bool,
        activa: bool,
        orden: int,
        filtros_contexto: dict[str, list[str]],
        opciones_respuesta: list[dict[str, str]],
    ) -> dict[str, Any]:
        texto_normalizado = self.normalizar_texto(texto)
        if not texto_normalizado:
            raise ValueError("El texto de la pregunta es obligatorio.")

        return {
            "texto": texto_normalizado,
            "tipo": self.normalizar_texto(tipo),
            "obligatoria": bool(obligatoria),
            "activa": bool(activa),
            "orden": int(orden),
            "filtros_contexto": filtros_contexto,
            "opciones_respuesta": opciones_respuesta,
        }

    # Bloque CDLform: funcion/metodo guardar_pregunta; encapsula una operacion del flujo del modulo.
    def guardar_pregunta(
        self,
        id_pregunta_en_edicion: str | None,
        payload: dict[str, Any],
    ) -> str:
        if id_pregunta_en_edicion:
            self.pregunta_service.actualizar_pregunta(
                id_pregunta=id_pregunta_en_edicion,
                **payload,
            )
            return "Nueva version de la pregunta creada correctamente."

        self.pregunta_service.crear_pregunta(**payload)
        return "Pregunta creada correctamente."

    # Bloque CDLform: funcion/metodo eliminar_pregunta; encapsula una operacion del flujo del modulo.
    def eliminar_pregunta(self, id_pregunta: str | None) -> str:
        if not id_pregunta:
            raise ValueError("Selecciona una pregunta primero.")
        self.pregunta_service.eliminar_pregunta(id_pregunta)
        return "Pregunta desactivada correctamente para conservar el historial."

    # Bloque CDLform: funcion/metodo requiere_opciones; encapsula una operacion del flujo del modulo.
    def requiere_opciones(self, tipo: str) -> bool:
        return self.normalizar_texto(tipo).lower() in {
            "seleccion_unica",
            "seleccion_multiple",
        }

    # Bloque CDLform: funcion/metodo mensaje_opciones; encapsula una operacion del flujo del modulo.
    def mensaje_opciones(self, tipo: str) -> str:
        tipo_normalizado = self.normalizar_texto(tipo).lower()

        if tipo_normalizado == "seleccion_multiple":
            return (
                "Agrega opciones para seleccion multiple. "
                "El operario podra marcar mas de una y cada una puede tener su propia accion correctiva."
            )

        if tipo_normalizado == "seleccion_unica":
            return (
                "Agrega opciones para seleccion unica. "
                "Cada opcion puede tener una accion correctiva opcional."
            )

        return "Este tipo de pregunta no requiere opciones configurables."

    # Bloque CDLform: funcion/metodo existe_valor_opcion; encapsula una operacion del flujo del modulo.
    def existe_valor_opcion(
        self,
        valor: str,
        opciones_actuales: list[dict[str, Any]],
    ) -> bool:
        valor_normalizado = self.normalizar_texto(valor).upper()
        for opcion in opciones_actuales:
            actual = self.normalizar_texto(opcion.get("valor")).upper()
            if actual == valor_normalizado:
                return True
        return False

    # Bloque CDLform: funcion/metodo construir_opcion_temporal; encapsula una operacion del flujo del modulo.
    def construir_opcion_temporal(
        self,
        valor: str,
        accion_correctiva: str,
    ) -> dict[str, str]:
        valor_normalizado = self.normalizar_texto(valor)
        if not valor_normalizado:
            raise ValueError("Debes ingresar un valor para la opcion.")

        return {
            "id_opcion": "",
            "valor": valor_normalizado,
            "accion_correctiva": self.normalizar_texto(accion_correctiva),
        }


