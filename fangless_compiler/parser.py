from ply import yacc
from lexer import FanglessLexer
from common import VERBOSE_PARSER, TOKENS
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


# =================================== BASIC ===================================
def p_all(token_list: yacc.YaccProduction) -> None:
    """all    :   START_TOKEN statement_group END_TOKEN"""
    _ = token_list


def p_error(token_list: yacc.YaccProduction) -> None:
    print(f"Parser Error near '{token_list}' in line {token_list.lineno}")


# ================================== LITERALS =================================
def p_literal(token_list: yacc.YaccProduction) -> None:
    """literal  :   structure
                |   number
                |   bool
                |   NONE
                |   NAME
    """
    if (token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None):
        msg = f"Name: {token_list[1]} not defined"
        raise SyntaxError(msg)


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
            |   L_CURLY_BRACE epsilon R_CURLY_BRACE
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
    """key_value_pair   :   literal COLON literal"""
    _ = token_list


# ================================= LIST, SET, TUPLE ==========================
# both tuples and list can be declared empty so general structure considers
# series of literals (general series) or empty called epsilon
def p_list(token_list: yacc.YaccProduction) -> None:
    """list :   L_BRACKET completed_general_series R_BRACKET
            |   L_BRACKET epsilon R_BRACKET
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
# TODO: binary operations are not passing all tests
def p_binary_operation(token_list: yacc.YaccProduction) -> None:
    """binary_operation     :   L_PARENTHESIS binary_operation R_PARENTHESIS
                            |   binary_operand binary_operator binary_operand
    """
    _ = token_list
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
# TODO(Kenneth): Ask if we want to add symbols here
def p_assignation(token_list: yacc.YaccProduction) -> None:
    """assignation  :   comma_assignation
                    |   name_assignation
                    |   index_assignation
    """
    _ = token_list


def p_comma_assignation(token_list: yacc.YaccProduction) -> None:
    """comma_assignation :   completed_name_comma_series EQUAL assignation_value"""
    names = token_list[1]
    for name in names:
        symbol_table[name] = 1


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


def p_name_assignation(token_list: yacc.YaccProduction) -> None:
    """name_assignation :   name_equal_series EQUAL assignation_value
                        |   NAME EQUAL assignation_value
    """
    if token_list.slice[1].type == "NAME":
        name = token_list[1]
        symbol_table[token_list[1]] = 1
    else:
        names = token_list[1]
        for name in names:
            symbol_table[name] = 1


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
    if (token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None):
        msg = f"Name: {token_list[1]} not defined"
        raise SyntaxError(msg)


def p_op_assignation(token_list: yacc.YaccProduction) -> None:
    """op_assignation   :   op_assignation_operand op_assignation_operator assignation_value"""
    _ = token_list


def p_op_assignation_operand(token_list: yacc.YaccProduction) -> None:
    """op_assignation_operand  :  index_literal
                               |  NAME
    """
    if (token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None):
        msg = f"Name: {token_list[1]} not defined"
        raise SyntaxError(msg)


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
    """scalar_statement   : index_literal
                          | ternary
                          | literal
    """
    _ = token_list


def p_complex_statement(token_list: yacc.YaccProduction) -> None:
    """complex_statement    :   if_block
                            |   while_block
                            |   for_block
                            |   assignation
                            |   op_assignation
                            |   binary_operation
                            |   unary_operation
                            |   scalar_statement
                            |   RETURN
                            |   CONTINUE
                            |   BREAK
                            |   PASS
                            |   epsilon
    """
    _ = token_list


def p_statement_group(token_list: yacc.YaccProduction) -> None:
    """statement_group    :   statement_group NEWLINE complex_statement
                          |   complex_statement
    """
    _ = token_list


def p_body(token_list: yacc.YaccProduction) -> None:
    """body     :   NEWLINE INDENT statement_group DEDENT"""
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
    """while   :   WHILE condition COLON body"""
    _ = token_list


# TODO: Repair for
def p_for_block(token_list: yacc.YaccProduction) -> None:
    """for_block    :   for else
                    |   for
    """
    _ = token_list


def p_for(token_list: yacc.YaccProduction) -> None:
    """for :   FOR completed_name_comma_series IN for_literal COLON body"""
    _ = token_list


def p_for_literal(token_list: yacc.YaccProduction) -> None:
    """for_literal :   epsilon"""
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
