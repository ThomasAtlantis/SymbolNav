from ply.lex import LexToken
from rich.console import Console
from rich.style import Style


console = Console(highlight=False)
source_code_style = Style(color="#888888")


def _get_line_number(lexdata: str, pos: int) -> int:
    """Calculate line number from lexpos."""
    if pos >= len(lexdata):
        pos = len(lexdata) - 1
    return lexdata[:pos].count('\n') + 1


def _get_line_start_pos(lexdata: str, pos: int) -> int:
    """Calculate the absolute position of the start of the line containing pos."""
    if pos >= len(lexdata):
        pos = len(lexdata) - 1
    # Find the last newline before pos
    last_newline = lexdata.rfind('\n', 0, pos)
    return last_newline + 1  # Position after the newline, or 0 if no newline found


class MathError(Exception):

    def __init__(self, message: str, token: LexToken):
        self.message = message
        self.token = token
        
        # Calculate line number and column
        lexdata = getattr(token.lexer, 'lexdata', '') if hasattr(token, 'lexer') else ''  # type: ignore
        if lexdata:
            self.lineno = _get_line_number(lexdata, token.lexpos)  # type: ignore
            line_start_pos = _get_line_start_pos(lexdata, token.lexpos)  # type: ignore
            self.column = token.lexpos - line_start_pos  # type: ignore
        else:
            # Fallback to token.lineno if available
            self.lineno = getattr(token, 'lineno', None)  # type: ignore
            self.column = None  # type: ignore
    
    def __str__(self):
        lineno_str = f" line {self.lineno}" if self.lineno is not None else ""
        column_str = f", column {self.column}" if self.column is not None else ""
        return f"{self.__class__.__name__}: {self.message} at position {self.token.lexpos}{lineno_str}{column_str}"  # type: ignore


class MathValueError(MathError):
    """Error from lexer - token.value contains the illegal character(s)"""
    
    def __init__(self, message: str, token: LexToken):
        super().__init__(message, token)
        # For MathValueError, token.value is the illegal character(s) from lexer
        # Use lexdata to get the full source for display
        lexdata = getattr(token.lexer, 'lexdata', '') if hasattr(token, 'lexer') else ''  # type: ignore
        if lexdata and self.lineno:
            lines = lexdata.split('\n')
            if 1 <= self.lineno <= len(lines):
                line_content = lines[self.lineno - 1]
                self.pos_hint = line_content + '\n' + ' ' * (self.column or 0) + '^'  # type: ignore
            else:
                self.pos_hint = lexdata
        else:
            self.pos_hint = getattr(token, 'value', '')
    
    def display_error(self):
        lexdata = getattr(self.token.lexer, 'lexdata', '') if hasattr(self.token, 'lexer') else ''  # type: ignore
        print(f"In LaTeXMath:")
        if lexdata:
            for line in lexdata.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)
        else:
            print(getattr(self.token, 'value', ''))
        print(f"{self.message} at line {self.lineno}, column {self.column}")
        if hasattr(self, 'pos_hint'):
            for line in self.pos_hint.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)


class MathSyntaxError(MathError):
    """Error from parser - token.value may be the problematic token or None"""
    
    def __init__(self, message: str, token: LexToken):
        super().__init__(message, token)
        # For MathSyntaxError, token.value is the token that caused the error
        # Use lexdata to get the full source for display
        lexdata = getattr(token.lexer, 'lexdata', '') if hasattr(token, 'lexer') else ''  # type: ignore
        if lexdata and self.lineno:
            lines = lexdata.split('\n')
            if 1 <= self.lineno <= len(lines):
                line_content = lines[self.lineno - 1]
                self.pos_hint = line_content + '\n' + ' ' * (self.column or 0) + '^'  # type: ignore
            else:
                self.pos_hint = lexdata
        else:
            self.pos_hint = getattr(token, 'value', '') or ''
    
    def display_error(self):
        lexdata = getattr(self.token.lexer, 'lexdata', '') if hasattr(self.token, 'lexer') else ''  # type: ignore
        print(f"In LaTeXMath:")
        if lexdata:
            for line in lexdata.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)
        else:
            print(getattr(self.token, 'value', '') or '')
        print(f"{self.message} at line {self.lineno}, column {self.column}")
        if hasattr(self, 'pos_hint'):
            for line in self.pos_hint.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)