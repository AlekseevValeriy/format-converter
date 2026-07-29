from formatconverter.nodes import Node

from .base_parser import Parser


class MarkdownParser(Parser):
    def parse(self, text: list[str]) -> Node:
        # TODO MarkdownParser
        ...