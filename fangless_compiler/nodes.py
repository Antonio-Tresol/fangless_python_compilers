from enum import Enum

class OperatorType(Enum):
    IF = "if"
    FUNCTION_CALL = "function_call"
    METHOD_CALL = "method_call"
    ATTRIBUTE_CALL = "attribute_call"
    SLICING = "slicing"
    INDEXING = "indexing"

NIL_NODE = None

class Node:
    def __init__(self, node_type: str) -> None:
        self.node_type = node_type
        self.adjacents = []
        self.max_adjacent = 0

    def add_adjacent(self, adj: "Node") -> int:
        pos = len(self.adjacents)
        if pos >= self.max_adjacent:
            error = (
                f"Node {self.node_type} can't have more than {self.max_adjacent} adjacents"
            )
            raise IndexError(error)

        self.adjacents.append(adj)

        return pos

    def locate_adjacent(self, adj: "Node") -> int:
        return self.adjacents.index(adj)

    def change_adjacent(self, pos: int, adj: "Node") -> None:
        if pos > self.max_adjacent:
            error = (
                f"Node {self.node_type} can't have more than {self.max_adjacent} adjacents"
            )
            raise IndexError(error)

        if pos >= len(self.adjacents):
            self.adjacents.append([])

        self.add_adjacent[pos] = adj

    def get_adjacent(self, pos: int) -> "Node":
        if pos > self.max_adjacent:
            error = (
                f"Node {self.node_type} can't have more than {self.max_adjacent} adjacents"
            )
            raise IndexError(error)

        if pos >= len(self.adjacents):
            self.adjacents.append([])

        return self.adjacents[pos]

    def __repr__(self):
        return f"(Node {self.node_type}, max_adjacents {self.max_adjacent}, adjacents {self.adjacents})"

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f"{level}Node: {self.node_type},\n"
        string += f"{level}Adjacents:\n"
        for adjacent in self.adjacents:
            if isinstance(adjacent, Node):
                string += adjacent.to_string(level + "\t")
            else:
                string += f"{level}\t{adjacent}\n"
        string += f"{level}}}\n"
        return string



class OperatorNode(Node):
    def __init__(self, operator: OperatorType) -> None:
        super().__init__("operator")
        self.operator = operator
        self.parenthesis = False
        self.max_adjacent = 2
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
            if isinstance(adjacent, Node):
                string += adjacent.to_string("\t")
            else:
                string += f"\t{adjacent}\n"
        string += f"{"}"}"

        return string

    def to_string(self, level: str) -> str:
        string = f"{level}{{\n"
        string += f"{level}Node: {self.node_type},\n"
        string += f"{level}Operator: {self.operator},\n"
        string += f"{level}Parenthesis: {self.parenthesis},\n"
        string += f"{level}Adjacents:\n"
        for adjacent in self.adjacents:
            if isinstance(adjacent, Node):
                string += adjacent.to_string(level + "\t")
            else:
                string += f"{level}\t{adjacent}\n"
        string += f"{level}}}\n"
        return string


class NameNode(Node):
    def __init__(self, identifier: str) -> None:
        super().__init__("name")
        self.id = identifier
        self.max_adjacent = 0
        # No tiene adyacentes

    def __repr__(self) -> str:
        return f"(Node {self.node_type} with id: {self.id})"

    def to_string(self, level: str) -> str:
        string = f"{level}{"{"}\n"
        string += f"{level}Node: {self.node_type}\n"
        string += f"{level}Id: {self.id}\n"
        string += f"{level}{"}"}\n"
        return string


class EpicNode(Node):
    def __init__(self, max_adjacents: int) -> None:
        super().__init__("epic")
        self.max_adjacents = max_adjacents

    def __repr__(self) -> str:
        return f"(Node {self.node_type})"
