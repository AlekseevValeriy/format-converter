import pytest

from formatconverter.nodes import EnvironmentNode, ListItemNode, ListNode, TableNode
from formatconverter.parsers.latex_parser.block_parsers import LatexEnvironmentParser


@pytest.fixture
def environment_block_parser():
    return LatexEnvironmentParser()


@pytest.mark.parametrize(
    "text, expected_node",
    [
        (
            r"""\begin{tabular}{ c c c }
    cell1 & cell2 & cell3 \\ 
    cell4 & cell5 & cell6 \\  
    cell7 & cell8 & cell9 \\   
\end{tabular}""",
            TableNode(
                [
                    ["cell1", "cell2", "cell3"],
                    ["cell4", "cell5", "cell6"],
                    ["cell7", "cell8", "cell9"],
                ]
            ),
        ),
        (
            r"""\begin{tabular}{ c c c }
    cell1 \\ 
    cell2 \\  
    cell3 \\   
\end{tabular}""",
            TableNode([["cell1"], ["cell2"], ["cell3"]]),
        ),
        (
            r"""\begin{table}[H]
    \centering{%
        \begin{tabular}{|c|c|c|c|}
            \hline
            Регион & Оборон. бюджет (млрд.) & Население (млн.) & Пилотов \\ \hline
        \end{tabular}%
    }
\end{table}""",
            TableNode(
                [["Регион", "Оборон. бюджет (млрд.)", "Население (млн.)", "Пилотов"]]
            ),
        ),
        (
            r"""\begin{table}[H]
\end{tableble}""",
            None,
        ),
        (
            r"""\begin{table}[H]
\end{table}""",
            TableNode([]),
        ),
        (
            r"""\begin{tabular}{||c c c c||} 
    \hline
    Col1 & Col2 & Col2 & Col3 \\ [0.5ex] 
    \hline\hline
    1 & 6 & 87837 & 787 \\ 
    \hline
    2 & 7 & 78 & 5415 \\
    3 & 545 & 778 & 7507 \\
    \hline
    
    \hline

    4 & 545 & 18744 & 7560 \\
    \hline
    5 & 88 & 788 & 6344 \\ [1ex] 
    \hline
    \hline
    \hline
    \hline
    \hline
\end{tabular}""",
            TableNode(
                [
                    ["Col1", "Col2", "Col2", "Col3"],
                    ["1", "6", "87837", "787"],
                    ["2", "7", "78", "5415"],
                    ["3", "545", "778", "7507"],
                    ["4", "545", "18744", "7560"],
                    ["5", "88", "788", "6344"],
                ]
            ),
        ),
        (
            r"""\begin{tabular}{ | m{5em} | m{1cm}| m{1cm} | } 
    \hline
    cell1 dummy text dummy text dummy text& cell2 & cell3 \\ 
    \hline
    cell1 dummy text dummy text dummy text & cell5 & cell6 \\ 
    \hline
    cell7 & cell8 & cell9 \\ 
    \hline
\end{tabular}""",
            TableNode(
                [
                    ["cell1 dummy text dummy text dummy text", "cell2", "cell3"],
                    ["cell1 dummy text dummy text dummy text", "cell5", "cell6"],
                    ["cell7", "cell8", "cell9"],
                ]
            ),
        ),
        (
            r"""\begin{tabular}{ |c|c|c| } 
\hline
col1 & col2 & col3 \\
\hline
\multirow{3}{4em}{Multiple row} & cell2 & cell3 \\ 
& cell5 & cell6 \\ 
& cell8 & cell9 \\ 
\hline
\end{tabular}""",
            TableNode(
                [
                    ["col1", "col2", "col3"],
                    [r"\multirow{3}{4em}{Multiple row}", "cell2", "cell3"],
                    ["", "cell5", "cell6"],
                    ["", "cell8", "cell9"],
                ]
            ),
        ),
        (
            r"""\begin{tabular}{ |p{3cm}|p{3cm}|p{3cm}|  }
Country Name or Area Name& ISO ALPHA 2 Code &ISO ALPHA 3 \\
\hline
Aland Islands & AX   & ALA \\
Albania &AL & ALB \\
Algeria    &DZ & DZA \\
\hline
\end{tabular}""",
            TableNode(
                [
                    ["Country Name or Area Name", "ISO ALPHA 2 Code", "ISO ALPHA 3"],
                    ["Aland Islands", "AX", "ALA"],
                    ["Albania", "AL", "ALB"],
                    ["Algeria", "DZ", "DZA"],
                ]
            ),
        ),
        (
            r"""\newglossaryentry{_ср}
{
    name={Система рынка},
    description={Система рынка это большое хранилище товаров с которым взаимодействуют агенты}
}""",
            EnvironmentNode(
                [
                    r"\newglossaryentry{_ср}",
                    r"{",
                    r"    name={Система рынка},",
                    r"    description={Система рынка это большое хранилище товаров с которым взаимодействуют агенты}",
                    r"}",
                ]
            ),
        ),
        (
            r"""\begin{tikzpicture}[remember picture, overlay]
    
    \node[opacity=1, inner sep=0pt] at (current page.center) {
        \includegraphics[width=\paperwidth, height=\paperheight, keepaspectratio=false]{../../assets/title_background.png}
    };
    
    \fill[black, opacity=0.6] (current page.north west) rectangle (current page.south east);
    
    
    \node[anchor=center, text=white!70, font=\normalsize]
    at ([yshift=-2.5cm]current page.center) {
        Версия 0.1 \quad $|$ \quad Автор Алексеев Валерий
    };
    
\end{tikzpicture}""",
            EnvironmentNode(
                [
                    r"\begin{tikzpicture}[remember picture, overlay]",
                    r"    ",
                    r"    \node[opacity=1, inner sep=0pt] at (current page.center) {",
                    r"        \includegraphics[width=\paperwidth, height=\paperheight, keepaspectratio=false]{../../assets/title_background.png}",
                    r"    };",
                    r"    ",
                    r"    \fill[black, opacity=0.6] (current page.north west) rectangle (current page.south east);",
                    r"    ",
                    r"    ",
                    r"    \node[anchor=center, text=white!70, font=\normalsize]",
                    r"    at ([yshift=-2.5cm]current page.center) {",
                    r"        Версия 0.1 \quad $|$ \quad Автор Алексеев Валерий",
                    r"    };",
                    r"    ",
                    r"\end{tikzpicture}",
                ]
            ),
        ),
        (
            r"""\begin{document}
\end{document}""",
            EnvironmentNode([r"\begin{document}", r"\end{document}"]),
        ),
        (
            r"""\begin{description}
    \item[Топливо]{Нефть, природный газ, уран, уголь, тяжелая вода.}
\end{description}""",
            ListNode(
                "description",
                [
                    ListItemNode(
                        "Топливо", "Нефть, природный газ, уран, уголь, тяжелая вода."
                    )
                ],
            ),
        ),
        (
            r"""\begin{itemize}
  \item List entries start with the command.
  \item Individual entries are indicated with a black dot, a so-called bullet.
  \item The text in the entries may be of any length.
\end{itemize}""",
            ListNode(
                "itemize",
                [
                    ListItemNode(None, "List entries start with the command."),
                    ListItemNode(
                        None,
                        "Individual entries are indicated with a black dot, a so-called bullet.",
                    ),
                    ListItemNode(None, "The text in the entries may be of any length."),
                ],
            ),
        ),
        (
            r"""\begin{enumerate}
  \item Items are numbered automatically.
  \item The numbers start at 1 with each use of the \texttt{enumerate} environment.
  \item Another entry in the list
\end{enumerate}""",
            ListNode(
                "enumerate",
                [
                    ListItemNode(None, "Items are numbered automatically."),
                    ListItemNode(
                        None,
                        r"The numbers start at 1 with each use of the \texttt{enumerate} environment.",
                    ),
                    ListItemNode(None, "Another entry in the list"),
                ],
            ),
        ),
        (
            r"""\begin{description}
   \item{This is an entry \textit{without} a label.}
   \item[Something short] A short one-line description.
   \item[Something long]{A much longer description. \blindtext[1]}
\end{description}""",
            ListNode(
                "description",
                [
                    ListItemNode(None, r"This is an entry \textit{without} a label."),
                    ListItemNode("Something short", "A short one-line description."),
                    ListItemNode(
                        "Something long", r"A much longer description. \blindtext[1]"
                    ),
                ],
            ),
        ),
        (
            r"""\begin{itemize}
  \item This is my first point
  \item Another point I want to make 
  \item[!] A point to exclaim something!
  \item[$\blacksquare$] Make the point fair and square.
  \item[NOTE] This entry has no bullet
  \item[] A blank label?
\end{itemize}""",
            ListNode(
                "itemize",
                [
                    ListItemNode(None, "This is my first point"),
                    ListItemNode(None, "Another point I want to make"),
                    ListItemNode("!", "A point to exclaim something!"),
                    ListItemNode(r"$\blacksquare$", "Make the point fair and square."),
                    ListItemNode("NOTE", "This entry has no bullet"),
                    ListItemNode(None, "A blank label?"),
                ],
            ),
        ),
        (
            r"""\begin{enumerate}
	\item{Создание объявления о продаже}
	\item{Подача заявки на покупку}
	\item{Покупка и продажа облигаций}
	\item{Покупка и продажа акций}
	\item{Заем денежных средств}
\end{enumerate}""",
            ListNode("enumerate",
            [
                ListItemNode(None, "Создание объявления о продаже"),
                ListItemNode(None, "Подача заявки на покупку"),
                ListItemNode(None, "Покупка и продажа облигаций"),
                ListItemNode(None, "Покупка и продажа акций"),
                ListItemNode(None, "Заем денежных средств"),
            ]),
        ),
        (
            r"""\begin{itemize}
\end{itemize}""",
            ListNode("itemize", []),
        ),
        (
            r"""\begin{itemize}
  \item This is my first point
  \item Another point I want to make 
  \item[!] A point to exclaim something!
  \item[$\blacksquare$] Make the point fair and square.
  \item[NOTE] This entry has no bullet
  \item[] A blank label?
\end{enumerate}""",
            None,
        ),
    ],
)
def test_block_parser_from_string(environment_block_parser, text, expected_node):
    assert environment_block_parser.parse(text.split("\n")) == expected_node


@pytest.mark.parametrize(
    "text, expected_node",
    [
        ([], None),
        ([""], None),
        (["", ""], EnvironmentNode(["", ""])),
    ],
)
def test_block_parser_from_list(environment_block_parser, text, expected_node):
    assert environment_block_parser.parse(text) == expected_node
