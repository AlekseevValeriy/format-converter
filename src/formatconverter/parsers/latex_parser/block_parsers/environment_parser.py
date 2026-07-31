import re

from formatconverter.nodes import *

from .base_block_parser import LatexBlockParser


class LatexEnvironmentParser(LatexBlockParser):
    def __init__(self):
        self.lists = ["enumerate", "itemize", "description"]
        self.tables = ["table", "table*", "tabular", "tabular*", "tabularx", "tabulary", "longtable", "supertabular", "xtab", "ltablex", "ltxtable", "tblr", "longtblr", "talltblr", "array", "matrix", "pmatrix", "bmatrix", "vmatrix"]


    def parse(self, block: list[str]) -> Node | None:
        if len(block) < 2:
            return None
        
        _block = block[:]
        
        match_begin = re.search(r"\\begin\{(.*?)\}", _block[0])
        match_end = re.search(r"\\end\{(.*?)\}", _block[-1])
        if (match_begin and match_end) and match_begin.group(1) != match_end.group(1):
            return None

        if table_node := self.try_parse_table(_block):
            return table_node
        elif list_node := self.try_parse_list(_block):
            return list_node
        else:
            return EnvironmentNode(_block)

    def try_parse_table(self, block: list[str]) -> Node | None:
        header = block[0]

        if not header.startswith(r"\begin{"):
            return None

        match = re.search(r"\\begin\{(.*?)\}", header)
        if not match or match.group(1) not in self.tables:
            return None
        
        table_node = TableNode([])

        for line in block:
            if "\\\\" in line:
                row = [a.strip(" ").replace("\\\\", "") for a in line.split("\\\\")[0].split("&")]
                table_node.grid.append(row)
                
        return table_node

    def try_parse_list(self, block: list[str]) -> Node | None:
        header = block[0]

        if not header.startswith(r"\begin"):
            return None

        list_class = header[header.find("{") + 1 : header.find("}")]

        if list_class not in self.lists:
            return None

        list_node = ListNode(list_class, [])

        for item_number in range(1, len(block) - 1):
            if item := self.try_parse_list_item(block[item_number]):
                list_node.childrens.append(item)

        return list_node

    def try_parse_list_item(self, line: str) -> ListItemNode | None:
        item_node = ListItemNode(None, "")
        line = line.strip()

        if not line.startswith(r"\item"):
            return None
        
        line = line.lstrip(r"\item")
        
        if "[" in line:
            match = re.search(r"\[(.*?)\]", line)

            if match and (marker := match.group(1)):
                item_node.marker = marker

            line = line[line.find("]") + 1:]
            
        if line.startswith("{"):
            line = line[1:-1]
            
        item_node.text = line.strip()

        return item_node
