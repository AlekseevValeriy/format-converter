from enum import Enum, auto

import regex

from formatconverter.nodes import LatexCommandNode, MarkupTextNode, Node, TextNode

from .base_block_parser import LatexBlockParser


class MarkupTextParseState(Enum):
    text = auto()
    command_start = auto()
    mandatory_arg_start = auto()
    mandatory_arg_end = auto()
    optional_arg_start = auto()
    optional_arg_end = auto()


class LatexMarkupTextParser(LatexBlockParser):
    def __init__(self) -> None:
        self.pattern = (
            r"(\\([a-zA-Z]+)\*?(?:(\[(?:[^[\]]|(?2))*\])|(\{(?:[^{}]|(?3))*\})|\s*)*)"
        )

    def parse(self, block: list[str] | str) -> Node | None:
        line = self.block_to_line(block)

        if line == None:
            return None
        elif line == "":
            return MarkupTextNode([TextNode("")])

        return self.divide_blocks(line)

    def divide_blocks(self, line: str) -> Node | None:
        node = MarkupTextNode([])
        last = 0

        for m in regex.finditer(self.pattern, line):
            match = m.group(0)

            if not match:
                continue

            command = match.rstrip()
            trailing = match[len(command) :]

            if node_before := self.define_node(line[last : m.start()]):
                node.childrens.append(node_before)

            if node_targer := self.define_node(command):
                node.childrens.append(node_targer)

            last = m.end() - len(trailing)

        if node_end := self.define_node(line[last:]):
            node.childrens.append(node_end)

        return node

    def define_node(self, line: str) -> Node | None:
        if not line:
            return None

        if regex.fullmatch(self.pattern, line):
            return LatexCommandNode(line)

        return TextNode(line)
