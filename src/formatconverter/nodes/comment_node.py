from dataclasses import dataclass

from .base_node import Node


@dataclass
class CommentNode(Node):
    text: str
