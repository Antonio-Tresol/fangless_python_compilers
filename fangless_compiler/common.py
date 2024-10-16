from random import choice
from ply.lex import LexToken
import colors
import error_messages

def new_token(
    new_type: str, line_number: int, column_number: int,
) -> LexToken:
    tok = LexToken()

    tok.type = new_type
    tok.value = None
    tok.lineno = line_number
    tok.lexpos = column_number

    return tok


def fill_symbol_table_with_builtin_functions(symbol_table: dict) -> None:
    for func in BUILTIN_FUNCTIONS:
        symbol_table[func] = FUNCTION


def color_msg(msg: str, rainbow: bool = True) -> str:
    new_msg = ""
    if rainbow:
        for letter in msg: 
            color_code = choice(colors.COLORS)
            new_msg += f"{color_code}{letter}{colors.RESET}"
    else:
        color_code = choice(colors.COLORS)
        new_msg = f"{color_code}{msg}{colors.RESET}"

    return new_msg


def add_remark() -> str:
    if SENSITIVE_PROGRAMMER:
        return ""
    return f"\n{choice(error_messages.connectors_tuple)} you {choice(error_messages.informative_remarks)}!"


def be_artistic() -> str:
    return choice(error_messages.masterpiece_tuple)


# ===== COMPILER CONSTANTS ==============

# ===== COMPILER FLAGS ==================
VERBOSE_INDENTATION = False
VERBOSE_LEXER = True
VERBOSE_PARSER = True
RAINBOW_ERRORS = False
SENSITIVE_PROGRAMMER = True

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
        "ARROW",
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
        # Classes
        "class": "CLASS",
        # Others
        "pass": "PASS",
        "as": "AS",
        "assert": "ASSERT",
        "del": "DEL",
        "is": "IS",
        "None": "NONE",
    }

TYPES = {
    "union",
    "int",
    "float",
    "list",
    "set",
    "tuple",
    "dict",
    "str",
    "bool",
    "None",
}

CONTAINER_TYPES = {
    "union",
    "list",
    "set",
    "tuple",
    "dict",
}

SCOPE_OPENED = "OPENED"

CLASS = 3
FUNCTION = 2
VARIABLE = 1

BUILTIN_FUNCTIONS = (
    "abs",
    "all",
    "any",
    "ascii",
    "bin",
    "bool",
    "breakpoint",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "classmethod",
    "compile",
    "complex",
    "delattr",
    "dict",
    "dir",
    "divmod",
    "enumerate",
    "eval",
    "exec",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "help",
    "hex",
    "id",
    "input",
    "int",
    "isinstance",
    "issubclass",
    "iter",
    "len",
    "list",
    "locals",
    "map",
    "max",
    "memoryview",
    "min",
    "next",
    "object",
    "oct",
    "open",
    "ord",
    "pow",
    "print",
    "property",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "setattr",
    "slice",
    "sorted",
    "staticmethod",
    "str",
    "sum",
    "super",
    "tuple",
    "type",
    "vars",
    "zip",
)
