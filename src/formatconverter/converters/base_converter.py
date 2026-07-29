from abc import ABC, abstractmethod

from formatconverter.nodes import Node


class Converter(ABC):
    @abstractmethod
    def convert(self, node: Node) -> list[str]: ...