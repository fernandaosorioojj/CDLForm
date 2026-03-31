from services.disparador_service import DisparadorService
from services.evento_op_service import EventoOPService
from services.jobtrack_config_service import JobtrackConfigService


class EventProcessor:
    def __init__(self) -> None:
        self.evento_service = EventoOPService()
        self.disparador_service = DisparadorService()
        self.jobtrack_config_service = JobtrackConfigService()

    def procesar_evento_externo(self, data: dict) -> dict:
        num_ordem = data.get("num_ordem") or data.get("NumOrdem") or data.get("op") or ""

        estado_anterior = data.get("estado_anterior", "")
        estado_nuevo = data.get("estado_nuevo", "")
        fecha_evento = data.get("fecha_evento", "")

        estacao = self.jobtrack_config_service.obtener_estacion_actual()

        if self.evento_service.ya_existe_evento_equivalente(
            num_ordem=num_ordem,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            fecha_evento=fecha_evento,
        ):
            eventos = self.evento_service.buscar_por_num_ordem(num_ordem)
            evento_existente = eventos[-1] if eventos else None

            if evento_existente:
                if not evento_existente.get("estacao_origen"):
                    self.evento_service.actualizar_evento(
                        str(evento_existente.get("id_evento", "")).strip(),
                        {"estacao_origen": estacao},
                    )
                    evento_existente["estacao_origen"] = estacao

                resultado = self.disparador_service.procesar_evento(evento_existente)
                evento_existente["debe_disparar"] = resultado["debe_disparar"]
                evento_existente["contexto_resuelto"] = resultado["contexto_resuelto"]
                evento_existente["mensaje"] = resultado["mensaje"]
                evento_existente["formulario"] = resultado["formulario"]
                return evento_existente

        evento = self.evento_service.crear_evento(
            num_ordem=num_ordem,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            fecha_evento=fecha_evento,
            id_apontamento=data.get("id_apontamento") or data.get("IdApontamento"),
            cod_recurso=data.get("cod_recurso") or data.get("CodRecurso"),
            operador=data.get("operador") or data.get("Operador"),
            cod_ativ=data.get("cod_ativ") or data.get("CodAtiv"),
            cod_setor=data.get("cod_setor") or data.get("CodSetor"),
            turno=data.get("turno") or data.get("Turno"),
            dt_producao=data.get("dt_producao") or data.get("DtProducao"),
            hora_inicio=data.get("hora_inicio") or data.get("HoraInicio"),
            hora_fim=data.get("hora_fim") or data.get("HoraFim"),
            descricao_op=data.get("descricao_op") or data.get("DescricaoOP") or data.get("DescricaoOp"),
            descricao_processo=data.get("descricao_processo") or data.get("DescricaoProcesso") or data.get("DescricaoOp"),
            obs=data.get("obs") or data.get("Obs"),
            qtd_produzida=data.get("qtd_produzida") or data.get("QtdProduzida"),
            qtd_planejado=(
                data.get("qtd_planejado")
                or data.get("QtdPlanejado")
                or data.get("QtdPlanejada")
            ),
            qtd_perdas=data.get("qtd_perdas") or data.get("QtdPerdas"),
            justificativa_perda=data.get("justificativa_perda") or data.get("JustificativaPerda"),
        )

        self.evento_service.actualizar_evento(
            str(evento.get("id_evento", "")).strip(),
            {"estacao_origen": estacao},
        )
        evento["estacao_origen"] = estacao

        resultado = self.disparador_service.procesar_evento(evento)

        evento["debe_disparar"] = resultado["debe_disparar"]
        evento["contexto_resuelto"] = resultado["contexto_resuelto"]
        evento["mensaje"] = resultado["mensaje"]
        evento["formulario"] = resultado["formulario"]

        return evento