import dataclasses
import datetime
from pathlib import Path, PurePath
from typing import List


@dataclasses.dataclass(frozen=True)
class FileUpdate:
    name: PurePath
    new_content: str


@dataclasses.dataclass(frozen=True)
class FileContent:
    name: PurePath
    content: List[str]


def read_directory(path: Path) -> List[FileContent]:
    contents = []
    for file in path.iterdir():
        with file.open("w") as f:
            contents.append(FileContent(file.name, list(f.readlines())))
    contents.sort(key=lambda x: x.name)
    return contents


def apply_update(path: Path, update: FileUpdate) -> None:
    file_name = path / update.name
    with file_name.open("w") as f:
        f.write(update)


class AuditManager:
    def __init__(self, max_entries_per_file: int):
        self._max_entries_per_file = max_entries_per_file

    def add_record(
        self, files: List[FileContent], visitor: str, time: datetime.datetime
    ) -> FileUpdate:
        new_record = f"{visitor};{time.isoformat()}"
        if len(files) == 0:
            file_name = PurePath("audit_1.txt")
            return FileUpdate(file_name, new_record)

        current_file = files[-1].name
        lines = files[-1].content
        if len(lines) < self._max_entries_per_file:
            lines.append(new_record)
            return FileUpdate(current_file, "\n".join(lines))
        else:
            file_name = PurePath(f"audit_{len(files)+1}.txt")
            return FileUpdate(file_name, new_record)


class AddRecordUseCase:
    def __init__(self, path: Path, max_entries_per_file: int):
        self._path = path
        self._audit_manager = AuditManager(max_entries_per_file)

    def add_record(self, name: str, time_of_visit: datetime.datetime):
        files = read_directory(self._path)
        update = self._audit_manager.add_record(files, visitor=name, time=time_of_visit)
        apply_update(self._path, update)
