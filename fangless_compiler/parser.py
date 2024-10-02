from ply import yacc
from lexer import FanglessLexer
from common import VERBOSE_PARSER, TOKENS
from collections import defaultdict
from typing import Any

# ================================ NEEDED OBJECTS =============================
tokens = TOKENS


symbol_table: defaultdict[str, Any] = defaultdict(lambda: None)


# =================================== BASIC ===================================
def p_all(token_list: yacc.YaccProduction) -> None:
    """all    :   START_TOKEN statement_group END_TOKEN"""
    _ = token_list


def p_error(token_list: yacc.YaccProduction) -> None:
    print(f"Parser Error near '{token_list}' in line {token_list.lineno}")


# # TODO: Delete later
# def p_doc_test(token_list: yacc.YaccProduction) -> None:
#     """doc_test     :   doc_test NEWLINE test_element
#                     |   test_element
#     """
#     _ = token_list


# # TODO: Delete later
# def p_test_element(token_list: yacc.YaccProduction) -> None:
#     """test_element     :   statement
#                         |   binary_operation
#                         |   unary_operation
#                         |   literal
#     """
#     _ = token_list


# ================================== LITERALS =================================
def p_literal(token_list: yacc.YaccProduction) -> None:
    """literal  :   structure
                |   string
                |   number
                |   bool
                |   NONE
                |   NAME
    """
    if (token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None):
        msg = f"Name: {token_list[1]} not defined"
        raise SyntaxError(msg)


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


# =============================== STRUCTURES ===================================
def p_structure(token_list: yacc.YaccProduction) -> None:
    """structure    :   dict
                    |   list
                    |   tuple
                    |   set
    """
    _ = token_list


# ============= DICTIONARY ===========================
def p_dict(token_list: yacc.YaccProduction) -> None:
    """dict :   L_CURLY_BRACE dict_content R_CURLY_BRACE"""
    _ = token_list


def p_dict_content(token_list: yacc.YaccProduction) -> None:
    """dict_content :   key_value_series
                    |   epsilon
    """
    _ = token_list


def p_key_value_series(token_list: yacc.YaccProduction) -> None:
    """key_value_series     :   key_value_series COMMA key_value_pair
                            |   key_value_pair
    """
    _ = token_list


def p_key_value_pair(token_list: yacc.YaccProduction) -> None:
    """key_value_pair   :   literal COLON literal"""
    _ = token_list


# ================================= LIST, SET, TUPLE ==========================
# both tuples and list can be declared empty so general structure considers
# series of literals (general series) or empty called epsilon
def p_list(token_list: yacc.YaccProduction) -> None:
    """list :   L_BRACKET general_structure_content R_BRACKET"""
    _ = token_list


def p_tuple(token_list: yacc.YaccProduction) -> None:
    """tuple    :   L_PARENTHESIS general_structure_content R_PARENTHESIS"""
    _ = token_list


def p_general_structure_content(token_list: yacc.YaccProduction) -> None:
    """general_structure_content    :   general_series
                                    |   epsilon
    """
    _ = token_list


# sets can not be declared empty so they can only have a general series inside
def p_set(token_list: yacc.YaccProduction) -> None:
    """set  :   L_CURLY_BRACE general_series R_CURLY_BRACE"""
    _ = token_list


def p_general_series(token_list: yacc.YaccProduction) -> None:
    """general_series   :   general_series COMMA literal
                        |   literal
    """
    _ = token_list


# ================================ UNARY OPERATIONS ===========================
# is not a syntax error to use an unary operator agains any literal
def p_unary_operation(token_list: yacc.YaccProduction) -> None:
    """unary_operation  :   PLUS literal
                        |   MINUS literal
                        |   NOT literal
                        |   TILDE literal
                        |   literal LEFT_SHIFT
                        |   literal RIGHT_SHIFT
    """
    _ = token_list


# ========================= BINARY OPERATIONS =================================
# TODO: should we put the first rule to recurse left?
def p_binary_operation(token_list: yacc.YaccProduction) -> None:
    """binary_operation     :   binary_operand binary_operator binary_operation
                            |   L_PARENTHESIS binary_operation R_PARENTHESIS
                            |   binary_operand binary_operator binary_operand
    """
    _ = token_list


def p_binary_operand(token_list: yacc.YaccProduction) -> None:
    """binary_operand   :   unary_operation
                        |   literal
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
# One can have many asignation following themselves
def p_assignation(token_list: yacc.YaccProduction) -> None:
    """assignation  :   assignation assignation_operator asignation_value
                    |   NAME assignation_operator asignation_value
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


def p_asignation_value(token_list: yacc.YaccProduction) -> None:
    """asignation_value     :  binary_operation
                            |  unary_operation
                            |  literal
    """
    _ = token_list


# ========================= STATEMENTS ========================================
# TODO(Any): add while
def p_statement(token_list: yacc.YaccProduction) -> None:
    """statement    :   if_block
                    |   assignation
                    |   while
                    |   binary_operation
                    |   unary_operation
                    |   literal
                    |   RETURN
                    |   CONTINUE
                    |   BREAK
                    |   PASS
                    |   epsilon
    """
    _ = token_list


def p_statement_group(token_list: yacc.YaccProduction) -> None:
    """statement_group    :   statement_group NEWLINE statement
                          |   statement
    """
    _ = token_list


def p_body(token_list: yacc.YaccProduction) -> None:
    """body     :   INDENT statement_group DEDENT"""
    _ = token_list


# ============================ CONDITIONALS ===================================
# TODO: what if we have a something like if (variable):
# TODO: if (variable is None), we might need to add it to binary operations
def p_condition(token_list: yacc.YaccProduction) -> None:
    """condition    :   binary_operation
                    |   unary_operation
                    |   literal
    """
    _ = token_list


# if block is if with the body and elifs and elses with their bodies to the end.
# it doesn't hold the newline token so that we can use it to group statements
# TODO: ambiguous grammar, different parse trees are available.
def p_if_block(token_list: yacc.YaccProduction) -> None:
    """if_block     :   if elif_block else
                    |   if elif_block
                    |   if else
                    |   if
    """
    _ = token_list


# if rule holds the if and its body or statement
# (which doesn't contain the newline token)
def p_if(token_list: yacc.YaccProduction) -> None:
    """if   :   IF condition COLON NEWLINE body
            |   IF condition COLON statement
    """
    _ = token_list


def p_elif_block(token_list: yacc.YaccProduction) -> None:
    """elif_block   :   elif_block elif
                    |   elif
    """
    _ = token_list


# same logic as if rule
def p_elif(token_list: yacc.YaccProduction) -> None:
    """elif     :   ELIF condition COLON NEWLINE body
                |   ELIF condition COLON statement
    """
    _ = token_list


# same for the as for if and elif rules
def p_else(token_list: yacc.YaccProduction) -> None:
    """else     :   ELSE COLON NEWLINE body
                |   ELSE COLON statement
    """
    _ = token_list


# =============================== LOOPS =======================================
# TODO: repair whiles
def p_while(token_list: yacc.YaccProduction) -> None:
    """while   :   WHILE condition COLON NEWLINE body"""
    _ = token_list

# =============================== FUNCTIONS ===================================


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

    def parse(self, source_code: str) -> Any:
        self.lexer.lex_stream(source_code)
        return self.parser.parse(lexer=self.lexer, debug=VERBOSE_PARSER)
