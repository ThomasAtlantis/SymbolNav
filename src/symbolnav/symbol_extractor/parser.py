from .mast import ASTNode
from .exceptions import MathSyntaxError


def wrap(content_type):
    def wrap_inner(func):
        format_name = func.__name__.replace('p_', '')
        from .lexer import lexer_config
        _format_rules = []
        for cmd in lexer_config[format_name].keys():
            _format_rules.append(f'| {cmd} L_BRACE {content_type} R_BRACE')
            _format_rules.append(f'| {cmd} symbol')
        _format_doc = f'{format_name} ' + '\n'.join(_format_rules).replace('|', ':', 1)
        func.__doc__ = _format_doc
        return func
    return wrap_inner

def expand(item, next_group):
    if isinstance(next_group, tuple):
        return tuple((item, *next_group))
    elif next_group is not None:
        return tuple((item, next_group))
    else:
        return item

def p_math(p):
    """math : group"""
    p[0] = p[1]


def p_group_item(p):
    """group : item group"""
    p[0] = expand(item=p[1], next_group=p[2])

def p_group_empty(p):
    """group : empty"""
    p[0] = p[1]

def p_item_frac(p):
    """item : FRAC L_BRACE group R_BRACE L_BRACE group R_BRACE"""
    p[0] = ASTNode('Fraction', numerator=p[3], denominator=p[6])

def p_item_empty(p):
    """item : empty"""
    p[0] = p[1]

def p_item_symbol_postfix(p):
    """item : format postfix
            | format_text postfix
            | symbol postfix"""
    if not p[2]:
        p[0] = p[1]
    else:
        p[0] = ASTNode('SymbolPostfix', symbol=p[1], postfix=p[2])

def p_item_general_postfix(p):
    """item : format_op postfix
            | coated postfix"""
    if not p[2]:
        p[0] = p[1]
    else:
        p[0] = ASTNode('GeneralPostfix', content=p[1], postfix=p[2])

def p_format_op(p):
    """format_op : CMD_SQRT symbol
                 | CMD_SQRT L_BRACE group R_BRACE"""
    content = p[3] if len(p) == 5 else p[2]
    p[0] = ASTNode('FormatOp', op=p[1], content=content)

def p_coated(p):
    """coated : L_PAREN group R_PAREN
              | L_BRACE_TEXT group R_BRACE_TEXT
              | L_BRACE group R_BRACE
              | L_BRACKET group R_BRACKET"""
    p[0] = ASTNode('Coated', coat_left=p[1], content=p[2], coat_right=p[3])

def p_coated_env(p):
    """coated : CMD_BEGIN L_BRACE TEXT R_BRACE group CMD_END L_BRACE TEXT R_BRACE"""
    coat_left, content, coat_right = ''.join(p[1:5]), p[5], ''.join(p[6:10])
    p[0] = ASTNode('Coated', coat_left=coat_left, content=content, coat_right=coat_right)

def p_symbol_number(p):
    """symbol : NUMBER_SYMBOL"""
    p[0] = ASTNode('Symbol', symbol=p[1], symbol_type='number')

def p_symbol_letter(p):
    """symbol : LETTER_SYMBOL"""
    p[0] = ASTNode('Symbol', symbol=p[1], symbol_type='letter')

def p_symbol_greek(p):
    """symbol : GREEK_SYMBOL"""
    p[0] = ASTNode('Symbol', symbol=p[1], symbol_type='greek')

def p_symbol_other(p):
    """symbol : OTHER_SYMBOL"""
    p[0] = ASTNode('Symbol', symbol=p[1], symbol_type='other')

def p_postfix_empty(p):
    """postfix : empty"""
    p[0] = p[1]

def p_postfix_1(p):
    """postfix : supscript
               | subscript"""
    p[0] = frozenset((p[1],))

def p_postfix_2(p):
    """postfix : supscript subscript
               | subscript supscript"""
    p[0] = frozenset((p[1], p[2]))

def p_supscript(p):
    """supscript : CARET L_BRACE group R_BRACE
                 | CARET format
                 | CARET format_text
                 | CARET symbol
                 | PRIME"""
    p[0] = ASTNode('Supscript', value=p[{2: 1, 5: 3, 3: 2}[len(p)]])


def p_subscript(p):
    """subscript : UNDERSCORE L_BRACE group R_BRACE
                 | UNDERSCORE format
                 | UNDERSCORE format_text
                 | UNDERSCORE symbol"""
    p[0] = ASTNode('Subscript', value=p[{5: 3, 3: 2}[len(p)]])


@wrap('group')
def p_format(p):
    content = p[2] if len(p) == 3 else p[3]
    p[0] = ASTNode('Format', format=p[1], content=content)


@wrap('text')
def p_format_text(p):
    content = p[2] if len(p) == 3 else p[3]
    p[0] = ASTNode('FormatText', format=p[1], content=content)


def p_text(p):
    """text : symbol
            | TEXT
            | empty"""
    p[0] = p[1]


def p_empty(p):
    """empty :"""
    p[0] = None

def p_error(p):
    if p:
        error_msg, note = f"error when parsing {p.type}", None
        if p.type == 'CMD_END':
            note = "This error at \\end{} is often caused by unmatched brackets/parentheses earlier in the expression. Please check for missing closing brackets ')' or '}' before this point.)"
        raise MathSyntaxError(error_msg, p, note=note)
    else:
        raise SyntaxError("error at EOF (possibly due to unmatched brackets/parentheses)")
