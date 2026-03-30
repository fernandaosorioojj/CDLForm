from __future__ import annotations

from core.enums import TipoPregunta
from models.pregunta import Pregunta
from repositories.pregunta_repository import PreguntaRepository
from utils.id_generator import generate_id


class PreguntaService:
    def __init__(self) -> None:
        self.repository = PreguntaRepository()

    def listar_preguntas(self, solo_activas: bool = False) -> list[dict]:
        preguntas = self.repository.get_all()

        if solo_activas:
            preguntas = [p for p in preguntas if p.get("activa", True)]

        return sorted(preguntas, key=lambda x: x.get("orden", 0))

    def obtener_pregunta(self, id_pregunta: str) -> dict | None:
        return self.repository.find_by_id(id_pregunta)

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

        tipo_enum = self._parse_tipo(tipo)

        nueva_pregunta = Pregunta(
            id_pregunta=generate_id(preguntas, "PREG", "id_pregunta"),
            texto=texto.strip(),
            tipo=tipo_enum,
            activa=activa,
            obligatoria=obligatoria,
            orden=orden,
            filtros_contexto=filtros_contexto or {},
            opciones_respuesta=opciones_respuesta or [],
        )

        self.repository.add(nueva_pregunta.to_dict())
        return nueva_pregunta.to_dict()

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

        tipo_enum = self._parse_tipo(tipo)

        pregunta_actualizada = Pregunta(
            id_pregunta=id_pregunta,
            texto=texto.strip(),
            tipo=tipo_enum,
            activa=activa,
            obligatoria=obligatoria,
            orden=orden,
            filtros_contexto=filtros_contexto or {},
            opciones_respuesta=opciones_respuesta or [],
        )

        return self.repository.update_by_id(
            id_pregunta,
            pregunta_actualizada.to_dict(),
        )

    def desactivar_pregunta(self, id_pregunta: str) -> bool:
        return self.repository.update_by_id(id_pregunta, {"activa": False})

    def eliminar_pregunta(self, id_pregunta: str) -> bool:
        if hasattr(self.repository, "delete_by_id"):
            return self.repository.delete_by_id(id_pregunta)
        raise AttributeError("El repositorio no soporta delete_by_id")

    def listar_preguntas_para_contexto(self, contexto: dict) -> list[dict]:
        preguntas = self.listar_preguntas(solo_activas=True)
        resultado: list[dict] = []

        for pregunta in preguntas:
            filtros = pregunta.get("filtros_contexto", {})
            if self._cumple_filtros(contexto, filtros):
                resultado.append(pregunta)

        return sorted(resultado, key=lambda x: x.get("orden", 0))

    def _cumple_filtros(self, contexto: dict, filtros: dict) -> bool:
        if not filtros:
            return True

        for clave, valores_permitidos in filtros.items():
            if not valores_permitidos:
                continue

            valor_contexto = contexto.get(clave)
            if valor_contexto is None:
                return False

            valor_contexto_normalizado = str(valor_contexto).strip()

            valores_normalizados = [
                str(valor).strip() for valor in valores_permitidos if str(valor).strip()
            ]

            if valor_contexto_normalizado not in valores_normalizados:
                return False

        return True

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
        }

        if tipo_limpio not in mapa:
            raise ValueError(f"Tipo de pregunta no válido: {tipo}")

        return mapa[tipo_limpio]