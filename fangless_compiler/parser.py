from ply import yacc
from lexer import FanglessLexer
from common import (
    VERBOSE_PARSER,
    VERBOSE_AST,
    TOKENS,
    CLASS,
    FUNCTION,
    VARIABLE,
    SCOPE_OPENED,
    TYPES,
    CONTAINER_TYPES,
    fill_symbol_table_with_builtin_functions,
    add_remark,
)
from exceptions import ParserError
from collections import defaultdict
from typing import Any

from abstract_syntax_tree.node import NIL_NODE
from abstract_syntax_tree.operator_node import (
    OperatorType,
    OperatorNode,
    Operand
)
from abstract_syntax_tree.epic_node import EpicNode
from abstract_syntax_tree.name_node import NameNode

# ================================ NEEDED OBJECTS =============================
tokens = TOKENS

precedence = (
    ("right", "EQUAL"),
    ("left", "EQUAL_EQUAL", "NOT_EQUAL", "LESS_THAN", "LESS_EQUAL",
     "GREATER_THAN", "GREATER_EQUAL"),
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
undefined_classes: set[str] = set()
parser_state_info: defaultdict[str, int] = defaultdict(lambda: None)
parser_state_info["loops"] = 0
parser_state_info["functions"] = 0
parser_state_info["classes"] = 0
errors: list[str] = []

# =============================ERROR CHECKING==================================
def does_name_exist(token_list: yacc.YaccProduction) -> None:
    if (token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None):
        error = (
               f"--Name: '{token_list[1]}' is not defined "
               f"at {token_list.lineno(1)}--{add_remark()}"
              )
        errors.append(error)
        raise ParserError(error)


def validate_variable_declaration_or_class_scope(
    token_list: yacc.YaccProduction,
) -> None:
    """check variables are declared
    and handle the special case for self in class context
    """
    if (
        token_list.slice[1].type == "NAME"
        and symbol_table[token_list[1]] is None
        and (token_list[1] != "self" or parser_state_info["classes"] <= 0)
    ):
        error = (
            f"--Name: '{token_list[1]}' is not defined at "
            f" line {token_list.lineno(1)}"
            f"--{add_remark()}"
        )
        errors.append(error)
        raise ParserError(error)


def validate_flow_tokens_are_in_context(token_list: yacc.YaccProduction) -> None:
    t_type = token_list.slice[1].type
    # if it is continue or break, check we are in a loop
    if t_type in {"CONTINUE", "BREAK"} and parser_state_info["loops"] <= 0:
        line_number = token_list.lineno(1)
        error = (
            f"--Cant call '{token_list[1]}' on this context on line {line_number}"
            f"--{add_remark()}"
        )
        errors.append(error)
        raise ParserError(error)
    # if it is pass check we are in a loop or inside a functions
    if (
        t_type == "PASS"
        and parser_state_info["loops"] <= 0
        and parser_state_info["functions"] <= 0
    ):
        error = (
            f"--Cant call 'pass' on this"
            f" context on line {token_list.lineno(1)}--{add_remark()}"
        )
        errors.append(error)
        raise ParserError(error)


def p_error(token_list: yacc.YaccProduction) -> None:
    error = f"Parser Error near '{token_list}' in line {token_list.lineno}"
    errors.append(error)
    raise ParserError(error)


# =================================== BASIC ===================================
def p_all(token_list: yacc.YaccProduction) -> None:
    """all    :   START_TOKEN statement_group END_TOKEN"""
    if len(undefined_functions) > 0:
        error = "--Names:--"
        for function in undefined_functions:
            if symbol_table[function]:
                continue
            error += f"\n'{function}'"
        error += f"\n--Were not defined as functions--{add_remark()}"
        errors.append(error)
        raise ParserError(error)

    if len(undefined_classes) > 0:
        error = "--Names:"
        for function in undefined_functions:
            error += f"\n'{function}'"
        error += f"\nWere not defined as classes--{add_remark()}"
        errors.append(error)
        raise ParserError(error)

    group: list = token_list[2]
    token_list[0] = group

    if VERBOSE_AST:
        for line, statement in enumerate(group):
            print(f"\n\n=============== Statement: {line} ===============")
            print(statement)
            print("============================================\n")


# ================================== LITERALS =================================
def p_number(token_list: yacc.YaccProduction) -> None:
    """number   :   MINUS number
                |   FLOATING_NUMBER
                |   INTEGER_NUMBER
                |   BINARY_NUMBER
                |   OCTAL_NUMBER
                |   HEXADECIMAL_NUMBER
    """
    if len(token_list) > 2:
        token_list[0] = -token_list[2]
        return

    token_list[0] = token_list[1]


def p_bool(token_list: yacc.YaccProduction) -> None:
    """bool     :   TRUE
                |   FALSE
    """
    # convert to equivalent boolean value and send it up
    token_list[0] = token_list[1] == "True"


def p_literal(token_list: yacc.YaccProduction) -> None:
    """literal  :   structure
                |   number
                |   bool
                |   NONE
                |   NAME
    """
    does_name_exist(token_list)
    match token_list.slice[1].type:
        case "NAME":
            # for names we create a node so that
            # we know we have to resolve it at some point.
            token_list[0] = NameNode(token_list[1])
        case "NONE":
            token_list[0] = None
        case _:
            token_list[0] = token_list[1]

# =============================== STRUCTURES ===================================
def p_structure(token_list: yacc.YaccProduction) -> None:
    """structure    :   dict
                    |   list
                    |   tuple
                    |   set
                    |   string
    """
    # structure come ready, so just send we just send it up
    token_list[0] = token_list[1]


def p_string(token_list: yacc.YaccProduction) -> None:
    """string   :   STRING
                |   UNICODE_STRING
                |   RAW_STRING
    """
    match token_list.slice[1].type:
        case "STRING":
            token_list[0] = token_list[1]
        case "UNICODE_STRING":
            token_list[0] = str(token_list[1])
        case "RAW_STRING":
            if isinstance(token_list[1], bytes):
                token_list[0] = token_list[1].decode("utf-8", errors="replace")
            else:
                token_list[0] = str(token_list[1])


# ============= DICTIONARY ===========================
def p_dict(token_list: yacc.YaccProduction) -> None:
    """dict :   L_CURLY_BRACE completed_key_value_series R_CURLY_BRACE
            |   L_CURLY_BRACE R_CURLY_BRACE
    """
    # if empty dictionary
    if len(token_list) == 3:
        token_list[0] = {}
        return

    # when the dictionary is not empty
    key_values = token_list[2]
    keys = key_values["keys"]
    values = key_values["values"]

    token_list[0] = dict(zip(keys, values))


def p_completed_key_value_series(token_list: yacc.YaccProduction) -> None:
    """completed_key_value_series   :   key_value_series COMMA
                                    |   key_value_series
    """
    # the key_value_series is ready, just send it up
    token_list[0] = token_list[1]


def p_key_value_series(token_list: yacc.YaccProduction) -> None:
    """key_value_series     :   key_value_series COMMA key_value_pair
                            |   key_value_pair
    """
    # if we only have one key_value_pair
    if len(token_list) == 2:
        new_key_value = token_list[1]
        keys_and_values = {
            "keys": [new_key_value["key"]],
            "values": [
                new_key_value["value"],
            ],
        }
        token_list[0] = keys_and_values
        return

    # if we have a series of them
    keys_and_values = token_list[1]
    new_key_value = token_list[3]
    # we add them to the new dictionary
    keys_and_values["keys"].append(new_key_value["key"])
    keys_and_values["values"].append(new_key_value["value"])

    token_list[0] = keys_and_values


def p_key_value_pair(token_list: yacc.YaccProduction) -> None:
    """key_value_pair   :   non_mutable_literal COLON scalar_statement"""
    # for key value pairs we build a dict with it key and its value and
    # we send it up
    token_list[0] = {"key": token_list[1], "value": token_list[3]}


def p_non_mutable_literal(token_list: yacc.YaccProduction) -> None:
    """non_mutable_literal  :   name_dot_series
                            |   index_literal
                            |   ternary
                            |   tuple
                            |   string
                            |   number
                            |   bool
                            |   function_call
                            |   method_call
                            |   NONE
                            |   NAME
    """
    match token_list.slice[1].type:
        case "NAME":
            # we make a name node here because we have work to do
            token_list[0] = NameNode(token_list[1])
        case "NONE":
            token_list[0] = None
        case _:
            token_list[0] = token_list[1]


# ================================= LIST, SET, TUPLE ==========================
# both tuples and list can be declared empty so general structure considers
# series of literals (general series) or empty
def p_list(token_list: yacc.YaccProduction) -> None:
    """list :   L_BRACKET completed_general_series R_BRACKET
            |   L_BRACKET R_BRACKET
    """
    # if we do not have elements inside the list
    if len(token_list) == 3:
        token_list[0] = []
        return
    # if we have elements inside
    series = token_list[2]
    token_list[0] = series


# sets can not be declared empty 
def p_set(token_list: yacc.YaccProduction) -> None:
    """set  :   L_CURLY_BRACE completed_general_series R_CURLY_BRACE"""
    series = token_list[2]
    token_list[0] = set(series)


def p_completed_general_series(token_list: yacc.YaccProduction) -> None:
    """completed_general_series :   general_series COMMA
                                |   general_series
    """
    token_list[0] = token_list[1]


def p_general_series(token_list: yacc.YaccProduction) -> None:
    """general_series   :   general_series COMMA scalar_statement
                        |   scalar_statement
    """
    if len(token_list) == 2:
        token_list[0] = [token_list[1]]
        return

    series = token_list[1]
    series.append(token_list[3])
    token_list[0] = series


def p_completed_tuple_series(token_list: yacc.YaccProduction) -> None:
    """completed_tuple_series   :   tuple_series COMMA
                                |   tuple_series
                                |   scalar_statement COMMA
    """
    token_list[0] = token_list[1]


def p_tuple_series(token_list: yacc.YaccProduction) -> None:
    """tuple_series     :   tuple_series COMMA scalar_statement
                        |   tuple_series_start
    """
    if len(token_list) == 2:
        token_list[0] = token_list[1]
        return

    series = token_list[1]
    series.append(token_list[3])
    token_list[0] = series


def p_tuple_series_start(token_list: yacc.YaccProduction) -> None:
    """tuple_series_start     :   scalar_statement COMMA scalar_statement"""
    token_list[0] = [token_list[1], token_list[3]]


def p_tuple(token_list: yacc.YaccProduction) -> None:
    """tuple    :   L_PARENTHESIS completed_tuple_series R_PARENTHESIS
                |   L_PARENTHESIS R_PARENTHESIS
    """
    series = []
    if len(token_list) > 3:
        if isinstance(token_list[2], list): 
            series = token_list[2]
        else:
            series = [token_list[2]]

    token_list[0] = tuple(series)


# ================================ UNARY OPERATIONS ===========================
# is not a syntax error to use an unary operator agains any literal
def p_unary_operation(token_list: yacc.YaccProduction) -> None:
    """unary_operation  :   L_PARENTHESIS unary_operation R_PARENTHESIS
                        |   PLUS unary_operand
                        |   MINUS unary_operand
                        |   NOT unary_operand
                        |   TILDE unary_operand
    """
    # if the unary operations has parenthesis
    if token_list.slice[1].type == "L_PARENTHESIS":
        node: OperatorNode = token_list[2]
        node.parenthesis = True
        token_list[0] = node
    else:
        unary_op_node = OperatorNode(operator=token_list[1])
        unary_op_node.set_center_operand(token_list[2])
        token_list[0] = unary_op_node


def p_unary_operand(token_list: yacc.YaccProduction) -> None:
    """unary_operand    :   L_PARENTHESIS unary_operand R_PARENTHESIS
                        |   unary_operation
                        |   scalar_statement
    """
    # if the operand has parenthesis and is an OperatorNode
    if token_list.slice[1].type == "L_PARENTHESIS":
        if isinstance(token_list[2], OperatorNode):
            node: OperatorNode = token_list[2]
            node.parenthesis = True

        token_list[0] = token_list[2]
        return
    # when it is unary operation or scalar statement just send it up
    token_list[0] = token_list[1]


# ========================= BINARY OPERATIONS =================================
def p_binary_operation(token_list: yacc.YaccProduction) -> None:
    """binary_operation     :   L_PARENTHESIS binary_operation R_PARENTHESIS
                            |   binary_operand binary_operator binary_operand
    """
    # if we have parenthesis, we know we have a node so just add them
    if token_list.slice[1].type == "L_PARENTHESIS":
        node: OperatorNode = token_list[2]
        node.parenthesis = True
        token_list[0] = node
    else:  # when building a new binary operation
        binary_op_node = OperatorNode(operator=token_list[2])
        binary_op_node.set_left_operand(token_list[1])
        binary_op_node.set_right_operand(token_list[3])
        token_list[0] = binary_op_node


def p_binary_operand(token_list: yacc.YaccProduction) -> None:
    """binary_operand  :   unary_operand
                       |   binary_operation
    """
    # both come ready, just send it up
    token_list[0] = token_list[1]


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
    operators = token_list[1]
    # if we have a two token operator
    if len(token_list) > 2:
        operators = operators + " " + token_list[2]
    token_list[0] = operators


# ========================= ASSIGNATIONS ======================================
def p_assignation(token_list: yacc.YaccProduction) -> None:
    """assignation  :   comma_assignation
                    |   dot_assignation
                    |   name_assignation
                    |   index_assignation
    """
    # they are ready, so send it up
    token_list[0] = token_list[1]


def p_comma_assignation(token_list: yacc.YaccProduction) -> None:
    """comma_assignation :   completed_name_comma_series EQUAL assignation_value"""
    names: list[NameNode] = token_list[1]
    for name in names:
        # if the name is not in the symbol table add it to the stack
        # to keep track of scope variables
        if symbol_table[name.id] is None:
            stack.append(name.id)
        # TODO(@all): add it value
        symbol_table[name.id] = VARIABLE
    # assignation node
    assignation = OperatorNode(OperatorType.UNPACK_ASSIGNATION)
    assignation.set_left_operand(token_list[1])
    assignation.set_right_operand(token_list[3])
    token_list[0] = assignation


def p_completed_name_comma_series(token_list: yacc.YaccProduction) -> None:
    """completed_name_comma_series  : name_comma_series COMMA
                                    | name_comma_series
    """
    # it's ready, just send it up and ignore the comma
    token_list[0] = token_list[1]


def p_name_comma_series(token_list: yacc.YaccProduction) -> None:
    """name_comma_series    : name_comma_series COMMA NAME
                            | NAME COMMA NAME
    """
    # if this is the first pair of names, make a list of them
    if token_list.slice[1].type == "NAME":
        token_list[0] = [
            NameNode(identifier=token_list[1]),
            NameNode(identifier=token_list[3]),
        ]
    else:  # when we have already some names, just add the name to the list
        names = token_list[1]
        names.append(NameNode(identifier=token_list[3]))
        token_list[0] = names


def p_assignation_value(token_list: yacc.YaccProduction) -> None:
    """assignation_value    :   binary_operation
                            |   unary_operation
                            |   scalar_statement
                            |   completed_assignation_series
    """
    # they are already packed, send it up
    token_list[0] = token_list[1]


def p_completed_assignation_series(token_list: yacc.YaccProduction) -> None:
    """completed_assignation_series   :   assignation_series COMMA
                                      |   assignation_series
    """
    token_list[0] = token_list[1]


def p_assignation_series(token_list: yacc.YaccProduction) -> None:
    """assignation_series   :   assignation_series COMMA literal
                            |   assignation_series_start
    """
    if len(token_list) == 2:
        token_list[0] = token_list[1]
        return

    series = token_list[1]
    series.append(token_list[3])
    token_list[0] = series


def p_assignation_series_start(token_list: yacc.YaccProduction) -> None:
    """assignation_series_start   :   literal COMMA literal"""
    token_list[0] = [token_list[1], token_list[3]]


def p_dot_assignation(token_list: yacc.YaccProduction) -> None:
    """dot_assignation :   name_dot_series EQUAL assignation_value"""
    assignation = OperatorNode(OperatorType.ASSIGNATION)
    assignation.set_left_operand(token_list[1])
    assignation.set_right_operand(token_list[3])

    token_list[0] = assignation


def p_name_dot_series(token_list: yacc.YaccProduction) -> None:
    """name_dot_series  :   name_dot_series DOT NAME
                        |   NAME DOT NAME
    """
    validate_variable_declaration_or_class_scope(token_list)

    new_node = OperatorNode(OperatorType.ATTRIBUTE_CALL)
    # if we are starting the series of dot names
    if token_list.slice[1].type == "NAME":
        new_node.set_left_operand(NameNode(identifier=token_list[1]))
        new_node.set_right_operand(NameNode(identifier=token_list[3]))
        token_list[0] = new_node
    else:  # if we already have a series of names, extend the tree to the right
        attribute_subtree: OperatorNode = token_list[1]
        # new node will have as left the last attribute in the tree
        # which is in the rightmost position of the tree
        new_node.set_left_operand(attribute_subtree.get_rightmost())
        # its right will be the new name in the series
        new_node.set_right_operand(NameNode(identifier=token_list[3]))
        # and that subtree will be planted at the rightmost position of the last tree
        attribute_subtree.set_rightmost(new_node)
        token_list[0] = attribute_subtree


def p_name_assignation(token_list: yacc.YaccProduction) -> None:
    """name_assignation :   name_equal_series EQUAL assignation_value
                        |   var_declaration EQUAL assignation_value
                        |   NAME EQUAL assignation_value
    """
    name = token_list[1]
    assignation: OperatorNode = NIL_NODE
    # if we have a var declaration or a name
    if not isinstance(name, tuple):
        operation = OperatorType.ASSIGNATION

        if symbol_table[token_list[1]] is None:
            stack.append(token_list[1])
            operation = OperatorType.VAR_DECLARATION

        assignation = OperatorNode(operation)
        symbol_table[token_list[1]] = VARIABLE

        # the name left
        assignation.set_left_operand(NameNode(token_list[1]))
        # the value right
        assignation.set_right_operand(token_list[3])
        token_list[0] = assignation
    # when we have a name equal series
    else:
        root, last_tree = name

        operation = (
            OperatorType.ASSIGNATION 
            if last_tree.get_right_operand().id in symbol_table 
            else OperatorType.VAR_DECLARATION
        )
        assignation = OperatorNode(operation)

        # the leaves of the tree are the names so far
        for name_node in root.get_leaves():
            if symbol_table[name_node.id] is None:
                stack.append(name_node.id)
            symbol_table[name_node.id] = VARIABLE
        # the new assignation node will have as left
        # the right of the las tree
        assignation.set_left_operand(last_tree.get_right_operand())
        # and as left the new name
        assignation.set_right_operand(token_list[3])
        # finally that new assignation node will be the last tree new right
        last_tree.set_right_operand(assignation)
        token_list[0] = root


def p_name_equal_series(token_list: yacc.YaccProduction) -> None:
    """name_equal_series   : name_equal_series EQUAL NAME
                           | NAME EQUAL NAME
    """    
    new_tree: OperatorNode = NIL_NODE

    # if we are starting the name series
    if token_list.slice[1].type == "NAME":
        operation = (
            OperatorType.ASSIGNATION 
            if token_list[1] in symbol_table 
            else OperatorType.VAR_DECLARATION
        )
        new_tree = OperatorNode(operation)
        new_tree.set_left_operand(NameNode(identifier=token_list[1]))
        new_tree.set_right_operand(NameNode(identifier=token_list[3]))
        token_list[0] = (new_tree, new_tree)
    else:  # when we already have a series
        tree = token_list[1]
        root, last_tree = tree

        operation = (
            OperatorType.ASSIGNATION 
            if last_tree.get_right_operand().id in symbol_table 
            else OperatorType.VAR_DECLARATION
        )
        new_tree = OperatorNode(operation)

        new_tree.set_left_operand(last_tree.get_right_operand())
        new_tree.set_right_operand(NameNode(identifier=token_list[3]))
        last_tree.set_right_operand(new_tree)
        token_list[0] = (root, new_tree)


def p_index_assignation(token_list: yacc.YaccProduction) -> None:
    """index_assignation    :   index_literal EQUAL assignation_value"""
    assignation = OperatorNode(OperatorType.ASSIGNATION)
    assignation.set_left_operand(token_list[1])
    assignation.set_right_operand(token_list[3])

    token_list[0] = assignation


def p_index_literal(token_list: yacc.YaccProduction) -> None:
    """index_literal    :   index_literal L_BRACKET slice R_BRACKET
                        |   index_literal L_BRACKET index R_BRACKET
                        |   structure L_BRACKET slice R_BRACKET
                        |   structure L_BRACKET index R_BRACKET
                        |   name_dot_series L_BRACKET slice R_BRACKET
                        |   name_dot_series L_BRACKET index R_BRACKET
                        |   NAME L_BRACKET slice R_BRACKET
                        |   NAME L_BRACKET index R_BRACKET
    """
    does_name_exist(token_list)
    tree: OperatorNode = NIL_NODE

    # if we have a slice in the brackets
    if isinstance(token_list[3], EpicNode):
        tree = OperatorNode(OperatorType.SLICING)
        temp_node: EpicNode = token_list[3]
        tree.add_named_adjacent(
            Operand.SLICE,
            {
                Operand.START: temp_node.get_adjacent(Operand.START),
                Operand.END: temp_node.get_adjacent(Operand.END),
            },
        )
    # Indexing
    else:
        tree = OperatorNode(OperatorType.INDEXING)
        tree.add_named_adjacent(Operand.INDEX, token_list[3])

    # if we are indexing over a variable
    if token_list.slice[1].type == "NAME":
        tree.add_named_adjacent(Operand.INSTANCE, NameNode(identifier=token_list[1]))
    else:  # if we are indexing directly into a structure
        tree.add_named_adjacent(Operand.INSTANCE, token_list[1])

    token_list[0] = tree


def p_slice(token_list: yacc.YaccProduction) -> None:
    """slice    :   index COLON index
                |   COLON index
    """
    # sending a temp node up to recognize it
    temp_node = EpicNode(2)
    if len(token_list) == 4:
        temp_node.add_named_adjacent(Operand.START, token_list[1])
        temp_node.add_named_adjacent(Operand.END, token_list[3])
    else:
        temp_node.add_named_adjacent(Operand.END, token_list[2])
    token_list[0] = temp_node


def p_index(token_list: yacc.YaccProduction) -> None:
    """index    :   scalar_statement"""
    token_list[0] = token_list[1]


def p_op_assignation(token_list: yacc.YaccProduction) -> None:
    """op_assignation   :   op_assignation_operand op_assignation_operator assignation_value"""
    operation = OperatorNode(token_list[2])
    operation.set_left_operand(token_list[1])
    operation.set_right_operand(token_list[3])

    token_list[0] = operation


def p_op_assignation_operand(token_list: yacc.YaccProduction) -> None:
    """op_assignation_operand   :   name_dot_series
                                |   index_literal
                                |   NAME
    """
    name = token_list[1]
    if isinstance(name, list):
        if symbol_table[name[1]] is None:
            error = (
                f"--Name: '{name[1]}' is not defined at line {token_list.lineno(1)}"
                f"--{add_remark()}"
            )
            errors.append(error)
            raise ParserError(error)
    else:
        does_name_exist(token_list)

    # TODO(Antonio)
    if token_list.slice[1].type == "NAME":
        token_list[0] = NameNode(token_list[1])
    else:
        token_list[0] = token_list[1]


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
    token_list[0] = token_list[1]


# ========================= VARIABLES & HINTS =================================
def p_var_declaration(token_list: yacc.YaccProduction) -> None:
    """var_declaration  :   NAME COLON hints"""
    token_list[0] = token_list[1]


def p_hints(token_list: yacc.YaccProduction) -> None:
    """hints  : hints BAR hint
              | hint
    """
    _ = token_list


def p_hint(token_list: yacc.YaccProduction) -> None:
    """hint  : container_type
             | NAME
             | NONE
    """
    hint = token_list[1]
    if token_list.slice[1].type == "NAME" and token_list[1] not in TYPES:
        error = (
            f"--TYPE HINTS: '{token_list[1]}' is not a valid type "
            f"on line {token_list.lineno(1)}--{add_remark()}"
        )
        errors.append(error)
        raise ParserError(error)
    if isinstance(hint, list):
        for type_hint in hint:
            if type_hint not in TYPES:
                error = (
                    f"--TYPE HINTS: '{token_list[1]}' is not a "
                    f"valid type on line {token_list.lineno(1)}--{add_remark()}"
                )
                errors.append(error)
                raise ParserError(error)


def p_container_type(token_list: yacc.YaccProduction) -> None:
    """container_type  : NAME L_BRACKET type_series R_BRACKET"""
    if token_list[1] not in CONTAINER_TYPES:
        error = (
            f"--TYPE HINTS: '{token_list[1]}' is not a valid "
            f"container type on line {token_list.lineno(1)}--{add_remark()}"
        )
        errors.append(error)
        raise ParserError(error)
    token_list[0] = token_list[3]


def p_type_series(token_list: yacc.YaccProduction) -> None:
    """type_series  : type_series COMMA NAME
                    | NAME
    """
    if token_list.slice[1].type == "NAME":
        token_list[0] = [token_list[1]]
    else:
        types = token_list[1]
        types.append(token_list[3])
        token_list[0] = types


# ========================= STATEMENTS ========================================
def p_scalar_statement(token_list: yacc.YaccProduction) -> None:
    """scalar_statement :   name_dot_series
                        |   binary_operation
                        |   unary_operation
                        |   index_literal
                        |   ternary
                        |   literal
                        |   function_call
                        |   method_call
                        |   NAME
    """
    does_name_exist(token_list)
    if token_list.slice[1].type == "NAME":
        token_list[0] = NameNode(identifier=token_list[1])

    token_list[0] = token_list[1]


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
    validate_flow_tokens_are_in_context(token_list)
    match token_list.slice[1].type:
        case "CONTINUE":
            token_list[0] = OperatorNode(OperatorType.CONTINUE, max_adjacents=0)
        case "BREAK":
            token_list[0] = OperatorNode(OperatorType.BREAK, max_adjacents=0)
        case "PASS":
            token_list[0] = OperatorNode(OperatorType.PASS, max_adjacents=0)
        case _:
            token_list[0] = token_list[1]


def p_dot_pass(token_list: yacc.YaccProduction) -> None:
    """dot_pass    :   DOT DOT DOT"""
    if parser_state_info["functions"] <= 0:
        error = (
            f"--Cant call 'TRIPLE DOT' on this "
            f"context on line {token_list.lineno(1)}--{add_remark()}"
        )
        errors.append(error)
        raise ParserError(error)
    token_list[0] = OperatorNode(OperatorType.PASS, max_adjacents=0)


def p_statement_group(token_list: yacc.YaccProduction) -> None:
    """statement_group    :   statement_group NEWLINE complex_statement
                          |   complex_statement
    """
    if len(token_list) == 2:
        token_list[0] = [token_list[1]]
        return
    group = token_list[1]
    group.append(token_list[3])
    token_list[0] = group


def p_body(token_list: yacc.YaccProduction) -> None:
    """body     :   NEWLINE open_scope statement_group DEDENT"""
    local_var = stack.pop()
    while local_var != SCOPE_OPENED:
        symbol_table[local_var] = None
        local_var = stack.pop()
    token_list[0] = token_list[3]


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
    token_list[0] = token_list[1]


def p_if_block(token_list: yacc.YaccProduction) -> None:
    """if_block     :   if elif_block else
                    |   if elif_block
                    |   if else
                    |   if
    """
    if_tree: OperatorNode = token_list[1]
    token_amount = len(token_list)
    for i in range(2, token_amount):
        if_tree.add_deepest(Operand.ALTERNATIVE, token_list[i])
    token_list[0] = if_tree


def p_if(token_list: yacc.YaccProduction) -> None:
    """if   :   IF condition COLON body
            |   IF condition COLON complex_statement
    """
    if_node = OperatorNode(OperatorType.IF, max_adjacents=3)
    if_node.add_named_adjacent(Operand.CONDITION, token_list[2])
    if_node.add_named_adjacent(Operand.BODY, token_list[4])
    token_list[0] = if_node


def p_elif_block(token_list: yacc.YaccProduction) -> None:
    """elif_block   :   elif_block elif
                    |   elif
    """
    if len(token_list) == 3:
        new_node = token_list[2]
        elif_tree: OperatorNode = token_list[1]
        elif_tree.add_deepest(Operand.ALTERNATIVE, new_node)

    token_list[0] = token_list[1]


# same logic as if rule
def p_elif(token_list: yacc.YaccProduction) -> None:
    """elif     :   ELIF condition COLON body
                |   ELIF condition COLON complex_statement
    """
    if_node = OperatorNode(OperatorType.ELIF, max_adjacents=3)
    if_node.add_named_adjacent(Operand.CONDITION, token_list[2])
    if_node.add_named_adjacent(Operand.BODY, token_list[4])
    token_list[0] = if_node


# same for the as for if and elif rules
def p_else(token_list: yacc.YaccProduction) -> None:
    """else     :   ELSE COLON body
                |   ELSE COLON complex_statement
    """
    token_list[0] = token_list[3]


def p_ternary(token_list: yacc.YaccProduction) -> None:
    """ternary  :   literal IF condition ELSE scalar_statement"""
    if_node = OperatorNode(OperatorType.TERNARY)
    if_node.add_named_adjacent(Operand.CONDITION, token_list[3])
    if_node.add_named_adjacent(
        Operand.VALUES,
        {
            True: token_list[1],
            False: token_list[5],
        },
    )
    token_list[0] = if_node


# =============================== LOOPS =======================================
def p_while_block(token_list: yacc.YaccProduction) -> None:
    """while_block  :   while else
                    |   while
    """
    while_node : OperatorNode = token_list[1]
    if len(token_list) == 3:
        while_node.add_named_adjacent(Operand.ALTERNATIVE, token_list[2])
    token_list[0] = while_node


def p_while(token_list: yacc.YaccProduction) -> None:
    """while   :   while_open condition COLON body"""
    parser_state_info["loops"] -= 1
    while_node = OperatorNode(OperatorType.WHILE, max_adjacents=3)
    while_node.add_named_adjacent(Operand.CONDITION, token_list[2])
    while_node.add_named_adjacent(Operand.BODY, token_list[4])
    token_list[0] = while_node


def p_while_open(token_list: yacc.YaccProduction) -> None:
    """while_open   :   WHILE"""
    parser_state_info["loops"] += 1
    _ = token_list


def p_for_block(token_list: yacc.YaccProduction) -> None:
    """for_block    :   for else
                    |   for
    """
    for_node: OperatorNode = token_list[1]
    if len(token_list) == 3:
        for_node.add_named_adjacent(Operand.ALTERNATIVE, token_list[2])
    token_list[0] = for_node


def p_for(token_list: yacc.YaccProduction) -> None:
    """for :   for_open for_symbols IN for_literal COLON body"""
    parser_state_info["loops"] -= 1

    local_var = stack.pop()
    while local_var != SCOPE_OPENED:
        symbol_table[local_var] = None
        local_var = stack.pop()

    for_node = OperatorNode(OperatorType.FOR, max_adjacents=4)
    for_node.add_named_adjacent(Operand.SYMBOLS, token_list[2])
    for_node.add_named_adjacent(Operand.FOR_LITERAL, token_list[4])
    for_node.add_named_adjacent(Operand.BODY, token_list[6])

    token_list[0] = for_node


def p_for_open(token_list: yacc.YaccProduction) -> None:
    """for_open :   FOR"""
    parser_state_info["loops"] += 1
    stack.append(SCOPE_OPENED)
    _ = token_list


def p_for_symbols(token_list: yacc.YaccProduction) -> None:
    """for_symbols  :   for_symbols COMMA NAME
                    |   NAME
    """
    # when we have one name
    if token_list.slice[1].type == "NAME":
        if symbol_table[token_list[1]] is None:
            stack.append(token_list[1])
        symbol_table[token_list[1]] = VARIABLE
        token_list[0] = [NameNode(identifier=token_list[1])]
    else:  # when we already have some for symbols
        if symbol_table[token_list[3]] is None:
            stack.append(token_list[3])
        symbol_table[token_list[3]] = VARIABLE
        names = token_list[1]
        names.append(NameNode(identifier=token_list[3]))
        token_list[0] = names


def p_for_literal(token_list: yacc.YaccProduction) -> None:
    """for_literal  :   structure
                    |   function_call
                    |   NAME
    """
    does_name_exist(token_list)
    if token_list.slice[1].type == "NAME":
        token_list[0] = NameNode(identifier=token_list[1])
        return

    token_list[0] = token_list[1]


# =============================== FUNCTIONS ===================================
def p_return_statement(token_list: yacc.YaccProduction) -> None:
    """return_statement :   RETURN return_value_list
                        |   RETURN
    """
    if parser_state_info["functions"] <= 0:
        error = (
            f"--Cant call RETURN 'on this context "
            f"on line {token_list.lineno(1)}--{add_remark()}"
        )
        errors.append(error)
        raise ParserError(error)

    node = OperatorNode(OperatorType.RETURN)
    if len(token_list) == 3:
        node.set_center_operand(token_list[2])
    else:
        node.set_center_operand(None)

    token_list[0] = node


def p_return_value_list(token_list: yacc.YaccProduction) -> None:
    """return_value_list    :   return_value_list COMMA return_value
                            |   return_value
    """
    value_list = token_list[1]

    if isinstance(value_list, list):
        value_list.append(token_list[3])
        token_list[0] = value_list
    else:
        token_list[0] = [token_list[1]]


def p_return_value(token_list: yacc.YaccProduction) -> None:
    """return_value :   binary_operation
                    |   unary_operation
                    |   scalar_statement
    """
    token_list[0] = token_list[1]


def p_function_definition(token_list: yacc.YaccProduction) -> None:
    """function_definition  :   def_open NAME complete_argument_list COLON body
                            |   def_open NAME complete_argument_list ARROW hints COLON body
    """
    parser_state_info["functions"] -= 1

    local_var = stack.pop()
    while local_var != SCOPE_OPENED:
        symbol_table[local_var] = None
        local_var = stack.pop()

    symbol_table[token_list[2]] = FUNCTION
    undefined_functions.discard(token_list[2])

    func_node = OperatorNode(OperatorType.FUNC_DECLARATION, max_adjacents=3)
    func_node.add_named_adjacent(Operand.FUNCTION_NAME, NameNode(token_list[2]))
    func_node.add_named_adjacent(Operand.ARGUMENTS, token_list[3])
    body_index = 5 if len(token_list) == 6 else 7
    func_node.add_named_adjacent(Operand.BODY, token_list[body_index])
    token_list[0] = func_node



def p_def_open(token_list: yacc.YaccProduction) -> None:
    """def_open :   DEF"""
    parser_state_info["functions"] += 1
    _ = token_list


def p_mixed_argument_list(token_list: yacc.YaccProduction) -> None:
    """mixed_argument_list   :  argument_list COMMA default_argument_list
                             |  argument_list COMMA default_argument_list COMMA
    """
    arguments = token_list[1]
    default_arguments = token_list[3]
    arguments.extend(default_arguments)
    token_list[0] = arguments


def p_complete_argument_list(token_list: yacc.YaccProduction) -> None:
    """complete_argument_list   :   L_PARENTHESIS argument_list COMMA R_PARENTHESIS
                                |   L_PARENTHESIS argument_list R_PARENTHESIS
                                |   L_PARENTHESIS default_argument_list COMMA R_PARENTHESIS
                                |   L_PARENTHESIS default_argument_list R_PARENTHESIS
                                |   L_PARENTHESIS mixed_argument_list R_PARENTHESIS
                                |   L_PARENTHESIS R_PARENTHESIS
    """
    stack.append(SCOPE_OPENED)
    # argument list
    if len(token_list) == 3:
        token_list[0] = []
        return

    arguments: list = token_list[2]
    for argument in arguments:
        if isinstance(argument, dict):
            argument_id = argument["argument"].id
        else:
            argument_id = argument.id

        if symbol_table[argument_id] is None:
            stack.append(argument_id)
        symbol_table[argument_id] = VARIABLE

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
    token_list[0] = {"argument": token_list[1], "default": token_list[3]}


def p_argument(token_list: yacc.YaccProduction) -> None:
    """argument   :   NAME COLON hints
                  |   NAME
    """
    token_list[0] = NameNode(identifier=token_list[1])


def p_function_call(token_list: yacc.YaccProduction) -> None:
    """function_call    :   NAME complete_parameter_list"""
    symbol = symbol_table[token_list[1]]
    if symbol not in {FUNCTION, CLASS}:
        undefined_functions.add(token_list[1])

    function_node = OperatorNode(OperatorType.FUNCTION_CALL)
    function_node.add_named_adjacent(Operand.FUNCTION_NAME, NameNode(token_list[1]))
    parameter_list: list = token_list[2]
    function_node.add_named_adjacent(Operand.ARGUMENTS, parameter_list)
    token_list[0] = function_node


def p_complete_parameter_list(token_list: yacc.YaccProduction) -> None:
    """complete_parameter_list  :   L_PARENTHESIS parameter_list COMMA R_PARENTHESIS
                                |   L_PARENTHESIS parameter_list R_PARENTHESIS
                                |   L_PARENTHESIS R_PARENTHESIS
    """
    param_list = token_list[2]

    if isinstance(param_list, list):
        token_list[0] = param_list
    else:
        token_list[0] = []


def p_parameter_list(token_list: yacc.YaccProduction) -> None:
    """parameter_list   :   parameter_list COMMA parameter
                        |   parameter
    """
    parameters = token_list[1]
    if len(token_list) == 4:
        parameters.append(token_list[3])
        token_list[0] = parameters
    else:
        token_list[0] = [parameters]


def p_parameter(token_list: yacc.YaccProduction) -> None:
    """parameter    :   scalar_statement
                    |   binary_operand
                    |   unary_operation
    """
    token_list[0] = token_list[1]


def p_method_call(token_list: yacc.YaccProduction) -> None:
    """method_call  :   callable DOT function_call
                    |   name_dot_series complete_parameter_list
    """
    method_node = OperatorNode(OperatorType.METHOD_CALL)
    function_node: OperatorNode = NIL_NODE

    if token_list.slice[2].type == "DOT":
        function_node: OperatorNode = token_list[3]
        method_node.add_named_adjacent(Operand.INSTANCE, token_list[1])
    else:
        names_subtree: OperatorNode = token_list[1]

        function_node = OperatorNode(OperatorType.FUNCTION_CALL)
        function_node.add_named_adjacent(
            Operand.FUNCTION_NAME,
            names_subtree.get_rightmost(),
        )
        function_node.add_named_adjacent(Operand.ARGUMENTS, token_list[2])

        names_subtree = names_subtree.promote_righmost_sibling()
        method_node.add_named_adjacent(Operand.INSTANCE, names_subtree)

    method_node.add_named_adjacent(Operand.METHOD, function_node)
    token_list[0] = method_node


def p_callable(token_list: yacc.YaccProduction) -> None:
    """callable :   structure
                |   bool
                |   FLOATING_NUMBER
                |   BINARY_NUMBER
                |   OCTAL_NUMBER
                |   HEXADECIMAL_NUMBER
    """
    token_list[0] = token_list[1]


# =============================== CLASSES =====================================
def p_class_definition(token_list: yacc.YaccProduction) -> None:
    """class_definition :   class_header COLON body
                        |   class_header L_PARENTHESIS NAME R_PARENTHESIS COLON body
    """
    parser_state_info["classes"] -= 1
    class_node = OperatorNode(OperatorType.CLASS_DECLARATION, max_adjacents=3)
    class_node.add_named_adjacent(Operand.CLASS_NAME, NameNode(token_list[1]))

    # TODO(Antonio)
    if len(token_list) == 7:
        if token_list[1] == token_list[3]:
            error = (
                    f"--Class: '{token_list[1]}' cannot inherit "
                    f"from themselves on line {token_list.lineno(1)}--{add_remark()}"
                  )
            errors.append(error)
            raise ParserError(error)

        if symbol_table[token_list[3]] is None:
            undefined_classes.add(token_list[3])

        class_node.add_named_adjacent(Operand.PARENT_CLASS, NameNode(token_list[3]))
        class_node.add_named_adjacent(Operand.BODY, token_list[6])
    else:
        class_node.add_named_adjacent(Operand.BODY, token_list[3])

    token_list[0] = class_node


def p_class_header(token_list: yacc.YaccProduction) -> None:
    """class_header :   CLASS NAME"""
    symbol_table[token_list[2]] = CLASS
    undefined_classes.discard(token_list[2])
    parser_state_info["classes"] += 1
    token_list[0] = token_list[2]


# =============================== OTHER =======================================
def p_epsilon(token_list: yacc.YaccProduction) -> None:
    """epsilon  :"""
    _ = token_list


# =============================== PARSER ======================================
class FanglessParser:
    def __init__(self, lexer: FanglessLexer = None) -> None:
        if lexer is None:
            lexer = FanglessLexer()
            lexer.build()
        self.lexer = lexer
        self.parser = yacc.yacc(start="all", debug=VERBOSE_PARSER)
        self.errors = errors
        fill_symbol_table_with_builtin_functions(symbol_table)

    def parse(self, source_code: str) -> Any:
        self.lexer.lex_stream(source_code)
        return self.parser.parse(
            lexer=self.lexer,
            debug=VERBOSE_PARSER,
        )