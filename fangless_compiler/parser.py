from ply import yacc
from lexer import FanglessLexer
from typing import Any

tokens = None


def p_input(token_list: yacc.YaccProduction) -> None:
    """input    :  START_TOKEN END_TOKEN """

# def p_literal(token_list: yacc.YaccProduction) -> None:
#     """literal  :   bool
#                 |   number
#                 |   string
#                 |   structure
#                 |   NAME
#     """


# def p_bool(token_list: yacc.YaccProduction) -> None:
#     """bool     :   TRUE
#     |   FALSE
#     """


# def p_number(token_list: yacc.YaccProduction) -> None:
#     """number   :   FLOAT_NUMBER
#     |   INTEGER_NUMBER
#     |   BINARY_NUMBER
#     |   OCTAL_NUMBER
#     |   HEXADECIMAL_NUMBER
#     """


# def p_string(token_list: yacc.YaccProduction) -> None:
#     """string   :   STRING
#     |   UNICODESTRING
#     |   RAWSTRING
#     """


# def p_structure(token_list: yacc.YaccProduction) -> None:
#     """structure    :   list
#     |   dict
#     |   tuple
#     |   set
#     """


# def p_list(token_list: yacc.YaccProduction) -> None:
#     """list :   L_BRACKET
#     general_structure_content
#     R_BRACKET
#     """


# def p_dict(token_list: yacc.YaccProduction) -> None:
#     """dict :   L_CURLY_BRACE
#     dict_content
#     R_CURLY_BRACE
#     """


# def p_tuple(token_list: yacc.YaccProduction) -> None:
#     """tuple    :   L_PARENTHESIS
#     general_structure_content
#     R_PARENTHESIS
#     """


# def p_set(token_list: yacc.YaccProduction) -> None:
#     """set  :   L_CURLY_BRACE
#     p_general_series
#     R_CURLY_BRACE
#     """


# def p_general_structure_content(token_list: yacc.YaccProduction) -> None:
#     """general_structure_content    :   general_series
#     |
#     """


# def p_dict_content(token_list: yacc.YaccProduction) -> None:
#     """dict_content :   key_value_series
#     |
#     """


# def p_general_series(token_list: yacc.YaccProduction) -> None:
#     """general_series   :   literal
#     |   literal
#         COMMA
#         general_series
#     """


# def p_key_value_series(token_list: yacc.YaccProduction) -> None:
#     """key_value_series     :   key_value_pair
#     |   key_value_pair
#         COMMA
#         key_value_series
#     """


# def p_key_value_pair(token_list: yacc.YaccProduction) -> None:
#     """key_value_pair   :   literal
#     COLON
#     literal
#     """


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


class FanglessParser:
    def __init__(self, lexer: FanglessLexer = None) -> None:
        if lexer is None:
            lexer = FanglessLexer()
        self.lexer = lexer
        tokens = self.lexer.tokens
        self.parser = yacc.yacc(start="input", debug=True)

    def parse(self, source_code: str) -> Any:
        self.lexer.lex_stream(source_code)
        return self.parser.parse(lexer=self.lexer, debug=True)
