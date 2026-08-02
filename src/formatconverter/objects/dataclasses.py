from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from formatconverter.code_generators.base_code_generator import CodeGenerator
from formatconverter.enums import LangsEnum, WorkMode
from formatconverter.parsers.base_parser import Parser


@dataclass
class ConvertPack:
    parser: Parser
    code_generator: CodeGenerator


@dataclass
class ParsedInput:
    work_mode: WorkMode
    path: Path | None
    old_lang: LangsEnum | None
    new_lang: LangsEnum | None


@dataclass
class ScenarioData:
    scenario_condition: Callable
    convert_pack: ConvertPack
    old_suffix: str
    new_suffix: str

@dataclass
class FileContent:
    path: Path
    content: list[str]
