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




def test_positive_cases() -> None:
    for test in positive_tests:
        positive_parser = FanglessParser()
        with test.open("r", encoding="utf-8") as source:
            print(f"-Positive Test: testing '{test.name}")
            content = source.read()
            positive_parser.parse(content)
            assert positive_parser.error_count == 0


def test_negative_cases() -> None:
    for test in negative_tests:
        negative_parser = FanglessParser()
        with test.open("r", encoding="utf-8") as source:
            content = source.read()
            negative_parser.parse(content)
            assert negative_parser.error_count > 0


def test_ast_cases() -> None:
    for test in negative_tests:
        negative_parser = FanglessParser()
        with test.open("r", encoding="utf-8") as source:
            content = source.read()
            negative_parser.parse(content)
            assert negative_parser.error_count == 0
