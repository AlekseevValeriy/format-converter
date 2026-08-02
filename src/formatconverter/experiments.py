from formatconverter.parsers.latex_parser.block_lexer import LatexBlockLexer
import regex
from pprint import pprint

def run():
    # pattern = r"(\\([a-zA-Z]+)\*?(?:(\[(?:[^[\]]|(?2))*\])|(\{(?:[^{}]|(?3))*\})|\s*)*)"
    pattern = (
        r"(\\[a-zA-Z]+\*?(?:(?:\[(?:[^[\]]|(?R))*\])|(?:\{(?:[^{}]|(?R))*\})|\s*)*)"
    )
    text = r"\gls{ст}\gls{ст}"
    parts = []
    last = 0

    for m in regex.finditer(pattern, text):
        parts.append(text[last : m.start()])  # text before command
        parts.append(m.group(0))  # the command itself
        last = m.end()

    parts.append(text[last:])

    pprint(parts)