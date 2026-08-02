from formatconverter.enums import BlockType
from formatconverter.nodes import *
from formatconverter.parsers.latex_parser.block_parsers import *


class LatexBlockHandler:
    def __init__(self):
        self._block_parsers: dict[BlockType, LatexBlockParser] = {
            BlockType.environment: LatexEnvironmentParser(),
            BlockType.command: LatexCommandParser(),
            BlockType.markup_text: LatexMarkupTextParser(),
            BlockType.text: LatexTextParser(),
        }

        self._text_correctors: list[tuple[str, str]] = []

        self.mix_format: list[str] = []

    def handle(self, block: tuple[BlockType, list[str]]) -> Node | None:
        # TODO: change walk by line format

        text = block[1]
        text = [line.rstrip() for line in block[1]]

        return self._block_parsers[block[0]].parse(text)
