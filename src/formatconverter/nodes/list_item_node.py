from dataclasses import dataclass

from .base_node import Node


@dataclass
class ListItemNode(Node):
    marker: str
    text: str