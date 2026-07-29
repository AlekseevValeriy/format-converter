from abc import ABC, abstractmethod

from formatconverter.nodes import Node


class Parser(ABC):
    @abstractmethod
    def parse(self, text: list[str]) -> Node: ...