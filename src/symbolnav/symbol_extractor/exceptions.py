from typing import Any, Optional, TypedDict, cast, Protocol, TYPE_CHECKING
from ply.lex import LexToken, Lexer
from rich.console import Console
from rich.style import Style
from rich.text import Text


console = Console(highlight=False)
source_code_style = Style(color="#888888", bold=False)
error_style = Style(color="red", bold=True)
error_char_style = Style(color="red", bold=True)
message_style = Style(color="white", bold=False)
note_style = Style(color="yellow", bold=False)

class ActualLexer(Protocol):
    lexdata: str
    source_line: int
    source_column: int
    file: str

class ActualLexToken(Protocol):
    lexer: ActualLexer
    type: int
    value: str
    lineno: int
    lexpos: int


class MathError(Exception):

    def __init__(self, message: str, token: Optional[LexToken] = None, note: Optional[str] = None):
        token_ = cast(ActualLexToken, token)
        self.abs_pos = token_.lexpos
        self.lexdata = token_.lexer.lexdata
        self.src_lineno = token_.lexer.source_line
        self.src_column = token_.lexer.source_column
        self.file = token_.lexer.file
        
        assert 0 <= self.abs_pos < len(self.lexdata), "Invalid position"
        
        rel_lineno = self.lexdata.count('\n', 0, self.abs_pos) + 1
        rel_column = self.abs_pos - self.lexdata.rfind('\n', 0, self.abs_pos)
        self.abs_lineno = self.src_lineno + rel_lineno - 1
        self.abs_column = rel_column
        if rel_lineno == 1: self.abs_column += self.src_column - 1
        
        lines = self.lexdata.split('\n')
        assert 1 <= rel_lineno <= len(lines), "Invalid line number"
        self.pos_hint_lines = self._build_pos_hint(lines, rel_lineno, rel_column)
        self.message = self._build_message(message, self.abs_lineno, self.abs_column, note)
    
    def _build_message(self, message: str, abs_lineno: int, abs_column: int, note: Optional[str]) -> Text:
        message_text = Text(f"{__class__.__name__}: ", style=error_style) + Text(f"{message} at File {self.file}, line {abs_lineno}, column {abs_column}:\n", style=message_style)
        if note is not None:
            message_text += Text(f"Note: {note}\n", style=note_style)
        return message_text
    
    def _build_pos_hint(self, lines: list[str], rel_lineno: int, rel_column: int) -> list[Text]:
        # Build formatted pos_hint with error highlighting
        pos_hint_lines = []
        for i, line in enumerate(lines):
            if i == rel_lineno - 1:
                pos_hint_lines.append((
                    Text(line[:rel_column - 1], style=source_code_style)
                    + Text(line[rel_column - 1], style=error_char_style)
                    + Text(line[rel_column:], style=source_code_style)
                ))
                pos_hint_lines.append(
                    Text(' ' * (rel_column - 1) + '^', style=error_char_style))
            else:
                regular_line_text = Text(line, style=source_code_style)
                pos_hint_lines.append(regular_line_text)
        return pos_hint_lines
    
    def display_error(self):
        console.print(self.message)
        for line_text in self.pos_hint_lines:
            console.print(" " * 4, end="")
            console.print(line_text)
        console.print()

class MathValueError(MathError):
    """Error from lexer - token.value contains the illegal character(s)"""

class MathSyntaxError(MathError):
    """Error from parser - token.value may be the problematic token or None"""
