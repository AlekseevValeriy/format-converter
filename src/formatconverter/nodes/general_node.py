from dataclasses import dataclass

from .base_node import Node


@dataclass
class GeneralNode(Node):
    childrens: list[Node]