from __future__ import annotations

from datetime import datetime
from typing import Any

from services.jobtrack.apontamento_query_service import ApontamentoQueryService
from services.forms.formulario_service import FormularioService
from models.formulario import ESTADO_EN_APERTURA, ESTADO_PENDIENTE_OPERARIO


class ApontamentoProcesadoService:
    MENSAJE_SIN_PLANTILLA_ACTIVA = "No existe una plantilla activa de preguntas para "

    def __init__(
        self,
        apontamento_query_service: ApontamentoQueryService | None = None,
        formulario_service: FormularioService | None = None,
    ) -> None:
        self.apontamento_query_service = (
            apontamento_query_service or ApontamentoQueryService()
        )
        self.formulario_service = formulario_service or FormularioService()

    def _ensure_storage(self) -> None:
        return None

    def _leer_registros(self) -> list[dict[str, Any]]:
        return []

    def _guardar_registros(self, registros: list[dict[str, Any]]) -> None:
        return None

    @staticmethod
    def _normalizar_id_apontamento(valor: Any) -> str:
        if valor is None:
            raise ValueError("El IdApontamento no puede venir vacÃ­o.")

        if isinstance(valor, int):
            return str(valor)

        if isinstance(valor, float):
            if valor.is_integer():
                return str(int(valor))
            return str(valor).strip()

        texto = str(valor).strip()
        if not texto:
            raise ValueError("El IdApontamento no puede venir vacÃ­o.")

        try:
            numero = float(texto)
            if numero.is_integer():
                return str(int(numero))
        except ValueError:
            pass

        return texto

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @classmethod
    def _es_error_sin_plantilla_activa(cls, exc: Exception) -> bool:
        return cls.MENSAJE_SIN_PLANTILLA_ACTIVA in str(exc)

    def _formulario_puede_abrirse(self, formulario: dict[str, Any] | None) -> bool:
        if not formulario:
            return False

        estado = self._normalizar_texto(formulario.get("estado"))
        return estado in {ESTADO_EN_APERTURA, ESTADO_PENDIENTE_OPERARIO}

    @staticmethod
    def _serializar_valor(valor: Any) -> Any:
        if valor is None:
            return None

        if isinstance(valor, datetime):
            return valor.isoformat()

        if hasattr(valor, "isoformat"):
            try:
                return valor.isoformat()
            except TypeError:
                pass

        return valor

    def listar_registros_procesados(self) -> list[dict[str, Any]]:
        return self._leer_registros()

    def listar_ids_procesados(self) -> set[str]:
        ids: set[str] = set()

        for formulario in self.formulario_service.listar_formularios():
            try:
                ids.add(
                    self._normalizar_id_apontamento(formulario.id_apontamento)
                )
            except ValueError:
                continue

        return ids

    def fue_procesado(self, id_apontamento: Any) -> bool:
        id_normalizado = self._normalizar_id_apontamento(id_apontamento)
        return id_normalizado in self.listar_ids_procesados()

    def listar_apontamientos_pendientes_estacion_actual(
        self,
        limit: int = 50,
        solo_finalizados: bool = True,
        solo_con_num_ordem: bool = True,
    ) -> dict[str, Any]:
        contexto = self.apontamento_query_service.obtener_contexto_estacion_actual()
        apontamentos = self.apontamento_query_service.listar_apontamentos_estacion_actual(
            limit=limit,
            solo_finalizados=solo_finalizados,
        )

        ids_procesados = self.listar_ids_procesados()

        pendientes: list[dict[str, Any]] = []
        omitidos_ya_procesados: list[dict[str, Any]] = []
        omitidos_sin_num_ordem: list[dict[str, Any]] = []

        for apontamento in apontamentos:
            id_apontamento = self._normalizar_id_apontamento(
                apontamento.get("IdApontamento")
            )
            num_ordem = self._normalizar_texto(apontamento.get("NumOrdem"))

            if id_apontamento in ids_procesados:
                omitidos_ya_procesados.append(apontamento)
                continue

            if solo_con_num_ordem and not num_ordem:
                omitidos_sin_num_ordem.append(apontamento)
                continue

            pendientes.append(apontamento)

        return {
            "contexto": contexto,
            "total_consultados": len(apontamentos),
            "total_pendientes": len(pendientes),
            "total_omitidos_ya_procesados": len(omitidos_ya_procesados),
            "total_omitidos_sin_num_ordem": len(omitidos_sin_num_ordem),
            "apontamientos_pendientes": pendientes,
            "apontamientos_omitidos_ya_procesados": omitidos_ya_procesados,
            "apontamientos_omitidos_sin_num_ordem": omitidos_sin_num_ordem,
        }

    def registrar_apontamento_procesado(
        self,
        apontamento: dict[str, Any],
        contexto: dict[str, Any] | None = None,
        estado: str = "pendiente_formulario",
        id_formulario: str | None = None,
        observacion: str | None = None,
    ) -> dict[str, Any]:
        registros = self._leer_registros()

        id_apontamento = self._normalizar_id_apontamento(
            apontamento.get("IdApontamento")
        )

        for registro in registros:
            if self._normalizar_id_apontamento(
                registro.get("id_apontamento")
            ) == id_apontamento:
                return registro

        registro = self._construir_registro_apontamento(
            apontamento=apontamento,
            contexto=contexto,
            estado=estado,
            id_formulario=id_formulario,
            observacion=observacion,
        )

        registros.append(registro)
        self._guardar_registros(registros)
        return registro

    def _construir_registro_apontamento(
        self,
        apontamento: dict[str, Any],
        contexto: dict[str, Any] | None = None,
        estado: str = "pendiente_formulario",
        id_formulario: str | None = None,
        observacion: str | None = None,
    ) -> dict[str, Any]:
        contexto = contexto or {}
        id_apontamento = self._normalizar_id_apontamento(
            apontamento.get("IdApontamento")
        )

        return {
            "id_evento_cola": self._normalizar_texto(apontamento.get("IdEvento")),
            "id_apontamento": id_apontamento,
            "num_ordem": self._normalizar_texto(apontamento.get("NumOrdem")),
            "cod_recurso": self._normalizar_texto(apontamento.get("CodRecurso")),
            "cod_setor": self._normalizar_texto(apontamento.get("CodSetor")),
            "turno": self._serializar_valor(apontamento.get("Turno")),
            "hora_inicio": self._serializar_valor(apontamento.get("HoraInicio")),
            "hora_fim": self._serializar_valor(apontamento.get("HoraFim")),
            "operador": self._normalizar_texto(apontamento.get("Operador")),
            "supervisor": self._normalizar_texto(
                apontamento.get("Supervisor")
                or apontamento.get("supervisor")
                or apontamento.get("supervisor_apontamento")
            ),
            "descripcion_op": self._normalizar_texto(apontamento.get("DescricaoOP")),
            "descripcion_proceso": self._normalizar_texto(
                apontamento.get("DescricaoProcesso")
            ),
            "qtd_produzida": self._serializar_valor(apontamento.get("QtdProduzida")),
            "qtd_planejado": self._serializar_valor(apontamento.get("QtdPlanejado")),
            "qtd_perdas": self._serializar_valor(apontamento.get("QtdPerdas")),
            "justificativa_perda": self._normalizar_texto(
                apontamento.get("JustificativaPerda")
            ),
            "obs": self._normalizar_texto(apontamento.get("Obs")),
            "estacion": self._normalizar_texto(contexto.get("estacion")),
            "cod_recursos_estacion": list(contexto.get("cod_recursos", [])),
            "estado": self._normalizar_texto(estado) or "pendiente_formulario",
            "id_formulario": self._normalizar_texto(id_formulario),
            "observacion": self._normalizar_texto(observacion),
            "fecha_registro": datetime.now().isoformat(timespec="seconds"),
        }

    def registrar_apontamientos_procesados(
        self,
        apontamientos: list[dict[str, Any]],
        contexto: dict[str, Any] | None = None,
        estado: str = "pendiente_formulario",
    ) -> list[dict[str, Any]]:
        registros_guardados: list[dict[str, Any]] = []

        for apontamento in apontamientos:
            registro = self.registrar_apontamento_procesado(
                apontamento=apontamento,
                contexto=contexto,
                estado=estado,
            )
            registros_guardados.append(registro)

        return registros_guardados

    def _evento_cola_a_apontamento(
        self,
        evento: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "IdEvento": evento.get("id_evento"),
            "IdApontamento": evento.get("id_apontamento"),
            "NumOrdem": evento.get("num_ordem"),
            "CodRecurso": evento.get("cod_recurso"),
            "CodSetor": evento.get("cod_setor"),
            "Operador": evento.get("operador"),
            "Supervisor": evento.get("supervisor")
            or evento.get("Supervisor")
            or evento.get("supervisor_apontamento"),
            "Turno": evento.get("turno"),
            "HoraInicio": evento.get("hora_inicio"),
            "HoraFim": evento.get("hora_fim"),
        }

    def actualizar_estado_apontamento(
        self,
        id_apontamento: Any,
        estado: str,
        id_formulario: str | None = None,
        observacion: str | None = None,
    ) -> dict[str, Any]:
        id_normalizado = self._normalizar_id_apontamento(id_apontamento)
        registros = self._leer_registros()

        for registro in registros:
            if self._normalizar_id_apontamento(
                registro.get("id_apontamento")
            ) == id_normalizado:
                registro["estado"] = self._normalizar_texto(estado)
                registro["fecha_actualizacion"] = datetime.now().isoformat(
                    timespec="seconds"
                )

                if id_formulario is not None:
                    registro["id_formulario"] = self._normalizar_texto(id_formulario)

                if observacion is not None:
                    registro["observacion"] = self._normalizar_texto(observacion)

                self._guardar_registros(registros)
                return registro

        raise ValueError(
            f"No existe un apuntamiento procesado con IdApontamento {id_normalizado}."
        )

    def listar_registros_pendientes_formulario(
        self,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        estados_reintentables = {"pendiente_formulario", "error_formulario"}

        registros = [
            registro
            for registro in self._leer_registros()
            if self._normalizar_texto(registro.get("estado")) in estados_reintentables
            and self._normalizar_texto(registro.get("num_ordem"))
        ]

        if limit > 0:
            return registros[:limit]

        return registros

    def crear_formularios_desde_registros_pendientes(
        self,
        limit: int = 50,
    ) -> dict[str, Any]:
        pendientes = self.listar_registros_pendientes_formulario(limit=limit)

        formularios_creados: list[dict[str, Any]] = []
        formularios_existentes: list[dict[str, Any]] = []
        errores: list[dict[str, Any]] = []

        for registro in pendientes:
            try:
                resultado = (
                    self.formulario_service.crear_formulario_pendiente_desde_registro_apontamento(
                        registro
                    )
                )
                formulario = resultado["formulario"]
                id_apontamento = registro["id_apontamento"]

                if resultado["ya_existia"]:
                    formularios_existentes.append(formulario)
                    self.actualizar_estado_apontamento(
                        id_apontamento=id_apontamento,
                        estado="formulario_existente",
                        id_formulario=formulario.get("id_formulario"),
                    )
                else:
                    formularios_creados.append(formulario)
                    self.actualizar_estado_apontamento(
                        id_apontamento=id_apontamento,
                        estado="formulario_creado",
                        id_formulario=formulario.get("id_formulario"),
                    )

            except Exception as exc:
                error = {
                    "id_apontamento": registro.get("id_apontamento"),
                    "num_ordem": registro.get("num_ordem"),
                    "error": str(exc),
                }
                errores.append(error)

                try:
                    self.actualizar_estado_apontamento(
                        id_apontamento=registro.get("id_apontamento"),
                        estado="error_formulario",
                        observacion=str(exc),
                    )
                except Exception:
                    pass

        return {
            "total_pendientes_formulario": len(pendientes),
            "total_formularios_creados": len(formularios_creados),
            "total_formularios_existentes": len(formularios_existentes),
            "total_errores": len(errores),
            "formularios_creados": formularios_creados,
            "formularios_existentes": formularios_existentes,
            "errores": errores,
        }

    def sincronizar_y_crear_formularios_desde_cola_sql(
        self,
        limit_consulta: int = 50,
        solo_con_num_ordem: bool = True,
    ) -> dict[str, Any]:
        contexto = self.apontamento_query_service.obtener_contexto_estacion_actual()
        cod_recursos = list(contexto.get("cod_recursos", []))
        eventos = self.apontamento_query_service.listar_eventos_op_pendientes(
            cod_recursos=cod_recursos,
            limit=limit_consulta,
        )

        registrados: list[dict[str, Any]] = []
        formularios_creados: list[dict[str, Any]] = []
        formularios_existentes: list[dict[str, Any]] = []
        omitidos_ya_procesados: list[dict[str, Any]] = []
        omitidos_sin_num_ordem: list[dict[str, Any]] = []
        omitidos_sin_plantilla_activa: list[dict[str, Any]] = []
        errores: list[dict[str, Any]] = []

        for evento in eventos:
            id_evento = evento.get("id_evento")
            apontamento = self._evento_cola_a_apontamento(evento)

            try:
                id_apontamento = self._normalizar_id_apontamento(
                    apontamento.get("IdApontamento")
                )
                num_ordem = self._normalizar_texto(apontamento.get("NumOrdem"))

                formulario_existente = (
                    self.formulario_service.obtener_formulario_por_id_apontamento(
                        id_apontamento
                    )
                )

                if formulario_existente:
                    if self._formulario_puede_abrirse(formulario_existente):
                        formularios_existentes.append(formulario_existente)
                    else:
                        omitidos_ya_procesados.append(evento)

                    self.apontamento_query_service.marcar_evento_op_pendiente_procesado(
                        id_evento
                    )
                    continue

                if solo_con_num_ordem and not num_ordem:
                    motivo = "Omitido por la app: evento sin NumOrdem."
                    omitidos_sin_num_ordem.append(evento)
                    self.apontamento_query_service.marcar_evento_op_pendiente_omitido(
                        id_evento=id_evento,
                        motivo=motivo,
                    )
                    continue

                registro = self._construir_registro_apontamento(
                    apontamento=apontamento,
                    contexto=contexto,
                    estado="pendiente_formulario",
                )
                registrados.append(registro)

                resultado = (
                    self.formulario_service.crear_formulario_pendiente_desde_registro_apontamento(
                        registro
                    )
                )
                formulario = resultado["formulario"]

                if resultado["ya_existia"]:
                    formularios_existentes.append(formulario)
                else:
                    formularios_creados.append(formulario)

                self.apontamento_query_service.marcar_evento_op_pendiente_procesado(
                    id_evento
                )

            except Exception as exc:
                if self._es_error_sin_plantilla_activa(exc):
                    motivo = f"Omitido por la app: {str(exc)}"
                    omitidos_sin_plantilla_activa.append(evento)
                    try:
                        self.apontamento_query_service.marcar_evento_op_pendiente_omitido(
                            id_evento=id_evento,
                            motivo=motivo,
                        )
                    except Exception:
                        pass
                    continue

                error = {
                    "id_evento": id_evento,
                    "id_apontamento": evento.get("id_apontamento"),
                    "num_ordem": evento.get("num_ordem"),
                    "error": str(exc),
                }
                errores.append(error)

                try:
                    self.apontamento_query_service.marcar_evento_op_pendiente_error(
                        id_evento=id_evento,
                        mensaje_error=str(exc),
                    )
                except Exception:
                    pass

        return {
            "contexto": contexto,
            "total_consultados": len(eventos),
            "total_pendientes_nuevos": len(registrados),
            "total_registrados_en_cola": len(registrados),
            "total_formularios_creados": len(formularios_creados),
            "total_formularios_existentes": len(formularios_existentes),
            "total_errores_formulario": len(errores),
            "total_omitidos_ya_procesados": len(omitidos_ya_procesados),
            "total_omitidos_sin_num_ordem": len(omitidos_sin_num_ordem),
            "total_omitidos_sin_plantilla_activa": len(omitidos_sin_plantilla_activa),
            "formularios_creados": formularios_creados,
            "formularios_existentes": formularios_existentes,
            "errores": errores,
        }

    def sincronizar_y_crear_formularios_estacion_actual(
        self,
        limit_consulta: int = 50,
        limit_creacion: int = 50,
        solo_finalizados: bool = True,
        solo_con_num_ordem: bool = True,
    ) -> dict[str, Any]:
        resultado_consulta = self.listar_apontamientos_pendientes_estacion_actual(
            limit=limit_consulta,
            solo_finalizados=solo_finalizados,
            solo_con_num_ordem=solo_con_num_ordem,
        )

        contexto = resultado_consulta["contexto"]
        pendientes = resultado_consulta["apontamientos_pendientes"]

        registrados = self.registrar_apontamientos_procesados(
            apontamientos=pendientes,
            contexto=contexto,
            estado="pendiente_formulario",
        )

        resultado_formularios = self.crear_formularios_desde_registros_pendientes(
            limit=limit_creacion,
        )

        return {
            "contexto": contexto,
            "total_consultados": resultado_consulta["total_consultados"],
            "total_pendientes_nuevos": resultado_consulta["total_pendientes"],
            "total_registrados_en_cola": len(registrados),
            "total_formularios_creados": resultado_formularios[
                "total_formularios_creados"
            ],
            "total_formularios_existentes": resultado_formularios[
                "total_formularios_existentes"
            ],
            "total_errores_formulario": resultado_formularios["total_errores"],
            "formularios_creados": resultado_formularios["formularios_creados"],
            "formularios_existentes": resultado_formularios["formularios_existentes"],
            "errores": resultado_formularios["errores"],
        }
