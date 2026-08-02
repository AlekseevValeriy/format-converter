from dataclasses import dataclass

from .base_node import Node


@dataclass
class LatexCommandNode(Node):
    text: str