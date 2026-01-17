import ply.lex as lex
from .exceptions import LaTeXValueError


def _get_line_number(lexer, pos):
    """Calculate line number from lexpos."""
    if pos >= len(lexer.lexdata):
        pos = len(lexer.lexdata) - 1
    return lexer.lexdata[:pos].count('\n') + 1


def _get_line_start_pos(lexer, pos):
    """Calculate the absolute position of the start of the line containing pos."""
    if pos >= len(lexer.lexdata):
        pos = len(lexer.lexdata) - 1
    # Find the last newline before pos
    last_newline = lexer.lexdata.rfind('\n', 0, pos)
    return last_newline + 1  # Position after the newline, or 0 if no newline found


tokens = (
    'MATH_DISPLAY', 'MATH_INLINE', 'MATH_EQUATION', 'MATH_PARENTHESIS', 'MATH_BRACKET',
    'TEXT', 'COMMENT',
)
states = (
    ('mathdisplay', 'exclusive'),
    ('mathequation', 'exclusive'),
    ('mathinline', 'exclusive'),
    ('mathparenthesis', 'exclusive'),
    ('mathbracket', 'exclusive'),
)

t_ignore = ' \t'

def t_COMMENT(t):
    r'%.*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_BEGIN_MATH_DISPLAY(t):
    r'\$\$'
    t.lexer.mark_start_pos = t.lexer.lexpos - len(t.value)  # Position of the $$
    t.lexer.code_start = t.lexer.lexpos  # Position after the $$
    t.lexer.code_start_line = _get_line_number(t.lexer, t.lexer.mark_start_pos)
    t.lexer.mark = t.value
    t.lexer.begin('mathdisplay')

def t_BEGIN_MATH_INLINE(t):
    r'\$'
    t.lexer.mark_start_pos = t.lexer.lexpos - len(t.value)  # Position of the $
    t.lexer.code_start = t.lexer.lexpos  # Position after the $
    t.lexer.code_start_line = _get_line_number(t.lexer, t.lexer.mark_start_pos)
    t.lexer.mark = t.value
    t.lexer.begin('mathinline')

def t_BEGIN_MATH_PARENTHESIS(t):
    r'\\\('
    t.lexer.mark_start_pos = t.lexer.lexpos - len(t.value)  # Position of the \(
    t.lexer.code_start = t.lexer.lexpos  # Position after the \(
    t.lexer.code_start_line = _get_line_number(t.lexer, t.lexer.mark_start_pos)
    t.lexer.mark = t.value
    t.lexer.begin('mathparenthesis')

def t_BEGIN_MATH_BRACKET(t):
    r'\\\['
    t.lexer.mark_start_pos = t.lexer.lexpos - len(t.value)  # Position of the \[
    t.lexer.code_start = t.lexer.lexpos  # Position after the \[
    t.lexer.code_start_line = _get_line_number(t.lexer, t.lexer.mark_start_pos)
    t.lexer.mark = t.value
    t.lexer.begin('mathbracket')

def t_BEGIN_EQUATION(t):
    r'\\begin[ ]*\{[ ]*equation[ ]*\}'
    t.lexer.mark_start_pos = t.lexer.lexpos - len(t.value)  # Position of the \begin{equation}
    t.lexer.code_start = t.lexer.lexpos  # Position after the \begin{equation}
    t.lexer.code_start_line = _get_line_number(t.lexer, t.lexer.mark_start_pos)
    t.lexer.mark = t.value
    t.lexer.begin('mathequation')

def t_LATEX_CMD(t):
    r'\\[a-zA-Z]+'
    t.type = 'TEXT'
    return t

def t_ESCAPED_BRACE(t):
    r'\\\{|\\\}'
    t.type = 'TEXT'
    return t

def t_ESCAPED_UNDERSCORE(t):
    r'\\\_'
    t.type = 'TEXT'
    return t

def t_ESCAPED_HASH(t):
    r'\\\#'
    t.type = 'TEXT'
    return t

def t_ESCAPED_AMPERSAND(t):
    r'\\\&'
    t.type = 'TEXT'
    return t

def t_ESCAPED_DOLLAR(t):
    r'\\\$'
    t.type = 'TEXT'
    return t

def t_ESCAPED_SEMICOLON(t):
    r'\\\;'
    t.type = 'TEXT'
    return t

def t_ESCAPED_PERCENT(t):
    r'\\\%'
    t.type = 'TEXT'
    return t

def t_ESCAPED_BACKSLASH(t):
    r'\\\\'
    t.type = 'TEXT'
    return t

def t_TEXT(t):
    r'[^\$\\%]+'
    return t

t_mathdisplay_ignore = ' \t'

