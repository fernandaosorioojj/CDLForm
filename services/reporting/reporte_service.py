"""Servicios que preparan datos para reportes y auditorias de gestion.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from models.formulario import Formulario
from services.forms.formulario_service import FormularioService
from services.forms.pregunta_service import PreguntaService
from services.forms.plantilla_preguntas_service import PlantillaPreguntasService
from services.forms.respuesta_service import RespuestaService
from services.jobtrack.apontamento_query_service import ApontamentoQueryService


# Bloque CDLform: clase ReporteService; agrupa estado y comportamiento de esta parte del flujo.
class ReporteService:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        formulario_service: FormularioService | None = None,
        respuesta_service: RespuestaService | None = None,
        pregunta_service: PreguntaService | None = None,
        plantilla_preguntas_service: PlantillaPreguntasService | None = None,
        apontamento_query_service: ApontamentoQueryService | None = None,
    ) -> None:
        self.formulario_service = formulario_service or FormularioService()
        self.respuesta_service = respuesta_service or RespuestaService()
        self.pregunta_service = pregunta_service or PreguntaService()
        self.plantilla_preguntas_service = (
            plantilla_preguntas_service or PlantillaPreguntasService()
        )
        self.apontamento_query_service = (
            apontamento_query_service or ApontamentoQueryService()
        )

    # Bloque CDLform: funcion/metodo _formulario_a_dict; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _formulario_a_dict(formulario: Formulario) -> dict[str, Any]:
        return formulario.to_dict()

    # Bloque CDLform: funcion/metodo listar_formularios; encapsula una operacion del flujo del modulo.
    def listar_formularios(self) -> list[Formulario]:
        return self.formulario_service.listar_formularios()

    # Bloque CDLform: funcion/metodo obtener_serie_acciones_correctivas_ultimos_7_dias; encapsula una operacion del flujo del modulo.
    def obtener_serie_acciones_correctivas_ultimos_7_dias(self) -> list[dict[str, Any]]:
        hoy = datetime.now().date()
        inicio = hoy - timedelta(days=6)
        conteos = {
            inicio + timedelta(days=offset): 0
            for offset in range(7)
        }

        for accion in self.listar_acciones_correctivas():
            fecha = self._resolver_fecha_dashboard(
                accion.get("fecha_formulario"),
            )
            if fecha is None:
                continue

            fecha_dia = fecha.date()
            if fecha_dia in conteos:
                conteos[fecha_dia] += 1

        return [
            {
                "label": fecha.strftime("%d/%m"),
                "value": conteos[fecha],
            }
            for fecha in sorted(conteos.keys())
        ]

    # Bloque CDLform: funcion/metodo obtener_serie_formularios_hoy_por_estado; encapsula una operacion del flujo del modulo.
    def obtener_serie_formularios_hoy_por_estado(self) -> list[dict[str, Any]]:
        hoy = datetime.now().date()
        formularios_hoy: list[Formulario] = []

        for formulario in self.listar_formularios():
            fecha = self._resolver_fecha_dashboard(
                formulario.fecha_formulario,
                formulario.fecha_actualizacion,
                formulario.fecha_creacion,
            )
            if fecha and fecha.date() == hoy:
                formularios_hoy.append(formulario)

        orden_estados = [
            "pendiente_operario",
            "en_apertura",
            "en_progreso",
            "completado",
            "cancelado",
        ]
        conteos = {estado: 0 for estado in orden_estados}
        extras: dict[str, int] = {}

        for formulario in formularios_hoy:
            estado = str(formulario.estado or "").strip().lower()
            if not estado:
                continue
            if estado in conteos:
                conteos[estado] += 1
            else:
                extras[estado] = extras.get(estado, 0) + 1

        etiquetas = {
            "pendiente_operario": "Pendiente",
            "en_apertura": "Apertura",
            "en_progreso": "En progreso",
            "completado": "Completado",
            "cancelado": "Cancelado",
        }

        serie = [
            {
                "label": etiquetas.get(estado, estado.title()),
                "value": valor,
            }
            for estado, valor in conteos.items()
        ]
        serie.extend(
            {
                "label": estado.title(),
                "value": valor,
            }
            for estado, valor in sorted(extras.items())
        )
        return serie

    # Bloque CDLform: funcion/metodo obtener_metricas_dashboard; encapsula una operacion del flujo del modulo.
    def obtener_metricas_dashboard(self) -> dict[str, Any]:
        acciones_semana = self.obtener_serie_acciones_correctivas_ultimos_7_dias()
        formularios_hoy = self.obtener_serie_formularios_hoy_por_estado()

        return {
            "acciones_semana": acciones_semana,
            "formularios_hoy": formularios_hoy,
            "kpis": {
                "acciones_total": sum(item["value"] for item in acciones_semana),
                "formularios_hoy_total": sum(item["value"] for item in formularios_hoy),
                "formularios_hoy_completados": sum(
                    item["value"]
                    for item in formularios_hoy
                    if str(item.get("label")) == "Completado"
                ),
            },
        }

    # Bloque CDLform: funcion/metodo listar_formularios_completados; encapsula una operacion del flujo del modulo.
    def listar_formularios_completados(self) -> list[Formulario]:
        return self.formulario_service.listar_formularios_por_estado("completado")

    # Bloque CDLform: funcion/metodo obtener_formulario; encapsula una operacion del flujo del modulo.
    def obtener_formulario(self, id_formulario: str) -> Formulario | None:
        return self.formulario_service.obtener_formulario_por_id(id_formulario)

    # Bloque CDLform: funcion/metodo obtener_respuestas_de_formulario; encapsula una operacion del flujo del modulo.
    def obtener_respuestas_de_formulario(self, id_formulario: str) -> list[dict]:
        respuestas = self.respuesta_service.listar_respuestas_por_formulario(
            id_formulario
        )
        return [respuesta.to_dict() for respuesta in respuestas]

    # Bloque CDLform: funcion/metodo obtener_preguntas_de_formulario; encapsula una operacion del flujo del modulo.
    def obtener_preguntas_de_formulario(self, formulario: Formulario) -> list[dict]:
        if formulario.id_plantilla_preguntas:
            return self.pregunta_service.listar_preguntas_para_plantilla(
                formulario.id_plantilla_preguntas
            )

        return []

    # Bloque CDLform: funcion/metodo obtener_detalle_auditoria_formulario; encapsula una operacion del flujo del modulo.
    def obtener_detalle_auditoria_formulario(
        self,
        formulario: Formulario,
    ) -> list[dict[str, Any]]:
        preguntas = self.obtener_preguntas_de_formulario(formulario)
        respuestas = self.obtener_respuestas_de_formulario(formulario.id_formulario)

        preguntas_por_id = {
            pregunta.get("id_pregunta"): pregunta
            for pregunta in preguntas
        }
        respuestas_por_pregunta: dict[str, list[dict[str, Any]]] = {}
        for respuesta in respuestas:
            id_pregunta = str(respuesta.get("id_pregunta", "")).strip()
            respuestas_por_pregunta.setdefault(id_pregunta, []).append(respuesta)

        filas: list[dict[str, Any]] = []
        for pregunta in preguntas:
            id_pregunta = str(pregunta.get("id_pregunta", "")).strip()
            respuestas_pregunta = respuestas_por_pregunta.get(id_pregunta, [])

            if not respuestas_pregunta:
                filas.append(
                    self._construir_fila_auditoria(
                        pregunta=pregunta,
                        respuesta=None,
                    )
                )
                continue

            for respuesta in respuestas_pregunta:
                filas.append(
                    self._construir_fila_auditoria(
                        pregunta=pregunta,
                        respuesta=respuesta,
                    )
                )

        ids_listados = {fila["id_pregunta"] for fila in filas}
        for respuesta in respuestas:
            id_pregunta = str(respuesta.get("id_pregunta", "")).strip()
            if id_pregunta in ids_listados:
                continue
            filas.append(
                self._construir_fila_auditoria(
                    pregunta=preguntas_por_id.get(id_pregunta, {}),
                    respuesta=respuesta,
                )
            )

        return filas

    # Bloque CDLform: funcion/metodo obtener_metadata_plantilla_formulario; encapsula una operacion del flujo del modulo.
    def obtener_metadata_plantilla_formulario(
        self,
        formulario: Formulario,
    ) -> dict[str, Any]:
        if not formulario.id_plantilla_preguntas:
            return {}

        plantilla = self.plantilla_preguntas_service.repository.obtener_por_id(
            formulario.id_plantilla_preguntas
        )
        if not plantilla:
            return {}

        return {
            "id_plantilla": plantilla.id_plantilla,
            "clave_plantilla": plantilla.clave_plantilla,
            "version": plantilla.version,
            "activa": plantilla.activa,
            "fecha_creacion": plantilla.fecha_creacion,
            "fecha_desactivacion": plantilla.fecha_desactivacion,
            "cantidad_preguntas": len(plantilla.items),
        }

    # Bloque CDLform: funcion/metodo resolver_version_plantilla_formulario; encapsula una operacion del flujo del modulo.
    def resolver_version_plantilla_formulario(self, formulario: Formulario) -> str:
        if formulario.version_plantilla_preguntas:
            return str(formulario.version_plantilla_preguntas)

        metadata_plantilla = self.obtener_metadata_plantilla_formulario(formulario)
        if metadata_plantilla.get("version"):
            return str(metadata_plantilla["version"])

        return "Sin plantilla"

    # Bloque CDLform: funcion/metodo construir_resumen_auditoria_formulario; encapsula una operacion del flujo del modulo.
    def construir_resumen_auditoria_formulario(
        self,
        formulario: Formulario,
    ) -> dict[str, Any]:
        preguntas = self.obtener_preguntas_de_formulario(formulario)
        respuestas = self.obtener_respuestas_de_formulario(formulario.id_formulario)
        metadata_plantilla = self.obtener_metadata_plantilla_formulario(formulario)

        return {
            "id_formulario": formulario.id_formulario,
            "identificador": formulario.identificador,
            "cod_setor": formulario.cod_setor or formulario.area,
            "cod_recurso": formulario.cod_recurso or formulario.maquina,
            "operario": formulario.operario,
            "id_plantilla_preguntas": formulario.id_plantilla_preguntas,
            "clave_plantilla_preguntas": (
                metadata_plantilla.get("clave_plantilla")
                or self._clave_plantilla_desde_formulario(formulario)
            ),
            "version_plantilla_preguntas": formulario.version_plantilla_preguntas,
            "cantidad_preguntas": len(preguntas),
            "cantidad_respuestas": len(respuestas),
            "fecha_respuesta_operario": self._resolver_fecha_respuesta_operario(
                formulario,
                respuestas,
            ),
            "estado": formulario.estado,
        }

    # Bloque CDLform: funcion/metodo listar_acciones_correctivas; encapsula una operacion del flujo del modulo.
    def listar_acciones_correctivas(
        self,
        incluir_supervisor_sql: bool = False,
    ) -> list[dict[str, Any]]:
        filas: list[dict[str, Any]] = []
        formularios = self.listar_formularios()
        supervisores_por_apontamento = {
            str(formulario.id_apontamento or "").strip(): str(
                formulario.supervisor_apontamento or ""
            ).strip()
            for formulario in formularios
            if str(formulario.id_apontamento or "").strip()
            and str(formulario.supervisor_apontamento or "").strip()
        }
        if incluir_supervisor_sql:
            supervisores_sql = self._obtener_supervisores_formularios(formularios)
            supervisores_por_apontamento.update(
                {
                    id_apontamento: supervisor
                    for id_apontamento, supervisor in supervisores_sql.items()
                    if supervisor
                }
            )

        for formulario in formularios:
            detalle = self.obtener_detalle_auditoria_formulario(formulario)
            id_apontamento = str(formulario.id_apontamento or "").strip()

            for respuesta in detalle:
                accion_correctiva = str(
                    respuesta.get("accion_correctiva") or ""
                ).strip()
                if not accion_correctiva:
                    continue

                filas.append(
                    {
                        "id_formulario": formulario.id_formulario,
                        "identificador": formulario.identificador,
                        "id_apontamento": formulario.id_apontamento,
                        "operario": formulario.operario,
                        "supervisor": supervisores_por_apontamento.get(
                            id_apontamento,
                            "",
                        ),
                        "cod_setor": formulario.cod_setor or formulario.area,
                        "cod_recurso": formulario.cod_recurso or formulario.maquina,
                        "turno": formulario.turno,
                        "estado": formulario.estado,
                        "fecha_formulario": formulario.fecha_formulario,
                        "id_pregunta": respuesta.get("id_pregunta", ""),
                        "pregunta": respuesta.get("pregunta", ""),
                        "respuesta": respuesta.get("respuesta", ""),
                        "id_opcion": respuesta.get("id_opcion", ""),
                        "opcion": respuesta.get("opcion", ""),
                        "accion_correctiva": accion_correctiva,
                    }
                )

        return sorted(
            filas,
            key=lambda fila: (
                str(fila.get("fecha_formulario") or ""),
                str(fila.get("id_formulario") or ""),
                str(fila.get("id_pregunta") or ""),
            ),
            reverse=True,
        )

    # Bloque CDLform: funcion/metodo _obtener_supervisores_formularios; encapsula una operacion del flujo del modulo.
    def _obtener_supervisores_formularios(
        self,
        formularios: list[Formulario],
    ) -> dict[str, str]:
        ids_apontamento = [
            formulario.id_apontamento
            for formulario in formularios
            if str(formulario.id_apontamento or "").strip()
        ]

        try:
            return self.apontamento_query_service.listar_supervisores_por_id_apontamentos(
                ids_apontamento
            )
        except Exception:
            return {}

    # Bloque CDLform: funcion/metodo generar_reporte; encapsula una operacion del flujo del modulo.
    def generar_reporte(
        self,
        estado: str | None = None,
    ) -> list[dict[str, Any]]:
        formularios = self.formulario_service.listar_formularios()

        estado_normalizado = str(estado or "").strip()
        if estado_normalizado:
            formularios = [
                formulario
                for formulario in formularios
                if formulario.estado == estado_normalizado
            ]

        formularios_ordenados = sorted(
            formularios,
            key=lambda formulario: (
                formulario.fecha_formulario,
                formulario.id_formulario,
            ),
            reverse=True,
        )

        return [
            self._formulario_a_dict(formulario)
            for formulario in formularios_ordenados
        ]

    # Bloque CDLform: funcion/metodo _construir_fila_auditoria; encapsula una operacion del flujo del modulo.
    def _construir_fila_auditoria(
        self,
        pregunta: dict[str, Any],
        respuesta: dict[str, Any] | None,
    ) -> dict[str, Any]:
        respuesta = respuesta or {}
        id_opcion = str(respuesta.get("id_opcion") or "").strip()
        opcion = self._buscar_opcion(pregunta, id_opcion)

        return {
            "id_pregunta": str(
                respuesta.get("id_pregunta") or pregunta.get("id_pregunta") or ""
            ).strip(),
            "pregunta": str(pregunta.get("texto") or "").strip() or "-",
            "version_pregunta": pregunta.get("version", "-"),
            "pregunta_activa": bool(pregunta.get("activa", False)),
            "respuesta": self._formatear_respuesta(respuesta),
            "id_opcion": id_opcion,
            "opcion": str(opcion.get("valor") or "").strip() if opcion else "",
            "opciones_disponibles": self._formatear_opciones_disponibles(pregunta),
            "accion_correctiva": str(
                respuesta.get("accion_correctiva_aplicada")
                or (opcion or {}).get("accion_correctiva")
                or ""
            ).strip(),
        }

    # Bloque CDLform: funcion/metodo _buscar_opcion; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _buscar_opcion(
        pregunta: dict[str, Any],
        id_opcion: str,
    ) -> dict[str, Any] | None:
        if not id_opcion:
            return None

        for opcion in pregunta.get("opciones_respuesta", []):
            if not isinstance(opcion, dict):
                continue
            if str(opcion.get("id_opcion", "")).strip() == id_opcion:
                return opcion

        return None

    # Bloque CDLform: funcion/metodo _clave_plantilla_desde_formulario; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _clave_plantilla_desde_formulario(formulario: Formulario) -> str:
        cod_setor = str(formulario.cod_setor or formulario.area or "").strip().upper()
        cod_recurso = str(
            formulario.cod_recurso or formulario.maquina or ""
        ).strip().upper()

        if not cod_setor or not cod_recurso:
            return ""

        return f"TPL-{cod_setor}-{cod_recurso}"

    # Bloque CDLform: funcion/metodo _formatear_respuesta; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _formatear_respuesta(respuesta: dict[str, Any]) -> str:
        respuesta_texto = respuesta.get("respuesta_texto")
        respuesta_numero = respuesta.get("respuesta_numero")

        if respuesta_texto not in (None, ""):
            return str(respuesta_texto).strip()

        if respuesta_numero not in (None, ""):
            return str(respuesta_numero).strip()

        return "-"

    # Bloque CDLform: funcion/metodo _formatear_opciones_disponibles; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _formatear_opciones_disponibles(pregunta: dict[str, Any]) -> str:
        opciones = []
        for opcion in pregunta.get("opciones_respuesta", []):
            if not isinstance(opcion, dict):
                continue
            valor = str(opcion.get("valor") or "").strip()
            if valor:
                opciones.append(valor)

        return ", ".join(opciones)

    # Bloque CDLform: funcion/metodo _resolver_fecha_respuesta_operario; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _resolver_fecha_respuesta_operario(
        formulario: Formulario,
        respuestas: list[dict[str, Any]],
    ) -> str:
        fechas_respuestas = [
            str(respuesta.get("fecha_creacion") or "").strip()
            for respuesta in respuestas
            if str(respuesta.get("fecha_creacion") or "").strip()
        ]
        if fechas_respuestas:
            return max(fechas_respuestas)

        return formulario.fecha_actualizacion or formulario.fecha_creacion or ""

    # Bloque CDLform: funcion/metodo _resolver_fecha_dashboard; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _resolver_fecha_dashboard(*valores: Any) -> datetime | None:
        for valor in valores:
            fecha = ReporteService._coerce_datetime(valor)
            if fecha is not None:
                return fecha
        return None

    # Bloque CDLform: funcion/metodo _coerce_datetime; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _coerce_datetime(valor: Any) -> datetime | None:
        texto = str(valor or "").strip()
        if not texto:
            return None

        candidatos = [
            texto,
            texto.replace("Z", "+00:00"),
            texto.replace(" ", "T"),
        ]
        for candidato in candidatos:
            try:
                return datetime.fromisoformat(candidato)
            except ValueError:
                continue

        formatos = (
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M",
        )
        for formato in formatos:
            try:
                return datetime.strptime(texto, formato)
            except ValueError:
                continue

        return None
