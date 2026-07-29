import re
from enum import Enum, auto

from formatconverter.enums import BlockType


class AnalysisState(Enum):
    line = auto()
    structure = auto()


class LatexBlocker:
    def __init__(self):
        self.analysis_state: AnalysisState = (
            AnalysisState.line
        )
        self.block_memory = []

        self.blocks_rules: ... = {
            BlockType.environment: self.structure_case_comparison,
            BlockType.command: self.command_case_comparison,
            BlockType.markup_text: self.mix_case_comparison,
        }

        self.command_patterns: list[str] = [r"^\\.*}\n", r"^\\\w+\n"]
        self.mix_patterns: list[str] = [r"\\.*}"]
        self.structure_patterns: list[list[str]] = [
            [r"^\\begin{.*(}|])\n", r"^\\end{.*}\n"],
            [r"^\\newglossaryentry{.*}\n", r"^}\n"],
        ]

    def drop_analysis_state(self):
        self.analysis_state = AnalysisState.line

    def pop_block_memory(self):
        temp_block_memory = self.block_memory
        self.block_memory = []

        return temp_block_memory

    def decompose(self, line: str) -> tuple[list[str], BlockType] | None:
        for block_type in self.blocks_rules:
            if self.blocks_rules[block_type](line):
                if self.analysis_state == AnalysisState.structure:
                    return None
                else:
                    return self.pop_block_memory(), block_type

        return self.pop_block_memory(), BlockType.text

    def command_case_comparison(self, line: str) -> bool:
        if self.analysis_state == AnalysisState.structure:
            return False

        if result := any(
            re.fullmatch(pattern, line) for pattern in self.command_patterns
        ):
            self.block_memory.append(line)

        return result

    def mix_case_comparison(self, line: str) -> bool:
        if self.analysis_state == AnalysisState.structure:
            return False

        for pattern in self.mix_patterns:
            result: list[str] = re.findall(pattern, line)

            if (len(result) >= 1) and (len(result[0]) < len(line)):
                self.block_memory.append(line)
                return True

        return False

    def structure_case_comparison(self, line: str) -> bool:
        match self.analysis_state:
            case AnalysisState.line:
                for pattern_1, pattern_2 in self.structure_patterns:
                    if re.fullmatch(pattern_1, line):
                        self.analysis_state = AnalysisState.structure
                        self.block_memory.append(line)
                        return True
            case AnalysisState.structure:
                for pattern_1, pattern_2 in self.structure_patterns:
                    if re.fullmatch(pattern_2, line):
                        self.analysis_state = AnalysisState.line
                        self.block_memory.append(line)
                        return True

        return self.analysis_state == AnalysisState.structure
