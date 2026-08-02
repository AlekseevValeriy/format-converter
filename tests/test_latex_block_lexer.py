import pytest

from formatconverter.enums import BlockType
from formatconverter.parsers.latex_parser.block_lexer import LatexBlockLexer


@pytest.fixture
def lexer():
    return LatexBlockLexer()


@pytest.mark.parametrize(
    "text, expected_blocks",
    [
        (
            r"""
\subsection{Обновление рынка}
состоит из таймера и издателя (отправителя сообщений).

\TickDuration{} секунд в реальном времени эквивалентны \TickDuration{} минутам в игровом.
\begin{enumerate}
\item{Инвентарь (хранилище товаров, портфель, баланс)}
\end{enumerate}
""",
            [
                (BlockType.command, ["\\subsection{Обновление рынка}"]),
                (
                    BlockType.text,
                    ["состоит из таймера и издателя (отправителя сообщений)."],
                ),
                (BlockType.text, [""]),
                (
                    BlockType.markup_text,
                    [
                        "\\TickDuration{} секунд в реальном времени эквивалентны \\TickDuration{} минутам в игровом.",
                    ],
                ),
                (
                    BlockType.environment,
                    [
                        "\\begin{enumerate}",
                        "\\item{Инвентарь (хранилище товаров, портфель, баланс)}",
                        "\\end{enumerate}",
                    ],
                ),
            ],
        ),
        (
            r"""
\subsection{Обновление рынка}
""",
            [(BlockType.command, [r"\subsection{Обновление рынка}"])],
        ),
        (
            r"""
\subsection{Обновление рынка}

\subsection{Обновление рынка}
""",
            [
                (BlockType.command, [r"\subsection{Обновление рынка}"]),
                (BlockType.text, [r""]),
                (BlockType.command, [r"\subsection{Обновление рынка}"]),
            ],
        ),
        (
            "состоит из таймера и издателя (отправителя сообщений).",
            [
                (
                    BlockType.text,
                    ["состоит из таймера и издателя (отправителя сообщений)."],
                )
            ],
        ),
        (
            r"""

""",
            [
                (
                    BlockType.text,
                    [""],
                )
            ],
        ),
        (
            "\\",
            [
                (
                    BlockType.text,
                    ["\\"],
                )
            ],
        ),
        (
            r"""
\begin{enumerate}
    \item{Инвентарь (хранилище товаров, портфель, баланс)}
    состоит из таймера и издателя (отправителя сообщений).

    \TickDuration{} секунд в реальном времени эквивалентны \TickDuration{} минутам в игровом.
\end{enumerate}
""",
            [
                (
                    BlockType.environment,
                    [
                        "\\begin{enumerate}",
                        "    \\item{Инвентарь (хранилище товаров, портфель, баланс)}",
                        "    состоит из таймера и издателя (отправителя сообщений).",
                        "",
                        "    \\TickDuration{} секунд в реальном времени эквивалентны \\TickDuration{} минутам в игровом.",
                        "\\end{enumerate}",
                    ],
                ),
            ],
        ),
        (
            r"""
\begin{enumerate}
    \item{Инвентарь (хранилище товаров, портфель, баланс)}
""",
            [],
        ),
        (
            r"""
Описание регионов. Описание:
\begin{table}[H]
	\centering{%
		\begin{tabular}{|c|c|c|c|}
			\hline
			Регион & Оборон. бюджет (млрд.) & Население (млн.) & Пилотов \\ \hline
			B      & 1 514,7                & 69               & 12      \\ \hline
			A      & 18 101,6               & 358              & 98      \\ \hline
			G      & 1 608,2                & 90               & 14      \\ \hline
			C      & 4 394,5                & 1476             & 58      \\ \hline
			R      & 2 730,2                & 133              & 19      \\ \hline
		\end{tabular}%
	}
\end{table}
""",
            [
                (BlockType.text, [r"Описание регионов. Описание:"]),
                (
                    BlockType.environment,
                    [
                        r"\begin{table}[H]",
                        r"	\centering{%",
                        r"		\begin{tabular}{|c|c|c|c|}",
                        r"			\hline",
                        r"			Регион & Оборон. бюджет (млрд.) & Население (млн.) & Пилотов \\ \hline",
                        r"			B      & 1 514,7                & 69               & 12      \\ \hline",
                        r"			A      & 18 101,6               & 358              & 98      \\ \hline",
                        r"			G      & 1 608,2                & 90               & 14      \\ \hline",
                        r"			C      & 4 394,5                & 1476             & 58      \\ \hline",
                        r"			R      & 2 730,2                & 133              & 19      \\ \hline",
                        r"		\end{tabular}%",
                        r"	}",
                        r"\end{table}",
                    ],
                ),
            ],
        ),
        (
            r"""
\begin{tabular}{|c|c|c|c|}
    \hline
    Регион & Оборон. бюджет (млрд.) & Население (млн.) & Пилотов \\ \hline
    B      & 1 514,7                & 69               & 12      \\ \hline
    A      & 18 101,6               & 358              & 98      \\ \hline
    G      & 1 608,2                & 90               & 14      \\ \hline
    C      & 4 394,5                & 1476             & 58      \\ \hline
    R      & 2 730,2                & 133              & 19      \\ \hline
\end{tabular}%
""",
            [
                (
                    BlockType.environment,
                    [
                        r"\begin{tabular}{|c|c|c|c|}",
                        r"    \hline",
                        r"    Регион & Оборон. бюджет (млрд.) & Население (млн.) & Пилотов \\ \hline",
                        r"    B      & 1 514,7                & 69               & 12      \\ \hline",
                        r"    A      & 18 101,6               & 358              & 98      \\ \hline",
                        r"    G      & 1 608,2                & 90               & 14      \\ \hline",
                        r"    C      & 4 394,5                & 1476             & 58      \\ \hline",
                        r"    R      & 2 730,2                & 133              & 19      \\ \hline",
                        r"\end{tabular}%",
                    ],
                ),
            ],
        ),
    ],
)
def test_latex_block_lexer(lexer: LatexBlockLexer, text, expected_blocks):
    blocks = []
    text = remove_empty_lines(text.split("\n"))
    for block in lexer.iter(text):
        blocks.append(block)

    assert blocks == expected_blocks


def remove_empty_lines(text: list[str]) -> list[str]:
    if not text[0]:
        text.pop(0)
    if not text[-1]:
        text.pop()

    return text
