tokens = (
    # 'PS', 'WS', 'ADD', 'SUB', 'MUL', 'DIV', 'L_PAREN', 'R_PAREN', 'L_BRACE', 'R_BRACE', 'L_BRACKET', 'R_BRACKET', 'BAR', 'FUNC_LIM', 'LIM_APPROACH_SYM', 'FUNC_INT', 'FUNC_SUM', 'FUNC_PROD', 'FUNC_LOG', 'FUNC_LN', 'FUNC_SIN', 'FUNC_COS', 'FUNC_TAN', 'FUNC_CSC', 'FUNC_SEC', 'FUNC_COT', 'FUNC_ARCSIN', 'FUNC_ARCCOS', 'FUNC_ARCTAN', 'FUNC_ARCCSC', 'FUNC_ARCSEC', 'FUNC_ARCCOT', 'FUNC_SINH', 'FUNC_COSH', 'FUNC_TANH', 'FUNC_ARSINH', 'FUNC_ARCOSH', 'FUNC_ARTANH', 'FUNC_SQRT', 'CMD_TIMES', 'CMD_CDOT', 'CMD_DIV', 'CMD_FRAC', 'CMD_MATHIT', 'UNDERSCORE', '_', 'CARET', 'COLON', 'WS_CHAR', 'DIFFERENTIAL', 'LETTER', 'DIGIT', 'NUMBER', 'EQUAL', 'LT', 'LTE', 'GT', 'GTE', 'BANG', 'SYMBOL'
    'ADD', 'SUB', 'MUL', 'DIV', 
    'EQUAL', 'LT', 'LTE', 'GT', 'GTE',
    'CMD_TIMES', 'CMD_CDOT', 'CMD_DIV', 'COLON',
    'CARET', 'UNDERSCORE',
    'L_BRACE', 'R_BRACE',
    'SYMBOL',
    'CMD_MATHBF', 'CMD_TEXT', 'CMD_MATHBB', 'CMD_MATHIT', 'CMD_IN',
    'TEXT',
)

states = (
    ('textmode', 'exclusive'), 
)

t_ignore = ' \t\r\n'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_EQUAL = r'='
t_LT = r'<'
t_LTE = r'\\leq'
t_GT = r'>'
t_GTE = r'\\geq'
t_CMD_TIMES = r'\\times'
t_CMD_CDOT = r'\\cdot'
t_CMD_DIV = r'\\div'
t_COLON = r':'
t_CARET = r'\^'
t_UNDERSCORE = r'_'
t_R_BRACE = r'\}'
t_CMD_MATHBF = r'\\mathbf'
t_CMD_MATHBB = r'\\mathbb'
t_CMD_MATHIT = r'\\mathit'
t_CMD_IN = r'\\in'
t_SYMBOL = r'[a-zA-Z0-9]'

def t_CMD_TEXT(t):
    r'\\text'
    t.lexer.expect_text_brace = True
    return t

def t_L_BRACE(t):
    r'\{'
    if hasattr(t.lexer, 'expect_text_brace') and t.lexer.expect_text_brace:
        t.lexer.expect_text_brace = False
        t.lexer.previous_state = t.lexer.lexstate
        t.lexer.begin('textmode')
        t.lexer.brace_depth = 1
        t.lexer.text_parts = []
    return t

def t_textmode_textpart(t):
    r'[^{}]+'
    if hasattr(t.lexer, 'text_parts'):
        t.lexer.text_parts.append(t.value)
    return None

def t_textmode_L_BRACE(t):
    r'\{'
    if hasattr(t.lexer, 'brace_depth'):
        t.lexer.brace_depth += 1
    if hasattr(t.lexer, 'text_parts'):
        t.lexer.text_parts.append('{')
    return None

def t_textmode_R_BRACE(t):
    r'\}'
    if not hasattr(t.lexer, 'brace_depth'):
        t.lexer.brace_depth = 0
    t.lexer.brace_depth -= 1
    
    if t.lexer.brace_depth <= 0:
        previous_state = getattr(t.lexer, 'previous_state', 'INITIAL')
        if hasattr(t.lexer, 'text_parts') and t.lexer.text_parts:
            text_content = ''.join(t.lexer.text_parts)
            t.lexer.text_parts = []
            t.lexer.brace_depth = 0
            t.lexer.begin(previous_state)
            t.lexer.lexpos = t.lexer.lexpos - 1
            t.type = 'TEXT'
            t.value = text_content
            return t
        else:
            t.lexer.text_parts = []
            t.lexer.brace_depth = 0
            t.lexer.begin(previous_state)
            t.type = 'R_BRACE'
            return t
    else:
        if hasattr(t.lexer, 'text_parts'):
            t.lexer.text_parts.append('}')
        return None

def t_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}'")

def t_textmode_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}' in text mode")