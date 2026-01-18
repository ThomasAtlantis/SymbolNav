from typing import Optional
import ply.yacc as yacc
import ply.lex as lex
from .mast import ASTNode
from .lexer import *
from .parser import *


class LaTeXMathInterpreter:

    def __init__(self, debug: bool = False):
        self.lexer = lex.lex()
        self.parser = yacc.yacc(debug=debug, write_tables=False)
    
    def parse(
        self, 
        latex: str, 
        file: Optional[str], 
        line: Optional[int], 
        column: Optional[int]
    ) -> ASTNode:
        setattr(self.lexer, 'source_line', line)
        setattr(self.lexer, 'source_column', column)
        setattr(self.lexer, 'file', file)
        result = self.parser.parse(latex, lexer=self.lexer)
        return result
