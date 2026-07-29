from dataclasses import dataclass

from .base_node import Node


@dataclass
class ImageNode(Node):
    source: str
    description: str