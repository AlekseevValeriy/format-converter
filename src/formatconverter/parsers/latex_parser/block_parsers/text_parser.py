from formatconverter.nodes import Node, TextNode, CommentNode

from .base_block_parser import LatexBlockParser


class LatexTextParser(LatexBlockParser):
    def parse(self, block: list[str] | str) -> Node | None:
        line = self.block_to_line(block)
        if line == None:
            return None

        return TextNode(line)
