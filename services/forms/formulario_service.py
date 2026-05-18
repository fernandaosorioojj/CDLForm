"""Servicios de negocio para formularios, preguntas, plantillas y respuestas.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pyodbc

from models.formulario import (
    ESTADO_CANCELADO,
    ESTADO_COMPLETADO,
    ESTADO_EN_APERTURA,
    ESTADO_EN_PROGRESO,
    ESTADO_PENDIENTE_OPERARIO,
    Formulario,
)
from repositories.formulario_repository import FormularioRepository
from services.forms.plantilla_preguntas_service import PlantillaPreguntasService
from services.forms.pregunta_service import PreguntaService


# Bloque CDLform: clase FormularioService; agrupa estado y comportamiento de esta parte del flujo.
class FormularioService:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        formulario_repository: FormularioRepository | None = None,
        plantilla_preguntas_service: PlantillaPreguntasService | None = None,
        pregunta_service: PreguntaService | None = None,
    ) -> None:
        self.formulario_repository = formulario_repository or FormularioRepository()
        self.plantilla_preguntas_service = (
            plantilla_preguntas_service or PlantillaPreguntasService()
        )
        self.pregunta_service = pregunta_service or PreguntaService()

    # Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    # Bloque CDLform: funcion/metodo _serializar_valor; encapsula una operacion del flujo del modulo.
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

    # Bloque CDLform: funcion/metodo _normalizar_id_apontamento; encapsula una operacion del flujo del modulo.
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

    # Bloque CDLform: funcion/metodo _es_error_constraint_estado_en_progreso; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _es_error_constraint_estado_en_progreso(exc: Exception) -> bool:
        if not isinstance(exc, pyodbc.IntegrityError):
            return False

        mensaje = str(exc)
        return "CK_formularios_operario_estado" in mensaje

    # Bloque CDLform: funcion/metodo _generar_id_formulario; encapsula una operacion del flujo del modulo.
    def _generar_id_formulario(self) -> str:
        formularios = self.formulario_repository.listar_formularios()
        maximo = 0

        for formulario in formularios:
            valor = formulario.id_formulario
            if not valor.startswith("FORM-"):
                continue

            try:
                numero = int(valor.split("-")[-1])
            except ValueError:
                continue

            if numero > maximo:
                maximo = numero

        return f"FORM-{maximo + 1:04d}"

    # Bloque CDLform: funcion/metodo _obtener_fecha_formulario; encapsula una operacion del flujo del modulo.
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

    # Bloque CDLform: funcion/metodo _validar_formulario_nuevo_con_plantilla; encapsula una operacion del flujo del modulo.
    @staticmethod
    def _validar_formulario_nuevo_con_plantilla(formulario: Formulario) -> None:
        if not formulario.id_formulario:
            raise ValueError("No se puede crear un formulario sin id_formulario.")

        if not formulario.identificador:
            raise ValueError("No se puede crear un formulario sin identificador u OP.")

        if not formulario.id_apontamento:
            raise ValueError("No se puede crear un formulario sin IdApontamento.")

        if not formulario.fecha_formulario:
            raise ValueError("No se puede crear un formulario sin fecha_formulario.")

        if not (formulario.cod_setor or formulario.area):
            raise ValueError("No se puede crear un formulario sin CodSetor.")

        if not (formulario.cod_recurso or formulario.maquina):
            raise ValueError("No se puede crear un formulario sin CodRecurso.")

        if not formulario.id_plantilla_preguntas:
            raise ValueError(
                "No se puede crear un formulario sin id_plantilla_preguntas."
            )

        if int(formulario.version_plantilla_preguntas or 0) <= 0:
            raise ValueError(
                "No se puede crear un formulario sin version_plantilla_preguntas."
            )

    # Bloque CDLform: funcion/metodo listar_formularios; encapsula una operacion del flujo del modulo.
    def listar_formularios(self) -> list[Formulario]:
        return self.formulario_repository.listar_formularios()

    # Bloque CDLform: funcion/metodo listar_formularios_por_estado; encapsula una operacion del flujo del modulo.
    def listar_formularios_por_estado(self, estado: str) -> list[Formulario]:
        return self.formulario_repository.listar_por_estado(estado)

    # Bloque CDLform: funcion/metodo listar_formularios_por_estados; encapsula una operacion del flujo del modulo.
    def listar_formularios_por_estados(self, estados: list[str]) -> list[Formulario]:
        estados_normalizados = {
            self._normalizar_texto(estado)
            for estado in estados
            if self._normalizar_texto(estado)
        }

        if not estados_normalizados:
            return []

        return [
            formulario
            for formulario in self.listar_formularios()
            if formulario.estado in estados_normalizados
        ]

    # Bloque CDLform: funcion/metodo listar_formularios_pendientes_operario; encapsula una operacion del flujo del modulo.
    def listar_formularios_pendientes_operario(self) -> list[Formulario]:
        pendientes = self.listar_formularios_por_estados(
            [
                ESTADO_EN_APERTURA,
                ESTADO_PENDIENTE_OPERARIO,
            ]
        )

        return sorted(
            pendientes,
            key=lambda formulario: (
                formulario.fecha_creacion,
                formulario.id_formulario,
            ),
        )

    # Bloque CDLform: funcion/metodo obtener_siguiente_formulario_pendiente_operario; encapsula una operacion del flujo del modulo.
    def obtener_siguiente_formulario_pendiente_operario(self) -> Formulario | None:
        pendientes = self.listar_formularios_pendientes_operario()
        if not pendientes:
            return None
        return pendientes[0]

    # Bloque CDLform: funcion/metodo obtener_formulario_por_id; encapsula una operacion del flujo del modulo.
    def obtener_formulario_por_id(self, id_formulario: str) -> Formulario | None:
        return self.formulario_repository.obtener_por_id(id_formulario)

    # Bloque CDLform: funcion/metodo obtener_formulario_por_id_apontamento; encapsula una operacion del flujo del modulo.
    def obtener_formulario_por_id_apontamento(
        self,
        id_apontamento: Any,
    ) -> Formulario | None:
        id_normalizado = self._normalizar_id_apontamento(id_apontamento)
        return self.formulario_repository.obtener_por_id_apontamento(id_normalizado)

    # Bloque CDLform: funcion/metodo existe_formulario_para_apontamento; encapsula una operacion del flujo del modulo.
    def existe_formulario_para_apontamento(self, id_apontamento: Any) -> bool:
        return self.obtener_formulario_por_id_apontamento(id_apontamento) is not None

    # Bloque CDLform: funcion/metodo guardar_formulario; encapsula una operacion del flujo del modulo.
    def guardar_formulario(self, formulario: Formulario) -> Formulario:
        if not self.formulario_repository.obtener_por_id(formulario.id_formulario):
            self._validar_formulario_nuevo_con_plantilla(formulario)
        return self.formulario_repository.guardar(formulario)

    # Bloque CDLform: funcion/metodo crear_formulario_pendiente_desde_registro_apontamento; encapsula una operacion del flujo del modulo.
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
        if not cod_setor:
            raise ValueError("No se puede crear formulario sin CodSetor.")

        hora_fim = self._serializar_valor(
            registro.get("hora_fim") or registro.get("HoraFim")
        )
        fecha_formulario = self._obtener_fecha_formulario(hora_fim)
        ahora = datetime.now().isoformat(timespec="seconds")
        plantilla_preguntas = self.plantilla_preguntas_service.obtener_activa(
            cod_recurso=cod_recurso,
            cod_setor=cod_setor,
        )
        if not plantilla_preguntas:
            plantilla_preguntas = self.pregunta_service.asegurar_plantilla_para_contexto(
                cod_recurso=cod_recurso,
                cod_setor=cod_setor,
            )
        if not plantilla_preguntas:
            raise ValueError(
                "No existe una plantilla activa de preguntas para "
                f"CodSetor {cod_setor or '-'} y CodRecurso {cod_recurso}."
            )

        formulario = Formulario(
            id_formulario=self._generar_id_formulario(),
            identificador=identificador,
            id_apontamento=id_apontamento,
            fecha_formulario=fecha_formulario,
            area=cod_setor,
            maquina=cod_recurso,
            cod_recurso=cod_recurso,
            cod_setor=cod_setor,
            turno=self._serializar_valor(
                registro.get("turno") or registro.get("Turno")
            ),
            hora_fim=hora_fim,
            operario=self._normalizar_texto(
                registro.get("operador") or registro.get("operario")
            ),
            supervisor_apontamento=self._normalizar_texto(
                registro.get("supervisor_apontamento")
                or registro.get("supervisor")
                or registro.get("Supervisor")
            ),
            estacion=self._normalizar_texto(registro.get("estacion")),
            evento_origen="apontamento_sql",
            estado=ESTADO_EN_APERTURA,
            descripcion_op=self._normalizar_texto(
                registro.get("descripcion_op") or registro.get("DescricaoOP")
            ),
            descripcion_proceso=self._normalizar_texto(
                registro.get("descripcion_proceso")
                or registro.get("descricao_processo")
                or registro.get("DescricaoProcesso")
            ),
            observacion_general=self._normalizar_texto(registro.get("obs")),
            fecha_creacion=ahora,
            fecha_actualizacion=ahora,
            id_plantilla_preguntas=plantilla_preguntas.id_plantilla,
            version_plantilla_preguntas=plantilla_preguntas.version,
        )

        self._validar_formulario_nuevo_con_plantilla(formulario)
        guardado = self.formulario_repository.add_formulario(formulario)

        return {
            "ya_existia": False,
            "formulario": guardado,
        }

    # Bloque CDLform: funcion/metodo actualizar_estado_formulario; encapsula una operacion del flujo del modulo.
    def actualizar_estado_formulario(
        self,
        id_formulario: str,
        estado: str,
        observacion_general: str | None = None,
    ) -> Formulario:
        formulario = self.obtener_formulario_por_id(id_formulario)
        if not formulario:
            raise ValueError(f"No existe el formulario {id_formulario}.")

        formulario.estado = self._normalizar_texto(estado)
        formulario.fecha_actualizacion = datetime.now().isoformat(timespec="seconds")

        if observacion_general is not None:
            formulario.observacion_general = self._normalizar_texto(
                observacion_general
            )

        return self.formulario_repository.guardar(formulario)

    # Bloque CDLform: funcion/metodo actualizar_campos_formulario; encapsula una operacion del flujo del modulo.
    def actualizar_campos_formulario(
        self,
        id_formulario: str,
        cambios: dict[str, Any],
    ) -> Formulario:
        formulario = self.obtener_formulario_por_id(id_formulario)
        if not formulario:
            raise ValueError(f"No existe el formulario {id_formulario}.")

        formulario.actualizar(cambios)
        formulario.fecha_actualizacion = datetime.now().isoformat(timespec="seconds")

        return self.formulario_repository.guardar(formulario)

    # Bloque CDLform: funcion/metodo asignar_plantilla_activa_si_falta; encapsula una operacion del flujo del modulo.
    def asignar_plantilla_activa_si_falta(
        self,
        id_formulario: str,
    ) -> Formulario:
        # SOPORTE / REPARACION MANUAL:
        # No es parte del cierre normal del formulario operario. Sirve para
        # recuperar formularios antiguos creados sin plantilla asignada.
        formulario = self.obtener_formulario_por_id(id_formulario)
        if not formulario:
            raise ValueError(f"No existe el formulario {id_formulario}.")

        if formulario.id_plantilla_preguntas:
            return formulario

        plantilla_preguntas = self.plantilla_preguntas_service.obtener_activa(
            cod_recurso=formulario.cod_recurso or formulario.maquina,
            cod_setor=formulario.cod_setor or formulario.area,
        )
        if not plantilla_preguntas:
            plantilla_preguntas = self.pregunta_service.asegurar_plantilla_para_contexto(
                cod_recurso=formulario.cod_recurso or formulario.maquina,
                cod_setor=formulario.cod_setor or formulario.area,
            )
        if not plantilla_preguntas:
            raise ValueError(
                "No existe una plantilla activa de preguntas para "
                f"CodSetor {formulario.cod_setor or formulario.area or '-'} y "
                f"CodRecurso {formulario.cod_recurso or formulario.maquina or '-'}."
            )

        return self.actualizar_campos_formulario(
            id_formulario=id_formulario,
            cambios={
                "id_plantilla_preguntas": plantilla_preguntas.id_plantilla,
                "version_plantilla_preguntas": plantilla_preguntas.version,
            },
        )

    # Bloque CDLform: funcion/metodo asignar_operario; encapsula una operacion del flujo del modulo.
    def asignar_operario(
        self,
        id_formulario: str,
        operario: str,
    ) -> Formulario:
        operario_normalizado = self._normalizar_texto(operario)
        if not operario_normalizado:
            raise ValueError("El operario no puede venir vacío.")

        return self.actualizar_campos_formulario(
            id_formulario=id_formulario,
            cambios={
                "operario": operario_normalizado,
            },
        )

    # Bloque CDLform: funcion/metodo marcar_formulario_en_apertura; encapsula una operacion del flujo del modulo.
    def marcar_formulario_en_apertura(self, id_formulario: str) -> Formulario:
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado=ESTADO_EN_APERTURA,
        )

    # Bloque CDLform: funcion/metodo marcar_formulario_pendiente_operario; encapsula una operacion del flujo del modulo.
    def marcar_formulario_pendiente_operario(self, id_formulario: str) -> Formulario:
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado=ESTADO_PENDIENTE_OPERARIO,
        )

    # Bloque CDLform: funcion/metodo marcar_formulario_completado; encapsula una operacion del flujo del modulo.
    def marcar_formulario_completado(
        self,
        id_formulario: str,
        observacion_general: str | None = None,
    ) -> Formulario:
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado=ESTADO_COMPLETADO,
            observacion_general=observacion_general,
        )

    # Bloque CDLform: funcion/metodo marcar_formulario_cancelado; encapsula una operacion del flujo del modulo.
    def marcar_formulario_cancelado(
        self,
        id_formulario: str,
        observacion_general: str | None = None,
    ) -> Formulario:
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado=ESTADO_CANCELADO,
            observacion_general=observacion_general,
        )

    # Bloque CDLform: funcion/metodo marcar_formulario_en_progreso; encapsula una operacion del flujo del modulo.
    def marcar_formulario_en_progreso(
        self,
        id_formulario: str,
        observacion_general: str | None = None,
    ) -> Formulario:
        try:
            return self.actualizar_estado_formulario(
                id_formulario=id_formulario,
                estado=ESTADO_EN_PROGRESO,
                observacion_general=observacion_general,
            )
        except Exception as exc:
            if not self._es_error_constraint_estado_en_progreso(exc):
                raise

            # FALLBACK TEMPORAL:
            # Compatibilidad para bases que aun no ejecutaron el script 006.
            return self.actualizar_estado_formulario(
                id_formulario=id_formulario,
                estado=ESTADO_PENDIENTE_OPERARIO,
                observacion_general=observacion_general,
            )

    # Bloque CDLform: funcion/metodo marcar_formulario_enviado; encapsula una operacion del flujo del modulo.
    def marcar_formulario_enviado(
        self,
        id_formulario: str,
        observacion_general: str | None = None,
    ) -> Formulario:
        # LEGACY / ALIAS:
        # Nombre antiguo conservado para compatibilidad. El flujo actual usa
        # marcar_formulario_completado().
        return self.actualizar_estado_formulario(
            id_formulario=id_formulario,
            estado=ESTADO_COMPLETADO,
            observacion_general=observacion_general,
        )
