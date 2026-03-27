from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

from core.exceptions import DuplicateEntityError, NotFoundError, RepositoryError
from utils.json_manager import JsonManager

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        JsonManager.ensure_file_exists(self.file_path, [])

    def _read_raw(self) -> list[dict]:
        data = JsonManager.read_json(self.file_path, [])

        if not isinstance(data, list):
            raise RepositoryError(
                f"el archivo '{self.file_path}' debe contener una lista de registros"
            )

        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise RepositoryError(
                    f"el registro en posición {index} del archivo '{self.file_path}' no es un objeto válido"
                )

        return data

    def _write_raw(self, items: list[dict]) -> None:
        JsonManager.write_json(self.file_path, items)

    @abstractmethod
    def _from_dict(self, data: dict) -> T:
        pass

    @abstractmethod
    def _get_entity_id(self, entity: T) -> str:
        pass

    def list_all(self) -> list[T]:
        return [self._from_dict(item) for item in self._read_raw()]

    def save_all(self, entities: list[T]) -> None:
        serialized = [entity.to_dict() for entity in entities]
        self._write_raw(serialized)

    def get_by_id(self, entity_id: str) -> T:
        for entity in self.list_all():
            if self._get_entity_id(entity) == entity_id:
                return entity

        raise NotFoundError(f"no se encontró un registro con id '{entity_id}'")

    def exists(self, entity_id: str) -> bool:
        try:
            self.get_by_id(entity_id)
            return True
        except NotFoundError:
            return False

    def add(self, entity: T) -> None:
        entity_id = self._get_entity_id(entity)

        if self.exists(entity_id):
            raise DuplicateEntityError(f"ya existe un registro con id '{entity_id}'")

        entities = self.list_all()
        entities.append(entity)
        self.save_all(entities)

    def update(self, entity: T) -> None:
        entity_id = self._get_entity_id(entity)
        entities = self.list_all()

        updated = False
        new_entities: list[T] = []

        for current in entities:
            if self._get_entity_id(current) == entity_id:
                new_entities.append(entity)
                updated = True
            else:
                new_entities.append(current)

        if not updated:
            raise NotFoundError(f"no se encontró un registro con id '{entity_id}' para actualizar")

        self.save_all(new_entities)

    def delete(self, entity_id: str) -> None:
        entities = self.list_all()
        filtered_entities = [
            entity for entity in entities if self._get_entity_id(entity) != entity_id
        ]

        if len(filtered_entities) == len(entities):
            raise NotFoundError(f"no se encontró un registro con id '{entity_id}' para eliminar")

        self.save_all(filtered_entities)