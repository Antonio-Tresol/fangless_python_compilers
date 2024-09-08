# test_lexer.py
import pytest
from lexer import FanglessPythonLexer

# Test cases for the lexer

# Basic Literals
literals_cases = [
    ("123", "NUMBER", 123.0),
    ("123.456", "NUMBER", 123.456),
    ("1.23e+4", "NUMBER", 1.23e4),
    ("1.23e-4", "NUMBER", 1.23e-4),
    ('"Hello, World!"', "STRING", "Hello, World!"),
    ("'Hello, World!'", "STRING", "Hello, World!"),
]

# Reserved Words
reserved_words_cases = [
    ("def", "DEF"),
    ("return", "RETURN"),
    ("if", "IF"),
    ("else", "ELSE"),
    ("elif", "ELIF"),
    ("and", "AND"),
    ("or", "OR"),
    ("not", "NOT"),
    ("True", "TRUE"),
    ("False", "FALSE"),
    ("while", "WHILE"),
    ("for", "FOR"),
    ("continue", "CONTINUE"),
    ("break", "BREAK"),
    ("in", "IN"),
    ("range", "RANGE"),
    ("class", "CLASS"),
    ("pass", "PASS"),
]

# Arithmetic Operators
arithmetic_operators_cases = [
    ("+", "PLUS"),
    ("-", "MINUS"),
    ("*", "MULT"),
    ("/", "DIV"),
    ("%", "MOD"),
]

# Comparison Operators
comparison_operators_cases = [
    ("==", "EQUAL"),
    ("<", "LESS_THAN"),
    (">", "GREATER_THAN"),
]

# Punctuation
punctuation_cases = [
    (".", "DOT"),
    (":", "COLON"),
    (",", "COMMA"),
    (";", "SEMICOLON"),
    ("!", "EXCLAMATION"),
]

# Others
others_cases = [
    ("=", "ASSIGN"),
    ("@", "AT_SIGN"),
]

# Indentation
indentation_cases = [
    ("  ", "INDENT", 0),
    ("  \n  ", "INDENT", 1),
    ("   \n   ", "INDENT", 1),
    ("    \n  ", "DEDENT", 1),
    ("    \n    ", "DEDENT", 1),
    ("    \n   ", "DEDENT", 1),
    ("    \n      ", "DEDENT", 1),
]

# Newline
newline_cases = [
    ("\n", "NEWLINE"),
    ("\n\n", "NEWLINE"),
]

# Parentheses
parentheses_cases = [
    ("(", "L_PARENTHESIS"),
    (")", "R_PARENTHESIS"),
    ("[", "L_BRACKET"),
    ("]", "R_BRACKET"),
    ("{", "L_CURLY_BRACE"),
    ("}", "R_CURLY_BRACE"),
]

# Comments
comments_cases = [
    ("# This is a comment", None),
    ("# This is another comment\n", None),
    (
        '"""hello world 4793@\n#$%^& asdfad f &#^&&       \n 979bmario pikachu'
        ' \n \t are you here? for i am schizophrenic in range """',
        None,
    ),
    (
        "'''hello world 4793@\n#$%^& asdfad f &#^&&      \n 979bmario pikachu"
        " \n \t are you here? def i am schizophrenic return '''",
        None,
    ),
]


@pytest.fixture
def lexer() -> FanglessPythonLexer:
    lexer = FanglessPythonLexer()
    lexer.build()
    return lexer


# Test functions for each case


def test_literals(lexer: FanglessPythonLexer) -> None:
    for case in literals_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]
        assert token.value == case[2]


def test_reserved_words(lexer: FanglessPythonLexer) -> None:
    for case in reserved_words_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_arithmetic_operators(lexer: FanglessPythonLexer) -> None:
    for case in arithmetic_operators_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_comparison_operators(lexer: FanglessPythonLexer) -> None:
    for case in comparison_operators_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_punctuation(lexer: FanglessPythonLexer) -> None:
    for case in punctuation_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_others(lexer: FanglessPythonLexer) -> None:
    for case in others_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_newline(lexer: FanglessPythonLexer) -> None:
    for case in newline_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_parentheses(lexer: FanglessPythonLexer) -> None:
    for case in parentheses_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_comments(lexer: FanglessPythonLexer) -> None:
    for case in comments_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token is None


# Test complex cases


def test_complex_case(lexer: FanglessPythonLexer) -> None:
    code = """
        def my_function(arg1, arg2):
            if arg1 > arg2:
                return arg1
            else:
                return arg2

        my_function(10, 5)
    """
    lexer.lexer.input(code)
    tokens = []
    while True:
        token = lexer.lexer.token()
        if not token:
            break
        tokens.append(token)

    # Check for expected tokens
    assert tokens[0].type == "NEWLINE"
    assert tokens[1].type == "WHITESPACE"
    assert tokens[2].type == "DEF"
    assert tokens[3].type == "WHITESPACE"
    assert tokens[4].type == "NAME"
    assert tokens[5].type == "L_PARENTHESIS"
    assert tokens[6].type == "NAME"
    assert tokens[7].type == "COMMA"
    assert tokens[8].type == "NAME"
    assert tokens[9].type == "R_PARENTHESIS"
    assert tokens[10].type == "COLON"
    assert tokens[11].type == "NEWLINE"
    assert tokens[12].type == "WHITESPACE"
    assert tokens[13].type == "IF"
    assert tokens[14].type == "WHITESPACE"
    assert tokens[15].type == "NAME"
    assert tokens[16].type == "WHITESPACE"
    assert tokens[17].type == "GREATER_THAN"
    assert tokens[18].type == "WHITESPACE"
    assert tokens[19].type == "NAME"
    assert tokens[20].type == "COLON"
    assert tokens[21].type == "NEWLINE"
    assert tokens[22].type == "WHITESPACE"
    assert tokens[23].type == "RETURN"
    assert tokens[24].type == "WHITESPACE"
    assert tokens[25].type == "NAME"
    assert tokens[26].type == "NEWLINE"
    assert tokens[27].type == "WHITESPACE"
    assert tokens[28].type == "ELSE"
    assert tokens[29].type == "COLON"
    assert tokens[30].type == "NEWLINE"
    assert tokens[31].type == "WHITESPACE"
    assert tokens[32].type == "RETURN"
    assert tokens[33].type == "WHITESPACE"
    assert tokens[34].type == "NAME"
    assert tokens[35].type == "NEWLINE"
    assert tokens[36].type == "WHITESPACE"
    assert tokens[37].type == "NAME"
    assert tokens[38].type == "L_PARENTHESIS"
    assert tokens[39].type == "NUMBER"
    assert tokens[40].type == "COMMA"
    assert tokens[41].type == "NUMBER"
    assert tokens[42].type == "R_PARENTHESIS"
    assert tokens[43].type == "NEWLINE"
