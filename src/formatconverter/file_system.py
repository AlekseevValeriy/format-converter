from collections.abc import Callable
from pathlib import Path

from formatconverter.objects import FileContent, Text


class FileSystem:
    def read_file(self, path: Path) -> Text:
        with open(path, "r", encoding="utf-8", errors='ignore') as file:
            return file.readlines()
        
    def write_file(self, path: Path, text: Text):
        with open(path, "w", encoding="utf-8", errors='ignore') as file:
            file.writelines(text)
            
    def add_suffix(self, path: Path, suffix: str) -> Path:        
        return path.with_suffix(suffix)

    def write_files(self, files: list[FileContent]):
        for file_content in files:
            self.write_file(file_content.path, file_content.content)
            
    def mkdir(self, path: Path, suffix:str=""):
        path.with_name(path.name + suffix).mkdir(exist_ok=True, parents=True)
            
    def get_file_content(self, path: Path) -> FileContent:
        return FileContent(path, self.read_file(path)) 

    def get_files_content(self, path: Path, predicate: Callable = lambda a: a) -> list[FileContent]:
        return [self.get_file_content(file) for file in path.rglob("*") if file.is_file() and predicate(file)]