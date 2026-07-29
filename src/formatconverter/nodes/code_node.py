from dataclasses import dataclass

from .base_node import Node


@dataclass
class CodeNode(Node):
    language: str
    content: str