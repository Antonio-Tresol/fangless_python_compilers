# Compiler constants

from ply.lex import LexToken


def new_token(
    new_type: str, line_number: int, column_number: int,
) -> LexToken:
    tok = LexToken()

    tok.type = new_type
    tok.value = None
    tok.lineno = line_number
    tok.lexpos = column_number

    return tok
