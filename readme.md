
# Python Compiler Project

## Setting up the Virtual Environment (optional)

1. **Install `virtualenv`**:

   If you haven't already, install `virtualenv` using pip:

   ```bash
   pip install virtualenv
   ```

2. **Create the Virtual Environment**:

   Navigate to your project's root directory in your terminal and create the virtual environment:

   ```bash
   virtualenv python_compiler_venv 
   # or 
   python3 -m venv python_compiler_venv 
   ```

3. **Activate the Virtual Environment**:

   * **Command Prompt (cmd)**:

     ```bash
     python_compiler_venv\Scripts\activate.bat 
     ```

   * **PowerShell**:

     ```powershell
     python_compiler_venv\Scripts\activate.ps1
     ```

   * **Git Bash (or other Unix-like shells)**:

     ```bash
     source python_compiler_venv/Scripts/activate
     ```

**Note:** To deactivate the virtual environment when you're done, simply type `deactivate` in your terminal.

If the virtual enviroment is active the dependencies will be install there and not in your root python enviroment.

## Install Dependencies

   To install the required project dependencies from requirements.txt:

   ```bash
   pip install -r requirements.txt
   ```

## Tests

Unit test are done using the pytest library. Each component of the compiler has its own test.
To execute the unit test on a component e.g. the lexer, the following command can be used

 ```bash
   pytest tests/test_lexer.py
 ```


 For the parser there are many test cases in dir tests. All named input_test_something.py
 All of them should end properly by executing the following command

 ```bash
   python fangless_compiler/compiler.py input_test_something.py
 ```

 In the case of the parser, to run the tests make sure VERBOSE_TESTING is True in fangless_compiler/compiler_settings.py and then run

 ```bash
 python tests/test_parser.py <option>
 ```
 where option can be `[negative, positive, ast, compile]` 

## Run the compiler

To run the compiler over a .py file use the followin command

 ```bash
   python fangless_compiler/compiler.py <program.py>
 ```

## Compiler Settings

The compiler's behavior can be customized through various settings in `compiler_settings.py`.

### Debug Output Settings

- `VERBOSE_INDENTATION`: Shows detailed code indentation in generated output
- `VERBOSE_LEXER`: Displays token identification during lexical analysis
- `VERBOSE_PARSER`: Shows grammar rule applications during parsing
- `VERBOSE_AST`: Prints the Abstract Syntax Tree structure
- `VERBOSE_TESTER`: Displays detailed test execution information
- `VERBOSE_COMPILER`: Shows compilation phases and decisions

### Error Handling Settings

- `RAINBOW_ERRORS`: Enables colorized error messages
- `SENSITIVE_PROGRAMMER`: Uses gentler language in error messages

### Compiler Configuration

Default output paths:
```python
OUTPUT_CODE_FILE_PATH = "output/output.cpp"
OUTPUT_NAME = "output/output.out"
```

Available C++ compilers:
- `g++` (default)
- `clang++`

To change the compiler:
```python
COMPILER = "clang++"  # or "g++"
```

Each compiler includes optimizations and warning flags:
- C++20 standard (`-std=c++20`)
- Optimization level 3 (`-O3`)
- Warning flags (`-Wall`, `-Wextra`)
- Colored diagnostics

Example compiler configuration:
```python
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
    }
}
```

## Unsupported grammar

Due to time and complexity limitations, not all valid Python grammar is supported by this transpiler. As a result, certain features and functionalities have been excluded and will not work as expected. A comprehensive list of these unsupported features, along with examples, can be found in the [unsupported_cases.md](./unsupported_casses.md) file.