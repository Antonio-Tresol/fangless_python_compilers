from abstract_syntax_tree.operator_node import (
    Operand,
    OperatorNode,
    OperatorType,
)
from abstract_syntax_tree.name_node import (
    NameNode,
)
from common import (
    BUILTIN_FUNCTIONS,
    BUILTIN_METHODS,
)

from graph_operations import topological_sort

NOT_A_OPERATOR_NODE = (
    list,
    dict,
    tuple,
    set,
    int,
    float,
    str,
    bool,
    type(None),
    NameNode,
)

class FanglessGenerator:
    def __init__(self) -> None:
        self.iter_count = 0

        self.function_definitions: dict = {}

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
            "+=": self.visit_direct_binary,
            "-=": self.visit_direct_binary,
            "*=": self.visit_direct_binary,
            "/=": self.visit_direct_binary,
            "%=": self.visit_direct_binary,
            "&=": self.visit_direct_binary,
            "|=": self.visit_direct_binary,
            "^=": self.visit_direct_binary,
            "<<=": self.visit_direct_binary,
            ">>=": self.visit_direct_binary,
            "not": self.visit_unary,
            "~": self.visit_unary,
            "in": self.visit_binary_func,
            "**": self.visit_binary_func,
            "//": self.visit_binary_func,
            "is": self.visit_binary_func,
            "is not": self.visit_binary_func,
            "not in": self.visit_binary_func,
            "**=": self.visit_func_assignation,
            "//=": self.visit_func_assignation,
        }

    def generate_code(self, tree_list: list[OperatorNode],
            function_dependencies: dict[str, list]) -> str:
        copyright_str = (
            "//Copyright 2024, code automatically generated by: "
            "A. Badilla, Joseph Valverde & Kenneth Villalobos\n\n"
        )
        include = '#include "../fangless_compiler/cpp_source/Headers.hpp"\n\n'
        main = ("int main() {"
                f"\n {self.visit_tree(tree_list, is_standalone=True)}"
                "return 0;\n }"
        )

        function_order = topological_sort(function_dependencies)
        function_decs = "namespace GF {\n\n"
        for function in function_order:
            function_decs += f"{self.function_definitions[function]}\n\n"
        function_decs += "};\n\n"

        return f"{copyright_str} {include} {function_decs} {main}"

    def visit_tree(
        self, tree_list: list[OperatorNode], is_standalone: bool = False
    ) -> str:
        statements = ""
        for subtree in tree_list:
            if isinstance(subtree, OperatorNode):
                statements += self.operator_handlers[subtree.operator](subtree)
                if (
                    is_standalone
                    and subtree.operator != OperatorType.FUNC_DECLARATION
                ):
                    statements += ";\n"

            elif (subtree is not None) or (not is_standalone):
                statements += (
                    f"// {self.visit_instance(subtree)}\n"
                    if is_standalone
                    else self.visit_instance(subtree)
                )

        return statements

    def visit_instance(self, instance) -> str:
        """Writes the code for creating an instance of a given object"""
        if isinstance(instance, (int, str, float, bool, type(None), NameNode)):
            return self.visit_basic_instance(instance)
        return self.visit_structure_instance(instance)

    def visit_basic_instance(self, instance) -> str:
        """Writes the code for creating an instance of a basic object
        (int, str, float, bool, None)
        """
        if isinstance(instance, bool):
            bool_instance = "true" if instance else "false"
            return f"Bool::spawn({bool_instance})"
        if isinstance(instance, str):
            return f'String::spawn("{instance}")'
        if instance is None:
            return "None::spawn()"
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

        return (
            f"(Function::boolEval({condition}))? "
            f"{values[True]} : {values[False]}"
        )

    def visit_conditional(self, tree: OperatorNode) -> str:
        true_body = tree.get_adjacent(Operand.BODY)
        true_body = self.visit_tree(true_body, is_standalone=True)

        condition = tree.get_adjacent(Operand.CONDITION)
        condition = self.visit_tree([condition])

        alternative_tree = tree.get_adjacent(Operand.ALTERNATIVE)

        if_str = "if" if tree.operator == OperatorType.IF else "else if"

        operation = (
            f"{if_str}(Function::boolEval({condition})) {{ \n {true_body} }}"
        )

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

        builtin_function: bool = (function_name in BUILTIN_FUNCTIONS)
        namespace = ""
        if  builtin_function or function_name in BUILTIN_METHODS:
            namespace = (
                "BF::"
                if builtin_function else
                ""
            )
            if function_name in {"bool", "float", "int", "union", "isascii"}:
                function_name += "_"
        else:
            namespace = "GF::"
            parameters_str = f"Function::spawnArgs({parameters_str})"

        return f"{namespace}{function_name}({parameters_str})"

    def visit_method_call(self, tree: OperatorNode) -> str:
        left_child = tree.get_adjacent(Operand.INSTANCE)
        left_child = self.visit_tree([left_child])

        right_child = tree.get_adjacent(Operand.METHOD)
        right_child = self.visit_tree([right_child])

        return f"{left_child}->{right_child}"

    def visit_attribute_call(self, tree: OperatorNode) -> None:
        instance = tree.get_left_operand(Operand.INSTANCE)
        instance = self.visit_tree([instance])

        method = tree.get_adjacent(Operand.METHOD)
        method = self.visit_tree([method])

    def visit_slicing(self, tree: OperatorNode) -> str:
        instance = tree.get_adjacent(Operand.INSTANCE)
        instance = self.visit_tree([instance])

        slice_dict = tree.get_adjacent(Operand.SLICE)

        end = self.visit_tree([slice_dict[Operand.END]])
        if slice_dict[Operand.START] is not None:
            start = self.visit_tree([slice_dict[Operand.START]])
            return f"{instance}->slice(Slice({start}, {end}))"

        return f"{instance}->slice(Slice({end}))"

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

        if (
            isinstance(right_child, OperatorNode)
            and right_child.operator == OperatorType.VAR_DECLARATION
        ):
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
        names = tree.get_left_operand()
        value = tree.get_right_operand()
        value = f"BF::list({self.visit_tree([value])})"

        code = f"auto iter_{self.iter_count} = {value};"
        for index, name in enumerate(names):
            code += (
                f"auto {name.id} = "
                f"(*iter_{self.iter_count})[Number::spawn({index})];\n"
            )
        code = code[:-2]
        self.iter_count += 1

        return code
  
    def visit_return(self, tree: OperatorNode) -> str:
        return_value = tree.get_center_operand()
        update = tree.get_adjacent(Operand.UPDATE_ARGS)
        if update is None:
            update = ""

        if return_value is None:
            return f"{update}return None::spawn()"

        if len(return_value) == 1:
            return_value = self.visit_tree([return_value[0]])
            return f"{update}return {return_value}"
        return_values = [self.visit_tree([stmnt]) for stmnt in return_value]
        return_values = f"Tuple::spawn({{ {', '.join(return_values)} }})"

        return f"{update}return {return_values}"

    def visit_while(self, tree: OperatorNode) -> str:
        condition = tree.get_adjacent(Operand.CONDITION)
        condition = self.visit_tree([condition])
        body = tree.get_adjacent(Operand.BODY)

        pre_define = ""
        post_define = ""
        alternative = tree.get_adjacent(Operand.ALTERNATIVE)
        if alternative is not None:
            alternative = self.visit_tree(alternative,
                is_standalone=True)

            pre_define = (
                f"auto canElse_{self.iter_count} = Bool::spawn(true);\n"
            )
            dont_else  = f"canElse_{self.iter_count} = Bool::spawn(false);\n"

            self.dont_else_on_break(body, dont_else)

            post_define = (
                f"\nif(Function::boolEval(canElse_{self.iter_count})) {{"
                f"{alternative} }}"
            )
            self.iter_count += 1
        
        body = self.visit_tree(body, is_standalone=True)

        return (
            f"{pre_define} while (Function::boolEval({condition})) {{ \n"
            f"{body} }}"
            f"{post_define}"
        )

    def visit_for(self, tree: OperatorNode) -> str:
        for_literal = tree.get_adjacent(Operand.FOR_LITERAL)
        body = tree.get_adjacent(Operand.BODY)
        for_symbols = tree.get_adjacent(Operand.SYMBOLS)
        alternative = tree.get_adjacent(Operand.ALTERNATIVE)

        pre_define = ""
        post_define = ""

        # Multiple structures
        if isinstance(for_literal, NameNode):
            for_literal = self.visit_tree([for_literal])

        # One structure
        else:
            pre_define = (
                f"auto iter_{self.iter_count} = "
                f"{self.visit_tree([for_literal])};\n"
            )
            for_literal = f"iter_{self.iter_count}"
            self.iter_count += 1
        
        # Has else
        if alternative is not None:
            alternative = self.visit_tree(alternative, True)
            pre_define += (
                f"auto canElse_{self.iter_count} = Bool::spawn(true);\n"
            )
            dont_else  = f"canElse_{self.iter_count} = Bool::spawn(false);\n"

            self.dont_else_on_break(body, dont_else)
            post_define = (
                f"\nif(Function::boolEval(canElse_{self.iter_count})) {{"
                f"{alternative} }}"
            )
            self.iter_count += 1

        # One symbol
        if len(for_symbols) == 1:
            for_symbols = f"auto& {for_symbols[0].id}"
            body = self.visit_tree(body, is_standalone=True)
            return (
                f"{pre_define}"
                f"for ({for_symbols} : *{for_literal}) {{ \n {body} }}"
                f"{post_define}"
            )

        # Multiple symbols
        body_pre_define = ""
        body_pre_define += "auto tuple = symbols->asTuple();\n"

        for i, name in enumerate(for_symbols):
            body_pre_define += (
                f"auto {name.id} = tuple->at(Number::spawn({i}));\n"
            )

        body = self.visit_tree(body, is_standalone=True)

        return (
            f"{pre_define}"
            f"for (auto symbols : *{for_literal})"
            f" {{ \n {body_pre_define} {body} }}"
            f"{post_define}"
        )
  
    def visit_func_declaration(self, tree: OperatorNode) -> str:
        func_name = tree.get_adjacent(Operand.FUNCTION_NAME)
        arguments = tree.get_adjacent(Operand.ARGUMENTS)

        declaration = (
            "template <typename... Args>"
            f"auto {func_name.id}"
            "(std::tuple<std::shared_ptr<Args>...> args) {"
        )
        for index, name in enumerate(arguments):
            if isinstance(name, NameNode):
                declaration += f"auto {name.id} = std::get<{index}>(args);\n"
            else:
                declaration += (
                    f"auto {name[Operand.ARGUMENT].id} = "
                    f"Function::getArgOrDefault<{index}>(args, "
                    f" {self.visit_tree([name[Operand.DEFAULT]])});\n"
                )

        body = tree.get_adjacent(Operand.BODY)
        argument_strs = []
        for arg in arguments:
            if isinstance(arg, dict):
                argument_strs.append(arg[Operand.ARGUMENT].id)
            else:
                argument_strs.append(arg.id)
        arguments = ", ".join(argument_strs)

        update = (
            "auto newArgs = Function::spawnArgs("
            f" {arguments});\n"
            "Function::updateArgs(args, newArgs);\n"
        )

        has_return = self.update_args(body, update)

        if not has_return:
            fake_return = OperatorNode(OperatorType.RETURN)
            fake_return.set_center_operand(None)
            fake_return.add_named_adjacent(Operand.UPDATE_ARGS, update)
            body.append(fake_return)
        body = self.visit_tree(body, is_standalone=True)
        self.function_definitions[func_name.id] = f"{declaration} {body} }}"
        return ""

    def visit_class_declaration(self, tree: OperatorNode) -> None:
        # sacar el nombre
        # sacar definir los atributos
        # definir sus metodos
        pass

    def visit_pass(self, tree: OperatorNode) -> str:
        _ = tree
        return "// There was a pass here"

    def visit_break(self, tree: OperatorNode) -> str:
        dont_else = tree.get_adjacent(Operand.DONT_ELSE)
        if dont_else is None:
            dont_else = ""

        return f"{dont_else} break"

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
            return f"({left_child} " f"{tree.operator} " f"{right_child})"

        return f"{left_child} " f"{tree.operator} " f"{right_child}"

    def visit_other_operators(self, tree: OperatorNode) -> None:
        pass

    def visit_binary_func(self, tree: OperatorNode) -> str:
        left_child = tree.get_left_operand()
        left_child = self.visit_tree([left_child])

        right_child = tree.get_right_operand()
        right_child = self.visit_tree([right_child])

        func = "BF::"
        if tree.operator == "**":
            func += "pow"
        elif tree.operator == "//":
            func += "intDiv"
        elif "in" in tree.operator:
            func += "in"
        elif "is" in tree.operator:
            func += "is"
        else:
            func += tree.operator

        func = f"{func}({left_child}, {right_child})"
        if "not" in tree.operator:
            func = f"({func})->negate()"

        if tree.parenthesis:
            return f"({func})"
        return func
    
    def visit_func_assignation(self, tree: OperatorNode) -> str:
        name = tree.get_left_operand()
        name = self.visit_tree([name])

        tree.operator = tree.operator[:-1]
        right = self.visit_tree([tree])

        return f"{name} = {right}"

    def update_args(self, body: list, update: str) -> bool: 
        has_return = False
        for stmnt in body:
            if isinstance(stmnt, OperatorNode):
                if (stmnt.operator == OperatorType.IF or 
                    stmnt.operator == OperatorType.ELIF or
                    stmnt.operator == OperatorType.WHILE or
                    stmnt.operator == OperatorType.FOR):
                    new_body = stmnt.get_adjacent(Operand.BODY)
                    has_return = (
                        self.update_args(
                            new_body, update)
                        or has_return
                    )
                    alternative = stmnt.get_adjacent(Operand.ALTERNATIVE)
                    if alternative is not None:
                        if not isinstance(alternative, list):
                            alternative = [alternative]
                        has_return = (
                            self.update_args(
                                alternative, update)
                            or has_return
                        )
                elif stmnt.operator == OperatorType.RETURN:
                    stmnt.add_named_adjacent(Operand.UPDATE_ARGS, update)
                    has_return = True
                        
        return has_return
    
    def dont_else_on_break(self, body: list, dont_else: str) -> bool: 
        has_break = False
        for stmnt in body:
            if isinstance(stmnt, OperatorNode):
                if (stmnt.operator == OperatorType.IF or 
                    stmnt.operator == OperatorType.ELIF):
                    new_body = stmnt.get_adjacent(Operand.BODY)
                    has_break = (
                        self.dont_else_on_break(new_body, dont_else)
                        or has_break
                    )
                    alternative = stmnt.get_adjacent(Operand.ALTERNATIVE)
                    if alternative is not None:
                        if not isinstance(alternative, list):
                            alternative = [alternative]
                        has_break = (
                            self.dont_else_on_break(alternative, dont_else)
                            or has_break
                        )
                elif stmnt.operator == OperatorType.BREAK:
                    stmnt.add_named_adjacent(Operand.DONT_ELSE, dont_else)
                    has_break = True
                        
        return has_break