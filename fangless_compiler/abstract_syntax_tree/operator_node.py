from enum import Enum
from typing import Any

from abstract_syntax_tree.node import Node


class OperatorType(Enum):
    TERNARY = "ternary_operation"
    IF = "if"
    ELIF = "elif"
    FUNCTION_CALL = "function_call"
    METHOD_CALL = "method_call"
    ATTRIBUTE_CALL = "attribute_call"
    SLICING = "slicing"
    INDEXING = "indexing"
    ASSIGNATION = "="
    UNPACK_ASSIGNATION = "unpack_assign"
    RETURN = "return"
    WHILE = "while"
    FOR = "for"
    FUNC_DECLARATION = "func_declaration"
    CLASS_DECLARATION = "class_declaration"
    METHOD_DECLARATION = "method_declaration"


class Operand(Enum):
    # default
    LEFT = 0
    RIGHT = 1
    CENTER = 2

    INDEX = 3
    INSTANCE = 4
    SLICE = 5
    START = 6
    END = 7
    CONDITION = 8
    VALUES = 9
    FUNCTION_NAME = 10
    ARGUMENTS = 11
    METHOD = 12
    BODY = 13
    ELIF = 14
    ALTERNATIVE = 15
    SYMBOLS = 16
    FOR_LITERAL = 17
    CLASS_NAME = 18
    PARENT_CLASS = 19

    def __repr__(self) -> str:
        return str(self.name).lower()

    def __str__(self) -> str:
        return str(self.name).lower()


class OperatorNode(Node):
    def __init__(self, operator: OperatorType, max_adjacents: int = 2) -> None:
        super().__init__("operator")
        if isinstance(operator, str):
            self.operator = operator.strip()
        else:
            self.operator = operator.value
        self.parenthesis = False
        self.max_adjacents = max_adjacents

    def __repr__(self) -> str:
        string = "{\n"
        string += f'  "Node": "{self.node_type}",\n'
        string += f'  "Operator": "{self.operator}",\n'
        if self.parenthesis:
            string += f'  "Parenthesis": {self.parenthesis},\n'
        string += '  "Adjacents": {\n'
        for key, adjacent in self.adjacents.items():
            string = self.append_adjacent_nodes("    ", string, key, adjacent)
        string += "  }\n"
        string += "}"
        return string

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f'{level}  "Node": "{self.node_type}",\n'
        string += f'{level}  "Operator": "{self.operator}",\n'

        if self.parenthesis:
            string += f'{level}  "Parenthesis": {self.parenthesis},\n'

        string += f'{level}  "Adjacents": {{\n'
        for key, adjacent in self.adjacents.items():
            string = self.append_adjacent_nodes(
                level + "    ", string, key, adjacent,
            )

        string += f"{level}  }}\n"
        string += f"{level}}}\n"
        return string

    def add_named_adjacent(self, key: Operand, adj: "Node") -> Operand:
        length = len(self.adjacents)
        if length >= self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more"
                f" than {self.max_adjacents} adjacents"
            )
            raise IndexError(error)
        if key not in Operand:
            error = f'"{key}" is not a valid key for Node: {self.node_type}'
            raise ValueError(error)
        self.adjacents[key] = adj
        return key

    def set_left_operand(self, value: Any) -> None:
        self.adjacents[Operand.LEFT] = value

    def set_center_operand(self, value: Any) -> None:
        self.adjacents[Operand.CENTER] = value

    def set_right_operand(self, value: Any) -> None:
        self.adjacents[Operand.RIGHT] = value

    def get_left_operand(self) -> None:
        if Operand.CENTER in self.adjacents:
            return self.adjacents.get(Operand.CENTER, None)
        return self.adjacents.get(Operand.LEFT, None)

    def get_right_operand(self) -> Any:
        if Operand.CENTER in self.adjacents:
            return self.adjacents.get(Operand.CENTER, None)
        return self.adjacents.get(Operand.RIGHT, None)

    def get_leftmost(self) -> Any:
        current = self
        while isinstance(current, Node):
            left = current.get_adjacent(Operand.LEFT)
            if left is None:
                return current
            current = left
        return current

    def get_rightmost(self) -> Any:
        current = self
        while isinstance(current, Node):
            right = current.get_adjacent(Operand.RIGHT)
            if right is None:
                return current
            current = right
        return current

    def set_rightmost(self, new: Node) -> None:
        parent = self
        current = parent.get_right_operand()
        while isinstance(current, Node):
            right = current.get_adjacent(Operand.RIGHT)
            if right is None:
                parent.set_right_operand(new)
                return
            parent = current
            current = right
        parent.set_right_operand(new)

    def set_leftmost(self, new: Node) -> None:
        parent = self
        current = parent.get_left_operand()
        while isinstance(current, Node):
            left = current.get_adjacent(Operand.LEFT)
            if left is None:
                parent.set_left_operand(new)
                return
            parent = current
            current = left
        parent.set_left_operand(new)

    def promote_righmost_sibling(self) -> Node:
        grand_parent = self
        parent = grand_parent.get_right_operand()

        if parent is None:
            error = (
                f"Node {self.node_type} tried to promote a non existent child"
            )
            raise IndexError(error)
        # if parent is not a node or it doesn't have adjacents, just return it
        # so that the transplant can be done outside
        if not isinstance(parent, OperatorNode) or len(parent.adjacents) == 0:
            return grand_parent.get_left_operand()

        current = parent.get_right_operand()
        while isinstance(current, Node):
            right = current.get_adjacent(Operand.RIGHT)
            if right is None:
                # get sibling up
                left = parent.get_left_operand()
                # move sibling up
                grand_parent.set_left_operand(left)
                return self
            grand_parent = parent
            parent = current
            current = right

        left = parent.get_left_operand()
        grand_parent.set_left_operand(left)
        return self
