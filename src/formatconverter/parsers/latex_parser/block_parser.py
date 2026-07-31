from formatconverter.enums import BlockType
from formatconverter.nodes import *
from formatconverter.parsers.latex_parser.block_parsers import *


class LatexBlocksParser:
    def __init__(self):
        self.block_parsers: dict[BlockType, LatexBlockParser] = {
            BlockType.environment: LatexEnvironmentParser(),
            BlockType.command: LatexCommandParser(),
            BlockType.markup_text: LatexMarkupTextParser(),
            BlockType.text: LatexTextParser(),
        }

        self.mix_format: list[str] = []

    def parse_block(self, block: list[str], type: BlockType) -> Node | None:
        return self.block_parsers[type].parse(block)
