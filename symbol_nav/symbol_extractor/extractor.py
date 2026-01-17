from typing import Generator
from .interpreter import LaTeXMathInterpreter
from .mast import ASTNode
from .exceptions import MathSyntaxError, MathValueError


class SymbolExtractor:

    def __init__(self):
        self.parser = LaTeXMathInterpreter()

    def extract_symbol(self, latex: str) -> Generator[ASTNode]:
        try:
            ast = self.parser.parse(latex)
        except (MathSyntaxError, MathValueError) as e:
            print(latex)
            print(e.cursor)
            print(e)
            return iter(())  # type: ignore
        
        def _traverse(ast: ASTNode | None):
            if ast is None or not isinstance(ast, ASTNode):
                return
            if ast.node_type == 'SymbolPostfix':
                symbol = ast.attributes.get('symbol')
                if symbol is None:
                    return
                if symbol.node_type == 'Symbol' and symbol.attributes.get('symbol_type') not in ('greek', 'letter'):
                    return
                yield ast
            else:
                for value in ast.attributes.values():
                    yield from _traverse(value)
        return _traverse(ast)