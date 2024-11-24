from pathlib import Path
import sys
import common
from lexer import FanglessLexer
from parser import FanglessParser
from code_generator import FanglessGenerator
import subprocess


class FanglessCompiler:
    def __init__(self) -> None:
        self.lexer = FanglessLexer()
        self.lexer.build()
        self.generator = FanglessGenerator()

    def compile(self) -> str:
        program_to_compile_file_name = Path(sys.argv[1])

        with program_to_compile_file_name.open("r") as source_file:
            content = source_file.read()
            self.parser = FanglessParser(self.lexer)
            tree = self.parser.parse(content)
            return self.generator.generate_code(tree)

    def test_lexer(self) -> None:
        program_to_compile_file_name = Path(sys.argv[1])

        with program_to_compile_file_name.open("r") as source_file:
            content = source_file.read()

            self.lexer.lex_stream(content)


def main() -> None:
    compiler = FanglessCompiler()
    generated_code = compiler.compile()
    # format the cpp generated using clang-format
    cpp_file_path = Path("fangless_compiler/cpp_source/temp.cpp")
    cpp_file_path.write_text(generated_code, encoding="utf-8")
    # Run clang-format on the temporary file
    try:
        result = subprocess.run(  # noqa: S603 input is not from user
            ["/usr/bin/clang-format", "fangless_compiler/cpp_source/temp.cpp"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        print("Returning unformatted code")
        if common.VERBOSE_COMPILER:
            print("Unformatted code:")
            print(generated_code)
        return generated_code
    except FileNotFoundError:
        print("clang-format not found. Returning unformatted code")
        if common.VERBOSE_COMPILER:
            print("Unformatted code:")
            print(generated_code)
        return generated_code
    else:
        if common.VERBOSE_COMPILER:
            print("Formatted code:")
            print(result.stdout)
        cpp_file_path.write_text(result.stdout, encoding="utf-8")
        return result.stdout


if __name__ == "__main__":
    main()
