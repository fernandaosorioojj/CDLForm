from pathlib import Path

from repositories.base_repository import BaseRepository

from repositories.base_repository import BaseRepository


class EventoOPRepository(BaseRepository):
    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path or Path("storage/eventos_op.json"))