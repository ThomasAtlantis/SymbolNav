from ply.lex import LexToken


class MathError(Exception):

    def __init__(self, message: str, token: LexToken):
        self.message = message
        self.token = token
        self.cursor = " " * token.lexpos + "^"  # type: ignore
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message} at position {self.token.lexpos}"  # type: ignore

class MathValueError(MathError):
    pass

class MathSyntaxError(MathError):
    pass