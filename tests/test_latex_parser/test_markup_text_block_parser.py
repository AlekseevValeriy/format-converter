import pytest

from formatconverter.nodes import CommandNode, MarkupTextNode, TextNode
from formatconverter.parsers.latex_parser.block_parsers import LatexMarkupTextParser


@pytest.fixture
def markup_text_block_parser():
    return LatexMarkupTextParser()


@pytest.mark.parametrize(
    "text, expected_node",
    [
        ([], None),
        ([""], MarkupTextNode([TextNode("")])),
        ("", MarkupTextNode([TextNode("")])),
        (" ", MarkupTextNode([TextNode(" ")])),
        ("\t", MarkupTextNode([TextNode("\t")])),
        (
            r"Этот документ служит единым источником истины",
            MarkupTextNode(
                [TextNode(r"Этот документ служит единым источником истины")]
            ),
        ),
        (
            r"Примерный алгоритм установки параметров: \inputminted{rust}{code/2.rs}",
            MarkupTextNode(
                [
                    TextNode("Примерный алгоритм установки параметров: "),
                    CommandNode(r"\inputminted{rust}{code/2.rs}"),
                ]
            ),
        ),
        (
            r"Примерный алгоритм установки параметров: \inputminted{rust}{code/2.rs} Примерный алгоритм установки параметров:",
            MarkupTextNode(
                [
                    TextNode("Примерный алгоритм установки параметров: "),
                    CommandNode(r"\inputminted{rust}{code/2.rs}"),
                    TextNode(" Примерный алгоритм установки параметров:"),
                ]
            ),
        ),
        (
            r"\glsdesc{_ст}. \gls{ст} состоит из таймера и издателя (отправителя сообщений). Каждые \TickDuration{} секунд система тиков",
            MarkupTextNode(
                [
                    CommandNode(r"\glsdesc{_ст}"),
                    TextNode(". "),
                    CommandNode(r"\gls{ст}"),
                    TextNode(
                        " состоит из таймера и издателя (отправителя сообщений). Каждые "
                    ),
                    CommandNode(r"\TickDuration{}"),
                    TextNode(" секунд система тиков"),
                ]
            ),
        ),
        (
            r"дателя (отправите. \gls{ст} состоит из таймера и издателя (отправителя сообщений). Каждые \TickDuration{} секунд система тиков(отправите. \gls{ст} состоит из таймера и издателя (отправителя сообщений). Каждые \TickDuration{} секунд",
            MarkupTextNode(
                [
                    TextNode("дателя (отправите. "),
                    CommandNode(r"\gls{ст}"),
                    TextNode(
                        " состоит из таймера и издателя (отправителя сообщений). Каждые "
                    ),
                    CommandNode(r"\TickDuration{}"),
                    TextNode(" секунд система тиков(отправите. "),
                    CommandNode(r"\gls{ст}"),
                    TextNode(
                        " состоит из таймера и издателя (отправителя сообщений). Каждые "
                    ),
                    CommandNode(r"\TickDuration{}"),
                    TextNode(" секунд"),
                ]
            ),
        ),
        (
            r"\gls{ст}",
            MarkupTextNode([CommandNode(r"\gls{ст}")]),
        ),
        (
            r".\gls{ст}.",
            MarkupTextNode([TextNode("."), CommandNode(r"\gls{ст}"), TextNode(".")]),
        ),
        (
            r"\gls{ст}\gls{ст}",
            MarkupTextNode(
                [
                    CommandNode(r"\gls{ст}"),
                    CommandNode(r"\gls{ст}"),
                ]
            ),
        ),
    ],
)
def test_markup_block_parser(markup_text_block_parser, text, expected_node):
    assert markup_text_block_parser.parse(text) == expected_node
