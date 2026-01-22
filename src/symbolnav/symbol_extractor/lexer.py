from typing import OrderedDict
from .exceptions import MathValueError

def UnionRegex(regex_list: list[str]) -> str:
    return r'(' + r'|'.join(frozenset(regex_list)) + r')'

lexer_config = OrderedDict({
    'symbol': OrderedDict(
        NUMBER_SYMBOL=r'([0-9])',
        LETTER_SYMBOL=r'([a-zA-Z])',
        GREEK_SYMBOL=UnionRegex([
            r'\\alpha', r'\\beta', r'\\gamma', r'\\delta', r'\\epsilon', r'\\zeta', r'\\eta', r'\\theta', r'\\iota', r'\\kappa', r'\\lambda', r'\\mu', r'\\nu', r'\\xi', r'\\pi', r'\\rho', r'\\sigma', r'\\tau', r'\\upsilon', r'\\phi', r'\\chi', r'\\psi', r'\\omega', 
            r'\\Alpha', r'\\Beta', r'\\Gamma', r'\\Delta', r'\\Epsilon', r'\\Zeta', r'\\Eta', r'\\Theta', r'\\Iota', r'\\Kappa', r'\\Lambda', r'\\Mu', r'\\Nu', r'\\Xi', r'\\Pi', r'\\Rho', r'\\Sigma', r'\\Tau', r'\\Upsilon', r'\\Phi', r'\\Chi', r'\\Psi', r'\\Omega', 
            r'\\varepsilon', r'\\vartheta', r'\\varpi', r'\\varrho', r'\\varsigma', r'\\varphi', 
        ]),
        OTHER_SYMBOL=UnionRegex([
            r'\\dots', r'\\cdots', r'\\arg', r'\\emptyset', r'\\infty', r'\\max', r'\\min', r'\\sum', r'\\exp',
            r'\\nolimits', r'\\ln', r'\\log', r'\\partial', r'\\prod', r'\\nabla', r'\\left', r'\\right', r'\\lim', r'\\top',
            r'\|', r'\\linebreak', r'\\square', r'\\quad', r'\\mid', r'&', r',', r'\.', r'\\prime',
            r'=', r'\\triangleq', r'\\neq', r'\\approx', r'\\sim', r'<', r'\\leq', r'\\le', r'>', r'\\geq', r'\\ge', r'\\leftarrow', r'\\rightarrow', r'\\Leftarrow', r'\\Rightarrow', r'\\in', r'\\notin', r'\\setminus', r'\\subset', r'\\cup', r'\\circ', r'\\cdot', r'\\to', r'\+', r'-', r'\*', r'/', r'\\times', r'\\div', r':', r'\|', 
            # r'\\ ', # TODO: add this back in
            r'\\\\',
            # TODO: \leq is recognized as \le q
        ]),
    ),
    'format': OrderedDict(
        CMD_MATHBF=r'\\mathbf',
        CMD_MATHBB=r'\\mathbb',
        CMD_MATHIT=r'\\mathit',
        CMD_BM=r'\\bm',
        CMD_MATHCAL=r'\\mathcal',
        CMD_HAT=r'\\hat',
        CMD_TILDE=r'\\tilde',
        CMD_MATHRM=r'\\mathrm',
    ),
    'format_text': OrderedDict(
        CMD_TEXT=r'\\text',
        CMD_LABEL=r'\\label',
        OPERATOR_NAME=r'\\operatorname',
    ),
})


tokens = [
    'CARET', 'UNDERSCORE', 'PRIME',
    'L_BRACE', 'R_BRACE',
    'L_BRACE_TEXT', 'R_BRACE_TEXT',
    'CMD_SQRT',
    'TEXT',
    'L_PAREN', 'R_PAREN', 'L_BRACKET', 'R_BRACKET',
    'FRAC',
    'CMD_BEGIN', 'CMD_END',
    'OPERATOR_NAME'
]
for key in lexer_config:
    tokens.extend(list(lexer_config[key].keys()))
tokens = list(set(tokens))

states = (
    ('textmode', 'exclusive'),
)

t_ignore = ' \t\r\n'

t_CARET = r'\^'
t_UNDERSCORE = r'_'
t_PRIME = r'\''
t_R_BRACE = r'\}'
t_FRAC = r'\\frac'
t_CMD_SQRT = r'\\sqrt'
t_textmode_ignore = ''
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACE_TEXT = r'\\{'
t_R_BRACE_TEXT = r'\\}'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'

def t_OPERATOR_NAME(t):
    r'\\operatorname'
    t.lexer.expect_text_brace = True
    return t

def t_CMD_TEXT(t):
    r'\\text'
    t.lexer.expect_text_brace = True
    return t


def t_CMD_LABEL(t):
    r'\\label'
    t.lexer.expect_text_brace = True
    return t

def t_CMD_BEGIN(t):
    r'\\begin'
    t.lexer.expect_text_brace = True
    return t

def t_CMD_END(t):
    r'\\end'
    t.lexer.expect_text_brace = True
    return t

# Line break in LaTeX (used in align environments)
# This must be defined after all other \\ commands to avoid conflicts
# PLY will match the longest pattern, so \\text will match \\text, not \\ + text
# def t_LINEBREAK(t):
#     r'\\\\'
#     return t

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

for key in lexer_config:
    for symbol, regex in lexer_config[key].items():
        if f"t_{symbol}" not in globals():
            globals()[f"t_{symbol}"] = regex


def t_error(t):
    raise MathValueError(f"Illegal character '{t.value[0]}'", t)


def t_textmode_error(t):
    raise MathValueError(f"Illegal character '{t.value[0]}' in text mode", t)
