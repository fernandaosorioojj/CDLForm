from __future__ import annotations

from typing import List, Optional

from core.exceptions import ValidationError, NotFoundError
from models.operario import Operario
from repositories.operario_repository import OperarioRepository
from utils.id_generator import generate_id


class OperarioService:
    def __init__(self, operario_repository: Optional[OperarioRepository] = None):
        self.operario_repository = operario_repository or OperarioRepository()

    def crear_operario(
        self,
        nombre: str,
        area: str,
        maquina: str,
        activo: bool = True,
    ) -> Operario:
        self._validar_datos_obligatorios(
            nombre=nombre,
            area=area,
            maquina=maquina,
        )

        registros_existentes = self.operario_repository.get_all()

        id_operario = generate_id(
            prefix="OPER",
            records=registros_existentes,
            field_name="id_operario",
        )

        operario = Operario(
            id_operario=id_operario,
            nombre=nombre.strip(),
            area=area.strip(),
            maquina=maquina.strip(),
            activo=activo,
        )

        self.operario_repository.add_operario(operario)
        return operario

    def obtener_operario_por_id(self, id_operario: str) -> Operario:
        if not id_operario or not str(id_operario).strip():
            raise ValidationError("El id_operario es obligatorio.")

        operario = self.operario_repository.get_operario_by_id(id_operario.strip())

        if not operario:
            raise NotFoundError(f"No se encontró el operario '{id_operario}'.")

        return operario

    def listar_operarios(self, solo_activos: bool = True) -> List[Operario]:
        if solo_activos:
            return self.operario_repository.get_operarios_activos()

        return self.operario_repository.get_all_operarios()

    def listar_operarios_por_area(self, area: str, solo_activos: bool = True) -> List[Operario]:
        if not area or not area.strip():
            raise ValidationError("El área es obligatoria.")

        return self.operario_repository.get_operarios_por_area(
            area=area.strip(),
            solo_activos=solo_activos,
        )

    def listar_operarios_por_maquina(self, maquina: str, solo_activos: bool = True) -> List[Operario]:
        if not maquina or not maquina.strip():
            raise ValidationError("La máquina es obligatoria.")

        return self.operario_repository.get_operarios_por_maquina(
            maquina=maquina.strip(),
            solo_activos=solo_activos,
        )

    def listar_operarios_por_area_y_maquina(
        self,
        area: str,
        maquina: str,
        solo_activos: bool = True,
    ) -> List[Operario]:
        if not area or not area.strip():
            raise ValidationError("El área es obligatoria.")

        if not maquina or not maquina.strip():
            raise ValidationError("La máquina es obligatoria.")

        return self.operario_repository.get_operarios_por_area_y_maquina(
            area=area.strip(),
            maquina=maquina.strip(),
            solo_activos=solo_activos,
        )

    def cambiar_estado_operario(self, id_operario: str, activo: bool) -> Operario:
        if not id_operario or not id_operario.strip():
            raise ValidationError("El id_operario es obligatorio.")

        operario_actual = self.operario_repository.get_operario_by_id(id_operario.strip())

        if not operario_actual:
            raise NotFoundError(f"No se encontró el operario '{id_operario}'.")

        operario_actualizado = Operario(
            id_operario=operario_actual.id_operario,
            nombre=operario_actual.nombre,
            area=operario_actual.area,
            maquina=operario_actual.maquina,
            activo=activo,
        )

        self.operario_repository.update_operario(
            id_operario=operario_actualizado.id_operario,
            operario=operario_actualizado,
        )

        return operario_actualizado

    def actualizar_operario(
        self,
        id_operario: str,
        nombre: str,
        area: str,
        maquina: str,
        activo: bool = True,
    ) -> Operario:
        if not id_operario or not id_operario.strip():
            raise ValidationError("El id_operario es obligatorio.")

        self._validar_datos_obligatorios(
            nombre=nombre,
            area=area,
            maquina=maquina,
        )

        operario_existente = self.operario_repository.get_operario_by_id(id_operario.strip())

        if not operario_existente:
            raise NotFoundError(f"No se encontró el operario '{id_operario}'.")

        operario_actualizado = Operario(
            id_operario=id_operario.strip(),
            nombre=nombre.strip(),
            area=area.strip(),
            maquina=maquina.strip(),
            activo=activo,
        )

        self.operario_repository.update_operario(
            id_operario=operario_actualizado.id_operario,
            operario=operario_actualizado,
        )

        return operario_actualizado

    def _validar_datos_obligatorios(
        self,
        nombre: str,
        area: str,
        maquina: str,
    ) -> None:
        if not nombre or not nombre.strip():
            raise ValidationError("El nombre del operario es obligatorio.")

        if not area or not area.strip():
            raise ValidationError("El área del operario es obligatoria.")

        if not maquina or not maquina.strip():
            raise ValidationError("La máquina del operario es obligatoria.")