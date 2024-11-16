# test_parser.py
import pytest
from pathlib import Path
from utils import add_package_from_parent_to_context

add_package_from_parent_to_context("fangless_compiler")

from parser import FanglessParser
from lexer import FanglessLexer
import common
import ply

positive_path = Path("tests/positive/")
positive_tests = [
    positive_path.joinpath(Path(file.name)) for file in positive_path.glob("*.py")
]

negative_path = Path("test/negative/")
negative_tests = [
    negative_path.joinpath(Path(file.name)) for file in negative_path.glob("*.py")
]

ast_path = Path("test/ast/")
ast_tests = [
    negative_path.joinpath(Path(file.name)) for file in negative_path.glob("*.py")
]


def print_error_header(test_name: str, header: str) -> None:
    """Print formatted error header with separators."""
    separator = "=" * 80
    print(f"\n{separator}")
    print(f"TEST FAILURE: {header}")
    print(f"File: {test_name}")
    print(separator)


def test_positive_cases() -> None:
    for test in positive_tests:
        try:
            positive_parser = FanglessParser()
            with test.open("r", encoding="utf-8") as source:
                print(f"\n🔍 Testing positive case: {test.name}")
                content = source.read()
                positive_parser.parse(content)
                assert positive_parser.error_count == 0, (
                    f"\n❌ Expected no errors but found {positive_parser.error_count}"
                )
                print(f"✅ Test passed: {test.name}")
        except Exception as e:
            print_error_header(test.name, "POSITIVE TEST FAILED")
            print(f"❌ Error details:\n{e}")
            print(f"📍 Error location: {e.__traceback__.tb_lineno}")
            raise e


def test_negative_cases() -> None:
    for test in negative_tests:
        try:
            negative_parser = FanglessParser()
            with test.open("r", encoding="utf-8") as source:
                print(f"\n🔍 Testing negative case: {test.name}")
                content = source.read()
                negative_parser.parse(content)
                assert negative_parser.error_count > 0, (
                    "\n❌ Expected errors but found none"
                )
                print(f"✅ Test passed: {test.name}")
        except Exception as e:
            print_error_header(test.name, "NEGATIVE TEST FAILED")
            print(f"❌ Error details:\n{e}")
            print(f"📍 Error location: {e.__traceback__.tb_lineno}")
            raise e


def test_ast_cases() -> None:
    for test in ast_tests:  # Fixed: was using negative_tests
        try:
            ast_parser = FanglessParser()
            with test.open("r", encoding="utf-8") as source:
                print(f"\n🔍 Testing AST case: {test.name}")
                content = source.read()
                ast_parser.parse(content)
                assert ast_parser.error_count == 0, (
                    f"\n❌ Expected no errors but found {ast_parser.error_count}"
                )
                print(f"✅ Test passed: {test.name}")
        except Exception as e:
            print_error_header(test.name, "AST TEST FAILED")
            print(f"❌ Error details:\n{e}")
            print(f"📍 Error location: {e.__traceback__.tb_lineno}")
            raise e