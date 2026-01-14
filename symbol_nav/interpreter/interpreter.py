import ply.lex as lex
import ply.yacc as yacc

from mast import to_dict
from lexer import *
from parser import *

class LaTeXMathInterpreter:

    def __init__(self, debug: bool = False):
        self.lexer = lex.lex()
        self.parser = yacc.yacc(debug=debug, write_tables=False)
    
    def parse(self, latex: str):
        result = self.parser.parse(latex, lexer=self.lexer)
        return result

if __name__ == '__main__':
    import json
    parser = LaTeXMathInterpreter(debug=True)
    test_cases = [
        # r'x \leq y + 1',
        # r'x \gt y \times z',
        # r'x \leq y \cdot z',
        # r'x \leq y \div z',
        # r'x \leq y : z',
        # r'x \leq y^2',
        # r'a \leq b^{a=1}_{b=2}',
        r'\mathbf{H}^\text{out} \in \mathbb{R}^{N \times d}',
        # r'\text{abc}'
    ]
    for latex in test_cases:
        try:
            result = parser.parse(latex)
        except MathSyntaxError as e:
            print(latex)
            print(e.cursor)
            print(e)
            print(parser.parser.symstack)
            print()
            continue
        except ValueError as e:
            print(f"ValueError: {e}")
            print(f"LaTeX: {latex}")
            print()
            continue
        print(f"LaTeX: {latex}")
        print(json.dumps(to_dict(result, recursive=True), indent=2))
        print()