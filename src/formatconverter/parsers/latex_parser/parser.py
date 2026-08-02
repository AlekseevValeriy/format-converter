from formatconverter.nodes import GeneralNode, Node
from formatconverter.parsers import Parser

from .block_handler import LatexBlockHandler
from .block_lexer import LatexBlockLexer


class LatexParser(Parser):
    def __init__(self):
        self.block_lexer = LatexBlockLexer()
        self.block_handler = LatexBlockHandler()

    def parse(self, text: list[str]) -> Node:
        node = GeneralNode([])

        for block in self.block_lexer.iter(text):
            if block and (parsed := self.block_handler.handle(block)):
                node.childrens.append(parsed)

        return node
