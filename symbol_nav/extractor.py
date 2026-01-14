import json
from interpreter.mast import ASTNode, to_dict
from interpreter.interpreter import LaTeXMathInterpreter
from interpreter.exceptions import MathSyntaxError
from renderer import render

def traverse_ast(ast: ASTNode):
    """Traverse the AST to collect all SymbolPostfix nodes."""
    if isinstance(ast, ASTNode) and ast.node_type == 'SymbolPostfix':
        yield ast
    elif isinstance(ast, ASTNode):
        for key, value in ast.attributes.items():
            yield from traverse_ast(value)

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

    for symbol_postfix in traverse_ast(result):
        print(render(symbol_postfix))