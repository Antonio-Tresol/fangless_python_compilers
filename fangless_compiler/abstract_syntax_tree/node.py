from typing import Any, Union
NIL_NODE = None

AdjacentKey = int | float | str | tuple


class Node:
    def __init__(self, node_type: str) -> None:
        self.node_type = node_type
        self.adjacents = {}
        self.max_adjacents = 0

    def is_leaf(self) -> bool:
        return len(self.adjacents) == 0

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

    def get_adjacent(self, key: AdjacentKey) -> Union["Node", None]:
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

    def add_deepest(self, key: AdjacentKey, new: "Node") -> None:
        """Supposes there is a path between the root and the deepest made of 'key'"""
        current = self
        while isinstance(current, Node):
            right = current.get_adjacent(key)
            if right is None:
                current.add_named_adjacent(key, new)
                break
            current = right
