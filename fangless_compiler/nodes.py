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


class Node:
    def __init__(self, node_type: str) -> None:
        self.node_type = node_type
        self.adjacents = []
        self.max_adjacents = 0

    def add_adjacent(self, adj: "Node") -> int:
        pos = len(self.adjacents)
        if pos >= self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more than {self.max_adjacents}\n"
                " adjacents"
            )
            raise IndexError(error)

        self.adjacents.append(adj)
        return pos

    def locate_adjacent(self, adj: "Node") -> int:
        return self.adjacents.index(adj)

    def change_adjacent(self, pos: int, adj: "Node") -> None:
        if pos > self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more than {self.max_adjacents}"
                " adjacents"
            )
            raise IndexError(error)

        while pos >= len(self.adjacents):
            self.adjacents.append([])

        self.adjacents[pos] = adj

    def get_adjacent(self, pos: int) -> "Node":
        if pos > self.max_adjacents:
            error = (
                f"Node {self.node_type} can't have more than {self.max_adjacents}"
                " adjacents"
            )
            raise IndexError(error)

        while pos >= len(self.adjacents):
            self.adjacents.append([])

        return self.adjacents[pos]

    def __repr__(self) -> str:
        string = (
            f"{"{"}\nNode: {self.node_type},\n"
            f" adjacents:\n"
        )
        for adjacent in self.adjacents:
            if isinstance(adjacent, Node):
                string += adjacent.to_string("\t")
            else:
                string += f"\t{adjacent}\n"
        string += f"{"}"}"

        return string

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f"{level}Node: {self.node_type},\n"
        string += f"{level}Adjacents:\n"
        for adjacent in self.adjacents:
            string = self.append_adjacent_nodes(level, string, adjacent)
        string += f"{level}}}\n"
        return string

    def append_adjacent_nodes(self, level: str, string: str, adjacent: Any) -> None:
        if isinstance(adjacent, Node):
            string += adjacent.to_string(level + "\t")
        elif isinstance(adjacent, dict):
            for key, value in adjacent.items():
                if isinstance(value, Node):
                    string += f"{level}\t{key}: {value.to_string(level + "\t")}"
                else:
                    string += f"{level}\t{key}: {value}\n"
        elif isinstance(adjacent, list):
            for a in adjacent:
                if isinstance(a, Node):
                    string += a.to_string(level + "\t")
                else:
                    string += f"{level}\t{a}\n"
        else:
            string += f"{level}\t{adjacent}\n"
        return string

    def get_leaves(self) -> list["Node"]:
        if len(self.adjacents) == 0:
            return [self]
        nodes = []
        for adjacent in self.adjacents:
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
    def try_evaluate(self) -> bool: ...

    def __repr__(self) -> str:
        string = (
            f"{"{"}\nNode: {self.node_type},\n"
            f"operator: {self.operator}, \n"
            f"parenthesis: {self.parenthesis}, \n"
            f"adjacents:\n"
        )
        for adjacent in self.adjacents:
            string = self.append_adjacent_nodes("", string, adjacent)
        string += f"{"}"}"

        return string

    def to_string(self, level: str) -> str:
        string = f"{level}{"{"}\n"
        string += f"{level}Node: {self.node_type},\n"
        string += f"{level}Operator: {self.operator},\n"
        string += f"{level}Parenthesis: {self.parenthesis},\n"
        string += f"{level}Adjacents:\n"
        for adjacent in self.adjacents:
            string = self.append_adjacent_nodes(level, string, adjacent)

        string += f"{level}{"}"}\n"
        return string


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
