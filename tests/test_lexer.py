# test_lexer.py
import sys
import pytest
from pathlib import Path

# Add the fangless_compiler directory to the system path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "fangless_compiler"))

from lexer import FanglessLexer
import ply
# Test cases for the lexer

# Basic Literals
literals_cases = [
    ("123", "INTEGER_NUMBER", 123.0),
    ("123.456", "FLOATING_NUMBER", 123.456),
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
    ("*", "STAR"),
    ("/", "SLASH"),
    ("%", "MOD"),
]

# Comparison Operators
comparison_operators_cases = [
    ("=", "EQUAL"),
    ("<", "LESS_THAN"),
    (">", "GREATER_THAN"),
]

# Punctuation
punctuation_cases = [
    (".", "DOT"),
    (":", "COLON"),
    (",", "COMMA"),
]

# Others
others_cases = [
    ("=", "EQUAL"),
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
def lexer() -> FanglessLexer:
    lexer = FanglessLexer()
    lexer.build()
    return lexer


# Test functions for each case


def test_literals(lexer: FanglessLexer) -> None:
    for case in literals_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]
        assert token.value == case[2]


def test_reserved_words(lexer: FanglessLexer) -> None:
    for case in reserved_words_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_arithmetic_operators(lexer: FanglessLexer) -> None:
    for case in arithmetic_operators_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_comparison_operators(lexer: FanglessLexer) -> None:
    for case in comparison_operators_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_punctuation(lexer: FanglessLexer) -> None:
    for case in punctuation_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_others(lexer: FanglessLexer) -> None:
    for case in others_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_newline(lexer: FanglessLexer) -> None:
    for case in newline_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_parentheses(lexer: FanglessLexer) -> None:
    for case in parentheses_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token.type == case[1]


def test_comments(lexer: FanglessLexer) -> None:
    for case in comments_cases:
        lexer.lexer.input(case[0])
        token = lexer.lexer.token()
        assert token is None


# Test complex cases

def test_complex_case(lexer: FanglessLexer) -> None:
    code = "def my_function(arg1, arg2):\n  if arg1 > arg2: \n    return arg1 \n  else:\n    return arg2\nmy_function(10, 5)"  # noqa: E501
    lexer.lex_stream(code)
    tokens = lexer.token_stream
    index = 0
    # Check for expected tokens
    assert tokens[index].type == "START_TOKEN"
    index += 1
    assert tokens[index].type == "DEF"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "L_PARENTHESIS"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "COMMA"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "R_PARENTHESIS"
    index += 1
    assert tokens[index].type == "COLON"
    index += 1
    assert tokens[index].type == "NEWLINE"
    index += 1
    assert tokens[index].type == "INDENT"
    index += 1
    assert tokens[index].type == "IF"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "GREATER_THAN"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "COLON"
    index += 1
    assert tokens[index].type == "NEWLINE"
    index += 1
    assert tokens[index].type == "INDENT"
    index += 1
    assert tokens[index].type == "RETURN"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "DEDENT"
    index += 1
    assert tokens[index].type == "NEWLINE"
    index += 1
    assert tokens[index].type == "ELSE"
    index += 1
    assert tokens[index].type == "COLON"
    index += 1
    assert tokens[index].type == "NEWLINE"
    index += 1
    assert tokens[index].type == "INDENT"
    index += 1
    assert tokens[index].type == "RETURN"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "DEDENT"
    index += 1
    assert tokens[index].type == "DEDENT"
    index += 1
    assert tokens[index].type == "NEWLINE"
    index += 1
    assert tokens[index].type == "NAME"
    index += 1
    assert tokens[index].type == "L_PARENTHESIS"
    index += 1
    assert tokens[index].type == "INTEGER_NUMBER"
    index += 1
    assert tokens[index].type == "COMMA"
    index += 1
    assert tokens[index].type == "INTEGER_NUMBER"
    index += 1
    assert tokens[index].type == "R_PARENTHESIS"
    index += 1
    assert tokens[index].type == "END_TOKEN"
