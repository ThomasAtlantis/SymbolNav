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
        self.source_line = getattr(token.lexer, 'source_line', None) if hasattr(token, 'lexer') else None  # type: ignore
        self.source_column = getattr(token.lexer, 'source_column', None) if hasattr(token, 'lexer') else None  # type: ignore
        self.file = getattr(token.lexer, 'file', None) if hasattr(token, 'lexer') else None  # type: ignore
        
        if lexdata:
            # Calculate relative position within the math expression
            self.relative_lineno = _get_line_number(lexdata, token.lexpos)  # type: ignore
            line_start_pos = _get_line_start_pos(lexdata, token.lexpos)  # type: ignore
            self.relative_column = token.lexpos - line_start_pos  # type: ignore
            
            # If source position is provided, calculate absolute position in original document
            if self.source_line is not None:
                # Count newlines before the error position to get line offset
                newlines_before = lexdata[:token.lexpos].count('\n')  # type: ignore
                if newlines_before == 0:
                    # Error is on the first line of the math expression
                    # Column is source column + relative column
                    self.lineno = self.source_line
                    self.column = (self.source_column or 0) + self.relative_column
                else:
                    # Error is on a later line within the math expression
                    # Line is source line + line offset, column is relative column
                    self.lineno = self.source_line + newlines_before
                    self.column = self.relative_column
            else:
                # No source position, use relative position
                self.lineno = self.relative_lineno
                self.column = self.relative_column
        else:
            # Fallback to token.lineno if available
            if self.source_line is not None:
                self.lineno = source_line + (getattr(token, 'lineno', 1) - 1 if hasattr(token, 'lineno') else 0)  # type: ignore
            else:
                self.lineno = getattr(token, 'lineno', None)  # type: ignore
            self.column = getattr(token, 'column', None) if self.source_column is None else None  # type: ignore
    
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
        if lexdata and self.relative_lineno:
            lines = lexdata.split('\n')
            if 1 <= self.relative_lineno <= len(lines):
                line_content = lines[self.relative_lineno - 1]
                self.pos_hint = line_content + '\n' + ' ' * (self.relative_column or 0) + '^'  # type: ignore
            else:
                self.pos_hint = lexdata
        else:
            self.pos_hint = getattr(token, 'value', '')
    
    def display_error(self):
        lexdata = getattr(self.token.lexer, 'lexdata', '') if hasattr(self.token, 'lexer') else ''  # type: ignore
        print(f"In LaTeXMath at File {self.file}, line {self.source_line}, column {(self.source_column or 0) + 1}:")
        if lexdata:
            for line in lexdata.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)
        else:
            print(getattr(self.token, 'value', ''))
        print(f"{self.message} at File {self.file}, line {self.lineno}, column {(self.column or 0) + 1}")
        if hasattr(self, 'pos_hint'):
            for line in self.pos_hint.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)
        print()


class MathSyntaxError(MathError):
    """Error from parser - token.value may be the problematic token or None"""
    
    def __init__(self, message: str, token: LexToken):
        super().__init__(message, token)
        # For MathSyntaxError, token.value is the token that caused the error
        # Use lexdata to get the full source for display
        lexdata = getattr(token.lexer, 'lexdata', '') if hasattr(token, 'lexer') else ''  # type: ignore
        if lexdata and self.relative_lineno:
            lines = lexdata.split('\n')
            if 1 <= self.relative_lineno <= len(lines):
                line_content = lines[self.relative_lineno - 1]
                self.pos_hint = line_content + '\n' + ' ' * (self.relative_column or 0) + '^'  # type: ignore
            else:
                self.pos_hint = lexdata
        else:
            self.pos_hint = getattr(token, 'value', '') or ''
    
    def display_error(self):
        lexdata = getattr(self.token.lexer, 'lexdata', '') if hasattr(self.token, 'lexer') else ''  # type: ignore
        print(f"In LaTeXMath at File {self.file}, line {self.source_line}, column {(self.source_column or 0) + 1}:")
        if lexdata:
            for line in lexdata.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)
        else:
            print(getattr(self.token, 'value', '') or '')
        print(f"{self.message} at File {self.file}, line {self.lineno}, column {(self.column or 0) + 1}")
        if hasattr(self, 'pos_hint'):
            for line in self.pos_hint.split('\n'):
                console.print(" " * 4 + line, style=source_code_style)
        print()