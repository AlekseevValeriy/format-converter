from formatconverter.nodes import Node, TextNode

from .base_block_parser import LatexBlockParser


class LatexTextParser(LatexBlockParser):
    def parse(self, block: list[str] | str) -> Node | None:
        line = self.block_to_line(block)  
        
        return TextNode(line) if line != None else None
