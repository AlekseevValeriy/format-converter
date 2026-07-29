from dataclasses import dataclass

from .base_node import Node


@dataclass
class CommandNode(Node):
    text: str