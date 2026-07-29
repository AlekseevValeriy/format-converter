from enum import Enum, auto


class BlockType(Enum):
    environment = auto()
    command = auto()
    text = auto()
    markup_text = auto()