from __future__ import annotations

from datetime import datetime
from typing import Any

from repositories.formulario_repository import FormularioRepository


class FormularioService:
    def __init__(
        self,
        formulario_repository: FormularioRepository | None = None,
    ) -> None:
        self.formulario_repository = formulario_repository or FormularioRepository()

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

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

    @staticmethod
    def _normalizar_id_apontamento(valor: Any) -> str:
        if valor is None:
            raise ValueError("El IdApontamento no puede venir vacío.")

        if isinstance(valor, int):
            return str(valor)

        if isinstance(valor, float):
            if valor.is_integer():
                return str(int(valor))
            return str(valor).strip()

        texto = str(valor).strip()
        if not texto:
            raise ValueError("El IdApontamento no puede venir vacío.")

        try:
            numero = float(texto)
            if numero.is_integer():
                return str(int(numero))
        except ValueError:
            pass

        return texto

    def _generar_id_formulario(self) -> str:
        formularios = self.formulario_repository.listar_formularios()
        maximo = 0

        for formulario in formularios:
            valor = str(formulario.get("id_formulario", "")).strip()
            if not valor.startswith("FORM-"):
                continue

            try:
                numero = int(valor.split("-")[-1])
            except ValueError:
                continue

            if numero > maximo:
                maximo = numero

        return f"FORM-{maximo + 1:04d}"

    def _obtener_fecha_formulario(self, hora_fim: Any) -> str:
        if isinstance(hora_fim, datetime):
            return hora_fim.date().isoformat()

        texto = self._normalizar_texto(hora_fim)
        if not texto:
            return datetime.now().date().isoformat()

        try:
            return datetime.fromisoformat(texto).date().isoformat()
        except ValueError:
            return datetime.now().date().isoformat()

    def listar_formularios(self) -> list[dict]:
        return self.formulario_repository.listar_formularios()

    def listar_formularios_por_estado(self, estado: str) -> list[dict]:
        return self.formulario_repository.listar_por_estado(estado)

    def listar_formularios_pendientes_operario(self) -> list[dict]:
        pendientes = self.listar_formularios_por_estado("pendiente_operario")

        return sorted(
            pendientes,
            key=lambda formulario: (
                self._normalizar_texto(formulario.get("fecha_creacion")),
                self._normalizar_texto(formulario.get("id_formulario")),
            ),
        )

    def obtener_siguiente_formulario_pendiente_operario(self) -> dict | None:
        pendientes = self.listar_formularios_pendientes_operario()
        if not pendientes:
            return None
        return pendientes[0]

    def obtener_formulario_por_id(self, id_formulario: str) -> dict | None:
        return self.formulario_repository.obtener_por_id(id_formulario)

    def obtener_formulario_por_id_apontamento(
        self,
        id_apontamento: Any,
    ) -> dict | None:
        id_normalizado = self._normalizar_id_apontamento(id_apontamento)
        return self.formulario_repository.obtener_por_id_apontamento(id_normalizado)

    def existe_formulario_para_apontamento(self, id_apontamento: Any) -> bool:
        return self.obtener_formulario_por_id_apontamento(id_apontamento) is not None

    def crear_formulario_pendiente_desde_registro_apontamento(
        self,
        registro: dict[str, Any],
    ) -> dict[str, Any]:
        id_apontamento = self._normalizar_id_apontamento(
            registro.get("id_apontamento")
        )

        existente = self.obtener_formulario_por_id_apontamento(id_apontamento)
        if existente:
            return {
                "ya_existia": True,
                "formulario": existente,
            }

        identificador = self._normalizar_texto(
            registro.get("num_ordem") or registro.get("identificador")
        )
        if not identificador:
            raise ValueError(
                "No se puede crear formulario sin identificador o NumOrdem."
            )

        cod_recurso = self._normalizar_texto(
            registro.get("cod_recurso") or registro.get("maquina")
        )
        if not cod_recurso:
            raise ValueError("No se puede crear formulario sin CodRecurso.")

        cod_setor = self._normalizar_texto(
            registro.get("cod_setor") or registro.get("area")
        )

        hora_fim = self._serializar_valor(
            registro.get("hora_fim") or registro.get("HoraFim")
        )
        fecha_formulario = self._obtener_fecha_formulario(hora_fim)
        ahora = datetime.now().isoformat(timespec="seconds")

        formulario = {
            "id_formulario": self._generar_id_formulario(),
            "identificador": identificador,
            "id_apontamento": id_apontamento,
            "fecha_formulario": fecha_formulario,
            "area": cod_setor,
            "maquina": cod_recurso,
            "cod_recurso": cod_recurso,
            "cod_setor": cod_setor,
            "cod_ativ": self._serializar_valor(
                registro.get("cod_ativ") or registro.get("CodAtiv")
            ),
            "turno": self._serializar_valor(
                registro.get("turno") or registro.get("Turno")
            ),
            "hora_fim": hora_fim,
            "operario": self._normalizar_texto(
                registro.get("operador") or registro.get("operario")
            ),
            "estacion": self._normalizar_texto(registro.get("estacion")),
            "evento_origen": "apontamento_sql",
            "estado": "pendiente_operario",
            "descripcion_op": self._normalizar_texto(
                registro.get("descripcion_op") or registro.get("DescricaoOP")
            ),
            "descripcion_proceso": self._normalizar_texto(
                registro.get("descripcion_proceso")
                or registro.get("descricao_processo")
                or registro.get("DescricaoProcesso")
            ),
            "observacion_general": self._normalizar_texto(
                registro.get("obs")
            ),
            "fecha_creacion": ahora,
            "fecha_actualizacion": ahora,
        }

        guardado = self.formulario_repository.add_formulario(formulario)

        return {
            "ya_existia": False,
            "formulario": guardado,
        }

    def actualizar_estado_formulario(
        self,
        id_formulario: str,
        estado: str,
        observacion_general: str | None = None,
    ) -> dict:
        formulario = self.obtener_formulario_por_id(id_formulario)
        if not formulario:
            raise ValueError(f"No existe el formulario {id_formulario}.")

        cambios = {
            "estado": self._normalizar_texto(estado),
            "fecha_actualizacion": datetime.now().isoformat(timespec="seconds"),
        }

        if observacion_general is not None:
            cambios["observacion_general"] = self._normalizar_texto(
                observacion_general
            )

        actualizado = self.formulario_repository.actualizar_formulario(
            id_formulario,
            cambios,
        )

        if not actualizado:
            raise ValueError(f"No se pudo actualizar el formulario {id_formulario}.")

        return actualizado

    def actualizar_campos_formulario(
        self,
        id_formulario: str,
        cambios: dict[str, Any],
    ) -> dict:
        formulario = self.obtener_formulario_por_id(id_formulario)
        if not formulario:
            raise ValueError(f"No existe el formulario {id_formulario}.")

        cambios_normalizados = dict(cambios)
        cambios_normalizados["fecha_actualizacion"] = datetime.now().isoformat(
            timespec="seconds"
        )

        actualizado = self.formulario_repository.actualizar_formulario(
            id_formulario,
            cambios_normalizados,
        )

        if not actualizado:
            raise ValueError(f"No se pudo actualizar el formulario {id_formulario}.")

        return actualizado

    def asignar_operario(
        self,
        id_formulario: str,
        operario: str,
    ) -> dict:
        operario_normalizado = self._normalizar_texto(operario)
        if not operario_normalizado:
            raise ValueError("El operario no puede venir vacío.")

        return self.actualizar_campos_formulario(
            id_formulario=id_formulario,
            cambios={
                "operario": operario_normalizado,
            },
        )

    def marcar_formulario_en_apertura(self, id_formulario: str) -> dict:
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado="en_apertura",
        )

    def marcar_formulario_pendiente_operario(self, id_formulario: str) -> dict:
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado="pendiente_operario",
        )

    def marcar_formulario_completado(
        self,
        id_formulario: str,
        observacion_general: str | None = None,
    ) -> dict:
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado="completado",
            observacion_general=observacion_general,
        )