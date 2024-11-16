# temp node, pass potato up to do evil things
from abstract_syntax_tree.node import Node


class EpicNode(Node):
    def __init__(self, max_adjacents: int) -> None:
        super().__init__("epic")
        self.max_adjacents = max_adjacents

    def __repr__(self) -> str:
        return f"(Node {self.node_type})"
