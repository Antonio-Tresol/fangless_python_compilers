from enum import Enum
from typing import Any


class OperatorType(Enum):
    IF = "if"
    FUNCTION_CALL = "function_call"
    METHOD_CALL = "method_call"
    ATTRIBUTE_CALL = "attribute_call"
    SLICING = "slicing"
    INDEXING = "indexing"
    ASSIGNATION = "="


NIL_NODE = None

AdjacentKey = int | float | str | tuple


class Node:
    def __init__(self, node_type: str) -> None:
        self.node_type = node_type
        self.adjacents = {}
        self.max_adjacents = 0

    def add_adjacent(self, adj: "Node") -> int:
        pos = len(self.adjacents)
        if pos >= self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more"
                f" than {self.max_adjacents} adjacents"
            )
            raise IndexError(error)

        self.adjacents[pos] = adj
        return pos

    def locate_adjacent(self, adj: "Node") -> int:
        for pos, node in self.adjacents.items():
            if node == adj:
                return pos
        msg = f"Adjacent node not found in {self.node_type}"
        raise ValueError(msg)

    def change_adjacent(self, key: AdjacentKey, adj: "Node") -> None:
        if key >= self.max_adjacents or key not in self.adjacents:
            error = (
                f"Node {self.node_type} tried to change"
                f"nonexistent adjacent at position {key}"
            )
            raise IndexError(error)

        self.adjacents[key] = adj

    def get_adjacent(self, key: AdjacentKey) -> "Node":
        if key >= self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more "
                f"than {self.max_adjacents} adjacents"
            )
            raise IndexError(error)

        if key not in self.adjacents:
            error = f"Node {self.node_type} has no adjacent at position {key}"
            raise IndexError(error)

        return self.adjacents[key]

    def __repr__(self) -> str:
        string = (
            "{\n"
            f"Node: {self.node_type},\n"
            "adjacents:\n"
        )
        for key, adjacent in self.adjacents.items():
            if isinstance(adjacent, Node):
                string += adjacent.to_string("\t")
            else:
                string += f"\t{key}: {adjacent}\n"
        string += "}"
        return string

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f"{level}Node: {self.node_type},\n"
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
            string += f"{level}\tKey: {key}\n"
            string += adjacent.to_string(level + "\t")
        elif isinstance(adjacent, dict):
            string += f"{level}\tKey: {key}\n"
            for subkey, value in adjacent.items():
                if isinstance(value, Node):
                    string += f"{level}\t{subkey}: {value.to_string(level + '\t')}"
                else:
                    string += f"{level}\t{subkey}: {value}\n"
        elif isinstance(adjacent, list):
            string += f"{level}\tKey: {key}\n"
            for a in adjacent:
                if isinstance(a, Node):
                    string += a.to_string(level + "\t")
                else:
                    string += f"{level}\t{a}\n"
        else:
            string += f"{level}\t{key}: {adjacent}\n"
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
        self.operator = operator
        self.parenthesis = False
        self.max_adjacents = 2
        # mis adjacentes son mis operandos

    # TODO
    def try_evaluate(self) -> bool:
        ...

    def __repr__(self) -> str:
        string = f"{"{"}\n"
        string += f"Node: {self.node_type},\n"
        string += f"Operator: {self.operator},\n"
        if self.parenthesis:
            string += f"Parenthesis: {self.parenthesis},\n"
        string += "Adjacents:\n"
        for key, adjacent in self.adjacents.items():
            string = self.append_adjacent_nodes("", string, key, adjacent)
        string += "}"

        return string

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f"{level}Node: {self.node_type},\n"
        string += f"{level}Operator: {self.operator},\n"
        if self.parenthesis:
            string += f"{level}Parenthesis: {self.parenthesis},\n"
        string += f"{level}Adjacents:\n"
        for key, adjacent in self.adjacents.items():
            string = self.append_adjacent_nodes(level, string, key, adjacent)

        string += f"{level}}}\n"
        return string

    def add_left_child(self, value: Any) -> None:
        self.adjacents["left"] = value

    def add_right_child(self, value: Any) -> None:
        self.adjacents["right"] = value

    def add_left_child(self, value: Any) -> None:
        self.adjacents["left"] = value

    def add_right_child(self, value: Any) -> None:
        self.adjacents["right"] = value





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
