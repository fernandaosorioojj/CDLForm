"""Servicios de negocio para formularios, preguntas, plantillas y respuestas.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from datetime import datetime
from itertools import product
from typing import Any

from core.enums import TipoPregunta
from models.pregunta import Pregunta
from repositories.pregunta_repository import PreguntaRepository
from services.forms.plantilla_preguntas_service import PlantillaPreguntasService
from services.jobtrack.catalogo_contexto_service import CatalogoContextoService
from utils.id_generator import generate_id


# Bloque CDLform: clase PreguntaService; agrupa estado y comportamiento de esta parte del flujo.
class PreguntaService:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        repository: PreguntaRepository | None = None,
        plantilla_service: PlantillaPreguntasService | None = None,
        catalogo_contexto_service: CatalogoContextoService | None = None,
    ) -> None:
        self.repository = repository or PreguntaRepository()
        self.plantilla_service = plantilla_service or PlantillaPreguntasService()
        self.catalogo_contexto_service = (
            catalogo_contexto_service or CatalogoContextoService()
        )

    # Bloque CDLform: funcion/metodo listar_preguntas; encapsula una operacion del flujo del modulo.
    def listar_preguntas(self, solo_activas: bool = False) -> list[dict]:
        preguntas = self.repository.get_all()

        if solo_activas:
            preguntas = [p for p in preguntas if p.get("activa", True)]

        return sorted(
            preguntas,
            key=lambda x: (
                x.get("orden", 0),
                x.get("clave_pregunta", x.get("id_pregunta", "")),
                x.get("version", 1),
            ),
        )

    # Bloque CDLform: funcion/metodo obtener_pregunta; encapsula una operacion del flujo del modulo.
    def obtener_pregunta(self, id_pregunta: str) -> dict | None:
        return self.repository.find_by_id(id_pregunta)

    # Bloque CDLform: funcion/metodo crear_pregunta; encapsula una operacion del flujo del modulo.
    def crear_pregunta(
        self,
        texto: str,
        tipo: str,
        obligatoria: bool = True,
        activa: bool = True,
        orden: int = 1,
        filtros_contexto: dict | None = None,
        opciones_respuesta: list | None = None,
    ) -> dict:
        preguntas = self.repository.get_all()
        ahora = datetime.now().isoformat(timespec="seconds")
        id_pregunta = generate_id("PREG", preguntas, "id_pregunta")
        tipo_enum = self._parse_tipo(tipo)
        opciones_normalizadas = self._normalizar_opciones_respuesta(
            tipo=tipo_enum,
            opciones_respuesta=opciones_respuesta or [],
        )

        nueva_pregunta = Pregunta(
            id_pregunta=id_pregunta,
            texto=texto.strip(),
            tipo=tipo_enum,
            activa=activa,
            obligatoria=obligatoria,
            orden=orden,
            version=1,
            clave_pregunta=id_pregunta,
            fecha_creacion=ahora,
            fecha_actualizacion=ahora,
            filtros_contexto=filtros_contexto or {},
            opciones_respuesta=opciones_normalizadas,
        )

        pregunta_dict = self.repository.add(nueva_pregunta.to_dict())
        self._sincronizar_plantillas_por_preguntas([pregunta_dict])
        return pregunta_dict

    # Bloque CDLform: funcion/metodo actualizar_pregunta; encapsula una operacion del flujo del modulo.
    def actualizar_pregunta(
        self,
        id_pregunta: str,
        texto: str,
        tipo: str,
        obligatoria: bool = True,
        activa: bool = True,
        orden: int = 1,
        filtros_contexto: dict | None = None,
        opciones_respuesta: list | None = None,
    ) -> bool:
        pregunta_actual = self.repository.find_by_id(id_pregunta)
        if not pregunta_actual:
            raise ValueError("La pregunta no existe.")

        preguntas = self.repository.get_all()
        ahora = datetime.now().isoformat(timespec="seconds")
        id_nueva_version = generate_id("PREG", preguntas, "id_pregunta")
        tipo_enum = self._parse_tipo(tipo)
        clave_pregunta = str(
            pregunta_actual.get("clave_pregunta") or pregunta_actual.get("id_pregunta")
        ).strip()
        version_actual = int(pregunta_actual.get("version", 1))
        opciones_normalizadas = self._normalizar_opciones_respuesta(
            tipo=tipo_enum,
            opciones_respuesta=opciones_respuesta or [],
        )

        version_anterior = dict(pregunta_actual)
        version_anterior["activa"] = False
        version_anterior["fecha_actualizacion"] = ahora
        version_anterior["fecha_desactivacion"] = ahora
        version_anterior["reemplazada_por"] = id_nueva_version

        nueva_version = Pregunta(
            id_pregunta=id_nueva_version,
            texto=texto.strip(),
            tipo=tipo_enum,
            activa=activa,
            obligatoria=obligatoria,
            orden=orden,
            version=version_actual + 1,
            clave_pregunta=clave_pregunta,
            fecha_creacion=ahora,
            fecha_actualizacion=ahora,
            filtros_contexto=filtros_contexto or {},
            opciones_respuesta=opciones_normalizadas,
        )

        actualizado = self.repository.update_by_id(id_pregunta, version_anterior)
        if not actualizado:
            return False

        self.repository.add(nueva_version.to_dict())
        self._sincronizar_plantillas_por_preguntas(
            [version_anterior, nueva_version.to_dict()]
        )
        return True

    # Bloque CDLform: funcion/metodo desactivar_pregunta; encapsula una operacion del flujo del modulo.
    def desactivar_pregunta(self, id_pregunta: str) -> bool:
        pregunta_actual = self.repository.find_by_id(id_pregunta)
        if not pregunta_actual:
            raise ValueError("La pregunta no existe.")

        ahora = datetime.now().isoformat(timespec="seconds")
        pregunta_actualizada = dict(pregunta_actual)
        pregunta_actualizada["activa"] = False
        pregunta_actualizada["fecha_actualizacion"] = ahora
        pregunta_actualizada["fecha_desactivacion"] = ahora

        actualizado = self.repository.update_by_id(id_pregunta, pregunta_actualizada)
        if actualizado:
            self._sincronizar_plantillas_por_preguntas([pregunta_actualizada])
        return actualizado

    # Bloque CDLform: funcion/metodo eliminar_pregunta; encapsula una operacion del flujo del modulo.
    def eliminar_pregunta(self, id_pregunta: str) -> bool:
        return self.desactivar_pregunta(id_pregunta)

    # Bloque CDLform: funcion/metodo listar_preguntas_para_contexto; encapsula una operacion del flujo del modulo.
    def listar_preguntas_para_contexto(self, contexto: dict) -> list[dict]:
        contexto_normalizado = self._normalizar_contexto(contexto)
        if not contexto_normalizado:
            return []

        preguntas = [
            pregunta
            for pregunta in self.listar_preguntas(solo_activas=True)
            if self._cumple_filtros(
                contexto=contexto_normalizado,
                filtros=pregunta.get("filtros_contexto", {}),
            )
        ]

        return sorted(
            preguntas,
            key=lambda x: (
                x.get("orden", 0),
                x.get("clave_pregunta", x.get("id_pregunta", "")),
                x.get("version", 1),
            ),
        )

    # Bloque CDLform: funcion/metodo listar_preguntas_para_plantilla; encapsula una operacion del flujo del modulo.
    def listar_preguntas_para_plantilla(self, id_plantilla: str) -> list[dict]:
        plantilla = self.plantilla_service.repository.obtener_por_id(id_plantilla)
        if not plantilla:
            return []

        preguntas_por_id = {
            pregunta.get("id_pregunta"): pregunta
            for pregunta in self.listar_preguntas(solo_activas=False)
        }

        resultado: list[dict] = []
        for item in sorted(plantilla.items, key=lambda item: item.orden):
            pregunta = preguntas_por_id.get(item.id_pregunta)
            if pregunta:
                resultado.append(pregunta)

        return resultado

    # Bloque CDLform: funcion/metodo asegurar_plantilla_para_contexto; encapsula una operacion del flujo del modulo.
    def asegurar_plantilla_para_contexto(
        self,
        cod_recurso: str,
        cod_setor: str,
    ):
        contexto = self._normalizar_contexto(
            {
                "cod_recurso": cod_recurso,
                "cod_setor": cod_setor,
            }
        )
        if not contexto.get("cod_recurso") or not contexto.get("cod_setor"):
            return None

        preguntas = self.listar_preguntas_para_contexto(contexto)
        return self.plantilla_service.asegurar_plantilla_contexto(
            cod_recurso=contexto["cod_recurso"],
            cod_setor=contexto["cod_setor"],
            preguntas=preguntas,
        )

    # Bloque CDLform: funcion/metodo _cumple_filtros; encapsula una operacion del flujo del modulo.
    def _cumple_filtros(self, contexto: dict, filtros: dict) -> bool:
        if not filtros:
            return True

        for clave, valores_permitidos in filtros.items():
            clave_normalizada = self._normalizar_clave_filtro(clave)

            if not valores_permitidos:
                continue

            valor_contexto = contexto.get(clave_normalizada)
            if valor_contexto is None:
                return False

            valor_contexto_normalizado = self._normalizar_valor(valor_contexto)

            valores_normalizados = [
                self._normalizar_valor(valor)
                for valor in valores_permitidos
                if self._normalizar_valor(valor)
            ]

            if valor_contexto_normalizado not in valores_normalizados:
                return False

        return True

    # Bloque CDLform: funcion/metodo _normalizar_contexto; encapsula una operacion del flujo del modulo.
    def _normalizar_contexto(self, contexto: dict) -> dict:
        contexto_normalizado: dict[str, str] = {}

        for clave, valor in contexto.items():
            clave_normalizada = self._normalizar_clave_filtro(clave)
            valor_normalizado = self._normalizar_valor(valor)

            if valor_normalizado:
                contexto_normalizado[clave_normalizada] = valor_normalizado

        return contexto_normalizado

    # Bloque CDLform: funcion/metodo _normalizar_clave_filtro; encapsula una operacion del flujo del modulo.
    def _normalizar_clave_filtro(self, clave: str) -> str:
        clave_limpia = str(clave).strip().lower()

        aliases = {
            "codsetor": "cod_setor",
            "cod_setor": "cod_setor",
            "area": "cod_setor",
            "codrecurso": "cod_recurso",
            "cod_recurso": "cod_recurso",
            "maquina": "cod_recurso",
            "tipotrabajo": "tipo_trabajo",
            "tipo_trabajo": "tipo_trabajo",
            "turno": "turno",
        }

        return aliases.get(clave_limpia, clave_limpia)

    # Bloque CDLform: funcion/metodo _normalizar_valor; encapsula una operacion del flujo del modulo.
    def _normalizar_valor(self, valor: Any) -> str:
        return str(valor).strip().upper()

    # Bloque CDLform: funcion/metodo _normalizar_opciones_respuesta; encapsula una operacion del flujo del modulo.
    def _normalizar_opciones_respuesta(
        self,
        tipo: TipoPregunta,
        opciones_respuesta: list,
    ) -> list:
        if tipo not in {
            TipoPregunta.SELECCION_UNICA,
            TipoPregunta.SELECCION_MULTIPLE,
            TipoPregunta.SI_NO,
        }:
            return []

        opciones_normalizadas: list[dict] = []

        for indice, opcion in enumerate(opciones_respuesta, start=1):
            if not isinstance(opcion, dict):
                raise ValueError("Cada opcion de respuesta debe ser un diccionario.")

            valor = str(opcion.get("valor", "")).strip()
            if not valor:
                raise ValueError("Cada opcion de respuesta debe tener un valor.")

            id_opcion = str(opcion.get("id_opcion") or f"OPC-{indice:03d}").strip()
            opciones_normalizadas.append(
                {
                    "id_opcion": id_opcion,
                    "valor": valor,
                    "accion_correctiva": str(
                        opcion.get("accion_correctiva", "")
                    ).strip(),
                    "activa": bool(opcion.get("activa", True)),
                    "version": int(opcion.get("version", 1)),
                    "clave_opcion": str(
                        opcion.get("clave_opcion") or id_opcion
                    ).strip(),
                }
            )

        if tipo in {
            TipoPregunta.SELECCION_UNICA,
            TipoPregunta.SELECCION_MULTIPLE,
        } and not opciones_normalizadas:
            raise ValueError(
                "Las preguntas de seleccion deben tener al menos una opcion."
            )

        return opciones_normalizadas

    # Bloque CDLform: funcion/metodo _parse_tipo; encapsula una operacion del flujo del modulo.
    def _parse_tipo(self, tipo: str | TipoPregunta) -> TipoPregunta:
        if isinstance(tipo, TipoPregunta):
            return tipo

        if not isinstance(tipo, str):
            raise TypeError("tipo debe ser string o TipoPregunta")

        tipo_limpio = tipo.strip().lower()

        mapa = {
            "texto": TipoPregunta.TEXTO,
            "numero": TipoPregunta.NUMERO,
            "si_no": TipoPregunta.SI_NO,
            "seleccion_unica": TipoPregunta.SELECCION_UNICA,
            "seleccion_multiple": TipoPregunta.SELECCION_MULTIPLE,
        }

        if tipo_limpio not in mapa:
            raise ValueError(f"Tipo de pregunta no valido: {tipo}")

        return mapa[tipo_limpio]

    # Bloque CDLform: funcion/metodo _sincronizar_plantillas_por_preguntas; encapsula una operacion del flujo del modulo.
    def _sincronizar_plantillas_por_preguntas(
        self,
        preguntas_afectadas: list[dict[str, Any]],
    ) -> None:
        contextos_disponibles = self._obtener_contextos_disponibles()
        pares_contexto: set[tuple[str, str]] = set()

        for pregunta in preguntas_afectadas:
            pares_contexto.update(
                self._contextos_plantilla_para_pregunta(
                    pregunta,
                    contextos_disponibles=contextos_disponibles,
                )
            )

        if not pares_contexto:
            return

        for cod_recurso, cod_setor in pares_contexto:
            preguntas_contexto = self.listar_preguntas_para_contexto(
                {
                    "cod_recurso": cod_recurso,
                    "cod_setor": cod_setor,
                }
            )

            self.plantilla_service.asegurar_plantilla_contexto(
                cod_recurso=cod_recurso,
                cod_setor=cod_setor,
                preguntas=preguntas_contexto,
            )

    # Bloque CDLform: funcion/metodo _contextos_plantilla_para_pregunta; encapsula una operacion del flujo del modulo.
    def _contextos_plantilla_para_pregunta(
        self,
        pregunta: dict[str, Any],
        *,
        contextos_disponibles: list[dict[str, str]],
    ) -> set[tuple[str, str]]:
        filtros = pregunta.get("filtros_contexto", {})
        if not isinstance(filtros, dict):
            return set()

        contextos_coincidentes = {
            (
                self._normalizar_valor(contexto.get("cod_recurso", "")),
                self._normalizar_valor(contexto.get("cod_setor", "")),
            )
            for contexto in contextos_disponibles
            if self._cumple_filtros(contexto, filtros)
        }

        if contextos_coincidentes:
            return contextos_coincidentes

        return self._expandir_contextos_desde_catalogos(filtros)

    # Bloque CDLform: funcion/metodo _expandir_contextos_desde_catalogos; encapsula una operacion del flujo del modulo.
    def _expandir_contextos_desde_catalogos(
        self,
        filtros: dict[str, Any],
    ) -> set[tuple[str, str]]:
        cod_recursos = self._normalizar_lista_filtro(filtros.get("cod_recurso", []))
        cod_setores = self._normalizar_lista_filtro(filtros.get("cod_setor", []))

        if not cod_recursos:
            cod_recursos = [
                self._normalizar_valor(valor)
                for valor in self.catalogo_contexto_service.listar_cod_recursos()
                if self._normalizar_valor(valor)
            ]

        if not cod_setores:
            cod_setores = [
                self._normalizar_valor(valor)
                for valor in self.catalogo_contexto_service.listar_cod_setores()
                if self._normalizar_valor(valor)
            ]

        if not cod_recursos or not cod_setores:
            return set()

        return set(product(cod_recursos, cod_setores))

    # Bloque CDLform: funcion/metodo _obtener_contextos_disponibles; encapsula una operacion del flujo del modulo.
    def _obtener_contextos_disponibles(self) -> list[dict[str, str]]:
        contextos = self.catalogo_contexto_service.listar_contextos_recurso_setor()
        if not contextos:
            return []

        resultado: list[dict[str, str]] = []
        vistos: set[tuple[str, str]] = set()

        for contexto in contextos:
            cod_recurso = self._normalizar_valor(contexto.get("cod_recurso", ""))
            cod_setor = self._normalizar_valor(contexto.get("cod_setor", ""))
            if not cod_recurso or not cod_setor:
                continue

            clave = (cod_recurso, cod_setor)
            if clave in vistos:
                continue

            vistos.add(clave)
            resultado.append(
                {
                    "cod_recurso": cod_recurso,
                    "cod_setor": cod_setor,
                }
            )

        return resultado

    # Bloque CDLform: funcion/metodo _normalizar_lista_filtro; encapsula una operacion del flujo del modulo.
    def _normalizar_lista_filtro(self, valores: Any) -> list[str]:
        if valores is None:
            return []

        if not isinstance(valores, list):
            valores = [valores]

        resultado: list[str] = []
        for valor in valores:
            valor_normalizado = self._normalizar_valor(valor)
            if valor_normalizado and valor_normalizado not in resultado:
                resultado.append(valor_normalizado)

        return resultado
