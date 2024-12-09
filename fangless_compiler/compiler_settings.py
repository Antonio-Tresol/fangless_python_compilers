# ===== COMPILER FLAGS ==================

# Controls indentation output in generated code
# When True, prints all the proper indentation in the output code
VERBOSE_INDENTATION = False

# Controls token output from lexical analysis
# When True, prints each token as it's identified
# and uses the lexer debug output to print the tokenization process
VERBOSE_LEXER = False

# Controls parsing debug output
# When True, shows grammar rules used to parse the code
VERBOSE_PARSER = False

# Controls Abstract Syntax Tree visualization
# When True, prints the full AST structure after parsing
VERBOSE_AST = False

# Controls test execution output
# When True, shows the name and result of each test
VERBOSE_TESTER = False

# Controls compiler operation output
# When True, shows each compilation phase and decisions
VERBOSE_COMPILER = True

# Controls error message formatting
# When True, adds rainbow colors to error messages
RAINBOW_ERRORS = False

# Controls error message tone
# When True, the compiler wont use harsh language in error messages
SENSITIVE_PROGRAMMER = True

# ======================================
# COMPILER SETTINGS ===================
# ======================================
OUTPUT_CODE_FILE_PATH = "output/output.cpp"
OUTPUT_NAME = "output/output.out"
# The compiler to use for the C++ code
COMPILER = "g++"

# Compiler settings for the C++ compiler
COMPILER_SETTINGS = {
    "clang++": {
        "path": "/usr/bin/clang++",
        "standard_flags": [
            "-std=c++20",
            "-O3",
            "-fcolor-diagnostics",
            "-Wall",
            "-Wextra",
        ],
    },
    "g++": {
        "path": "/usr/bin/g++",
        "standard_flags": [
            "-std=c++20",
            "-O3",
            "-fdiagnostics-color=always",
            "-Wall",
            "-Wextra",
        ],
    },
}