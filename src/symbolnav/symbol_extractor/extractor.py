from typing import Generator, Optional
from symbolnav.symbol_extractor.interpreter import LaTeXMathInterpreter
from symbolnav.symbol_extractor.mast import ASTNode
from symbolnav.symbol_extractor.exceptions import MathSyntaxError, MathValueError


class SymbolExtractor:

    def __init__(self):
        self.parser = LaTeXMathInterpreter()

    def extract_symbol(self, latex: str, file: Optional[str] = None, source_line: Optional[int] = None, source_column: Optional[int] = None) -> Generator[ASTNode]:
        try:
            ast = self.parser.parse(latex, file=file, source_line=source_line, source_column=source_column)
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