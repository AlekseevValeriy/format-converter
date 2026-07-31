from abc import ABC, abstractmethod

from formatconverter.nodes import Node


class LatexBlockParser(ABC):
    @abstractmethod
    def parse(self, block) -> Node | None: ...
    
    def block_to_line(self, block: list[str] | str) -> str | None:
        if isinstance(block, list) and len(block) != 0:
            return block[0]
        if isinstance(block, str):
            return block
        return None