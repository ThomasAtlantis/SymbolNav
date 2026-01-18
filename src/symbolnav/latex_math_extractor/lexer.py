import ply.lex as lex
from symbolnav.latex_math_extractor.exceptions import LaTeXValueError

# ========================================================
# User configurable variables
# ========================================================

MATH_MODES = {
    'MATH_DISPLAY': {
        'beg': r'\$\$',
        'end': r'\$\$',
        'any': r'[^\$]+',
    },
    'MATH_INLINE': {
        'beg': r'\$',
        'end': r'\$',
        'any': r'[^$]+',
    },
    'MATH_PARENTHESIS': {
        'beg': r'\\\(',
        'end': r'\\\)',
        'any': r'[^\\]+|\\[^)]',
    },
    'MATH_BRACKET': {
        'beg': r'\\\[',
        'end': r'\\\]',
        'any': r'[^\\]+|\\[^\]]',
    },
    'MATH_EQUATION': {
        'beg': r'\\begin[ ]*\{[ ]*equation[ ]*\}',
        'end': r'\\end[ ]*\{[ ]*equation[ ]*\}',
        'any': r'.+',
    },
    'MATH_EQUATIONSTAR': {
        'beg': r'\\begin[ ]*\{[ ]*equation[ ]*\*[ ]*\}',
        'end': r'\\end[ ]*\{[ ]*equation[ ]*\*[ ]*\}',
        'any': r'.+',
    }
}

# Generate ESCAPED handlers - all have the same structure
ESCAPED_CHARS = [
    ('BRACE', r'\\\{|\\\}'),
    ('UNDERSCORE', r'\\\_'),
    ('HASH', r'\\\#'),
    ('AMPERSAND', r'\\\&'),
    ('DOLLAR', r'\\\$'),
    ('SEMICOLON', r'\\\;'),
    ('PERCENT', r'\\\%'),
    ('BACKSLASH', r'\\\\'),
]

# ========================================================
# Lexer definitions
# ========================================================
tokens = (
    'TEXT', 'COMMENT', *list(MATH_MODES.keys()),
)

for token_type in MATH_MODES:
    MATH_MODES[token_type]['state'] = token_type.lower().replace('_', '')

states = tuple(
    (config['state'], 'exclusive')
    for config in MATH_MODES.values()
)

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


def _make_begin_handler(state_name, begin_pattern, token_type):
    """Factory function to create BEGIN handlers for math modes."""
    def handler(t):
        t.lexer.mark_start_pos = t.lexer.lexpos - len(t.value)
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.code_start_line = _get_line_number(t.lexer, t.lexer.mark_start_pos)
        t.lexer.mark = t.value
        t.lexer.begin(state_name)
    handler.__doc__ = begin_pattern  # PLY uses __doc__ as the regex pattern
    handler.__name__ = f't_BEGIN_{token_type}'
    globals()[handler.__name__] = handler


def _make_end_handler(state_name, end_pattern, token_type):
    """Factory function to create END handlers for math modes."""
    def handler(t):
        t.marks = (t.lexer.mark, t.value)
        t.pos_beg = t.lexer.code_start
        t.pos_end = t.lexer.lexpos - len(t.value)
        t.mark_start_pos = t.lexer.mark_start_pos
        t.mark_end_pos = t.lexer.lexpos
        t.value = t.lexer.lexdata[t.pos_beg:t.pos_end]
        t.type = token_type
        t.lineno = t.lexer.code_start_line
        line_start_pos = _get_line_start_pos(t.lexer, t.lexer.mark_start_pos)
        t.column = t.lexer.mark_start_pos - line_start_pos
        t.lexer.begin('INITIAL')
        return t
    handler.__doc__ = end_pattern  # PLY uses __doc__ as the regex pattern
    handler.__name__ = f't_{state_name}_END_{token_type}'
    globals()[handler.__name__] = handler


def _make_any_handler(state_name, any_pattern):
    """Factory function to create 'any' handlers for math modes."""
    def handler(t):
        pass  # Just consume the content
    handler.__doc__ = any_pattern  # PLY uses __doc__ as the regex pattern
    handler.__name__ = f't_{state_name}_any'
    globals()[handler.__name__] = handler


def _make_error_handler(state_name):
    """Factory function to create error handlers for math modes."""
    def handler(t):
        raise LaTeXValueError(f"Unexpected token", t)
    handler.__name__ = f't_{state_name}_error'
    globals()[handler.__name__] = handler


t_ignore = ' \t\r\n'

def t_COMMENT(t):
    r'%.*'
    return t

def t_LATEX_CMD(t):
    r'\\[a-zA-Z]+'
    t.type = 'TEXT'
    return t

def t_TEXT(t):
    r'[^\$\\%]+'
    return t

for name, pattern in ESCAPED_CHARS:
    # Create handler with pattern captured in closure
    def make_escaped_handler(pat):
        def handler(t):
            t.type = 'TEXT'
            return t
        handler.__doc__ = pat  # PLY uses __doc__ as the regex pattern
        return handler
    handler = make_escaped_handler(pattern)
    handler.__name__ = f't_ESCAPED_{name}'
    globals()[handler.__name__] = handler

# Generate state-specific handlers for each math mode
for token_type, config in MATH_MODES.items():
    state_name = config['state']
    globals()[f't_{state_name}_ignore'] = ' \t\r\n'
    begin_handler = _make_begin_handler(state_name, config['beg'], token_type)
    end_handler = _make_end_handler(state_name, config['end'], token_type)
    any_handler = _make_any_handler(state_name, config['any'])
    error_handler = _make_error_handler(state_name)

def t_error(t):
    raise LaTeXValueError(f"Unexpected token", t)

lexer = lex.lex()
