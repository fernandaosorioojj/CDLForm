from __future__ import annotations

from typing import Optional

from core.exceptions import NotFoundError, ValidationError
from models.formulario import Formulario
from repositories.formulario_repository import FormularioRepository
from utils.id_generator import generate_id


class FormularioService:
    def __init__(self, formulario_repository: Optional[FormularioRepository] = None):
        self.formulario_repository = formulario_repository or FormularioRepository()

    def crear_formulario(
        self,
        identificador: str,
        operario: str,
        id_operario: str = "",
        contexto: Optional[dict] = None,
        evento_origen: Optional[str] = None,
        estado: str = "pendiente",
    ) -> Formulario:
        self._validar_datos_obligatorios(
            identificador=identificador,
            operario=operario,
            estado=estado,
        )

        registros_existentes = [
            formulario.to_dict() for formulario in self.formulario_repository.list_all()
        ]

        id_formulario = generate_id(
            prefix="FORM",
            records=registros_existentes,
            field_name="id_formulario",
        )

        contexto = contexto or {}

        formulario = Formulario(
            id_formulario=id_formulario,
            identificador=identificador.strip(),
            operario=operario.strip(),
            id_operario=id_operario.strip() if isinstance(id_operario, str) else "",
            cod_setor=str(contexto.get("cod_setor", "")).strip(),
            cod_recurso=str(contexto.get("cod_recurso", "")).strip(),
            cod_ativ=str(contexto.get("cod_ativ", "")).strip(),
            turno=str(contexto.get("turno", "")).strip(),
            tipo_trabajo=str(contexto.get("tipo_trabajo", "")).strip(),
            evento_origen=evento_origen.strip()
            if isinstance(evento_origen, str) and evento_origen.strip()
            else None,
            estado=estado.strip(),
        )

        self.formulario_repository.add_formulario(formulario)
        return formulario

    def obtener_formulario_por_id(self, id_formulario: str) -> Formulario:
        if not id_formulario or not id_formulario.strip():
            raise ValidationError("El id_formulario es obligatorio.")

        formulario = self.formulario_repository.get_by_id(id_formulario.strip())
        if not formulario:
            raise NotFoundError(f"No se encontró el formulario '{id_formulario}'.")

        return formulario
    
    def obtener_formulario_por_evento_origen(self, evento_origen: str) -> Formulario | None:
        if not evento_origen or not str(evento_origen).strip():
            return None

        return self.formulario_repository.get_by_evento_origen(
            str(evento_origen).strip()
        )


    def listar_formularios(self) -> list[Formulario]:
        return self.formulario_repository.list_all()

    def listar_formularios_por_estado(self, estado: str) -> list[Formulario]:
        if not estado or not estado.strip():
            raise ValidationError("El estado es obligatorio para filtrar formularios.")

        return self.formulario_repository.get_formularios_por_estado(estado.strip())

    def listar_formularios_por_operario(self, operario: str) -> list[Formulario]:
        if not operario or not operario.strip():
            raise ValidationError("El operario es obligatorio para filtrar formularios.")

        return self.formulario_repository.get_formularios_por_operario(operario.strip())

    def actualizar_estado_formulario(self, id_formulario: str, nuevo_estado: str) -> Formulario:
        if not id_formulario or not id_formulario.strip():
            raise ValidationError("El id_formulario es obligatorio.")

        if not nuevo_estado or not nuevo_estado.strip():
            raise ValidationError("El nuevo estado es obligatorio.")

        formulario = self.obtener_formulario_por_id(id_formulario.strip())
        formulario.estado = nuevo_estado.strip()

        self.formulario_repository.update_formulario(id_formulario.strip(), formulario)
        return formulario

    def asignar_operario(self, id_formulario: str, operario: str) -> Formulario:
        if not id_formulario or not id_formulario.strip():
            raise ValidationError("El id_formulario es obligatorio.")

        if not operario or not operario.strip():
            raise ValidationError("El operario es obligatorio.")

        formulario = self.obtener_formulario_por_id(id_formulario.strip())
        formulario.operario = operario.strip()

        self.formulario_repository.update_formulario(id_formulario.strip(), formulario)
        return formulario

    def _validar_datos_obligatorios(
        self,
        identificador: str,
        operario: str,
        estado: str,
    ) -> None:
        if not identificador or not identificador.strip():
            raise ValidationError("El identificador es obligatorio.")

        if not operario or not operario.strip():
            raise ValidationError("El operario es obligatorio.")

        if not estado or not estado.strip():
            raise ValidationError("El estado del formulario es obligatorio.")