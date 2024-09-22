from pathlib import Path
import sys
from lexer import FanglessPythonLexer


class FanglessPythonCompiler:
    def __init__(self) -> None:
        self.lexer = FanglessPythonLexer()
        self.lexer.build()

    def compile(self) -> None:
        program_to_compile_file_name = Path(sys.argv[1])

        with program_to_compile_file_name.open("r") as source_file:
            content = source_file.read()

            self.lexer.lex_stream(content)
            self.lexer.test()


def main() -> None:
    compiler = FanglessPythonCompiler()
    compiler.compile()

if __name__ == "__main__":
    main()
