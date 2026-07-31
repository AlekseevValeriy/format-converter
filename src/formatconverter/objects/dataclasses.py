from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from formatconverter.converters.base_converter import Converter
from formatconverter.enums import ConvertMode, LangsEnum, WorkMode
from formatconverter.parsers.base_parser import Parser

from .types import Text


@dataclass
class ConvertPack:
    parser: Parser
    converter: Converter


@dataclass
class ParsedInput:
    work_mode: WorkMode
    convert_mode: ConvertMode | None
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
    content: Text