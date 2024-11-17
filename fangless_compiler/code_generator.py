from typing import Any
from abstract_syntax_tree.operator_node import (
    Node,
    Operand,
    OperatorNode,
    OperatorType,
)


class FanglessGenerator:
    def __init__(self) -> None:
        self.operator_handlers: dict = {
            OperatorType.TERNARY: self.visit_ternary,
            OperatorType.IF: self.visit_conditional,
            OperatorType.ELIF: self.visit_conditional,
            OperatorType.FUNCTION_CALL: self.visit_function_call,
            OperatorType.METHOD_CALL: self.visit_method_call,
            OperatorType.ATTRIBUTE_CALL: self.visit_attribute_call,
            OperatorType.SLICING: self.visit_slicing,
            OperatorType.INDEXING: self.visit_indexing,
            OperatorType.ASSIGNATION: self.visit_assignation,
            OperatorType.UNPACK_ASSIGNATION: self.visit_unpack_assignation,
            OperatorType.RETURN: self.visit_return,
            OperatorType.WHILE: self.visit_while,
            OperatorType.FOR: self.visit_for,
            OperatorType.FUNC_DECLARATION: self.visit_func_declaration,
            OperatorType.CLASS_DECLARATION: self.visit_class_declaration,
            OperatorType.PASS: self.visit_pass,
            OperatorType.BREAK: self.visit_break,
            OperatorType.CONTINUE: self.visit_continue,
            "+": self.visit_direct_binary,
            "-": self.visit_direct_binary,
            "*": self.visit_direct_binary,
            "/": self.visit_direct_binary,
            "%": self.visit_direct_binary,
            "&": self.visit_direct_binary,
            "|": self.visit_direct_binary,
            "==": self.visit_direct_binary,
            "!=": self.visit_direct_binary,
            "<": self.visit_direct_binary,
            "<=": self.visit_direct_binary,
            ">": self.visit_direct_binary,
            ">=": self.visit_direct_binary,
        }

        self.symbol_table = {}

    def resolve_iterable(self, iterable) -> str:
        str_repr = ""


    def visit_tree(self, tree_list: list[OperatorNode]) -> str:
        statements = ""
        for subtree in tree_list:
            if isinstance(subtree, (dict, list, tuple, set)):
                statements += self.resolve_iterable(subtree)
            else:
                statements += self.operator_handlers[subtree.operator](subtree)
            statements += ";\n"
        return statements

    def visit_ternary(self, tree: OperatorNode) -> None:
        condition = tree.get_adjacent(Operand.CONDITION)
        if not is_leaf(condition):
            condition = self.visit_tree([condition])

        values = tree.get_adjacent(Operand.VALUES)

        return f"({condition})? {values[True]} : {values[False]}"

    def visit_conditional(self, tree: OperatorNode) -> None:
        "if true, condition, [elif | else]"
        true_body = tree.get_adjacent(Operand.BODY)
        if not is_leaf(true_body):
            true_body = self.visit_tree([true_body])

        condition = tree.get_adjacent(Operand.CONDITION)
        if not is_leaf(condition):
            condition = self.visit_tree([condition])

        else_list = tree.get_adjacent(Operand.ALTERNATIVE)
        if not is_leaf(else_list):
            else_list = self.visit_tree(else_list)

        # TODO (JOE): fake as fuck need to check else or if
        operation = f"if ({condition}) {{\n"
        f"{true_body}\n"
        f"}}"

        if else_list is None:
            return operation

        for else_statement in else_list:
            operation += "else "
            operation += else_statement

        return operation


    def visit_function_call(self, tree: OperatorNode) -> None:
        pass

    def visit_method_call(self, tree: OperatorNode) -> None:
        pass

    def visit_attribute_call(self, tree: OperatorNode) -> None:
        pass

    def visit_slicing(self, tree: OperatorNode) -> None:
        pass

    def visit_indexing(self, tree: OperatorNode) -> None:
        pass

    def visit_assignation(self, tree: OperatorNode) -> None:
        pass

    def visit_unpack_assignation(self, tree: OperatorNode) -> None:
        pass

    def visit_return(self, tree: OperatorNode) -> None:
        pass

    def visit_while(self, tree: OperatorNode) -> None:
        pass

    def visit_for(self, tree: OperatorNode) -> None:
        pass

    def visit_func_declaration(self, tree: OperatorNode) -> None:
        # sacar el nombre
        # sacar tomar argumentos
        # definir sus metodos
        pass

    def visit_class_declaration(self, tree: OperatorNode) -> None:
        # sacar el nombre
        # sacar definir los atributos
        # definir sus metodos
        pass

    def visit_pass(self, tree: OperatorNode) -> str:
        # nada bro
        return "// we had a pass here, hahhah"

    def visit_break(self, tree: OperatorNode) -> str:
        return "break"

    def visit_continue(self, tree: OperatorNode) -> str:
        return "continue"

    def visit_direct_binary(self, tree: OperatorNode) -> None:
        left_child = tree.get_left_operand()
        if not is_leaf(left_child):
            left_child = self.visit_tree([left_child])

        right_child = tree.get_right_operand()
        if not is_leaf(right_child):
            right_child = self.visit_tree([right_child])

        return (f" {left_child} "
        f"{tree.operator} "
        f"{right_child}")


    def visit_other_operators(self, tree: OperatorNode) -> None:
        pass

    # tipos de arboles (Operator type)


def is_leaf(node: Any) -> bool:
    if not isinstance(node, Node):
        if isinstance(node, (int, str, float, bool, None)):
            return True
        if isinstance(node, dict):
            return all(not isinstance(value, OperatorNode) for value in node.values())
        if isinstance(node, (list, tuple, set)):
            return all(not isinstance(value, OperatorNode) for value in node)

    return node.is_leaf()

