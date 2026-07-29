from dataclasses import dataclass

from .base_node import Node


@dataclass
class TextNode(Node):
    text: str