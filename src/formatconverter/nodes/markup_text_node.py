from dataclasses import dataclass

from .base_node import Node


@dataclass
class MarkupTextNode(Node):
    childrens: list[Node]