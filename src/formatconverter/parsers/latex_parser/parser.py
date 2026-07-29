from formatconverter.nodes import GeneralNode, Node
from formatconverter.parsers import Parser

from .block_parser import LatexBlocksParser
from .blocker import LatexBlocker


class LatexParser(Parser):
    def __init__(self):
        self.typefier = LatexBlocker()
        self.block_parser = LatexBlocksParser()

    def parse(self, text: list[str]) -> Node:
        self.typefier.drop_analysis_state()

        _text = text[:]
        node = GeneralNode([])

        for line in _text:
            if result := self.typefier.decompose(line):
                block, _type = result
                node.childrens.append(self.block_parser.parse_block(block, _type))

        return node
