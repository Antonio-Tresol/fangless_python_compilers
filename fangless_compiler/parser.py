from ply import yacc
from lexer import FanglessLexer
from typing import Any
from common import DEBUG_MODE, TOKENS

tokens = TOKENS


def p_input(token_list: yacc.YaccProduction) -> None:
    """input    :   START_TOKEN literal_series END_TOKEN"""
    _ = token_list


def p_error(token_list: yacc.YaccProduction) -> None:
    print(f"Parser Error near '{token_list.value}' in line {token_list.lineno}")


# TODO: Delete later
def p_literal_series(token_list: yacc.YaccProduction) -> None:
    """literal_series   :   literal
                        |   literal NEWLINE
                        |   literal NEWLINE literal_series
    """
    _ = token_list


def p_literal(token_list: yacc.YaccProduction) -> None:
    """literal  :   string
                |   number
                |   bool
                |   structure
                |   NAME
    """
    _ = token_list


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


# def p_binary_statement(token_list: yacc.YaccProduction) -> None:
#     """binary_statement     :   bynary_operation
#     |   binary_statement
#     """


# def p_math_operation(token_list: yacc.YaccProduction) -> None:
#     """binary_operation     :   literal
#     |   binary_operator
#         literal
#     """


# def p_math_operator(token_list: yacc.YaccProduction) -> None:
#     """binary_operator  :   PLUS
#     |   MINUS
#     |   STAR
#     |   SLASH
#     |   DOUBLE_SLASH
#     |   MOD
#     |   DOUBLE_STAR
#     |   AND
#     |   OR
#     |   NOT
#     |   EQUAL
#     """


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
