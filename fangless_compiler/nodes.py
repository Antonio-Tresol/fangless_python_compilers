from enum import Enum
from typing import Any


class OperatorType(Enum):
    TERNARY = "ternary_operation"
    IF = "if"
    FUNCTION_CALL = "function_call"
    METHOD_CALL = "method_call"
    ATTRIBUTE_CALL = "attribute_call"
    SLICING = "slicing"
    INDEXING = "indexing"
    ASSIGNATION = "="
    UNPACK_ASSIGNATION = "unpack_assign"


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

    def __repr__(self) -> str:
        return str(self.name).lower()

    def __str__(self) -> str:
        return str(self.name).lower()


NIL_NODE = None

AdjacentKey = int | float | str | tuple


class Node:
    def __init__(self, node_type: str) -> None:
        self.node_type = node_type
        self.adjacents = {}
        self.max_adjacents = 0

    def add_named_adjacent(self, key: AdjacentKey, adj: "Node") -> AdjacentKey:
        length = len(self.adjacents)
        if length >= self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more"
                f" than {self.max_adjacents} adjacents"
            )
            raise IndexError(error)

        self.adjacents[key] = adj
        return key

    def locate_adjacent(self, adj: "Node") -> AdjacentKey:
        for key, node in self.adjacents.items():
            if node == adj:
                return key
        msg = f"Adjacent node not found in {self.node_type}"
        raise ValueError(msg)

    def change_adjacent(self, key: AdjacentKey, adj: "Node") -> None:
        if len(self.adjacents) >= self.max_adjacents or key not in self.adjacents:
            error = (
                f"Node {self.node_type} tried to change"
                f"nonexistent adjacent at key {key}"
            )
            raise IndexError(error)

        self.adjacents[key] = adj

    def get_adjacent(self, key: AdjacentKey) -> "Node":
        return self.adjacents.get(key, None)

    def __repr__(self) -> str:
        string = "{\n"
        string += f'Node: "{self.node_type}",\n'
        string += "Adjacents:\n"
        for key, adjacent in self.adjacents.items():
            string = self.append_adjacent_nodes("", string, key, adjacent)
        string += "}"
        return string

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f'{level}Node: "{self.node_type}",\n'
        string += f"{level}Adjacents:\n"
        for key, adjacent in self.adjacents.items():
            string = self.append_adjacent_nodes(level, string, key, adjacent)
        string += f"{level}}}\n"
        return string

    def append_adjacent_nodes(
        self,
        level: str,
        string: str,
        key: AdjacentKey,
        adjacent: Any,
    ) -> str:
        if isinstance(adjacent, Node):
            string += f'{level}\t"{key}":\n'
            string += adjacent.to_string(level + "\t")
        elif isinstance(adjacent, dict):
            for subkey, value in adjacent.items():
                if isinstance(value, Node):
                    string += f'{level}\t"{subkey}":\n'
                    string += value.to_string(level + "\t")
                else:
                    string += f'{level}\t"{subkey}": {value}\n'
        elif isinstance(adjacent, list):
            string += f'{level}\t"{key}": [\n'
            for item in adjacent:
                if isinstance(item, Node):
                    string += item.to_string(level + "\t")
                else:
                    string += f"{level}\t{level}{item}\n"
            string += f"{level}\t]\n"
        else:
            string += f'{level}\t"{key}": {adjacent}\n'
        return string

    def get_leaves(self) -> list["Node"]:
        if len(self.adjacents) == 0:
            return [self]
        nodes = []
        for adjacent in self.adjacents.values():
            if isinstance(adjacent, Node):
                nodes.extend(adjacent.get_leaves())
            else:
                nodes.append(adjacent)
        return nodes


class OperatorNode(Node):
    def __init__(self, operator: OperatorType) -> None:
        super().__init__("operator")
        if isinstance(operator, str):
            self.operator = operator.strip()
        else:
            self.operator = operator.value
        self.parenthesis = False
        self.max_adjacents = 2
        # mis adjacentes son mis operandos

    # TODO
    def try_evaluate(self) -> bool:
        ...

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

    def add_named_adjacent(self, key: Operand, adj: "Node") -> Operand:
        length = len(self.adjacents)
        if length >= self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more"
                f" than {self.max_adjacents} adjacents"
            )
            raise IndexError(error)
        if key not in Operand:
            error = f"\"{key}\" is not a valid key for Node: {self.node_type}"
            raise ValueError(error)
        self.adjacents[key] = adj
        return key

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f'{level}  "Node": "{self.node_type}",\n'
        string += f'{level}  "Operator": "{self.operator}",\n'
        if self.parenthesis:
            string += f'{level}  "Parenthesis": {self.parenthesis},\n'
        string += f'{level}  "Adjacents": {{\n'
        for key, adjacent in self.adjacents.items():
            string = self.append_adjacent_nodes(level + "    ", string, key, adjacent,)
        string += f"{level}  }}\n"
        string += f"{level}}}\n"
        return string

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

    def promote_righmost_sibling(self) -> None:
        grand_parent = self
        parent = grand_parent.get_right_operand()

        if not isinstance(parent, OperatorNode) or parent.get_right_operand() is None:
            error = (
                f"Node {self.node_type} tried to remove rightmost "
                f"without having grand children"
            )
            raise IndexError(error)

        current = parent.get_right_operand()
        while isinstance(current, Node):
            right = current.get_adjacent(Operand.RIGHT)
            if right is None:
                # move sibling up
                left = parent.get_left_operand()
                # move sibling up
                grand_parent.set_left_operand(left)
                return
            grand_parent = parent
            parent = current
            current = right

        left = parent.get_left_operand()
        grand_parent.set_left_operand(left)

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

class NameNode(Node):
    def __init__(self, identifier: str) -> None:
        super().__init__("name")
        self.id = identifier
        self.max_adjacents = 0
        # No tiene adyacentes

    def __repr__(self) -> str:
        return f"(Node {self.node_type} with id: {self.id})"

    def to_string(self, level: str) -> str:
        string = f"{level}{"{"}\n"
        string += f"{level}Node: {self.node_type}\n"
        string += f"{level}Id: {self.id}\n"
        string += f"{level}{"}"}\n"
        return string


# temp node, pass potato up to do evil things
class EpicNode(Node):
    def __init__(self, max_adjacents: int) -> None:
        super().__init__("epic")
        self.max_adjacents = max_adjacents

    def __repr__(self) -> str:
        return f"(Node {self.node_type})"
