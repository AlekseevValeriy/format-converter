from formatconverter.nodes import Node, TextNode

from .base_block_parser import LatexBlockParser


class LatexTextParser(LatexBlockParser):
    def parse(self, block: list[str]) -> Node:
        return TextNode(*block)
