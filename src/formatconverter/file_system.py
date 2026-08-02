from collections.abc import Callable
from pathlib import Path

from formatconverter.objects.dataclasses import FileContent


class FileSystem:
    def read_file(self, path: Path) -> list[str]:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            return file.readlines()

    def write_file(self, path: Path, text: list[str]):
        with open(path, "w", encoding="utf-8", errors="ignore") as file:
            file.writelines(text)

    def add_suffix(self, path: Path, suffix: str) -> Path:
        if suffix in ("", "."):
            return path

        return path.with_suffix(suffix)

    def concat(self, new_dir: Path, file: Path):
        return new_dir / file.name

    def write_files(self, files: list[FileContent]):
        for file_content in files:
            self.write_file(file_content.path, file_content.content)

    def mkdir(self, path: Path, suffix: str = "") -> Path:  # not tested
        new_path = path.with_name(path.name + suffix)
        new_path.mkdir(exist_ok=True, parents=True)
        return new_path

    def get_file_content(self, path: Path) -> FileContent:
        return FileContent(path, self.read_file(path))

    def get_files_content(
        self, path: Path, predicate: Callable = lambda a: a
    ) -> list[FileContent]:
        return [
            self.get_file_content(file)
            for file in path.rglob("*")
            if file.is_file() and predicate(file)
        ]
