from enum import Enum, auto

from formatconverter.nodes import CommandNode, MarkupTextNode, Node, TextNode

from .base_block_parser import LatexBlockParser


class MarkupTextParseState(Enum):
    text = auto()
    command_start = auto()
    command_mandatory_arg_start = auto()
    command_optional_arg_start = auto()

class LatexMarkupTextParser(LatexBlockParser):
    def parse(self, block: list[str]) -> Node:
        markup_node = MarkupTextNode([])
        tmp_line = ""
        line = block[0]
        
        parse_state = None
        
        if line[0] == "\\":
            parse_state = MarkupTextParseState.command_start
        else:
            parse_state = MarkupTextParseState.text
        
        for char in line:
            match parse_state:
                case MarkupTextParseState.text:
                    if char == "\\":
                        markup_node.childrens.append(TextNode(tmp_line))
                        tmp_line = ""
                        parse_state = MarkupTextParseState.command_start
                    else:
                        tmp_line += char
                case MarkupTextParseState.command_start:
                    if char in ("\n", " "):
                        markup_node.childrens.append(CommandNode(tmp_line))
                        tmp_line = ""
                        parse_state = MarkupTextParseState.text
                    elif char == "[":
                        tmp_line += char
                        parse_state = MarkupTextParseState.command_optional_arg_start
                    elif char == "{":
                        tmp_line += char
                        parse_state = MarkupTextParseState.command_mandatory_arg_start
                    else:
                        tmp_line += char
                case MarkupTextParseState.command_mandatory_arg_start:
                    if char == "}":
                        markup_node.childrens.append(CommandNode(tmp_line))
                        tmp_line = ""
                        parse_state = MarkupTextParseState.text
                    else:
                        tmp_line += char
                case MarkupTextParseState.command_optional_arg_start:
                    if char in ("]", "{"):
                        tmp_line += char
                        parse_state = MarkupTextParseState.command_mandatory_arg_start
                    else:
                        tmp_line += char
        
        return markup_node