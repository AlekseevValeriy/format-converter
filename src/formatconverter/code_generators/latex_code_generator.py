from formatconverter.nodes import Node

from .base_code_generator import CodeGenerator


class LatexCodeGenerator(CodeGenerator):
    def generate(self, node: Node) -> list[str]: 
        # TODO LatexConverter
        ...