from dataclasses import dataclass

from .base_node import Node


@dataclass
class EnvironmentNode(Node):
    childrens: list[str]