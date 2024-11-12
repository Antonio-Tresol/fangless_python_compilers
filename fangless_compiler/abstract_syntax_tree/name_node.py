from abstract_syntax_tree.node import Node


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
