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
            e.display_error()
            return iter(())  # type: ignore
        
        def _traverse(ast: ASTNode | None | list):
            if ast is None:
                return
            if isinstance(ast, list):
                # Handle list of AST nodes (from multi_content)
                for item in ast:
                    yield from _traverse(item)
                return
            if not isinstance(ast, ASTNode):
                return
            if ast.node_type == 'SymbolPostfix':
                symbol = ast.attributes.get('symbol')
                if symbol is None:
                    return
                if symbol.node_type == 'Symbol' and symbol.attributes.get('symbol_type') not in ('greek', 'letter'):
                    return
                yield ast
            elif ast.node_type == 'Symbol':
                if ast.attributes.get('symbol_type') in ('greek', 'letter'):
                    yield ast
            for value in ast.attributes.values():
                yield from _traverse(value)
        return _traverse(ast)