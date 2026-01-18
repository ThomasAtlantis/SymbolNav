import ply.lex as lex
import ply.yacc as yacc
from typing import Optional
from symbolnav.symbol_extractor.lexer import *
from symbolnav.symbol_extractor.parser import *

class LaTeXMathInterpreter:

    def __init__(self, debug: bool = False):
        self.lexer = lex.lex()
        # # Set global lexer reference for p_error function to access
        # import symbol_nav.symbol_extractor.parser as parser_module
        # parser_module._current_lexer = self.lexer
        self.parser = yacc.yacc(debug=debug, write_tables=False)
    
    def parse(self, latex: str, file: Optional[str] = None, source_line: Optional[int] = None, source_column: Optional[int] = None) -> ASTNode:
        # Store source position information in lexer for error reporting
        # if hasattr(self.lexer, 'source_line'):
        #     self.lexer.source_line = source_line
        #     self.lexer.file = file
        #     self.lexer.source_column = source_column
        # else:
        #     # Create attributes if they don't exist
        setattr(self.lexer, 'source_line', source_line)
        setattr(self.lexer, 'source_column', source_column)
        setattr(self.lexer, 'file', file)
        result = self.parser.parse(latex, lexer=self.lexer)
        return result
