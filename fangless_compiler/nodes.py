class Node:
    def __init__(self, node_type: str) -> None:
        self.node_type = node_type
        self.name = "base node"
        self.adjacents = []
        self.max_adjacent = 0

    def add_adjacent(self, adj: "Node") -> int:
        pos = len(self.adjacents)
        if pos >= self.max_adjacent:
            error = (
                f"{self.name} can't have more than " f"{self.max_adjacent} adjacents"
            )
            raise IndexError(error)
        self.adjacents.append(adj)
        return pos

    def locate_adjacent(self, adj: "Node") -> int:
        return self.adjacents.index(adj)

    def change_adjacent(self, pos: int, adj: "Node") -> None:
        if pos >= len(self.adjacents):
            error = "Tried to change unexistent adjacent node"
            raise IndexError(error)
        self.add_adjacent[pos] = adj

    def __repr__(self):
        return f"{self.__class__}, max_adjacents {self.max_adjacent}, adjacents {self.adjacents}"


class OperatorNode(Node):
    def __init__(self, operator: str) -> None:
        super().__init__("operator")
        self.name = "operator node"
        self.operator = operator
        self.parenthesis = False
        self.max_adjacent = 2
        # mis adjacentes son mis operandos

    # TODO
    def try_evaluate(self) -> bool: ...


class NameNode(Node):
    def __init__(self, identifier: str) -> None:
        super().__init__("name")
        self.name = "name node"
        self.id = identifier
        self.max_adjacent = 0
        # No tiene adyacentes

    def __repr__(self) -> str:
        return f"({self.name} with id: {self.id})"
