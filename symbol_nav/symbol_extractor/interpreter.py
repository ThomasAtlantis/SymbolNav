import ply.lex as lex
import ply.yacc as yacc
from .lexer import *
from .parser import *

class LaTeXMathInterpreter:

    def __init__(self, debug: bool = False):
        self.lexer = lex.lex()
        # # Set global lexer reference for p_error function to access
        # import symbol_nav.symbol_extractor.parser as parser_module
        # parser_module._current_lexer = self.lexer
        self.parser = yacc.yacc(debug=debug, write_tables=False)
    
    def parse(self, latex: str) -> ASTNode:
        result = self.parser.parse(latex, lexer=self.lexer)
        return result
