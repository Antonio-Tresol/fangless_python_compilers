from pathlib import Path
import sys
from lexer import FanglessLexer
from parser import FanglessParser


class FanglessCompiler:
    def __init__(self) -> None:
        self.lexer = FanglessLexer()
        self.lexer.build()

    def compile(self) -> None:
        program_to_compile_file_name = Path(sys.argv[1])

        with program_to_compile_file_name.open("r") as source_file:
            content = source_file.read()
            self.parser = FanglessParser(self.lexer)
            return self.parser.parse(content)

    def test_lexer(self) -> None:
        program_to_compile_file_name = Path(sys.argv[1])

        with program_to_compile_file_name.open("r") as source_file:
            content = source_file.read()

            self.lexer.lex_stream(content)
            self.lexer.print_token_stream()


def main() -> None:
    compiler = FanglessCompiler()
    compiler.compile()


if __name__ == "__main__":
    main()
