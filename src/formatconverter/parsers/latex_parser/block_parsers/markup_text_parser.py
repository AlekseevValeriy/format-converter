from enum import Enum, auto
from string import punctuation

from formatconverter.nodes import CommandNode, MarkupTextNode, Node, TextNode

from .base_block_parser import LatexBlockParser


class MarkupTextParseState(Enum):
    text = auto()
    command_start = auto()
    mandatory_arg_start = auto()
    mandatory_arg_end = auto()
    optional_arg_start = auto()
    optional_arg_end = auto()


class LatexMarkupTextParser(LatexBlockParser):
    def parse(self, block: list[str] | str) -> Node | None:
        line = self.block_to_line(block)

        if line == None:
            return None
        elif line == "":
            return MarkupTextNode([TextNode("")])
        
        state_machine = LatexMarkupTextParserStateMachine(
            MarkupTextParseState.text, "", MarkupTextNode([])
        )
        
        [state_machine.next(char) for char in line]
        state_machine.end()

        return state_machine.markup_node


class LatexMarkupTextParserStateMachine:
    def __init__(
        self, state: MarkupTextParseState, temp_line: str, markup_node: MarkupTextNode
    ) -> None:
        self.state: MarkupTextParseState = state
        self.temp_line: str = temp_line
        self.markup_node: MarkupTextNode = markup_node
        self.punctation = punctuation + " \t"

    def next(self, char):
        match self.state:
            case MarkupTextParseState.text:
                if char == "\\":
                    self.pop_text()
                    self.set_command_state()
            case (
                MarkupTextParseState.command_start
                | MarkupTextParseState.optional_arg_end
                | MarkupTextParseState.mandatory_arg_end
            ):
                if char not in ("{", "[") and char in self.punctation:
                    self.pop_command()
                    self.set_text_state()
                elif char == "[":
                    self.set_optional_start_state()
                elif char == "{":
                    self.set_mandatory_start_state()
                elif char == "\\":
                    self.pop_command()
            case MarkupTextParseState.optional_arg_start:
                if char == "]":
                    self.set_optional_end_state()
            case MarkupTextParseState.mandatory_arg_start:
                if char == "}":
                    self.set_mandatory_end_state()
        self.add_char(char)
        
    def end(self):
        if not self.temp_line:
            return
        
        if self.temp_line.startswith("\\"):
            self.pop_command()
        else:
            self.pop_text()

    def set_text_state(self):
        self.state = MarkupTextParseState.text

    def set_command_state(self):
        self.state = MarkupTextParseState.command_start

    def set_mandatory_start_state(self):
        self.state = MarkupTextParseState.mandatory_arg_start

    def set_mandatory_end_state(self):
        self.state = MarkupTextParseState.mandatory_arg_end

    def set_optional_start_state(self):
        self.state = MarkupTextParseState.optional_arg_start

    def set_optional_end_state(self):
        self.state = MarkupTextParseState.optional_arg_end

    def add_char(self, char):
        self.temp_line += char

    def drop_temp_line(self):
        self.temp_line = ""

    def pop_text(self):
        if self.temp_line:
            self.markup_node.childrens.append(TextNode(self.temp_line))
        self.drop_temp_line()

    def pop_command(self):
        if self.temp_line:
            self.markup_node.childrens.append(CommandNode(self.temp_line))
        self.drop_temp_line()
