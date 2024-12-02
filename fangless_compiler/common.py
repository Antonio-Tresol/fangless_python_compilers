from random import choice
from ply.lex import LexToken
import colors
import error_messages


# ===== COMPILER FLAGS ==================
VERBOSE_INDENTATION = False
VERBOSE_LEXER = False
VERBOSE_PARSER = False
VERBOSE_AST = False
VERBOSE_TESTER = False
VERBOSE_COMPILER = True
RAINBOW_ERRORS = False
SENSITIVE_PROGRAMMER = False


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


def color_green(msg: str) -> str:
    return f"{colors.GREEN}{msg}{colors.RESET}"


def color_yellow(msg: str) -> str:
    return f"{colors.YELLOW}{msg}{colors.RESET}"


def print_step(step: str) -> None:
    print(f"\n{colors.CYAN}=====================================")
    print(f"\t{step}...")
    print(f"====================================={colors.RESET}\n")


def print_error(error: str) -> None:
    print(f"\n{colors.RED}-------------- ERROR ----------------")
    print(f"{error}{colors.RESET}\n")


def print_catastrophic_error(error: str, details : str) -> None:
    print(f"\n{colors.RED}==================================================================================================")
    remark = (
        color_msg("horseshit")
        if not SENSITIVE_PROGRAMMER else 
        f"{colors.RED}not working{colors.RESET}"
    )
    print(f"Your program is {colors.RESET}{remark}{colors.RED}, here is why:\n")
    print(color_msg(f"Error:\t\t{error}\nDetails:\t{details}", RAINBOW_ERRORS))
    if not SENSITIVE_PROGRAMMER:
        print(color_msg(be_artistic()))
    print(f"{colors.RED}=================================================================================================={colors.RESET}\n")


def add_remark() -> str:
    if SENSITIVE_PROGRAMMER:
        return ""
    return (
        f"\nMore details:\t{choice(error_messages.connectors_tuple)} "
        f"you {choice(error_messages.informative_remarks)}!"
    )


def add_name() -> str:
    if SENSITIVE_PROGRAMMER:
        return ""
    return choice(error_messages.names_tuple)


def be_artistic() -> str:
    return choice(error_messages.masterpiece_tuple)


# ========COMPILER CONSTANTS==============
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
        "COMMENT",
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

BUILTIN_METHODS = {
    # List methods
    'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 
    'pop', 'remove', 'reverse', 'sort', 

    # Tuple methods
    'count', 'index', 

    # Set methods
    'add', 'clear', 'copy', 'difference', 'discard', 'intersection', 
    'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 
    'union', 'update',

    # String methods
    'capitalize', 'casefold', 'center', 'encode', 'expandtabs', 'find', 'format', 
    'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 
    'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 
    'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 
    'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 
    'strip', 'swapcase', 'title', 'upper', 'zfill',

    # Dictionary methods
    'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 
    'setdefault', 'update', 'values',

    # Boolean methods (since bool is a subclass of int, it shares many methods with int)
    'real', 'imag', 'conjugate',
 
    # Integer methods
    'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real',

    # Float methods
    'as_integer_ratio', 'conjugate', 'imag', 'is_integer', 'real'
}


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

CPP_RESERVED_W = {
    "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool",
    "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t", "class",
    "compl", "concept", "const", "consteval", "constexpr", "constinit", "const_cast",
    "continue", "co_await", "co_return", "co_yield", "decltype", "default", "delete",
    "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern",
    "false", "float", "for", "friend", "goto", "if", "inline", "int", "long",
    "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator"
    , "or", "or_eq", "private", "protected", "public", "register",
    "reinterpret_cast", "requires", "return", "short", "signed", "sizeof", "static",
    "static_assert", "static_cast", "struct", "switch", "template", "this",
    "thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union",
    "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while",
    "xor", "xor_eq",
}
