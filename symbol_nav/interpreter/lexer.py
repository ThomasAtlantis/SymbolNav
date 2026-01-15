from .exceptions import MathValueError


tokens = (
    # 'PS', 'WS', 'ADD', 'SUB', 'MUL', 'DIV', 'L_PAREN', 'R_PAREN', 'L_BRACE', 'R_BRACE', 'L_BRACKET', 'R_BRACKET', 'BAR', 'FUNC_LIM', 'LIM_APPROACH_SYM', 'FUNC_INT', 'FUNC_SUM', 'FUNC_PROD', 'FUNC_LOG', 'FUNC_LN', 'FUNC_SIN', 'FUNC_COS', 'FUNC_TAN', 'FUNC_CSC', 'FUNC_SEC', 'FUNC_COT', 'FUNC_ARCSIN', 'FUNC_ARCCOS', 'FUNC_ARCTAN', 'FUNC_ARCCSC', 'FUNC_ARCSEC', 'FUNC_ARCCOT', 'FUNC_SINH', 'FUNC_COSH', 'FUNC_TANH', 'FUNC_ARSINH', 'FUNC_ARCOSH', 'FUNC_ARTANH', 'FUNC_SQRT', 'CMD_TIMES', 'CMD_CDOT', 'CMD_DIV', 'CMD_FRAC', 'CMD_MATHIT', 'UNDERSCORE', '_', 'CARET', 'COLON', 'WS_CHAR', 'DIFFERENTIAL', 'LETTER', 'DIGIT', 'NUMBER', 'EQUAL', 'LT', 'LTE', 'GT', 'GTE', 'BANG', 'SYMBOL'
    'ADD', 'SUB', 'MUL', 'DIV', 'BAR',
    'EQUAL', 'LT', 'LE', 'LTE', 'GT', 'GTE', 'TRIANGLEQUAL', 'APPROX', 'LEFTARROW', 'RIGHTARROW', 'LEFTARROW_DOUBLE', 'RIGHTARROW_DOUBLE',
    'CMD_TIMES', 'CMD_CDOT', 'CMD_DIV', 'COLON', 'SETMINUS', 'SUBSET', 'CUP', 'SIM',
    'CARET', 'UNDERSCORE', 'PRIME', 'CMD_PRIME',
    'L_BRACE', 'R_BRACE',
    'L_BRACE_TEXT', 'R_BRACE_TEXT',
    'NUMBER_SYMBOL', 'LETTER_SYMBOL', 'GREEK_SYMBOL', 'OTHER_SYMBOL',
    'CMD_MATHBF', 'CMD_TEXT', 'CMD_MATHBB', 'CMD_MATHIT', 'CMD_BM', 'CMD_MATHCAL', 'CMD_MATHRM', 'CMD_SQRT',
    'CMD_HAT', 'CMD_TILDE',
    'CMD_IN', 'CMD_CIRC', 'CMD_TO', 'CMD_NOTIN',
    'TEXT',
    'COMMA', 'PERIOD',
    'L_PAREN', 'R_PAREN', 'L_BRACKET', 'R_BRACKET', 'L_BMATRIX', 'R_BMATRIX',
    'FRAC',
)

states = (
    ('textmode', 'exclusive'),
)

t_ignore = ' \t\r\n'

# Binary operators
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_BAR = r'\|'
t_EQUAL = r'='
t_TRIANGLEQUAL = r'\\triangleq'
t_APPROX = r'\\approx'
t_LT = r'<'
t_LE = r'\\le'
t_LTE = r'\\leq'
t_GT = r'>'
t_GTE = r'\\geq'
t_SIM = r'\\sim'
t_LEFTARROW = r'\\leftarrow'
t_RIGHTARROW = r'\\rightarrow'
t_LEFTARROW_DOUBLE = r'\\Leftarrow'
t_RIGHTARROW_DOUBLE = r'\\Rightarrow'
t_CMD_TIMES = r'\\times'
t_CMD_CDOT = r'\\cdot'
t_CMD_DIV = r'\\div'
t_CMD_CIRC = r'\\circ'
t_CMD_TO = r'\\to'
t_SETMINUS = r'\\setminus'
t_SUBSET = r'\\subset'
t_CUP = r'\\cup'
t_COLON = r':'
t_CARET = r'\^'
t_UNDERSCORE = r'_'
t_PRIME = r'\''
t_CMD_PRIME = r'\\prime'
t_R_BRACE = r'\}'
t_FRAC = r'\\frac'

# Format commands
t_CMD_MATHBF = r'\\mathbf'
t_CMD_MATHBB = r'\\mathbb'
t_CMD_MATHIT = r'\\mathit'
t_CMD_MATHCAL = r'\\mathcal'
t_CMD_MATHRM = r'\\mathrm'
t_CMD_BM = r'\\bm'
t_CMD_HAT = r'\\hat'
t_CMD_TILDE = r'\\tilde'
t_CMD_SQRT = r'\\sqrt'
t_CMD_IN = r'\\in'
t_CMD_NOTIN = r'\\notin'
t_NUMBER_SYMBOL = r'([0-9])'
t_LETTER_SYMBOL = r'([a-zA-Z])'
t_GREEK_SYMBOL = r'(' + r'|'.join(r"\\" + symbol for symbol in [
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
    'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega',
    'varepsilon', 'vartheta', 'varpi', 'varrho', 'varsigma', 'varphi',
    'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma', 'Upsilon', 'Phi', 'Psi', 'Omega',
    'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma', 'Upsilon', 'Phi', 'Psi', 'Omega',
]) + r')'
t_OTHER_SYMBOL =  r'(' + r'|'.join(r"\\" + symbol for symbol in [
    'dots', 'cdots', 'arg', 'emptyset', 'infty', 'max', 'min', 'sum', 'exp',
    'nolimits', 'ln', 'log', 'partial', 'prod', 'nabla', 'left', 'right', 'lim', 'top',
    r'\|', 'linebreak'
]) + r')'
t_textmode_ignore = ''
t_COMMA = r','
t_PERIOD = r'\.'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACE_TEXT = r'\\{'
t_R_BRACE_TEXT = r'\\}'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_L_BMATRIX = r'\\begin{bmatrix}'
t_R_BMATRIX = r'\\end{bmatrix}'

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
    raise MathValueError(f"Illegal character '{t.value[0]}'", t)


def t_textmode_error(t):
    raise MathValueError(f"Illegal character '{t.value[0]}' in text mode", t)
