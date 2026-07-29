from dataclasses import dataclass

from .base_node import Node


@dataclass
class TableNode(Node):
    grid: list[list[str]]