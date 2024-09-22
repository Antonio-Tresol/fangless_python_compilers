# Copyright 2024, ode adapted from Garden Snake by A. Badilla Olivas, Joseph
# Valverde Kong and Kenneth Villalobos Solis

from compiler import common
from ply import lex


class FanglessPythonLexer:
    tokens = (
        ###
        # Functions
        "DEF",
        "NAME",
        "RETURN",
        ###
        # Conditionals
        "IF",
        "ELSE",
        "ELIF",
        # Logical
        "AND",
        "OR",
        "NOT",
        "TRUE",
        "FALSE",
        ###
        # Arithmetic
        "PLUS",
        "MINUS",
        "MULT",
        "DIV",
        "MOD",
        ###
        # Cycles
        "WHILE",
        "FOR",
        "CONTINUE",
        "BREAK",
        "IN",
        "RANGE",
        ###
        # Classes
        "CLASS",
        ###
        # Comparison
        "EQUAL",
        "LESS_THAN",
        "GREATER_THAN",
        ###
        # Literals
        "NUMBER",
        "STRING",
        ###
        # Indentation
        "INDENT",
        "DEDENT",
        ###
        # Punctuation
        "DOT",  # .
        "COLON",  # :
        "COMMA",  # ,
        "SEMICOLON",  # ;
        "EXCLAMATION",  # !
        ###
        # Parenthesis
        "L_PARENTHESIS",
        "R_PARENTHESIS",
        "L_BRACKET",
        "R_BRACKET",
        "L_CURLY_BRACE",
        "R_CURLY_BRACE",
        ###
        # Others
        "ASSIGN",
        "AT_SIGN",
        "PASS",
        "WHITESPACE",
        "NEWLINE",
        "ENDMARKER",
    )

    RESERVED = {
        # Functions
        "def": "DEF",
        "return": "RETURN",
        # Conditionals
        "if": "IF",
        "else": "ELSE",
        "elif": "ELIF",
        # Logical
        "and": "AND",
        "or": "OR",
        "not": "NOT",
        "True": "TRUE",
        "False": "FALSE",
        # Cycles
        "while": "WHILE",
        "for": "FOR",
        "continue": "CONTINUE",
        "break": "BREAK",
        "in": "IN",
        "range": "RANGE",
        # Classes
        "class": "CLASS",
        # Others
        "pass": "PASS",
    }

    precedence = (
        ("left", "EQUAL", "GREATER_THAN", "LESS_THAN"),
        ("left", "PLUS", "MINUS"),
        ("left", "MULT", "DIV"),
    )

    # ================================ Basic Rules =================================
    # Arithmetic
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_MULT = r"\*"
    t_DIV = r"/"
    t_MOD = r"%"

    # Comparison
    t_EQUAL = r"=="
    t_LESS_THAN = r"<"
    t_GREATER_THAN = r">"

    # Punctuation
    t_DOT = r"\."
    t_COLON = r":"
    t_COMMA = r","
    t_SEMICOLON = r";"
    t_EXCLAMATION = r"!"

    # Others
    t_ASSIGN = r"="
    t_AT_SIGN = r"@"

    # ============================== Methods ==================================
    def __init__(self) -> None:
        self.parenthesis_count = 0
        self.bracket_count = 0
        self.curly_braces_count = 0
        self.at_line_start = True
        self.curly_brace_count = 0

    def build(self, **kwargs: dict) -> None:
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data: str) -> None:
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def _new_token(self, token_type: str, line_number: int) -> lex.LexToken:
        token = lex.LexToken()
        token.type = token_type
        token.value = None
        token.lexer.lineno = line_number
        return token

    # ============================== literal Rules ============================
    def t_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?"""
        token.value = float(token.value)
        return token

    def t_comment(self, token: lex.LexToken) -> None:
        r"""([ ]*\043[^\n]*)|([ ]*\"\"\"[^\"]*\"\"\")|([ ]*\'\'\'[^\"]*\'\'\')"""
        token.lexer.lineno += 1
        token.lexer.skip(1)

    def t_STRING(self, token: lex.LexToken) -> lex.LexToken:
        r"""((\").*?(\"))|((\').*?(\'))"""
        token.value = str(token.value[1:-1])
        return token

    # ============================== Reserved Rules ===========================
    def t_NAME(self, token: lex.LexToken) -> lex.LexToken:
        r"""[a-zA-Z_][a-zA-Z0-9_]*"""
        token.type = self.RESERVED.get(token.value, "NAME")
        return token

    # ============================== Other Rules ==============================
    def t_WHITESPACE(self, token: lex.LexToken) -> None | lex.LexToken:
        r"""[ ]+"""
        if (
            self.at_line_start
            and self.parenthesis_count == 0
            and self.bracket_count == 0
            and self.curly_braces_count == 0
        ):
            return token
        return None

    # ============================== Prenthesis Rules =========================
    def t_L_PARENTHESIS(self, token: lex.LexToken) -> lex.LexToken:
        r"""\("""
        self.parenthesis_count += 1
        return token

    def t_R_PARENTHESIS(self, token: lex.LexToken) -> lex.LexToken:
        r"""\)"""
        # parser should check for underflow
        self.parenthesis_count -= 1
        return token

    def t_L_BRACKET(self, token: lex.LexToken) -> lex.LexToken:
        r"""\["""
        self.bracket_count += 0
        return token

    def t_R_BRACKET(self, token: lex.LexToken) -> lex.LexToken:
        r"""\]"""
        # parser should check for underflow
        self.bracket_count -= 1
        return token

    def t_L_CURLY_BRACE(self, token: lex.LexToken) -> lex.LexToken:
        r"""\{"""
        self.curly_brace_count += 1
        return token

    def t_R_CURLY_BRACE(self, token: lex.LexToken) -> lex.LexToken:
        r"""\}"""
        # parser should check for underflow
        self.curly_brace_count -= 1
        return token

    # ================================ Base Rules =============================
    def t_NEWLINE(self, token: lex.LexToken) -> None | lex.LexToken:
        r"""\n+"""
        token.lexer.lineno += len(token.value)
        token.type = "NEWLINE"
        if (
            self.parenthesis_count == 0
            and self.bracket_count == 0
            and self.curly_braces_count == 0
        ):
            return token
        return None

    def t_error(self, token: lex.LexToken) -> None:
        print("Skipping", repr(token.value[0]))
        token.lexer.skip(1)
        error = (
            f"{common.errors.TOKEN_NOT_FOUND}: {token.value[0]}, "
            f"at line number {token.lexer.lineno}"
        )
        raise SyntaxError(error)

    # ============================= Indentation rules =========================
    # Synthesize a DEDENT tag
    def DEDENT(self, line_number: int) -> lex.LexToken:
        return self._new_token("DEDENT", line_number)

    # Synthesize an INDENT tag
    def INDENT(self, line_number: int) -> lex.LexToken:
        return self._new_token("INDENT", line_number)
