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
    output_cpp_file_path = "fangless_compiler/cpp_source/tempi.cpp"
    output_cpp_file = Path(output_cpp_file_path)
    output_cpp_file.touch(exist_ok=True)
    output_cpp_file.write_text(generated_code, encoding="utf-8")
    try:
        clang_format = "/usr/bin/clang-format"
        result = subprocess.run(  # noqa: S603 input is not from user
            [clang_format, output_cpp_file_path],
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
    except FileNotFoundError:
        print("clang-format not found. Returning unformatted code")
        if common.VERBOSE_COMPILER:
            print("Unformatted code:")
            print(generated_code)
    else:
        if common.VERBOSE_COMPILER:
            print("Formatted code:")
            print(result.stdout)
        output_cpp_file.write_text(result.stdout, encoding="utf-8")
    try:
        cpp_compiler = "/usr/bin/g++"
        flags = ["-fsanitize=address", "-std=c++20"]
        result = subprocess.run(  # noqa: S603 input is not from user
            [cpp_compiler, *flags, output_cpp_file_path, "-o", "tempi.out"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        print("Compilation failed")
    else:
        print("Compilation successful")


if __name__ == "__main__":
    main()
