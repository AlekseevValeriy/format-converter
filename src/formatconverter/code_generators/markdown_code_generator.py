from collections.abc import Callable

from formatconverter.nodes import *

from .base_code_generator import CodeGenerator


class MarkdownCodeGenerator(CodeGenerator):
    def __init__(self):
        self.node_generates: dict[type[Node], Callable] = {
            GeneralNode: self.general_node_generate,
            LatexCommandNode: self.latex_command_node_generate,
            HeaderNode: self.header_node_generate,
            ImageNode: self.image_node_generate,
            ListNode: self.list_node_generate,
            MarkupTextNode: self.markup_text_node_generate,
            EnvironmentNode: self.environment_node_generate,
            TableNode: self.table_node_generate,
            TextNode: self.text_node_generate,
        }
        self.formatter = MarkdownFormatter()

    def generate(self, node: Node) -> list[str]:
        code: list[str] = []

        code += self.node_generates[type(node)](node)

        return code

    def general_node_generate(self, node: GeneralNode) -> list[str]:
        code: list[str] = []

        for item in node.childrens:
            code += self.generate(item)

        return code

    def list_node_generate(self, node: ListNode) -> list[str]:
        code = []

        match node.type:
            case "itemize":
                code += self.itemize_list_node_generate(node)
            case "enumerate":
                code += self.enumerate_list_node_generate(node)
            case "description":
                code += self.description_list_node_generate(node)

        return code

    def latex_command_node_generate(self, node: LatexCommandNode) -> list[str]:
        return [self.formatter.latex_command_format(node.text)]

    def header_node_generate(self, node: HeaderNode) -> list[str]:
        return [self.formatter.header_format(node.text, node.level)]

    def image_node_generate(self, node: ImageNode) -> list[str]:
        return [self.formatter.image_format(node.description, node.source)]

    def itemize_list_node_generate(self, node: ListNode) -> list[str]:
        return [
            self.itemize_list_item_node_generate(item)[0] for item in node.childrens
        ]

    def enumerate_list_node_generate(self, node: ListNode) -> list[str]:
        return [
            self.enumerate_list_item_node_generate(n + 1, item)[0]
            for n, item in enumerate(node.childrens)
        ]

    def description_list_node_generate(self, node: ListNode) -> list[str]:
        return [
            self.description_list_item_node_generate(item)[0] for item in node.childrens
        ]

    def itemize_list_item_node_generate(self, node: ListItemNode) -> list[str]:
        return [self.formatter.unordered_list_item_format(node.text)]

    def enumerate_list_item_node_generate(
        self, number: int, node: ListItemNode
    ) -> list[str]:
        return [self.formatter.ordered_list_item_format(number, node.text)]

    def description_list_item_node_generate(self, node: ListItemNode) -> list[str]:
        return [self.formatter.description_list_item_format(node.marker, node.text)]

    def markup_text_node_generate(self, node: MarkupTextNode) -> list[str]:
        code: list[str] = []

        for i in node.childrens:
            if isinstance(i, LatexCommandNode):
                code.append(self.formatter.latex_command_format(i.text))
            elif isinstance(i, TextNode):
                code.append(i.text)

        return ["".join(code)]

    def environment_node_generate(self, node: EnvironmentNode) -> list[str]:
        return node.childrens

    def table_node_generate(self, node: TableNode) -> list[str]:
        code = []

        for n, line in enumerate(node.grid):
            if n == 1:
                code.append("|" + ("-|" * len(line)))
            code.append("| " + " | ".join(line) + " |")

        return code

    def text_node_generate(self, node: TextNode) -> list[str]:
        return [node.text]


class MarkdownFormatter:
    def latex_command_format(self, text: str) -> str:
        return f"latex_command`{text}`"

    def header_format(self, title: str, level: int) -> str:
        level = min(max(level, 0), 10)

        return f"{'#' * level} {title}"

    def image_format(self, source: str, alt: str) -> str:
        return f"![{alt}]({source})"

    def unordered_list_item_format(self, item: str) -> str:
        return f"- {item}"

    def ordered_list_item_format(self, number: int, item: str) -> str:
        number = max(number, 0)

        return f"{number}. {item}"

    def task_list_item_format(self, checked: bool, item: str) -> str:
        return f"- [{'*' if checked else ' '}] {item}"

    def description_list_item_format(self, title: str | None, text: str) -> str:
        return f"- {title if title else ''}. {text}"
