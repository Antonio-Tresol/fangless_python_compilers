
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

## Install Dependencies:

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

or to execute all tests from the root of the repository

 ```bash
   pytest
 ```

## Run the compiler
To run the compiler over a .py file use the followin command

 ```bash
   python fangless_python_compiler/compiler.py <program.py>
 ```
