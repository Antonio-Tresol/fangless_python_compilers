# Copyright 2024, ode adapted from Garden Snake by A. Badilla Olivas, Joseph
# Valverde Kong and Kenneth Villalobos Solis

import errors
from indentation_manager import IndentationManager
from ply import lex

NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2


class FanglessPythonLexer:

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
        "as": "AS",
        "assert": "ASSERT",
        "del": "DEL",
        "is": "IS",
        "print": "PRINT",
    }

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
        "STAR",
        "SLASH",
        "DOUBLE_SLASH",
        "MOD",
        "PLUS_EQUAL",
        "MINUS_EQUAL",
        "STAR_EQUAL",
        "SLASH_EQUAL",
        "DOUBLE_SLASH_EQUAL",
        "MOD_EQUAL",
        "DOUBLE_STAR",
        "DOUBLE_STAR_EQUAL",
        ###
        # BITWISE
        "AMPERSAND",
        "BAR",
        "HAT",
        "TILDE",
        "LEFT_SHIFT",
        "RIGHT_SHIFT",
        "AMPERSAND_EQUAL",
        "BAR_EQUAL",
        "HAT_EQUAL",
        "LEFT_SHIFT_EQUAL",
        "RIGHT_SHIFT_EQUAL",

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
        "EQUAL_EQUAL",
        "NOTEQUAL",
        "LESS_THAN",
        "LESS_EQUAL",
        "GREATER_THAN",
        "GREATER_EQUAL",
        ###
        # Literals
        "FLOATING_NUMBER",
        "INTEGER_NUMBER",
        "BINARY_NUMBER",
        "OCTAL_NUMBER",
        "HEXADECIMAL_NUMBER",
        "STRING",
        "TRIPLE_STRING",
        "RAW_STRING",
        "UNICODE_STRING",
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
        "PASS",
        "WHITESPACE",
        "NEWLINE",
        "ENDMARKER",
    )

    precedence = (
        ("left", "EQUAL", "GREATER_THAN", "LESS_THAN"),
        ("left", "PLUS", "MINUS"),
        ("left", "MULT", "DIV"),
    )

    # ================================ Basic Rules =============================
    # Arithmetic
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_STAR = r"\*"
    t_SLASH = r"/"
    t_MOD = r"%"
    t_DOUBLE_SLASH = r"//"
    t_DOUBLE_STAR = r"\*\*"
    t_PLUS_EQUAL = r"\+="
    t_MINUS_EQUAL = r"-="
    t_STAR_EQUAL = r"\*="
    t_SLASH_EQUAL = r"/="
    t_DOUBLE_STAR_EQUAL = r"\*\*="
    t_DOUBLE_SLASH_EQUAL = r"//="
    t_MOD_EQUAL = r"%="
    # Comparison
    t_EQUAL = r"="
    t_EQUAL_EQUAL = r"=="
    t_NOTEQUAL = r"!="
    t_LESS_THAN = r"<"
    t_GREATER_THAN = r">"
    t_LESS_EQUAL = r"<="
    t_GREATER_EQUAL = r">="
    # Bitwise
    t_AMPERSAND = r"&"
    t_BAR = r"\|"
    t_HAT = r"\^"
    t_TILDE = r"~"
    t_LEFT_SHIFT = r"<<"
    t_RIGHT_SHIFT = r">>"
    t_AMPERSAND_EQUAL = r"&="
    t_BAR_EQUAL = r"\|="
    t_HAT_EQUAL = r"\^="
    t_LEFT_SHIFT_EQUAL = r"<<="
    t_RIGHT_SHIFT_EQUAL = r">>="
    # Punctuation
    t_DOT = r"\."
    t_COLON = r":"
    t_COMMA = r","
    t_SEMICOLON = r";"
    t_EXCLAMATION = r"!"
    # Others

    # ============================== Methods ==================================
    def __init__(self) -> None:
        self.parenthesis_count = 0
        self.bracket_count = 0
        self.curly_braces_count = 0
        # self.at_line_start = True
        self.curly_brace_count = 0

    def build(self, **kwargs: dict) -> None:
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self) -> None:
        for i, token in enumerate(self.tokens):
            print(f"Token {i}: {token}")

    def lex_stream(self, data: str) -> None:
        self.lexer.input(data)

        tokens = iter(self.lexer.token, None)

        tokens = IndentationManager.add_indentations(tokens, self.lexer)

        self.tokens = tokens

    def _new_token(self, token_type: str, line_number: int) -> lex.LexToken:
        token = lex.LexToken()
        token.type = token_type
        token.value = None
        token.lexer.lineno = line_number

        return token

    # ============================== literal Rules ============================
    def t_INTEGER_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""\d+"""
        token.value = int(token.value)

        return token

    def t_BINARY_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""0[bB][01]+"""
        token.value = int(token.value, 2)

        return token

    def t_OCTAL_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""0[oO][0-7]+"""
        token.value = int(token.value, 8)

        return token

    def t_HEXADECIMAL_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""0[xX][0-9a-fA-F]+"""
        token.value = int(token.value, 16)

        return token

    def t_FLOATING_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"""
        token.value = float(token.value)

        return token

    def t_comment(self, token: lex.LexToken) -> None:
        r"""([ ]*\043[^\n]*)|([ ]*\"\"\"[^\"]*\"\"\")|([ ]*\'\'\'[^\"]*\'\'\')"""  # noqa: E501
        token.lexer.lineno += 1
        token.lexer.skip(1)

    def t_TRIPLESTRING(self, token: lex.LexToken) -> lex.LexToken:
        r'"{3}([\s\S]*?"{3}) | \'{3}([\s\S]*?\'{3})'
        return token

    def t_RAWSTRING(self, token: lex.LexToken) -> lex.LexToken:
        r"""[rR](\"(\\.|[^\"\n]|(\\\n))*\") | [rR](\'(\\.|[^\'\n]|(\\\n))*\')"""
        return token

    def t_UNICODESTRING(self, token: lex.LexToken) -> lex.LexToken:
        r'[uU](\"(\\.|[^\"\n]|(\\\n))*\") | [uU](\'(\\.|[^\'\n]|(\\\n))*\')'
        return token

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

    def t_WHITESPACE(self, token: lex.LexToken) -> None | lex.LexToken:
        r""" [ \t\f]+ """
        value = token.value
        value = value.rsplit("\f", 1)[-1]
        pos = 0

        while True:
            pos = value.find("\t")
            if pos == -1:
                break
            n = 8 - (pos % 8)
            value = value[:pos] + " " * n + value[pos + 1:]
        token.value = value

        if (
            self.lexer.atLineStart
            and self.parenthesis_count == 0
            and self.bracket_count == 0
            and self.curly_braces_count == 0
        ):
            return token
        return None

    # ================================ Base Rules =============================

    def t_error(self, token: lex.LexToken) -> None:
        print("Skipping", repr(token.value[0]))
        token.lexer.skip(1)
        error = (
            f"{errors.TOKEN_NOT_FOUND}: {token.value[0]}, "
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
