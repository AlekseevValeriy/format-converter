import pytest

from formatconverter.nodes import TextNode
from formatconverter.parsers.latex_parser.block_parsers import LatexTextParser


@pytest.fixture
def text_block_parser():
    return LatexTextParser()


@pytest.mark.parametrize(
    "text, expected_node",
    [
        ([], None),
        ([""], TextNode("")),
        ("", TextNode("")),
        (" ", TextNode(" ")),
        ("\t", TextNode("\t")),
        (
            r"Этот документ служит единым источником истины",
            TextNode("Этот документ служит единым источником истины"),
        ),
        (
            r"Примерный алгоритм установки параметров: \inputminted{rust}{code/2.rs}",
            TextNode(
                r"Примерный алгоритм установки параметров: \inputminted{rust}{code/2.rs}"
            ),
        ),
        (
            r"Примерный алгоритм установки параметров: \input{code/2.rs}",
            TextNode(r"Примерный алгоритм установки параметров: \input{code/2.rs}"),
        ),
        (
            r"\glsdesc{_ст}. \gls{ст} состоит из таймера и издателя (отправителя сообщений). Каждые \TickDuration{} секунд система тиков",
            TextNode(
                r"\glsdesc{_ст}. \gls{ст} состоит из таймера и издателя (отправителя сообщений). Каждые \TickDuration{} секунд система тиков"
            ),
        ),
        (
            r"\documentclass{article}",
            TextNode(r"\documentclass{article}"),
        ),
        (r"\begin{enumerate}", TextNode(r"\begin{enumerate}")),
    ],
)
def test_text_block_parser(text_block_parser, text, expected_node):
    assert text_block_parser.parse(text) == expected_node
