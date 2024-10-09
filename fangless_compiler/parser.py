from ply import yacc
from lexer import FanglessLexer
from common import (
    VERBOSE_PARSER,
    TOKENS,
    OBJECT,
    FUNCTION,
    VARIABLE,
    SCOPE_OPENED,
    TYPES,
    fill_symbol_table_with_builtin_functions,
    color_msg,
    RAINBOW_ERRORS,
    AMOONGUS,
)
from collections import defaultdict
from typing import Any

# ================================ NEEDED OBJECTS =============================
tokens = TOKENS

precedence = (
    ("right", "EQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "STAR", "SLASH"),
    ("left", "DOUBLE_STAR"),
    ("left", "STAR_EQUAL", "SLASH_EQUAL", "DOUBLE_SLASH_EQUAL", "MOD_EQUAL",
     "PLUS_EQUAL", "MINUS_EQUAL", "DOUBLE_STAR_EQUAL", "AMPERSAND_EQUAL",
     "BAR_EQUAL", "HAT_EQUAL", "LEFT_SHIFT_EQUAL", "RIGHT_SHIFT_EQUAL"),
    ("left", "LEFT_SHIFT", "RIGHT_SHIFT"),
    ("left", "AMPERSAND"),
    ("left", "HAT"),
    ("left", "BAR"),
    ("left", "EQUAL_EQUAL", "NOT_EQUAL", "LESS_THAN", "LESS_EQUAL",
     "GREATER_THAN", "GREATER_EQUAL"),
    ("left", "NOT"),
    ("left", "AND"),
    ("left", "OR"),
)

symbol_table: defaultdict[str, Any] = defaultdict(lambda: None)
object_symbols: defaultdict[str, defaultdict[str, Any]] = defaultdict(
    lambda: defaultdict(lambda: None),
)

stack: list[str] = []
undefined_functions: set[str] = set()
parser_state_info: defaultdict[str, int] = defaultdict(lambda: None)
parser_state_info["loops"] = 0
parser_state_info["functions"] = 0
parser_state_info["classes"] = 0
errors: list[str] = []


# =============================ERROR CHECKING==================================
def does_name_exist(token_list: yacc.YaccProduction) -> None:
    if (token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None):
        msg = f"Name: '{token_list[1]}' is not defined at {token_list.lineno(1)}"
        errors.append(msg)
        raise SyntaxError(msg)


def p_error(token_list: yacc.YaccProduction) -> None:
    print(f"Parser Error near '{token_list}' in line {token_list.lineno}")


# =================================== BASIC ===================================
def p_all(token_list: yacc.YaccProduction) -> None:
    """all    :   START_TOKEN statement_group END_TOKEN"""
    if len(undefined_functions) > 0:
        msg = "Names:"
        for function in undefined_functions:
            msg += f"\n'{function}'"
        msg += "\nWere not defined"
        errors.append(msg)
        raise SyntaxError(msg)
    _ = token_list


# ================================== LITERALS =================================
def p_literal(token_list: yacc.YaccProduction) -> None:
    """literal  :   structure
                |   number
                |   bool
                |   NONE
                |   NAME
    """
    does_name_exist(token_list)


def p_number(token_list: yacc.YaccProduction) -> None:
    """number   :   FLOATING_NUMBER
                |   INTEGER_NUMBER
                |   BINARY_NUMBER
                |   OCTAL_NUMBER
                |   HEXADECIMAL_NUMBER
    """
    _ = token_list


def p_bool(token_list: yacc.YaccProduction) -> None:
    """bool     :   TRUE
                |   FALSE
    """
    _ = token_list


# =============================== STRUCTURES ===================================
def p_structure(token_list: yacc.YaccProduction) -> None:
    """structure    :   dict
                    |   list
                    |   tuple
                    |   set
                    |   string
    """
    _ = token_list


def p_string(token_list: yacc.YaccProduction) -> None:
    """string   :   STRING
                |   UNICODE_STRING
                |   RAW_STRING
    """
    _ = token_list


# ============= DICTIONARY ===========================
def p_dict(token_list: yacc.YaccProduction) -> None:
    """dict :   L_CURLY_BRACE completed_key_value_series R_CURLY_BRACE
            |   L_CURLY_BRACE R_CURLY_BRACE
    """
    _ = token_list


def p_completed_key_value_series(token_list: yacc.YaccProduction) -> None:
    """completed_key_value_series   :   key_value_series COMMA
                                    |   key_value_series
    """
    _ = token_list


def p_key_value_series(token_list: yacc.YaccProduction) -> None:
    """key_value_series     :   key_value_series COMMA key_value_pair
                            |   key_value_pair
    """
    _ = token_list


def p_key_value_pair(token_list: yacc.YaccProduction) -> None:
    """key_value_pair   :   non_mutable_literal COLON scalar_statement"""
    _ = token_list


def p_non_mutable_literal(token_list: yacc.YaccProduction) -> None:
    """non_mutable_literal  :   tuple
                            |   string
                            |   number
                            |   bool
                            |   NONE
                            |   NAME
    """
    _ = token_list


# ================================= LIST, SET, TUPLE ==========================
# both tuples and list can be declared empty so general structure considers
# series of literals (general series) or empty called epsilon
def p_list(token_list: yacc.YaccProduction) -> None:
    """list :   L_BRACKET completed_general_series R_BRACKET
            |   L_BRACKET R_BRACKET
    """
    _ = token_list


# sets can not be declared empty so they can only have a general series inside
def p_set(token_list: yacc.YaccProduction) -> None:
    """set  :   L_CURLY_BRACE completed_general_series R_CURLY_BRACE"""
    _ = token_list


def p_completed_general_series(token_list: yacc.YaccProduction) -> None:
    """completed_general_series :   general_series COMMA
                                |   general_series
    """
    _ = token_list


def p_general_series(token_list: yacc.YaccProduction) -> None:
    """general_series   :   general_series COMMA literal
                        |   literal
    """
    _ = token_list


def p_tuple(token_list: yacc.YaccProduction) -> None:
    """tuple    :   L_PARENTHESIS general_series COMMA literal R_PARENTHESIS
                |   L_PARENTHESIS general_series COMMA R_PARENTHESIS
                |   L_PARENTHESIS R_PARENTHESIS
    """
    _ = token_list


# ================================ UNARY OPERATIONS ===========================
# is not a syntax error to use an unary operator agains any literal
def p_unary_operation(token_list: yacc.YaccProduction) -> None:
    """unary_operation  :   L_PARENTHESIS unary_operation R_PARENTHESIS
                        |   PLUS unary_operand
                        |   MINUS unary_operand
                        |   NOT unary_operand
                        |   TILDE unary_operand
    """
    _ = token_list


def p_unary_operand(token_list: yacc.YaccProduction) -> None:
    """unary_operand    :   L_PARENTHESIS unary_operand R_PARENTHESIS
                        |   unary_operation
                        |   scalar_statement
    """
    _ = token_list


# ========================= BINARY OPERATIONS =================================
def p_binary_operation(token_list: yacc.YaccProduction) -> None:
    """binary_operation     :   L_PARENTHESIS binary_operation R_PARENTHESIS
                            |   binary_operand binary_operator binary_operand
    """
    token_list[0] = token_list[1]


def p_binary_operand(token_list: yacc.YaccProduction) -> None:
    """binary_operand   :   unary_operand
                        |   binary_operation
    """
    _ = token_list


def p_binary_operator(token_list: yacc.YaccProduction) -> None:
    """binary_operator  :   PLUS
                        |   MINUS
                        |   STAR
                        |   DOUBLE_STAR
                        |   SLASH
                        |   DOUBLE_SLASH
                        |   MOD
                        |   AND
                        |   OR
                        |   AMPERSAND
                        |   BAR
                        |   HAT
                        |   LEFT_SHIFT
                        |   RIGHT_SHIFT
                        |   EQUAL_EQUAL
                        |   NOT_EQUAL
                        |   LESS_THAN
                        |   LESS_EQUAL
                        |   GREATER_THAN
                        |   GREATER_EQUAL
                        |   IS NOT
                        |   IS
                        |   NOT IN
                        |   IN
    """
    _ = token_list


# ========================= ASSIGNATIONS ======================================
def p_assignation(token_list: yacc.YaccProduction) -> None:
    """assignation  :   comma_assignation
                    |   dot_assignation
                    |   name_assignation
                    |   index_assignation
    """
    _ = token_list


def p_comma_assignation(token_list: yacc.YaccProduction) -> None:
    """comma_assignation :   completed_name_comma_series EQUAL assignation_value"""
    names = token_list[1]
    for name in names:
        if symbol_table[name] is None:
            stack.append(name)
        symbol_table[name] = VARIABLE


def p_completed_name_comma_series(token_list: yacc.YaccProduction) -> None:
    """completed_name_comma_series  : name_comma_series COMMA
                                    | name_comma_series
    """
    token_list[0] = token_list[1]


def p_name_comma_series(token_list: yacc.YaccProduction) -> None:
    """name_comma_series    : name_comma_series COMMA NAME
                            | NAME COMMA NAME
    """
    if token_list.slice[1].type == "NAME":
        token_list[0] = [token_list[1], token_list[3]]
    else:
        names = token_list[1]
        names.append(token_list[3])
        token_list[0] = names


def p_assignation_value(token_list: yacc.YaccProduction) -> None:
    """assignation_value    :   binary_operation
                            |   unary_operation
                            |   scalar_statement
                            |   completed_general_series
    """
    _ = token_list


def p_dot_assignation(token_list: yacc.YaccProduction) -> None:
    """dot_assignation :   name_dot_series EQUAL assignation_value"""
    _ = token_list


def p_name_dot_series(token_list: yacc.YaccProduction) -> None:
    """name_dot_series  :   name_dot_series DOT NAME
                        |   NAME DOT NAME
    """
    if (
        token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None
        and (token_list[1] != "self" or parser_state_info["classes"] <= 0)
    ):
        msg = f"Name: '{token_list[1]}' is not defined at line {token_list.lineno(1)}"
        errors.append(msg)
        raise SyntaxError(msg)


def p_name_assignation(token_list: yacc.YaccProduction) -> None:
    """name_assignation :   name_equal_series EQUAL assignation_value
                        |   NAME EQUAL assignation_value
    """
    if token_list.slice[1].type == "NAME":
        if symbol_table[token_list[1]] is None:
            stack.append(token_list[1])
        symbol_table[token_list[1]] = VARIABLE
    else:
        names = token_list[1]
        for name in names:
            if symbol_table[name] is None:
                stack.append(name)
            symbol_table[name] = VARIABLE


def p_name_equal_series(token_list: yacc.YaccProduction) -> None:
    """name_equal_series   : name_equal_series EQUAL NAME
                           | NAME EQUAL NAME
    """
    if token_list.slice[1].type == "NAME":
        token_list[0] = [token_list[1], token_list[3]]
    else:
        names = token_list[1]
        names.append(token_list[3])
        token_list[0] = names


def p_index_assignation(token_list: yacc.YaccProduction) -> None:
    """index_assignation    :   index_literal EQUAL assignation_value"""
    _ = token_list


def p_index_literal(token_list: yacc.YaccProduction) -> None:
    """index_literal    :   index_literal L_BRACKET key_value_pair R_BRACKET
                        |   index_literal L_BRACKET literal R_BRACKET
                        |   structure L_BRACKET key_value_pair R_BRACKET
                        |   structure L_BRACKET literal R_BRACKET
                        |   NAME L_BRACKET key_value_pair R_BRACKET
                        |   NAME L_BRACKET literal R_BRACKET
    """
    does_name_exist(token_list)


def p_op_assignation(token_list: yacc.YaccProduction) -> None:
    """op_assignation   :   op_assignation_operand op_assignation_operator assignation_value"""
    _ = token_list


def p_op_assignation_operand(token_list: yacc.YaccProduction) -> None:
    """op_assignation_operand   :   name_dot_series
                                |   index_literal
                                |   NAME
    """
    name = token_list[1]
    if isinstance(name, list):
        if symbol_table[name[1]] is None:
            msg = f"Name: '{name[1]}' is not defined at line {token_list.lineno(1)}"
            errors.append(msg)
            raise SyntaxError(msg)
    else:
        does_name_exist(token_list)


def p_op_assignation_operator(token_list: yacc.YaccProduction) -> None:
    """op_assignation_operator  :   PLUS_EQUAL
                                |   MINUS_EQUAL
                                |   STAR_EQUAL
                                |   SLASH_EQUAL
                                |   DOUBLE_SLASH_EQUAL
                                |   MOD_EQUAL
                                |   DOUBLE_STAR_EQUAL
                                |   AMPERSAND_EQUAL
                                |   BAR_EQUAL
                                |   HAT_EQUAL
                                |   LEFT_SHIFT_EQUAL
                                |   RIGHT_SHIFT_EQUAL
    """
    _ = token_list


# ========================= STATEMENTS ========================================
def p_scalar_statement(token_list: yacc.YaccProduction) -> None:
    """scalar_statement :   name_dot_series
                        |   index_literal
                        |   ternary
                        |   literal
                        |   function_call
                        |   method_call
    """
    _ = token_list


def p_complex_statement(token_list: yacc.YaccProduction) -> None:
    """complex_statement    :   class_definition
                            |   if_block
                            |   while_block
                            |   for_block
                            |   assignation
                            |   function_definition
                            |   op_assignation
                            |   binary_operation
                            |   unary_operation
                            |   scalar_statement
                            |   return_statement
                            |   CONTINUE
                            |   BREAK
                            |   PASS
                            |   dot_pass
                            |   epsilon
    """
    if (
        (
            token_list.slice[1].type == "CONTINUE" or
            token_list.slice[1].type == "BREAK"
        ) and
        parser_state_info["loops"] <= 0
    ):
        line_number = token_list.lineno(1)
        msg = f"Cant call '{token_list[1]}' on this context on line {line_number}"
        errors.append(msg)
        raise SyntaxError(msg)

    elif (
        token_list.slice[1].type == "PASS" and
        (
            parser_state_info["loops"] <= 0 and
            parser_state_info["functions"] <= 0
        )
    ):
        msg = f"Cant call 'PASS' on this context on line {token_list.lineno(1)}"
        errors.append(msg)
        raise SyntaxError(msg)


def p_dot_pass(token_list: yacc.YaccProduction) -> None:
    """dot_pass    :   DOT DOT DOT"""
    if parser_state_info["functions"] <= 0:
        msg = f"Cant call 'TRIPLE DOT' on this context on line {token_list.lineno(1)}"
        errors.append(msg)
        raise SyntaxError(msg)
    _ = token_list


def p_statement_group(token_list: yacc.YaccProduction) -> None:
    """statement_group    :   statement_group NEWLINE complex_statement
                          |   complex_statement
    """
    _ = token_list


# TODO: check variables for scope using maybe a rule each time there is an indent
def p_body(token_list: yacc.YaccProduction) -> None:
    """body     :   NEWLINE open_scope statement_group DEDENT"""
    local_var = stack.pop()
    while local_var != SCOPE_OPENED:
        symbol_table[local_var] = None
        local_var = stack.pop()
    _ = token_list


def p_open_scope(token_list: yacc.YaccProduction) -> None:
    """open_scope     :   INDENT"""
    stack.append(SCOPE_OPENED)
    _ = token_list


# ============================ CONDITIONALS ===================================
def p_condition(token_list: yacc.YaccProduction) -> None:
    """condition    :   binary_operation
                    |   unary_operation
                    |   scalar_statement
    """
    _ = token_list


def p_if_block(token_list: yacc.YaccProduction) -> None:
    """if_block     :   if elif_block else
                    |   if elif_block
                    |   if else
                    |   if
    """
    _ = token_list


def p_if(token_list: yacc.YaccProduction) -> None:
    """if   :   IF condition COLON body
            |   IF condition COLON complex_statement
    """
    _ = token_list


def p_elif_block(token_list: yacc.YaccProduction) -> None:
    """elif_block   :   elif_block elif
                    |   elif
    """
    _ = token_list


# same logic as if rule
def p_elif(token_list: yacc.YaccProduction) -> None:
    """elif     :   ELIF condition COLON body
                |   ELIF condition COLON complex_statement
    """
    _ = token_list


# same for the as for if and elif rules
def p_else(token_list: yacc.YaccProduction) -> None:
    """else     :   ELSE COLON body
                |   ELSE COLON complex_statement
    """
    _ = token_list


def p_ternary(token_list: yacc.YaccProduction) -> None:
    """ternary  :   literal IF condition ELSE scalar_statement"""
    _ = token_list


# =============================== LOOPS =======================================
def p_while_block(token_list: yacc.YaccProduction) -> None:
    """while_block  :   while else
                    |   while
    """
    _ = token_list


def p_while(token_list: yacc.YaccProduction) -> None:
    """while   :   while_open condition COLON body"""
    parser_state_info["loops"] -= 1
    _ = token_list


def p_while_open(token_list: yacc.YaccProduction) -> None:
    """while_open   :   WHILE"""
    parser_state_info["loops"] += 1
    print("\n\n=================================================")
    print(f"starting loop: {parser_state_info["loops"]}")
    print("\n\n=================================================")
    _ = token_list


def p_for_block(token_list: yacc.YaccProduction) -> None:
    """for_block    :   for else
                    |   for
    """
    _ = token_list


def p_for(token_list: yacc.YaccProduction) -> None:
    """for :   for_open for_symbols IN for_literal COLON body"""
    parser_state_info["loops"] -= 1
    names = token_list[2]
    for name in names:
        symbol_table[name] = None


def p_for_open(token_list: yacc.YaccProduction) -> None:
    """for_open :   FOR"""
    parser_state_info["loops"] += 1
    _ = token_list


def p_for_symbols(token_list: yacc.YaccProduction) -> None:
    """for_symbols  :   for_symbols COMMA NAME
                    |   NAME
    """
    if token_list.slice[1].type == "NAME":
        symbol_table[token_list[1]] = VARIABLE
        token_list[0] = [token_list[1]]
    else:
        symbol_table[token_list[3]] = VARIABLE
        names = token_list[1]
        names.append(token_list[3])
        token_list[0] = names


def p_for_literal(token_list: yacc.YaccProduction) -> None:
    """for_literal  :   structure
                    |   function_call
                    |   NAME
    """
    does_name_exist(token_list)


# =============================== FUNCTIONS ===================================
def p_return_statement(token_list: yacc.YaccProduction) -> None:
    """return_statement :   RETURN return_value_list
                        |   RETURN
    """
    if parser_state_info["functions"] <= 0:
        msg = f"Cant call RETURN 'on this context on line {token_list.lineno(1)}"
        errors.append(msg)
        raise SyntaxError(msg)
    _ = token_list


def p_return_value_list(token_list: yacc.YaccProduction) -> None:
    """return_value_list    :   return_value_list COMMA return_value
                            |   return_value
    """
    _ = token_list


def p_return_value(token_list: yacc.YaccProduction) -> None:
    """return_value :   binary_operation
                    |   unary_operation
                    |   scalar_statement
    """
    _ = token_list


def p_function_definition(token_list: yacc.YaccProduction) -> None:
    """function_definition  :   def_open NAME complete_argument_list COLON body
                            |   def_open NAME complete_argument_list ARROW hints COLON body
    """
    parser_state_info["functions"] -= 1
    arguments = token_list[3]
    for argument in arguments:
        symbol_table[argument] = None
    symbol_table[token_list[2]] = FUNCTION
    undefined_functions.discard(token_list[2])


def p_def_open(token_list: yacc.YaccProduction) -> None:
    """def_open :   DEF"""
    parser_state_info["functions"] += 1
    _ = token_list


def p_complete_argument_list(token_list: yacc.YaccProduction) -> None:
    """complete_argument_list   :   L_PARENTHESIS argument_list COMMA R_PARENTHESIS
                                |   L_PARENTHESIS argument_list R_PARENTHESIS
                                |   L_PARENTHESIS default_argument_list R_PARENTHESIS
                                |   L_PARENTHESIS argument_list COMMA default_argument_list R_PARENTHESIS
                                |   L_PARENTHESIS R_PARENTHESIS
    """
    arguments = token_list[2]
    if len(token_list) == 6:
        default_arguments = token_list[4]
        arguments.extend(default_arguments)
    for argument in arguments:
        symbol_table[argument] = VARIABLE
    token_list[0] = arguments


def p_argument_list(token_list: yacc.YaccProduction) -> None:
    """argument_list    :   argument_list COMMA argument
                        |   argument
    """
    if len(token_list) == 2:
        token_list[0] = [token_list[1]]
    else:
        arguments = token_list[1]
        arguments.append(token_list[3])
        token_list[0] = arguments


def p_default_argument_list(token_list: yacc.YaccProduction) -> None:
    """default_argument_list    :   default_argument_list COMMA default_argument
                                |   default_argument
    """
    if len(token_list) == 2:
        token_list[0] = [token_list[1]]
    else:
        arguments = token_list[1]
        arguments.append(token_list[3])
        token_list[0] = arguments


def p_default_argument(token_list: yacc.YaccProduction) -> None:
    """default_argument :   argument EQUAL literal"""
    token_list[0] = token_list[1]


def p_argument(token_list: yacc.YaccProduction) -> None:
    """argument :   NAME COLON hints
                |   NAME
    """
    token_list[0] = token_list[1]


def p_hints(token_list: yacc.YaccProduction) -> None:
    """hints  : hints BAR hint
              | hint
    """
    _ = token_list


def p_hint(token_list: yacc.YaccProduction) -> None:
    """hint  : NAME L_BRACKET type_series R_BRACKET
             | NAME
             | NONE
    """
    if len(token_list) == 2 and token_list[1] not in TYPES:
        msg = f"TYPE HINTS: '{token_list[1]}' is not a valid type on line {token_list.lineno(1)}"
        errors.append(msg)
        raise SyntaxError(msg)


def p_type_series(token_list: yacc.YaccProduction) -> None:
    """type_series : type_series COMMA NAME
                   | NAME
    """
    if token_list.slice[1].type == "NAME" and token_list[1] not in TYPES:
        msg = f"TYPE HINTS: '{token_list[1]}' is not a valid type on line {token_list.lineno(1)}"
        errors.append(msg)
        raise SyntaxError(msg)
    if len(token_list) == 4 and token_list[3] not in TYPES:
        msg = f"TYPE HINTS: '{token_list[3]}' is not a valid type on line {token_list.lineno(3)}"
        errors.append(msg)
        raise SyntaxError(msg)


def p_function_call(token_list: yacc.YaccProduction) -> None:
    """function_call    :   NAME complete_parameter_list"""
    if symbol_table[token_list[1]] != FUNCTION and symbol_table[token_list[1]] != OBJECT:
        undefined_functions.add(token_list[1])


def p_complete_parameter_list(token_list: yacc.YaccProduction) -> None:
    """complete_parameter_list  :   L_PARENTHESIS parameter_list R_PARENTHESIS
                                |   L_PARENTHESIS R_PARENTHESIS
    """
    _ = token_list


def p_parameter_list(token_list: yacc.YaccProduction) -> None:
    """parameter_list   :   parameter_list COMMA parameter
                        |   parameter
    """
    _ = token_list


def p_parameter(token_list: yacc.YaccProduction) -> None:
    """parameter    :   scalar_statement
                    |   binary_operation
                    |   unary_operation
    """
    _ = token_list


def p_method_call(token_list: yacc.YaccProduction) -> None:
    """method_call  :   callable DOT function_call
                    |   name_dot_series complete_parameter_list
    """
    _ = token_list


def p_callable(token_list: yacc.YaccProduction) -> None:
    """callable :   structure
                |   bool
                |   FLOATING_NUMBER
                |   BINARY_NUMBER
                |   OCTAL_NUMBER
                |   HEXADECIMAL_NUMBER
    """
    _ = token_list


# =============================== CLASSES =====================================
# TODO: Check inheritence
def p_class_definition(token_list: yacc.YaccProduction) -> None:
    """class_definition :   class_header COLON body
                        |   class_header L_PARENTHESIS NAME R_PARENTHESIS COLON body
    """
    parser_state_info["classes"] -= 1
    _ = token_list


def p_class_header(token_list: yacc.YaccProduction) -> None:
    """class_header :   CLASS NAME"""
    symbol_table[token_list[2]] = OBJECT
    parser_state_info["classes"] += 1


# =============================== OTHER =======================================
def p_epsilon(token_list: yacc.YaccProduction) -> None:
    """epsilon  :"""
    _ = token_list


class FanglessParser:
    def __init__(self, lexer: FanglessLexer = None) -> None:
        if lexer is None:
            lexer = FanglessLexer()
        self.lexer = lexer
        self.parser = yacc.yacc(start="all", debug=VERBOSE_PARSER)
        fill_symbol_table_with_builtin_functions(symbol_table)

    def parse(self, source_code: str) -> Any:
        self.lexer.lex_stream(source_code)
        parsed_source_code = self.parser.parse(lexer=self.lexer, debug=VERBOSE_PARSER)
        self.print_errors()
        return parsed_source_code

    def print_errors(self) -> None:
        if len(errors) > 0:
            print("\n\n=================================================")
            print(f"Your program is {color_msg("horseshit")}, here is why:")
            [print(color_msg(error, RAINBOW_ERRORS)) for error in errors]
            print(color_msg(AMOONGUS))
            print("=================================================\n\n")