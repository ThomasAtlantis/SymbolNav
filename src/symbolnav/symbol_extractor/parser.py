from symbolnav.symbol_extractor.mast import ASTNode
from symbolnav.symbol_extractor.exceptions import MathSyntaxError


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
    """content : list"""
    pass_on(p)


def p_list(p):
    """list : relation COMMA list
            | relation PERIOD list
            | relation LINEBREAK list
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
                | relation LE relation
                | relation LTE relation
                | relation GT relation
                | relation GTE relation
                | relation CMD_IN relation
                | relation CMD_NOTIN relation
                | relation CMD_CIRC relation
                | relation CMD_TO relation
                | relation SETMINUS relation
                | relation SUBSET relation
                | relation LEFTARROW relation
                | relation RIGHTARROW relation
                | relation LEFTARROW_DOUBLE relation
                | relation RIGHTARROW_DOUBLE relation
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
          | mp CUP mp
          | mp SIM mp
          | FRAC L_BRACE multi_content R_BRACE L_BRACE multi_content R_BRACE
          | mp CMD_LABEL L_BRACE TEXT R_BRACE
          | unary"""
    if not pass_on(p):
        if len(p) == 8:
            p[0] = ASTNode('Fraction', numerator=p[3], denominator=p[6])
        elif len(p) == 6:
            if (hasattr(p[2], 'type') and p[2].type == 'CMD_LABEL') or p[2] == '\\label':
                label_content = p[4] if p[4] is not None else ''
                p[0] = ASTNode('Labeled', content=p[1], label=ASTNode('Label', content=label_content))
        else:
            p[0] = ASTNode('MP', op=p[2], left=p[1], right=p[3])


def p_unary(p):
    """unary : ADD unary
             | SUB unary
             | symbol_postfix
             | empty"""
    if not pass_on(p):
        p[0] = ASTNode('Unary', op=p[1], symbol=p[2])

def p_unary_general_postfix(p):
    """unary : format_op postfix
             | coated postfix"""
    p[0] = ASTNode('GeneralPostfix', content=p[1], postfix=p[2])

def p_format_op(p):
    """format_op : CMD_SQRT symbol
                 | CMD_SQRT L_BRACE multi_content R_BRACE"""
    content = p[3] if len(p) == 5 else p[2]
    p[0] = ASTNode('FormatOp', op=p[1], content=content)

def p_symbol_postfix(p):
    """symbol_postfix : format postfix
                      | symbol postfix"""
    p[0] = ASTNode('SymbolPostfix', symbol=p[1], postfix=p[2])

def p_coated(p):
    """coated : L_PAREN multi_content R_PAREN
              | L_BRACE_TEXT multi_content R_BRACE_TEXT
              | L_BRACE multi_content R_BRACE
              | L_BRACKET multi_content R_BRACKET
              | CMD_BEGIN L_BRACE TEXT R_BRACE multi_content CMD_END L_BRACE TEXT R_BRACE"""
    if len(p) == 10:
        coat_left, content, coat_right = ''.join(p[1:5]), p[5], ''.join(p[6:10])
        p[0] = ASTNode('Coated', coat_left=coat_left, content=content, coat_right=coat_right)
    else:
        p[0] = ASTNode('Coated', coat_left=p[1], content=p[2], coat_right=p[3])

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
                 | PRIME
                 | CARET CMD_PRIME
                 | CARET MUL"""
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
            | TEXT
            | empty"""
    pass_on(p)


def p_empty(p):
    """empty :"""
    p[0] = None


# Global reference to current lexer (set by interpreter)
# _current_lexer = None

def p_error(p):
    if p:
        # Check if this is an END token in a begin/end environment
        # This often indicates a bracket/parenthesis mismatch earlier
        error_msg = f"Syntax error when parsing {p.type}"
        if p.type == 'CMD_END':
            error_msg += " (Note: This error at \\end{} is often caused by unmatched brackets/parentheses earlier in the expression. Please check for missing closing brackets ')' or '}' before this point.)"
        raise MathSyntaxError(error_msg, p)
    else:
        # EOF error - this often happens when brackets/parentheses are not closed
        raise SyntaxError("Syntax error at EOF (possibly due to unmatched brackets/parentheses)")
