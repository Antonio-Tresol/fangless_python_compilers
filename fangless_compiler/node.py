class Node:
    def __init__(self, node_type: str) -> None:
        self.node_type = node_type
        self.adjacents = []
        self.max_adjacent = 0

    def add_adjecent(self, adj: "Node") -> int:
        pos = len(self.adjacents)
        if pos >= self.max_adjacent:
            error = (
                f"{self.__class__} can't have more than "
                f"{self.max_adjacent} adjacents"
            )
            raise IndexError(error)
        self.adjacents.append(adj)
        return pos

    def locate_adjecent(self, adj: "Node") -> int:
        return self.adjacents.index(adj)

    def change_adjecent(self, pos: int, adj: "Node") -> None:
        if pos >= len(self.adjacents):
            error = "Tried to change unexistent adjacent node"
            raise IndexError(error)
        self.add_adjecent[pos] = adj


class OperatorNode(Node):
    def __init__(self, operator: str, node_type: str) -> None:
        super().__init__(node_type)
        self.operator = operator
        self.max_adjacent = 2
        # mis adjacentes son mis operandos

    # TODO (Joe)
    def try_evaluate(self) -> bool: ...


class VariableNode(Node):
    def __init__(self, identifier: str, node_type: str) -> None:
        super().__init__(node_type)
        self.id = identifier
        self.max_adjacent = 0
        # No tiene adyacentes
