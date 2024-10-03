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


VERBOSE_INDENTATION = False
VERBOSE_LEXER = True
VERBOSE_PARSER = True

# ========TOKENS AND RESERVED WORDS=======
TOKENS = (
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
        "NOT_EQUAL",
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
        "IS",
        "PRINT",
        "WHITESPACE",
        "NEWLINE",
        "NONE",
        "START_TOKEN",
        "END_TOKEN",
    )

RESERVED_WORDS = {
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
        "len": "LEN",
        "None": "NONE",
    }
