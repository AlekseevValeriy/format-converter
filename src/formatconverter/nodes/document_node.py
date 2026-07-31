from dataclasses import dataclass

from .base_node import Node


@dataclass
class DocumentNode(Node):
    type: str
    childrens: list[Node]