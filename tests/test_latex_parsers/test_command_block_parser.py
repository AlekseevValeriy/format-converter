import pytest

from formatconverter.nodes import LatexCommandNode, HeaderNode
from formatconverter.parsers.latex_parser.block_parsers import LatexCommandParser


@pytest.fixture
def command_block_parser():
    return LatexCommandParser()


@pytest.mark.parametrize(
    "text, expected_node",
    [
        ### Command
        ([], None),
        ([""], LatexCommandNode("")),
        ("", LatexCommandNode("")),
        (" ", LatexCommandNode(" ")),
        ("\t", LatexCommandNode("\t")),
        (r"\section{text}", HeaderNode(True, 1, "text")),
        (r"\section{}", HeaderNode(True, 1, "")),
        (r"\section*{}", HeaderNode(False, 1, "")),
        (r"      \section*{     }        ", HeaderNode(False, 1, "")),
        (r"\subsection{text}", HeaderNode(True, 2, "text")),
        (r"\subsubsection{text}", HeaderNode(True, 3, "text")),
        (r"\paragraph{text}", HeaderNode(True, 4, "text")),
        (r"\subparagraph{text}", HeaderNode(True, 5, "text")),
        (r"\subsection*{text}", HeaderNode(False, 2, "text")),
        (r"\subsubsection*{text}", HeaderNode(False, 3, "text")),
        (r"\paragraph*{text}", HeaderNode(False, 4, "text")),
        (r"\subparagraph*{text}", HeaderNode(False, 5, "text")),
        (
            r"\subparagraph*{\subparagraph*{text}}",
            HeaderNode(False, 5, "\\subparagraph*{text}"),
        ),
        (r"\setmainfont{CMU Serif}", LatexCommandNode(r"\setmainfont{CMU Serif}")),
        (r"\setmonofont{JetBrains Mono}", LatexCommandNode(r"\setmonofont{JetBrains Mono}")),
        (
            r"\newfontfamily\symbolfont{Symbola}",
            LatexCommandNode(r"\newfontfamily\symbolfont{Symbola}"),
        ),
    ],
)
def test_command_block_parser(command_block_parser, text, expected_node):
    assert command_block_parser.parse(text) == expected_node
