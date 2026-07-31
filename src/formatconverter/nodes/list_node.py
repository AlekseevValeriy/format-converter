from dataclasses import dataclass

from .base_node import Node
from .list_item_node import ListItemNode


@dataclass
class ListNode(Node):
    type: str
    childrens: list[ListItemNode]