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

    def generate_code(self, tree_list: list[OperatorNode]) -> str:
        base_code = "//Copyright 2024, code automatically generated by:"
        base_code += "A. Badilla, Joseph Valverde & Kenneth Villalobos\n"
        base_code += '#include "Headers.hpp"\n'
        base_code += f"int main() {"{"}\n {self.visit_tree(tree_list, is_standalone=True)} return 0;\n {"}"}"

        return base_code

    def visit_tree(self, tree_list: list[OperatorNode], is_standalone : bool = False) -> str:
        statements = ""
        for subtree in tree_list:
            if not isinstance(subtree, (list, dict, tuple, set, int, float, str, bool, type(None))):
                statements += self.operator_handlers[subtree.operator](subtree)
            elif not is_standalone:
                if isinstance(subtree, (int, str, float, bool)):
                    statements += create_basic_instance(subtree)
                else:
                    statements += ""

            if is_standalone:
                statements += ";\n"

        return statements

    def visit_ternary(self, tree: OperatorNode) -> None:
        condition = tree.get_adjacent(Operand.CONDITION)
        condition = self.visit_tree([condition])

        values = tree.get_adjacent(Operand.VALUES)

        return f"({condition})? {values[True]} : {values[False]}"

    def visit_conditional(self, tree: OperatorNode) -> None:
        true_body = tree.get_adjacent(Operand.BODY)
        true_body = self.visit_tree(true_body, is_standalone=True)

        condition = tree.get_adjacent(Operand.CONDITION)
        condition = self.visit_tree([condition])

        alternative_tree = tree.get_adjacent(Operand.ALTERNATIVE)

        operation = f"if ({condition}) {"{"} \n" + f"{true_body}" + f"{"}"}"

        if alternative_tree is None:
            return operation

        if not isinstance(alternative_tree, list):
            alternative_tree = [alternative_tree]
        alternative_tree = self.visit_tree(alternative_tree)

        operation += f"\n else {"{"} \n" + f"{alternative_tree}" + f"{"}"}"

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
        _ = tree
        return "// we had a pass here, hahhah"

    def visit_break(self, tree: OperatorNode) -> str:
        _ = tree
        return "break"

    def visit_continue(self, tree: OperatorNode) -> str:
        _ = tree
        return "continue"

    def visit_direct_binary(self, tree: OperatorNode) -> None:
        left_child = tree.get_left_operand()
        left_child = self.visit_tree([left_child])

        right_child = tree.get_right_operand()
        right_child = self.visit_tree([right_child])

        if tree.parenthesis:
            return (f"({left_child} "
            f"{tree.operator} "
            f"{right_child})")

        return (f"{left_child} "
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

def create_basic_instance(instance) -> str:
    if isinstance(instance, (int, float)):
        return f"Number::spawn({instance})"
    elif isinstance(instance, (str)):
        return f"String::spawn({instance})"
    else:
        return f"Bool::spawn({instance})"

def create_structure_instance(instance) -> str:
    pass