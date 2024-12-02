from pathlib import Path
import sys
import common
from exceptions import (
    IndentationMismatchError,
    LexerError,
    ParserError,
)
from lexer import FanglessLexer
from parser import FanglessParser
from code_generator import FanglessGenerator
import subprocess
import compiler_settings as cs


OUTPUT_FILE = Path(cs.OUTPUT_CODE_FILE_PATH)


class FanglessCompiler:
    def __init__(self) -> None:
        self.lexer = FanglessLexer()
        self.lexer.build()
        self.generator = FanglessGenerator()

    def generate_code(self) -> str:
        program_to_compile_file_name = Path(sys.argv[1])

        with program_to_compile_file_name.open("r") as source_file:
            common.print_step("Lexing the input")
            content = source_file.read()
            try:
                self.parser = FanglessParser(self.lexer)

                common.print_step("Parsing the tokens")
                tree = self.parser.parse(content)
            except IndentationMismatchError as e:
                common.print_catastrophic_error("Could not indent", f"{e}")
                sys.exit()
            except LexerError as e:
                common.print_catastrophic_error("Could not lex", f"{e}")
                sys.exit()
            except ParserError as e:
                common.print_catastrophic_error("Could not parse", f"{e}")
                sys.exit()

            common.print_step("Generating the code")
            code = self.generator.generate_code(tree)

            OUTPUT_FILE.touch(exist_ok=True)
            OUTPUT_FILE.write_text(code, encoding="utf-8")

            return code

    def format_code(self, code: str) -> None:
        common.print_step("Formatting the code")
        try:
            clang_format = "/usr/bin/clang-format"
            result = subprocess.run(
                [clang_format, cs.OUTPUT_CODE_FILE_PATH],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            common.print_error("Could not call clang-format")
            print(e.stderr)
            if cs.VERBOSE_COMPILER:
                print(common.color_yellow("Unformatted code:"))
                print(code)

        except FileNotFoundError:
            common.print_error("Could not find clang-format")
            if cs.VERBOSE_COMPILER:
                print(common.color_yellow("Unformatted code:"))
                print(code)

        else:
            if cs.VERBOSE_COMPILER:
                print(common.color_yellow("Formatted code:"))
                print(result.stdout)
            OUTPUT_FILE.write_text(result.stdout, encoding="utf-8")

    def compile(self) -> None:
        common.print_step("Compiling the code")
        try:
            cpp_compiler = cs.COMPILER_SETTINGS[cs.COMPILER]["path"]
            flags = cs.COMPILER_SETTINGS[cs.COMPILER]["standard_flags"]
            subprocess.run(
                [
                    cpp_compiler,
                    *flags,
                    cs.OUTPUT_CODE_FILE_PATH,
                    "-o",
                    cs.OUTPUT_NAME,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            common.print_error("Could not find clang-format")
            print(e.stderr)

        else:
            print(
                common.color_green(
                    f"╔═══════════════════════════════════╗\n"
                    f"║ 🎉   Compilation Successful!   🎉 ║\n"
                    f"╚═══════════════════════════════════╝"
                )
            )

    def test_lexer(self) -> None:
        program_to_compile_file_name = Path(sys.argv[1])

        with program_to_compile_file_name.open("r") as source_file:
            content = source_file.read()

            self.lexer.lex_stream(content)


def main() -> None:
    compiler = FanglessCompiler()
    generated_code = compiler.generate_code()
    compiler.format_code(generated_code)
    compiler.compile()


if __name__ == "__main__":
    main()
