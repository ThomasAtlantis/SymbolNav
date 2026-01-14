from typing import Any
from mast import ASTNode
from exceptions import MathSyntaxError


def pass_on(p):
    if len(p) == 2:
        p[0] = p[1]
        return True
    return False

def p_math(p):
    """math : content"""
    pass_on(p)

def p_content(p):
    """content : relation"""
    pass_on(p)

def p_relation(p):
    """relation : relation EQUAL relation
                | relation LT relation
                | relation LTE relation
                | relation GT relation
                | relation GTE relation
                | relation CMD_IN relation
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
                      | SYMBOL postfix"""
    p[0] = ASTNode('SymbolPostfix', symbol=p[1], postfix=p[2])

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
    """supscript : CARET L_BRACE content R_BRACE
                 | CARET format
                 | CARET SYMBOL"""
    value = p[3] if len(p) == 5 else p[2]
    p[0] = [ASTNode('Supscript', value=value)]

def p_subscript(p):
    """subscript : UNDERSCORE L_BRACE content R_BRACE
                 | UNDERSCORE format
                 | UNDERSCORE SYMBOL"""
    value = p[3] if len(p) == 5 else p[2]
    p[0] = ASTNode('Subscript', value=value)

def p_format(p):
    """format : CMD_MATHBF L_BRACE content R_BRACE
              | CMD_MATHBF SYMBOL
              | CMD_TEXT L_BRACE text R_BRACE
              | CMD_TEXT SYMBOL
              | CMD_MATHBB L_BRACE content R_BRACE
              | CMD_MATHBB SYMBOL
              | CMD_MATHIT L_BRACE content R_BRACE
              | CMD_MATHIT SYMBOL"""
    if not pass_on(p):    
        content = p[2] if len(p) == 3 else p[3]
        p[0] = ASTNode('Format', format=p[1], content=content)

def p_text(p):
    """text : SYMBOL
            | TEXT"""
    pass_on(p)

def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if p:
        raise MathSyntaxError(f"Syntax error when parsing {p.type}", p)
    else:
        raise SyntaxError("Syntax error at EOF")