def t_mathdisplay_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_mathdisplay_END_MATH_DISPLAY(t):
    r'\$\$'
    t.marks = (t.lexer.mark, t.value)
    t.pos_beg = t.lexer.code_start
    t.pos_end = t.lexer.lexpos - len(t.value)
    t.mark_start_pos = t.lexer.mark_start_pos
    t.mark_end_pos = t.lexer.lexpos
    t.value = t.lexer.lexdata[t.pos_beg:t.pos_end]
    t.type = 'MATH_DISPLAY'
    t.lineno = t.lexer.code_start_line
    # Calculate relative position (from start of line) for the start marker
    line_start_pos = _get_line_start_pos(t.lexer, t.lexer.mark_start_pos)
    t.column = t.lexer.mark_start_pos - line_start_pos
    t.lexer.begin('INITIAL')
    return t

def t_mathdisplay_any(t):
    r'[^\$]+'

def t_mathdisplay_error(t):
    raise LaTeXValueError(f"Unexpected token", t)

t_mathinline_ignore = ' \t'

def t_mathinline_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_mathinline_END_MATH_INLINE(t):
    r'\$'
    t.marks = (t.lexer.mark, t.value)
    t.pos_beg = t.lexer.code_start
    t.pos_end = t.lexer.lexpos - len(t.value)
    t.mark_start_pos = t.lexer.mark_start_pos
    t.mark_end_pos = t.lexer.lexpos
    t.value = t.lexer.lexdata[t.pos_beg:t.pos_end]
    t.type = 'MATH_INLINE'
    t.lineno = t.lexer.code_start_line
    # Calculate relative position (from start of line) for the start marker
    line_start_pos = _get_line_start_pos(t.lexer, t.lexer.mark_start_pos)
    t.column = t.lexer.mark_start_pos - line_start_pos
    t.lexer.begin('INITIAL')
    return t

def t_mathinline_any(t):
    r'[^$]+'

def t_mathinline_error(t):
    raise LaTeXValueError(f"Unexpected token", t)

t_mathparenthesis_ignore = ' \t'

def t_mathparenthesis_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_mathparenthesis_END_MATH_PARENTHESIS(t):
    r'\\\)'
    t.marks = (t.lexer.mark, t.value)
    t.pos_beg = t.lexer.code_start
    t.pos_end = t.lexer.lexpos - len(t.value)
    t.mark_start_pos = t.lexer.mark_start_pos
    t.mark_end_pos = t.lexer.lexpos
    t.value = t.lexer.lexdata[t.pos_beg:t.pos_end]
    t.type = 'MATH_PARENTHESIS'
    t.lineno = t.lexer.code_start_line
    # Calculate relative position (from start of line) for the start marker
    line_start_pos = _get_line_start_pos(t.lexer, t.lexer.mark_start_pos)
    t.column = t.lexer.mark_start_pos - line_start_pos
    t.lexer.begin('INITIAL')
    return t

def t_mathparenthesis_any(t):
    r'[^\\]+|\\[^)]'

def t_mathparenthesis_error(t):
    raise LaTeXValueError(f"Unexpected token", t)

t_mathbracket_ignore = ' \t'

def t_mathbracket_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_mathbracket_END_MATH_BRACKET(t):
    r'\\\]'
    t.marks = (t.lexer.mark, t.value)
    t.pos_beg = t.lexer.code_start
    t.pos_end = t.lexer.lexpos - len(t.value)
    t.mark_start_pos = t.lexer.mark_start_pos
    t.mark_end_pos = t.lexer.lexpos
    t.value = t.lexer.lexdata[t.pos_beg:t.pos_end]
    t.type = 'MATH_BRACKET'
    t.lineno = t.lexer.code_start_line
    # Calculate relative position (from start of line) for the start marker
    line_start_pos = _get_line_start_pos(t.lexer, t.lexer.mark_start_pos)
    t.column = t.lexer.mark_start_pos - line_start_pos
    t.lexer.begin('INITIAL')
    return t

def t_mathbracket_any(t):
    r'[^\\]+|\\[^\]]'

def t_mathbracket_error(t):
    raise LaTeXValueError(f"Unexpected token", t)

t_mathequation_ignore = ' \t'

def t_mathequation_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_mathequation_END_MATH_EQUATION(t):
    r'\\end[ ]*\{[ ]*equation[ ]*\}'
    t.marks = (t.lexer.mark, t.value)
    t.pos_beg = t.lexer.code_start
    t.pos_end = t.lexer.lexpos - len(t.value)
    t.mark_start_pos = t.lexer.mark_start_pos
    t.mark_end_pos = t.lexer.lexpos
    t.value = t.lexer.lexdata[t.pos_beg:t.pos_end]
    t.type = 'MATH_EQUATION'
    t.lineno = t.lexer.code_start_line
    # Calculate relative position (from start of line) for the start marker
    line_start_pos = _get_line_start_pos(t.lexer, t.lexer.mark_start_pos)
    t.column = t.lexer.mark_start_pos - line_start_pos
    t.lexer.begin('INITIAL')
    return t

def t_mathequation_any(t):
    r'.+'

def t_mathequation_error(t):
    raise LaTeXValueError(f"Unexpected token", t)

def t_error(t):
    raise LaTeXValueError(f"Unexpected token", t)

lexer = lex.lex()
