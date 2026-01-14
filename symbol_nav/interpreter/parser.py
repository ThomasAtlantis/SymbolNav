from .lexer import t_BAR_TEXT, t_L_BRACE_TEXT, t_L_BRACKET, t_L_PAREN
from .mast import ASTNode
from .exceptions import MathSyntaxError


def pass_on(p):
    if len(p) == 2:
        p[0] = p[1]
        return True
    return False


def p_math(p):
    """math : multi_content"""
    pass_on(p)


def p_multi_content(p):
    """multi_content : content multi_content
                     | empty"""
    if not pass_on(p):
        if isinstance(p[2], list):
            p[0] = [p[1], *p[2]]
        elif p[2] is not None:
            p[0] = [p[1], p[2]]
        else:
            p[0] = p[1]


def p_content(p):
    """content : list
               | L_PAREN multi_content R_PAREN
               | L_BRACE_TEXT multi_content R_BRACE_TEXT
               | L_BRACKET multi_content R_BRACKET"""
    if not pass_on(p):
        p[0] = ASTNode('Bracket', bracket_left=p[1], content=p[2], bracket_right=p[3])


def p_list(p):
    """list : relation COMMA list
            | relation PERIOD list
            | relation"""
    if not pass_on(p):
        relations = [p[1]]
        if isinstance(p[3], list):
            relations.extend(p[3])
        elif p[3] is not None:
            relations.append(p[3])
        p[0] = ASTNode('List', items=relations, separator=p[2])


def p_relation(p):
    """relation : relation EQUAL relation
                | relation TRIANGLEQUAL relation
                | relation APPROX relation
                | relation LT relation
                | relation LTE relation
                | relation GT relation
                | relation GTE relation
                | relation CMD_IN relation
                | relation CMD_CIRC relation
                | relation CMD_TO relation
                | relation SETMINUS relation
                | relation SUBSET relation
                | relation BAR_TEXT relation
                | expr"""
    if not pass_on(p):
        p[0] = ASTNode('Relation', op=p[2], left=p[1], right=p[3])


def p_expr(p):
    """expr : additive"""
    pass_on(p)


def p_additive(p):
    """additive : additive ADD additive
                | additive SUB additive
                | mp"""
    if not pass_on(p):
        p[0] = ASTNode('Additive', op=p[2], left=p[1], right=p[3])


def p_mp(p):
    """mp : mp MUL mp
          | mp CMD_TIMES mp
          | mp DIV mp
          | mp CMD_DIV mp
          | mp CMD_CDOT mp
          | mp COLON mp
          | mp BAR mp
          | unary"""
    if not pass_on(p):
        p[0] = ASTNode('MP', op=p[2], left=p[1], right=p[3])


def p_unary(p):
    """unary : ADD unary
             | SUB unary
             | symbol_postfix"""
    if not pass_on(p):
        p[0] = ASTNode('Unary', op=p[1], symbol=p[2])


def p_symbol_postfix(p):
    """symbol_postfix : format postfix
                      | symbol postfix"""
    p[0] = ASTNode('SymbolPostfix', symbol=p[1], postfix=p[2])

def p_symbol(p):
    """symbol : NUMBER_SYMBOL
              | LETTER_SYMBOL
              | GREEK_SYMBOL
              | OTHER_SYMBOL
              | empty"""
    pass_on(p)

def p_postfix(p):
    """postfix : postfix_op
               | empty"""
    pass_on(p)


def p_postfix_op(p):
    """postfix_op : supscript
                  | subscript
                  | supscript subscript
                  | subscript supscript"""
    if not pass_on(p):
        p[0] = [p[1], p[2]]


def p_supscript(p):
    """supscript : CARET L_BRACE multi_content R_BRACE
                 | CARET format
                 | CARET symbol
                 | PRIME"""
    if not pass_on(p):
        value = p[3] if len(p) == 5 else p[2]
        p[0] = [ASTNode('Supscript', value=value)]


def p_subscript(p):
    """subscript : UNDERSCORE L_BRACE multi_content R_BRACE
                 | UNDERSCORE format
                 | UNDERSCORE symbol"""
    value = p[3] if len(p) == 5 else p[2]
    p[0] = ASTNode('Subscript', value=value)


# Define format commands and their content types
_FORMAT_CMDS = [
    ('CMD_MATHBF', 'multi_content'),
    ('CMD_MATHBB', 'multi_content'),
    ('CMD_MATHIT', 'multi_content'),
    ('CMD_BM', 'multi_content'),
    ('CMD_MATHCAL', 'multi_content'),
    ('CMD_TEXT', 'text'),  # CMD_TEXT uses 'text' instead of 'multi_content'
    ('CMD_HAT', 'multi_content'),
    ('CMD_TILDE', 'multi_content'),
    ('CMD_MATHRM', 'multi_content'),
    ('CMD_SQRT', 'multi_content'),
]

# Build format production rules dynamically
_format_rules = []
for cmd, content_type in _FORMAT_CMDS:
    _format_rules.append(f'{cmd} L_BRACE {content_type} R_BRACE')
    _format_rules.append(f'{cmd} symbol')
_format_doc = 'format : ' + _format_rules[0] + '\n' + '\n'.join('              | ' + rule for rule in _format_rules[1:])

def p_format(p):
    if not pass_on(p):
        content = p[2] if len(p) == 3 else p[3]
        p[0] = ASTNode('Format', format=p[1], content=content)

p_format.__doc__ = _format_doc


def p_text(p):
    """text : symbol
            | TEXT"""
    pass_on(p)


def p_empty(p):
    """empty :"""
    p[0] = None


def p_error(p):
    if p:
        raise MathSyntaxError(f"Syntax error when parsing {p.type}", p)
    else:
        raise SyntaxError("Syntax error at EOF")
