from ply import yacc
from lexer import FanglessLexer
from typing import Any
from common import DEBUG_MODE, TOKENS

# ================================ NEEDED OBJECTS =============================
tokens = TOKENS
from collections import defaultdict
from typing import Any

symbol_table: defaultdict[str, Any] = defaultdict(lambda: None)

# =================================== BASIC ===================================
def p_input(token_list: yacc.YaccProduction) -> None:
    """input    :   START_TOKEN operation_series END_TOKEN"""
    _ = token_list


def p_error(token_list: yacc.YaccProduction) -> None:
    print(f"Parser Error near '{token_list}' in line {token_list.lineno}")


# TODO: Delete later
def p_operation_series_test(token_list: yacc.YaccProduction) -> None:
    """operation_series : binary_operation
                        | binary_operation NEWLINE
                        | binary_operation NEWLINE operation_series
    """
    _ = token_list

# ================================== LITERALS =================================
def p_literal(token_list: yacc.YaccProduction) -> None:
    """literal  :   string
                |   number
                |   bool
                |   structure
                |   NAME
    """
    if (token_list.slice[1].type == "NAME" 
        and symbol_table(token_list[1]) is None):
        raise SyntaxError(f"Name: {token_list[1]} not defined")


def p_string(token_list: yacc.YaccProduction) -> None:
    """string   :   STRING
                |   UNICODE_STRING
                |   RAW_STRING
    """
    _ = token_list


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


# =============================== STRUCTURES =======================================
def p_structure(token_list: yacc.YaccProduction) -> None:
    """structure    :   dict
                    |   list
                    |   tuple
                    |   set
    """
    _ = token_list


def p_dict(token_list: yacc.YaccProduction) -> None:
    """dict :   L_CURLY_BRACE dict_content R_CURLY_BRACE"""
    _ = token_list


def p_list(token_list: yacc.YaccProduction) -> None:
    """list :   L_BRACKET general_structure_content R_BRACKET"""
    _ = token_list


def p_tuple(token_list: yacc.YaccProduction) -> None:
    """tuple    :   L_PARENTHESIS general_structure_content R_PARENTHESIS"""
    _ = token_list


def p_set(token_list: yacc.YaccProduction) -> None:
    """set  :   L_CURLY_BRACE general_series R_CURLY_BRACE"""
    _ = token_list


def p_dict_content(token_list: yacc.YaccProduction) -> None:
    """dict_content :   epsilon
                    |   key_value_series
    """
    _ = token_list


def p_general_structure_content(token_list: yacc.YaccProduction) -> None:
    """general_structure_content    :   epsilon
                                    |   general_series
    """
    _ = token_list


# ============================ SERIES =======================================
def p_key_value_series(token_list: yacc.YaccProduction) -> None:
    """key_value_series     :   key_value_pair
                            |   key_value_pair COMMA
                            |   key_value_pair COMMA key_value_series
    """
    _ = token_list


def p_general_series(token_list: yacc.YaccProduction) -> None:
    """general_series   :   literal
                        |   literal COMMA
                        |   literal COMMA general_series
    """
    _ = token_list


def p_key_value_pair(token_list: yacc.YaccProduction) -> None:
    """key_value_pair   :   literal COLON literal"""
    _ = token_list


# ================================ UNARY OPERATIONS ===============================
def p_unary_operation(token_list: yacc.YaccProduction) -> None:
    """unary_operation  :   PLUS literal
                        |   MINUS literal
                        |   NOT literal
                        |   TILDE literal
                        |   literal LEFT_SHIFT
                        |   literal RIGHT_SHIFT
    """
    _ = token_list


# ========================= BINARY OPERATIONS =======================================

def p_binary_operation(token_list: yacc.YaccProduction) -> None:
    """binary_operation     :   binary_operand binary_operator binary_operand
                            |   L_PARENTHESIS binary_operation R_PARENTHESIS
                            |   binary_operand binary_operator binary_operation
    """
    _ = token_list


def p_binary_operand(token_list: yacc.YaccProduction) -> None:
    """binary_operand   :   literal
                        |   unary_operation
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
                        |   EQUAL_EQUAL
                        |   NOT_EQUAL
                        |   LESS_THAN
                        |   LESS_EQUAL
                        |   GREATER_THAN
                        |   GREATER_EQUAL
    """
    _ = token_list


# ========================= ASSIGNATIONS ======================================

def p_assignation(token_list: yacc.YaccProduction) -> None:
    """assignation  :   NAME assignation_operator literal
                    |   NAME assignation_operator assignation
                    |   NAME assignation_operator unary_operation
                    |   NAME assignation_operator binary_operation
    """
    symbol_table[token_list[1]] = str(token_list[3])


def p_assignation_operator(token_list: yacc.YaccProduction) -> None:
    """assignation_operator :   EQUAL
                            |   PLUS_EQUAL
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

# All of this code is commented since it has not been tested ensuring
# functionality
# TODO(Any): Test the code
# def p_statement(token_list: yacc.YaccProduction) -> None:
#     """statement    :   unary_operation
#                     |   binary_operation
#                     |   assignation
#                     |   if_block
#                     |   while
#                     |   len
#                     |   RETURN
#                     |   CONTINUE
#                     |   BREAK
#                     |   PASS
#                     |   epsilon
#     """
#     _ = token_list


# def p_statement_group(token_list: yacc.YaccProduction) -> None:
#     """statement_group    :   statement
#                           |   statement NEWLINE statement_group
#     """
#     _ = token_list


# def p_body(token_list: yacc.YaccProduction) -> None:
#     """body    :   INDENT statement_group DEDENT
#     """
#     _ = token_list


# ============================ CONDITIONALS ===================================

# def p_condition(token_list: yacc.YaccProduction) -> None:
#     """condition    :   unary_operation
#                     |   binary_operation
#                     |   bool
#     """
#     _ = token_list


# def p_if(token_list: yacc.YaccProduction) -> None:
#     """if   :   IF condition COLON body"""
#     _ = token_list


# def p_if_block(token_list: yacc.YaccProduction) -> None:
#     """if_block   :   if
#                   |   if NEWLINE elif_block NEWLINE else
#                   |   if NEWLINE else"""
#     _ = token_list

# def p_elif(token_list: yacc.YaccProduction) -> None:
#     """elif   :   ELIF condition COLON body"""
#     _ = token_list


# def p_elif_block(token_list: yacc.YaccProduction) -> None:
#     """elif_block   :   elif
#                         elif NEWLINE elif_block"""
#     _ = token_list


# def p_else(token_list: yacc.YaccProduction) -> None:
#     """else   :   ELSE COLON body"""
#     _ = token_list


# =============================== LOOPS =======================================

# def p_while(token_list: yacc.YaccProduction) -> None:
#     """while   :   WHILE condition COLON body"""
#     _ = token_list


# =============================== FUNCTIONS ===================================

# def p_len(token_list: yacc.YaccProduction) -> None:
#     """len   :   LEN L_PARENTHESIS structure R_PARENTHESIS"""
#     _ = token_list


# =============================== OTHER =======================================

def p_epsilon(token_list: yacc.YaccProduction) -> None:
    """epsilon  :"""
    _ = token_list


class FanglessParser:
    def __init__(self, lexer: FanglessLexer = None) -> None:
        if lexer is None:
            lexer = FanglessLexer()
        self.lexer = lexer
        self.parser = yacc.yacc(start="input", debug=DEBUG_MODE)

    def parse(self, source_code: str) -> Any:
        self.lexer.lex_stream(source_code)
        return self.parser.parse(lexer=self.lexer, debug=DEBUG_MODE)
