from typing import Any
from abstract_syntax_tree.operator_node import (
    Node,
    Operand,
    OperatorNode,
    OperatorType,
)
from abstract_syntax_tree.name_node import (
    NameNode,
)
from common import (
    BUILTIN_FUNCTIONS
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
            OperatorType.VAR_DECLARATION: self.visit_assignation,
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
            "+": self.visit_unary_or_binary,
            "-": self.visit_unary_or_binary,
            "*": self.visit_direct_binary,
            "/": self.visit_direct_binary,
            "%": self.visit_direct_binary,
            "&": self.visit_direct_binary,
            "|": self.visit_direct_binary,
            "^": self.visit_direct_binary,
            "==": self.visit_direct_binary,
            "!=": self.visit_direct_binary,
            "<": self.visit_direct_binary,
            "<=": self.visit_direct_binary,
            ">": self.visit_direct_binary,
            ">=": self.visit_direct_binary,
            "<<": self.visit_direct_binary,
            ">>": self.visit_direct_binary,
            "and": self.visit_direct_binary,
            "or": self.visit_direct_binary,
            "not": self.visit_unary,
            "~": self.visit_unary,
        }

    def generate_code(self, tree_list: list[OperatorNode]) -> str:
        base_code = "//Copyright 2024, code automatically generated by: "
        base_code += "A. Badilla, Joseph Valverde & Kenneth Villalobos\n"
        base_code += '#include "../fangless_compiler/cpp_source/Headers.hpp"\n'
        base_code += f"int main() {{\n {self.visit_tree(tree_list, is_standalone=True)} return 0;\n }}"

        return base_code

    def visit_tree(self, tree_list: list[OperatorNode], is_standalone : bool = False) -> str:
        statements = ""
        for subtree in tree_list:
            if not isinstance(subtree, (list, dict, tuple, set, int, float, str, bool, type(None), NameNode)):
                statements += self.operator_handlers[subtree.operator](subtree)
                if is_standalone:
                    statements += ";\n"

            elif (subtree is not None) or (not is_standalone):
                statements += (
                    f"// {self.visit_instance(subtree)}\n"
                    if is_standalone else self.visit_instance(subtree)
                )

        return statements
    
    def visit_instance(self, instance) -> str:
        if isinstance(instance, (int, str, float, bool, type(None), NameNode)):
            return self.visit_basic_instance(instance)
        return self.visit_structure_instance(instance)


    def visit_basic_instance(self, instance) -> str:
        if isinstance(instance, bool):
            bool_instance = "true" if instance else "false"
            return f"Bool::spawn({bool_instance})"
        if isinstance(instance, str):
            return f'String::spawn("{instance}")'
        if instance is None:
            return f'None::spawn()'
        if isinstance(instance, (int, float)):
            return f"Number::spawn({instance})"

        return f"{instance.id}"


    def visit_structure_instance(self, instance) -> str:
        elements = ""
        if len(instance) > 0:
            elements += "{"
            if isinstance(instance, dict):
                for key, value in instance.items():
                    key_str = self.visit_tree([key])
                    value_sr = self.visit_tree([value])
                    elements += f"{{ {key_str}, {value_sr} }}, "
            else:
                for element in instance:
                    element_str = self.visit_tree([element])
                    elements += f"{element_str}, "

            elements = elements[:-2]
            elements += "}"

        if isinstance(instance, dict):
            return f"Dictionary::spawn({elements})"
        if isinstance(instance, tuple):
            return f"Tuple::spawn({elements})"
        if isinstance(instance, set):
            return f"Set::spawn({elements})"

        return f"List::spawn({elements})"

    def visit_ternary(self, tree: OperatorNode) -> str:
        condition = tree.get_adjacent(Operand.CONDITION)
        condition = self.visit_tree([condition])

        values = tree.get_adjacent(Operand.VALUES)

        return f"({condition})? {values[True]} : {values[False]}"

    def visit_conditional(self, tree: OperatorNode) -> str:
        true_body = tree.get_adjacent(Operand.BODY)
        true_body = self.visit_tree(true_body, is_standalone=True)

        condition = tree.get_adjacent(Operand.CONDITION)
        condition = self.visit_tree([condition])

        alternative_tree = tree.get_adjacent(Operand.ALTERNATIVE)

        if_str = "if" if tree.operator == OperatorType.IF else "else if"

        operation = f"{if_str} ({condition}) {{ \n {true_body} }}"

        if alternative_tree is None:
            return operation

        if isinstance(alternative_tree, OperatorNode):
            alternative_tree = self.visit_tree([alternative_tree])
            operation += f"\n{alternative_tree}"
        else:
            alternative_tree = self.visit_tree(alternative_tree, is_standalone=True)
            operation += f"\n else {{ \n {alternative_tree} }}"

        return operation

    def visit_function_call(self, tree: OperatorNode) -> None:
        parameters_str = ""
        parameters = tree.get_adjacent(Operand.ARGUMENTS)

        for parameter in parameters:
            parameters_str += f"{self.visit_tree([parameter])}, "
        if len(parameters) > 0:
            parameters_str = parameters_str[:-2]

        function_name = tree.get_adjacent(Operand.FUNCTION_NAME)
        function_name = function_name.id

        namespace = (
            "BF::"
            if function_name in BUILTIN_FUNCTIONS else
            ""
        )

        if (function_name == "bool" or
            function_name == "float" or
            function_name == "int"):
            function_name += "_"
        
        return f"{namespace}{function_name}({parameters_str})"

    def visit_method_call(self, tree: OperatorNode) -> None:
        pass

    def visit_attribute_call(self, tree: OperatorNode) -> None:
        pass

    def visit_slicing(self, tree: OperatorNode) -> str:
        instance = tree.get_adjacent(Operand.INSTANCE)
        instance = self.visit_tree([instance])

        slice_dict = tree.get_adjacent(Operand.SLICE)

        end = self.visit_instance(slice_dict[Operand.END])
        if slice_dict[Operand.START] is not None:
            start = self.visit_instance(slice_dict[Operand.START])
            return f"(*{instance})[Slice({start}, {end})]"
        
        return f"(*{instance})[Slice({end})]"


    def visit_indexing(self, tree: OperatorNode) -> None:
        instance = tree.get_adjacent(Operand.INSTANCE)
        instance = self.visit_tree([instance])

        index = tree.get_adjacent(Operand.INDEX)
        index = self.visit_tree([index])

        return f"(*{instance})[{index}]"


    def visit_assignation(self, tree: OperatorNode) -> str:
        left_child = tree.get_left_operand()
        left_child = self.visit_tree([left_child])

        right_child = tree.get_right_operand()

        code = ""

        if isinstance(right_child, OperatorNode) and right_child.operator == OperatorType.VAR_DECLARATION:
            true_right_child = right_child.get_left_operand().id
            right_child = self.visit_tree([right_child], is_standalone=True)
            code += right_child
            right_child = true_right_child

        else:
            right_child = self.visit_tree([right_child])

        auto = "auto" if tree.operator == OperatorType.VAR_DECLARATION else ""

        code += f"{auto} {left_child} = {right_child}"

        return code

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
        return "// There was a pass here"

    def visit_break(self, tree: OperatorNode) -> str:
        _ = tree
        return "break"

    def visit_continue(self, tree: OperatorNode) -> str:
        _ = tree
        return "continue"
    
    def visit_unary_or_binary(self, tree: OperatorNode) -> str:
        if Operand.CENTER in tree.adjacents:
            return self.visit_unary(tree)
        
        return self.visit_direct_binary(tree)
        
    def visit_unary(self, tree: OperatorNode) -> str:
        operand = tree.get_adjacent(Operand.CENTER)
        operand = self.visit_tree([operand])

        if tree.operator == "not":
            tree.operator = "!"

        if tree.parenthesis:
            return f"({tree.operator} {operand})"
        return f"{tree.operator} {operand}"
  
    def visit_direct_binary(self, tree: OperatorNode) -> str:
        left_child = tree.get_left_operand()
        left_child = self.visit_tree([left_child])

        right_child = tree.get_right_operand()
        right_child = self.visit_tree([right_child])

        if tree.operator == "and":
            tree.operator = "&&"
        elif tree.operator == "or":
            tree.operator = "||"

        if tree.parenthesis:
            return (f"({left_child} "
            f"{tree.operator} "
            f"{right_child})")

        return (f"{left_child} "
        f"{tree.operator} "
        f"{right_child}")


    def visit_other_operators(self, tree: OperatorNode) -> None:
        pass

    def translate_abs(self, parameters_str: str) -> str:
        return f"abs({parameters_str})"

    def translate_any(self, parameters_str: str) -> str:
        return f"abs({parameters_str})"
