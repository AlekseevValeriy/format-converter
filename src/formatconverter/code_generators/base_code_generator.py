from abc import ABC, abstractmethod

from formatconverter.nodes import Node


class CodeGenerator(ABC):
    @abstractmethod
    def generate(self, node: Node) -> list[str]: ...