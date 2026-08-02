import regex

from formatconverter.enums import BlockType
from formatconverter.objects.dataclasses import *


class LatexBlockLexer:
    def __init__(self):
        self._text: list[str] = []

        self._rules: ... = [
            self._try_environment_block_generate,
            self._try_markup_text_block_generate,
            self._try_command_block_generate,
            self._try_text_block_generate,
        ]

        self._markup_text_patterns: list[str] = [
            r"(\\([a-zA-Z]+)\*?(?:(\[(?:[^[\]]|(?2))*\])|(\{(?:[^{}]|(?3))*\})|\s*)*)",
        ]

        self._command_patterns: list[str] = [
            "^" + regex_ + "$" for regex_ in self._markup_text_patterns
        ]

        self._environment_patterns: dict[str, tuple[str, str]] = {
            "table": (
                r"^(\\begin\*?(?:(\[(?:[^[\]]|(?2))*\])|(\{(?:[^{}]|(?3))*\})|\s*)*)$",
                r"^(\\end\*?(?:(\[(?:[^[\]]|(?2))*\])|(\{(?:[^{}]|(?3))*\})|\s*)*)\%?$",
            ),
            "glossary": (r"^\\newglossaryentry{.*}$", r"^}$"),
        }

    def iter(self, text: list[str]):
        self._text = text
        return self

    def __iter__(self):
        return self

    def __next__(self) -> tuple[BlockType, list[str]] | None:
        for rule in self._rules:
            if self._is_text_empty():
                raise StopIteration

            if block := rule():
                return block

    def _take_line(self) -> str:
        if self._is_text_empty():
            raise IndexError()

        return self._text.pop(0)

    def _get_line(self) -> str:
        if self._is_text_empty():
            raise IndexError()

        return self._text[0].strip()

    def _is_text_empty(self) -> bool:
        return len(self._text) == 0

    def _try_command_block_generate(self) -> tuple[BlockType, list[str]] | None:
        line = self._get_line().strip()

        if not any(
            regex.fullmatch(pattern, line) for pattern in self._command_patterns
        ):
            return None

        return BlockType.command, [self._take_line()]

    def _try_markup_text_block_generate(self) -> tuple[BlockType, list[str]] | None:
        line = self._get_line()

        for pattern in self._markup_text_patterns:
            matches = regex.findall(pattern, line)

            if (len(matches) >= 1) and (len(matches[0][0]) < len(line)):
                return BlockType.markup_text, [self._take_line()]

        return None

    def _try_environment_block_generate(self) -> tuple[BlockType, list[str]] | None:
        line = self._get_line()
        buffer = []
        current_environment = {"mark": "", "type": ""}

        for type_ in self._environment_patterns:
            if regex.fullmatch(self._environment_patterns[type_][0], line.strip()):
                current_environment["type"] = type_
                break
        else:
            return None

        if line.startswith("\\begin"):
            current_environment["mark"] = line[: line.find("}")].removeprefix(
                "\\begin{"
            )

        buffer.append(self._take_line())

        while len(self._text) != 0:
            line = self._get_line()

            if regex.fullmatch(
                self._environment_patterns[current_environment["type"]][1], line
            ):
                if line.startswith("\\end") and current_environment["mark"]:
                    mark = line[: line.find("}")].removeprefix("\\end{")
                    if current_environment["mark"] == mark:
                        break
                else:
                    break
            buffer.append(self._take_line())
        else:
            return None
        buffer.append(self._take_line())

        return BlockType.environment, buffer

    def _try_text_block_generate(self) -> tuple[BlockType, list[str]]:
        return BlockType.text, [self._take_line()]
