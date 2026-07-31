from formatconverter.parsers.latex_parser.block_parsers import LatexEnvironmentParser

def run():
    line :str = r"""\begin{itemize}
      \item This is my first point
      \item Another point I want to make 
      \item[!] A point to exclaim something!
      \item[$\blacksquare$] Make the point fair and square.
      \item[NOTE] This entry has no bullet
      \item[] A blank label?
    \end{enumerate}"""
    print(LatexEnvironmentParser().parse(list(line.split("\n"))))
run()