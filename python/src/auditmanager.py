import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class IFileSystem(ABC):
    @abstractmethod
    def get_files(self) -> List[Path]:
        pass

    @abstractmethod
    def write_all_text(self, path: Path, content: str) -> None:
        pass

    @abstractmethod
    def read_all_lines(self, path: Path) -> List[str]:
        pass


class AuditManager:
    def __init__(
        self, max_entries_per_file: int, directory_name: Path, file_system: IFileSystem
    ):
        self._max_entries_per_file = max_entries_per_file
        self._directory_name = directory_name
        self._file_system = file_system

    def add_record(self, visitor: str, time: datetime.datetime) -> None:
        paths = self._file_system.get_files()
        new_record = f"{visitor};{time.isoformat()}"
        if len(paths) == 0:
            file_name = self._directory_name / "audit_1.txt"
            self._file_system.write_all_text(file_name, new_record)
            return

        current_file = paths[-1]
        lines = self._file_system.read_all_lines(current_file)
        if len(lines) < self._max_entries_per_file:
            lines.append(new_record)
            self._file_system.write_all_text(current_file, "\n".join(lines))
        else:
            file_name = self._directory_name / f"audit_{len(paths)+1}.txt"
            self._file_system.write_all_text(file_name, new_record)
