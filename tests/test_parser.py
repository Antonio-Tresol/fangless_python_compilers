# test_parser.py
from pathlib import Path
from utils import add_package_from_parent_to_context

add_package_from_parent_to_context("fangless_compiler")

from parser import FanglessParser
from lexer import FanglessLexer
from exceptions import ParserError, IndentationMismatchError, LexerError
import sys
from common import color_yellow
from compiler_settings import VERBOSE_TESTER

positive_path = Path("tests/positive/")
positive_tests = [
    positive_path.joinpath(Path(file.name)) for file in positive_path.glob("*.py")
]

negative_path = Path("tests/negative/")
negative_tests = [
    negative_path.joinpath(Path(file.name)) for file in negative_path.glob("*.py")
]

ast_path = Path("tests/ast/")
ast_tests = [
    ast_path.joinpath(Path(file.name)) for file in ast_path.glob("*.py")
]

compile_path = Path("tests/compile/")
compile_tests = [
    compile_path.joinpath(Path(file.name)) for file in compile_path.glob("*.py")
]


def print_error_header(test_name: str, header: str) -> None:
    """Print formatted error header with separators."""
    separator = "=" * 80
    print(f"\n{separator}")
    print(f"TEST FAILURE: {header}")
    print(f"File: {test_name}")
    print(separator)


def test_negative_cases() -> None:
    for test in negative_tests:
        test_specific_negative_case(test)


def test_specific_negative_case(path: Path) -> None:
    with path.open("r") as source:
        content = source.read()
        try:
            negative_parser = FanglessParser()
            negative_parser.parse(content)
            if not ("fake" in path.name) or VERBOSE_TESTER:
                print(f"❌ Expected error not raised for {path.name}")
        except (ParserError, IndentationMismatchError, LexerError) as e:
            if VERBOSE_TESTER:
                print(f"✅ Tests passed: {path.name}")


def test_specific_positive_case(path: Path, title: str) -> None:
    with path.open("r") as source:
        content = source.read()
        try:
            positive_parse = FanglessParser()
            positive_parse.parse(content)
            if VERBOSE_TESTER:
                print(f"✅ Tests passed: {path.name}")
        except (ParserError, IndentationMismatchError, LexerError) as e:
            if "fake" not in path.name or VERBOSE_TESTER:
                error_header = color_yellow("Error Summary")
                print(f"❌ Unexpected error raised for {path.name}")
                print(f"\n    {error_header}:\n      -{e}")
                print("")


def test_positives(cases: list, test_title: str) -> None:
    for test in cases:
        test_specific_positive_case(test, test_title)


def main() -> None:
    option = "positive"
    if len(sys.argv) == 2:
        option = sys.argv[1]
    print("\n🧪 Running tests for the parser")
    match option:
        case "positive":
            test_positives(positive_tests, "Positive")
        case "negative":
            test_negative_cases()
        case "ast":
            test_positives(ast_tests, "AST")
        case "compile":
            test_positives(compile_tests, "Compile")
        case _:
            print("Invalid option")


if __name__ == "__main__":
    main()
