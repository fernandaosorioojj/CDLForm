from __future__ import annotations

from typing import Optional

from repositories.formulario_repository import FormularioRepository
from repositories.pregunta_repository import PreguntaRepository
from repositories.respuesta_repository import RespuestaRepository


class ReporteService:
    def __init__(
        self,
        formulario_repository: Optional[FormularioRepository] = None,
        respuesta_repository: Optional[RespuestaRepository] = None,
        pregunta_repository: Optional[PreguntaRepository] = None,
    ) -> None:
        self.formulario_repository = formulario_repository or FormularioRepository()
        self.respuesta_repository = respuesta_repository or RespuestaRepository()
        self.pregunta_repository = pregunta_repository or PreguntaRepository()

    def generar_reporte(self, filtros: Optional[dict] = None) -> list[dict]:
        filtros_normalizados = self._normalizar_filtros(filtros or {})

        formularios = self.formulario_repository.list_all()
        respuestas = self.respuesta_repository.list_all()
        preguntas = self.pregunta_repository.get_all()

        mapa_preguntas = {
            str(pregunta.get("id_pregunta", "")).strip(): pregunta
            for pregunta in preguntas
            if str(pregunta.get("id_pregunta", "")).strip()
        }

        respuestas_por_formulario: dict[str, list] = {}
        for respuesta in respuestas:
            id_formulario = str(respuesta.id_formulario).strip()
            if not id_formulario:
                continue
            respuestas_por_formulario.setdefault(id_formulario, []).append(respuesta)

        filas: list[dict] = []

        for formulario in formularios:
            if not self._cumple_filtros_formulario(formulario, filtros_normalizados):
                continue

            respuestas_formulario = respuestas_por_formulario.get(
                str(formulario.id_formulario).strip(),
                [],
            )

            if not respuestas_formulario:
                fila_base = self._construir_fila_sin_respuesta(formulario)
                if self._cumple_filtros_fila(fila_base, filtros_normalizados):
                    filas.append(fila_base)
                continue

            for respuesta in respuestas_formulario:
                pregunta = mapa_preguntas.get(str(respuesta.id_pregunta).strip(), {})

                fila = self._construir_fila_reporte(
                    formulario=formulario,
                    respuesta=respuesta,
                    pregunta=pregunta,
                )

                if self._cumple_filtros_fila(fila, filtros_normalizados):
                    filas.append(fila)

        return sorted(
            filas,
            key=lambda fila: (
                str(fila.get("identificador", "")).strip().upper(),
                str(fila.get("operario", "")).strip().upper(),
                int(fila.get("orden", 0) or 0),
                str(fila.get("texto_pregunta", "")).strip().upper(),
            ),
        )

    def _construir_fila_reporte(self, formulario, respuesta, pregunta: dict) -> dict:
        return {
            "id_formulario": formulario.id_formulario,
            "identificador": formulario.identificador,
            "operario": formulario.operario,
            "id_operario": formulario.id_operario,
            "cod_setor": formulario.cod_setor,
            "cod_recurso": formulario.cod_recurso,
            "cod_ativ": formulario.cod_ativ,
            "turno": formulario.turno,
            "tipo_trabajo": formulario.tipo_trabajo,
            "estado_formulario": formulario.estado,
            "evento_origen": formulario.evento_origen,
            "id_respuesta": respuesta.id_respuesta,
            "id_pregunta": respuesta.id_pregunta,
            "texto_pregunta": pregunta.get("texto", ""),
            "tipo_pregunta": pregunta.get("tipo", ""),
            "obligatoria": pregunta.get("obligatoria", True),
            "orden": pregunta.get("orden", 0),
            "respuesta_texto": respuesta.respuesta_texto,
            "respuesta_numero": respuesta.respuesta_numero,
            "id_opcion": respuesta.id_opcion,
            "accion_correctiva_aplicada": respuesta.accion_correctiva_aplicada,
        }

    def _construir_fila_sin_respuesta(self, formulario) -> dict:
        return {
            "id_formulario": formulario.id_formulario,
            "identificador": formulario.identificador,
            "operario": formulario.operario,
            "id_operario": formulario.id_operario,
            "cod_setor": formulario.cod_setor,
            "cod_recurso": formulario.cod_recurso,
            "cod_ativ": formulario.cod_ativ,
            "turno": formulario.turno,
            "tipo_trabajo": formulario.tipo_trabajo,
            "estado_formulario": formulario.estado,
            "evento_origen": formulario.evento_origen,
            "id_respuesta": "",
            "id_pregunta": "",
            "texto_pregunta": "",
            "tipo_pregunta": "",
            "obligatoria": False,
            "orden": 0,
            "respuesta_texto": None,
            "respuesta_numero": None,
            "id_opcion": None,
            "accion_correctiva_aplicada": None,
        }

    def _normalizar_filtros(self, filtros: dict) -> dict:
        filtros_normalizados: dict[str, str] = {}

        for clave, valor in filtros.items():
            if valor is None:
                continue

            valor_limpio = str(valor).strip()
            if not valor_limpio:
                continue

            filtros_normalizados[str(clave).strip().lower()] = valor_limpio.upper()

        return filtros_normalizados

    def _cumple_filtros_formulario(self, formulario, filtros: dict) -> bool:
        mapa = {
            "id_formulario": formulario.id_formulario,
            "identificador": formulario.identificador,
            "operario": formulario.operario,
            "id_operario": formulario.id_operario,
            "cod_setor": formulario.cod_setor,
            "cod_recurso": formulario.cod_recurso,
            "cod_ativ": formulario.cod_ativ,
            "turno": formulario.turno,
            "tipo_trabajo": formulario.tipo_trabajo,
            "estado_formulario": formulario.estado,
            "evento_origen": formulario.evento_origen or "",
        }

        for clave in (
            "id_formulario",
            "identificador",
            "operario",
            "id_operario",
            "cod_setor",
            "cod_recurso",
            "cod_ativ",
            "turno",
            "tipo_trabajo",
            "estado_formulario",
            "evento_origen",
        ):
            valor_filtro = filtros.get(clave)
            if not valor_filtro:
                continue

            valor_actual = str(mapa.get(clave, "")).strip().upper()
            if valor_filtro not in valor_actual:
                return False

        return True

    def _cumple_filtros_fila(self, fila: dict, filtros: dict) -> bool:
        mapa = {
            "texto_pregunta": fila.get("texto_pregunta", ""),
            "tipo_pregunta": fila.get("tipo_pregunta", ""),
            "respuesta_texto": fila.get("respuesta_texto", "") or "",
            "respuesta_numero": "" if fila.get("respuesta_numero") is None else str(fila.get("respuesta_numero")),
            "id_opcion": fila.get("id_opcion", "") or "",
            "accion_correctiva_aplicada": fila.get("accion_correctiva_aplicada", "") or "",
        }

        for clave in (
            "texto_pregunta",
            "tipo_pregunta",
            "respuesta_texto",
            "respuesta_numero",
            "id_opcion",
            "accion_correctiva_aplicada",
        ):
            valor_filtro = filtros.get(clave)
            if not valor_filtro:
                continue

            valor_actual = str(mapa.get(clave, "")).strip().upper()
            if valor_filtro not in valor_actual:
                return False

        if "con_accion_correctiva" in filtros:
            valor = filtros["con_accion_correctiva"]
            tiene_accion = bool(str(fila.get("accion_correctiva_aplicada", "") or "").strip())

            if valor in {"SI", "TRUE", "1"} and not tiene_accion:
                return False
            if valor in {"NO", "FALSE", "0"} and tiene_accion:
                return False

        return True