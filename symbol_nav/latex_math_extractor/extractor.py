from typing import Generator, Optional, Tuple
from dataclasses import dataclass

from .exceptions import LaTeXValueError
from .lexer import lexer
import os


@dataclass
class LaTeXMath:
    filename: str
    line: int
    column: int
    type: str
    value: str
    contexts: Tuple[str, str]
    marks: Tuple[str, str]

    def __repr__(self):
        return f"LaTeXMath(type={self.type}, value={repr(self.value)})"


class LaTeXMathExtractor:

    def __init__(self):
        self.lexer = lexer
    
    def analyze(self, latex: Optional[str] = None, file: Optional[str] = None) -> Generator[LaTeXMath]:
        assert (latex is not None) ^ (file is not None), "Either latex or file must be provided"
        if file is not None:
            with open(file, 'r') as f:
                latex = f.read()
            file = os.path.abspath(file)
        else:
            file = "untitled.tex"

        self.lexer.input(latex)
        while True:
            try:
                tok = self.lexer.token()
            except LaTeXValueError as e:
                print(e.cursor)
                print(e)
                lexpos = getattr(e.token, 'lexpos', 0)
                print(self.lexer.lexdata[lexpos-10: lexpos], end="")
                print(f"<error>{self.lexer.lexdata[lexpos]}</error>", end="")
                print(self.lexer.lexdata[lexpos+1: lexpos+10], end="")
                break
            if tok is None:
                break
            if tok.type == 'COMMENT':
                continue
            if tok.type in ('MATH_DISPLAY', 'MATH_EQUATION', 'MATH_INLINE', 'MATH_PARENTHESIS', 'MATH_BRACKET'):
                context_span = 0
                while (
                    tok.mark_start_pos - context_span > 0 
                    and (
                        context_span < 50
                        or tok.lexer.lexdata[tok.mark_start_pos - context_span] not in (' ', '\n')
                    )
                ):
                    context_span += 1
                context_beg = tok.mark_start_pos - context_span
                context_span = 0
                while (
                    tok.mark_end_pos + context_span < len(tok.lexer.lexdata)
                    and (
                        context_span < 50
                        or tok.lexer.lexdata[tok.mark_end_pos + context_span] not in (' ', '\n')
                    )
                ):
                    context_span += 1
                context_end = tok.mark_end_pos + context_span
                latex_math = LaTeXMath(
                    filename=file,
                    line=tok.lineno,
                    column=tok.column,
                    type=tok.type,
                    value=tok.value,
                    marks=tok.marks,
                    contexts=(
                        tok.lexer.lexdata[context_beg: tok.mark_start_pos],
                        tok.lexer.lexdata[tok.mark_end_pos: context_end]
                    )
                )
                yield latex_math

if __name__ == '__main__':
    from rich.console import Console
    from rich.style import Style
    console = Console()
    style_marks = Style(color="#E285B5", bold=True)
    style_context = Style(color="#ffffff")
    style_value = Style(color="#77BCF1")
    
    extractor = LaTeXMathExtractor()
    for latex_math in extractor.analyze(file='sample.tex'):
        console.print(latex_math.contexts[0], style=style_context, end="")
        console.print(latex_math.marks[0], style=style_marks, end="", )
        console.print(latex_math.value, style=style_value, end="")
        console.print(latex_math.marks[1], style=style_marks, end="")
        console.print(latex_math.contexts[1], style=style_context, end="")
        console.print()
        break