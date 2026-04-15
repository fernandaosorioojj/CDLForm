from __future__ import annotations

from typing import Any

from models.formulario import (
    ESTADO_EN_APERTURA,
    ESTADO_PENDIENTE_OPERARIO,
    Formulario,
)
from services.forms.formulario_service import FormularioService
from services.forms.pregunta_service import PreguntaService
from services.forms.respuesta_service import RespuestaService


class FormularioOperarioPresenter:
    def __init__(
        self,
        formulario_service: FormularioService | None = None,
        pregunta_service: PreguntaService | None = None,
        respuesta_service: RespuestaService | None = None,
    ) -> None:
        self.formulario_service = formulario_service or FormularioService()
        self.pregunta_service = pregunta_service or PreguntaService()
        self.respuesta_service = respuesta_service or RespuestaService()

    @staticmethod
    def normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    def resolver_formulario_inicial(
        self,
        formulario: Formulario | None,
        contexto: dict[str, Any] | None,
    ) -> Formulario | None:
        if formulario is not None:
            return formulario

        if contexto:
            id_formulario = self.normalizar_texto(contexto.get("id_formulario"))
            if id_formulario:
                existente = self.formulario_service.obtener_formulario_por_id(
                    id_formulario
                )
                if existente:
                    return existente

            return Formulario.from_dict(
                {
                    "id_formulario": id_formulario or "FORM-TEST",
                    "identificador": self.normalizar_texto(
                        contexto.get("identificador") or contexto.get("num_ordem")
                    ),
                    "id_apontamento": self.normalizar_texto(
                        contexto.get("id_apontamento")
                        or contexto.get("IdApontamento")
                        or "TEST"
                    ),
                    "fecha_formulario": self.normalizar_texto(
                        contexto.get("fecha_formulario")
                        or contexto.get("DtProducao")
                    ),
                    "area": self.normalizar_texto(
                        contexto.get("area")
                        or contexto.get("cod_setor")
                        or contexto.get("CodSetor")
                    ),
                    "maquina": self.normalizar_texto(
                        contexto.get("maquina")
                        or contexto.get("cod_recurso")
                        or contexto.get("CodRecurso")
                    ),
                    "cod_recurso": self.normalizar_texto(
                        contexto.get("cod_recurso")
                        or contexto.get("CodRecurso")
                        or contexto.get("maquina")
                    ),
                    "cod_setor": self.normalizar_texto(
                        contexto.get("cod_setor")
                        or contexto.get("CodSetor")
                        or contexto.get("area")
                    ),
                    "turno": contexto.get("turno") or contexto.get("Turno"),
                    "hora_fim": contexto.get("hora_fim") or contexto.get("HoraFim"),
                    "operario": self.normalizar_texto(
                        contexto.get("operario") or contexto.get("operador")
                    ),
                    "estacion": self.normalizar_texto(contexto.get("estacion")),
                    "evento_origen": self.normalizar_texto(
                        contexto.get("evento_origen") or "test"
                    ),
                    "estado": self.normalizar_texto(
                        contexto.get("estado") or ESTADO_EN_APERTURA
                    )
                    or ESTADO_EN_APERTURA,
                    "descripcion_op": self.normalizar_texto(
                        contexto.get("descripcion_op")
                        or contexto.get("DescricaoOP")
                    ),
                    "descripcion_proceso": self.normalizar_texto(
                        contexto.get("descripcion_proceso")
                        or contexto.get("DescricaoProcesso")
                    ),
                    "observacion_general": self.normalizar_texto(
                        contexto.get("observacion_general") or contexto.get("obs")
                    ),
                    "fecha_creacion": self.normalizar_texto(
                        contexto.get("fecha_creacion")
                    ),
                    "fecha_actualizacion": self.normalizar_texto(
                        contexto.get("fecha_actualizacion")
                    ),
                }
            )

        return self.formulario_service.obtener_siguiente_formulario_pendiente_operario()

    def preparar_formulario(
        self,
        formulario: Formulario | None,
        operario_seleccionado: str,
    ) -> Formulario | None:
        if not formulario:
            return None

        formulario_persistido = self.formulario_service.obtener_formulario_por_id(
            formulario.id_formulario
        )
        if formulario_persistido:
            formulario = formulario_persistido

        if operario_seleccionado:
            formulario = self.formulario_service.asignar_operario(
                formulario.id_formulario,
                operario_seleccionado,
            )

        if formulario.estado == ESTADO_EN_APERTURA:
            return self.formulario_service.marcar_formulario_pendiente_operario(
                formulario.id_formulario
            )

        if formulario.estado != ESTADO_PENDIENTE_OPERARIO:
            return (
                self.formulario_service.obtener_formulario_por_id(
                    formulario.id_formulario
                )
                or formulario
            )

        return formulario

    def construir_contexto_preguntas(
        self,
        formulario: Formulario | None,
        operario_seleccionado: str = "",
    ) -> dict[str, Any]:
        if not formulario:
            return {}

        contexto = {
            "cod_setor": formulario.cod_setor or formulario.area,
            "cod_recurso": formulario.cod_recurso or formulario.maquina,
            "turno": formulario.turno,
            "estacion": formulario.estacion,
            "operario": formulario.operario or operario_seleccionado,
            "area": formulario.area or formulario.cod_setor,
            "maquina": formulario.maquina or formulario.cod_recurso,
        }
        return {
            clave: valor
            for clave, valor in contexto.items()
            if valor not in (None, "")
        }

    def obtener_preguntas_para_formulario(
        self,
        formulario: Formulario | None,
        operario_seleccionado: str = "",
    ) -> list[dict[str, Any]]:
        if not formulario:
            return []

        if formulario.id_plantilla_preguntas:
            preguntas = self.pregunta_service.listar_preguntas_para_plantilla(
                formulario.id_plantilla_preguntas
            )
        else:
            preguntas = []

        if not isinstance(preguntas, list):
            return []

        return sorted(
            preguntas,
            key=lambda pregunta: (
                int(pregunta.get("orden", 9999))
                if str(pregunta.get("orden", "")).isdigit()
                else 9999,
                self.normalizar_texto(pregunta.get("id_pregunta")),
            ),
        )

    def obtener_opciones_pregunta(
        self,
        pregunta: dict[str, Any],
    ) -> list[dict[str, str]]:
        opciones_crudas = (
            pregunta.get("opciones_respuesta")
            or pregunta.get("opciones")
            or pregunta.get("opciones_pregunta")
            or pregunta.get("alternativas")
            or []
        )

        opciones: list[dict[str, str]] = []

        for indice, item in enumerate(opciones_crudas, start=1):
            if isinstance(item, dict):
                id_opcion = self.normalizar_texto(
                    item.get("id_opcion")
                    or item.get("id")
                    or item.get("codigo")
                    or item.get("valor")
                    or f"OPC-{indice:03d}"
                )
                texto = self.normalizar_texto(
                    item.get("texto")
                    or item.get("valor")
                    or item.get("descripcion")
                    or item.get("nombre")
                    or item.get("label")
                    or id_opcion
                )
                accion_correctiva = self.normalizar_texto(
                    item.get("accion_correctiva")
                )
                if texto:
                    opciones.append(
                        {
                            "id_opcion": id_opcion,
                            "texto": texto,
                            "accion_correctiva": accion_correctiva,
                        }
                    )
            else:
                texto = self.normalizar_texto(item)
                if texto:
                    opciones.append(
                        {
                            "id_opcion": texto,
                            "texto": texto,
                            "accion_correctiva": "",
                        }
                    )

        return opciones

    def pregunta_es_obligatoria(self, pregunta: dict[str, Any]) -> bool:
        return bool(
            pregunta.get("obligatoria", False)
            or pregunta.get("requerida", False)
            or pregunta.get("required", False)
        )

    def validar_respuestas(
        self,
        respuestas_por_control: list[dict[str, Any]],
    ) -> tuple[bool, str]:
        for item in respuestas_por_control:
            pregunta = item["pregunta"]
            if not self.pregunta_es_obligatoria(pregunta):
                continue

            respuestas = item["respuestas"]
            if respuestas:
                continue

            texto_pregunta = self.normalizar_texto(
                pregunta.get("texto")
                or pregunta.get("pregunta")
                or pregunta.get("enunciado")
                or pregunta.get("id_pregunta")
                or "Sin texto"
            )
            return False, f"Debes responder la pregunta: {texto_pregunta}"

        return True, ""

    def guardar_formulario(
        self,
        formulario: Formulario,
        respuestas_por_control: list[dict[str, Any]],
        observacion_general: str,
    ) -> Formulario:
        for item in respuestas_por_control:
            pregunta = item["pregunta"]
            id_pregunta = self.normalizar_texto(pregunta.get("id_pregunta"))
            if not id_pregunta:
                continue

            for respuesta in item["respuestas"]:
                self.respuesta_service.crear_respuesta(
                    id_formulario=formulario.id_formulario,
                    id_pregunta=id_pregunta,
                    respuesta_texto=respuesta.get("respuesta_texto"),
                    respuesta_numero=respuesta.get("respuesta_numero"),
                    id_opcion=respuesta.get("id_opcion"),
                    accion_correctiva_aplicada=respuesta.get(
                        "accion_correctiva_aplicada"
                    ),
                )

        return self.formulario_service.marcar_formulario_completado(
            formulario.id_formulario,
            observacion_general=self.normalizar_texto(observacion_general),
        )

