# Copyright 2024, ode adapted from Garden Snake by A. Badilla Olivas, Joseph
# Valverde Kong and Kenneth Villalobos Solis

import colors
from indentation_manager import FanglessIndentationManager
from collections.abc import Iterable
from ply import lex
from common import new_token, TOKENS, RESERVED_WORDS, VERBOSE_LEXER
from exceptions import LexerError

class FanglessLexer:
    # tokens and reserve words definition
    RESERVED = RESERVED_WORDS
    tokens = TOKENS
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
    t_NOT_EQUAL = r"!="
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
    t_ARROW = r"->"
    # Others

    # ============================== Methods ==================================
    def __init__(self) -> None:
        self.parenthesis_count = 0
        self.bracket_count = 0
        self.curly_braces_count = 0
        self.curly_brace_count = 0
        self.token_stream = None

    def build(self, **kwargs: dict) -> None:
        self.lexer = lex.lex(module=self, **kwargs)

    def print_token_stream(self) -> None:
        print("FANGLESS: LEXER DEBUG START")
        for i, token in enumerate(self.token_stream):
            print(f"Token {i}: {token}")
        print("FANGLESS: LEXER DEBUG END")

    def lex_stream(self, data: str) -> None:
        self.lexer.input(data)

        lex_tokens = iter(self.lexer.token, None)
        lex_tokens = FanglessIndentationManager.add_indentations(
            lex_tokens,
            self.lexer,
        )

        lex_tokens = self.remove_redundant_newlines(lex_tokens)

        line_number = 1
        if len(lex_tokens) != 0:
            line_number = lex_tokens[-1].lineno
        lex_tokens.append(new_token("END_TOKEN", line_number, 0))
        lex_tokens.insert(0, new_token("START_TOKEN", 1, 0))
        self.token_stream = lex_tokens
        if VERBOSE_LEXER:
            self.print_token_stream()

    def remove_redundant_newlines(self, tokens: Iterable) -> None:
        n = len(tokens)
        new_full_quality_tokens = []
        for pos, token in enumerate(tokens):
            if (
                token.type == "NEWLINE"
                and pos + 1 < n
                and tokens[pos + 1].type in {"ELIF", "ELSE"}
            ):
                continue

            new_full_quality_tokens.append(token)
        return new_full_quality_tokens

    def token(self) -> lex.LexToken | None:
        if self.token_stream and len(self.token_stream) > 0:
            return self.token_stream.pop(0)
        return None

    # ============================== literal Rules ============================
    def t_FLOATING_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""(\d+(_\d+)*\.(\d+(_\d+)*)*)|(\.\d+(_\d+)*)"""
        token.value = float(token.value)

        return token

    def t_BINARY_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""0[bB][01]+(_[01]+)*"""
        token.value = int(token.value, 2)

        return token

    def t_OCTAL_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""0[oO][0-7]+(_[0-7]+)*"""
        token.value = int(token.value, 8)

        return token

    def t_HEXADECIMAL_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*"""
        token.value = int(token.value, 16)

        return token

    def t_INTEGER_NUMBER(self, token: lex.LexToken) -> lex.LexToken:
        r"""\d+(_\d+)*"""
        token.value = int(token.value)

        return token

    def t_COMMENT(self, token: lex.LexToken) -> None:
        r"""([ ]*\043[^\n]*)"""
        token.lexer.lineno += 1

    def t_TRIPLESTRING(self, token: lex.LexToken) -> lex.LexToken:
        r'"{3}([\s\S]*?"{3}) | \'{3}([\s\S]*?\'{3})'
        return token

    def t_RAWSTRING(self, token: lex.LexToken) -> lex.LexToken:
        r"""[rR](\"(\\.|[^\"\n]|(\\\n))*\") | [rR](\'(\\.|[^\'\n]|(\\\n))*\')"""
        return token

    def t_UNICODESTRING(self, token: lex.LexToken) -> lex.LexToken:
        r"[uU](\"(\\.|[^\"\n]|(\\\n))*\") | [uU](\'(\\.|[^\'\n]|(\\\n))*\')"
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
        self.bracket_count += 1

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
            and self.curly_brace_count == 0
        ):
            return token
        return None

    def t_WHITESPACE(self, token: lex.LexToken) -> None | lex.LexToken:
        r"""[ \t\f]+"""
        value = token.value
        value = value.rsplit("\f", 1)[-1]
        pos = 0

        while True:
            pos = value.find("\t")
            if pos == -1:
                break
            n = 8 - (pos % 8)
            value = value[:pos] + " " * n + value[pos + 1 :]
        token.value = value

        if (
            self.lexer.atLineStart
            and self.parenthesis_count == 0
            and self.bracket_count == 0
            and self.curly_brace_count == 0
        ):
            return token
        return None

    # ================================ Base Rules =============================

    def t_error(self, token: lex.LexToken) -> None:
        print("Skipping", repr(token.value[0]))
        token.lexer.skip(1)
        error = (
            f"{colors.TOKEN_NOT_FOUND}: {token.value[0]}, "
            f"at line number {token.lexer.lineno}"
        )
        raise LexerError(error)
