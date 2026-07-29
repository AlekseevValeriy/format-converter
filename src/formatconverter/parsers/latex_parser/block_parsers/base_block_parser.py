from abc import ABC, abstractmethod

from formatconverter.nodes import Node


class LatexBlockParser(ABC):
    @abstractmethod
    def parse(self, block: list[str]) -> Node: ...