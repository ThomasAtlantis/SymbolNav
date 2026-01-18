from ply.lex import LexToken


class LaTeXError(Exception):

    def __init__(self, message: str, token: LexToken):
        self.message = message
        self.token = token
        self.cursor = " " * token.lexpos + "^"  # type: ignore
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message} at position {self.token.lexpos} in line {self.token.lineno}"  # type: ignore

class LaTeXValueError(LaTeXError):
    pass
