from ply.lex import LexToken


class MathSyntaxError(Exception):

    def __init__(self, message: str, token: LexToken):
        self.message = message
        self.token = token
        self.cursor = " " * token.lexpos + "^"  # type: ignore
    
    def __str__(self):
        return f"{self.message} at position {self.token.lexpos}"  # type: ignore