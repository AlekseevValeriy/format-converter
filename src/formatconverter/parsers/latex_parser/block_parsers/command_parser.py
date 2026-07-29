from formatconverter.nodes import *

from .base_block_parser import LatexBlockParser


class LatexCommandParser(LatexBlockParser):
    def __init__(self) -> None:
        self.header_numbers: dict[str, int] = {
            "section": 1,
            "subsection": 2,
            "subsubsection": 3,
            "paragraph": 4,
            "subparagraph": 5,
        }

    def parse(self, block: list[str]) -> Node:
        line = block[0]

        if header_node := self.try_parse_header(line):
            return header_node

        return CommandNode(line)

    def try_parse_header(self, line: str) -> Node | None:
        header = line[1 : line.find("{")]
        if header not in self.header_numbers:
            return None

        number_visiable = not header.endswith("*")
        header = header.removesuffix("*")

        level = self.header_numbers[header]
        text = line[line.find("{") + 1 :].removesuffix("}").strip()

        return HeaderNode(number_visiable, level, text)
