from dataclasses import dataclass

from .base_node import Node


@dataclass
class HeaderNode(Node):
    number_visiable: bool
    level: int
    text: str