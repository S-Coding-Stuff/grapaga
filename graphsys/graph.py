from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass(frozen=True)
class Node:
    id: int | float | str # ID
    label: str | None = None # Optional label
    

    def __str__(self) -> str:
        return str(self.id)


@dataclass(frozen=True)
class Edge:
    source: Node
    target: Node
    weight: float = 1.0
    label: str | None = None # Optional label

    def __str__(self) -> str:
        return f"{self.source} -> {self.target} ({self.weight})"

class Graph:
    def __init__(self, directed: bool = False):
        self.directed = directed
        self._nodes_by_value: dict[int | float | str, Node] = {}
        self._adj_out: dict[Node, dict[Node, float]] = {}
        self._adj_in: dict[Node, dict[Node, float]] = {}
        
        # Data features for each node and edge
        # self._node_features: dict[Node, np.ndarray] = {}
        # self._edge_features: dict[tuple[Node, Node], np.ndarray] = {}


    @staticmethod
    def _node_value(node: Node | int | float | str) -> int | float | str:
        return node.id if isinstance(node, Node) else node


    @staticmethod
    def _edge_sort_key(edge: Edge) -> tuple[int, int | float | str, float]:
        return (
            0 if isinstance(edge.target.id, (int, float)) else 1,
            edge.target.id if isinstance(edge.target.id, (int, float)) else str(edge.target.id),
            edge.weight,
        )


    @staticmethod
    def _node_sort_key(node: Node) -> tuple[int, int | float | str]:
        return (
            0 if isinstance(node.id, (int, float)) else 1,
            node.id if isinstance(node.id, (int, float)) else str(node.id),
        )


    def _coerce_node(self, node_or_val: Node | int | float | str) -> Node:
        value = self._node_value(node_or_val)
        existing = self._nodes_by_value.get(value)
        if existing is not None:
            return existing

        node = node_or_val if isinstance(node_or_val, Node) else Node(value)
        self._nodes_by_value[value] = node
        self._adj_out[node] = {}
        self._adj_in[node] = {}
        return node


    def all_nodes(self) -> list[Node]:
        return sorted(self._nodes_by_value.values(), key=self._node_sort_key)


    @property
    def count(self) -> dict:
        return {"Nodes": len(self._nodes_by_value), "Edges": sum(len(targets) for targets in self._adj_out.values())}


    def add_edge(self, u: Node | int | float | str, v: Node | int | float | str, weight: float = 1.0) -> None:
        source = self._coerce_node(u)
        target = self._coerce_node(v)
        self._adj_out[source][target] = weight
        self._adj_in[target][source] = weight

        if not self.directed:
            self._adj_out[target][source] = weight
            self._adj_in[source][target] = weight


    def add_node(self, node: Node | int | float | str) -> None:
        self._coerce_node(node)


    # Backward-compatible aliases for older callers.
    addEdge = add_edge
    addNode = add_node


    def get_node(self, node_or_val) -> Node | None:
        return self._nodes_by_value.get(self._node_value(node_or_val))


    def getEdge(self, source, target) -> Edge | None:
        source_node = self.getNode(source)
        target_node = self.getNode(target)

        if source_node is None or target_node is None:
            return None

        weight = self._adj_out[source_node].get(target_node)
        if weight is None:
            return None
        return Edge(source_node, target_node, weight)


    def removeNode(self, node: Node | int | float | str) -> None:
        stored_node = self.getNode(node)
        if stored_node is None:
            return

        for target in list(self._adj_out[stored_node]):
            del self._adj_in[target][stored_node]
        for source in list(self._adj_in[stored_node]):
            del self._adj_out[source][stored_node]

        del self._adj_out[stored_node]
        del self._adj_in[stored_node]
        del self._nodes_by_value[stored_node.id]


    def removeEdge(self, source, target) -> None:
        source_node = self.getNode(source)
        target_node = self.getNode(target)

        if source_node is None or target_node is None:
            return

        if target_node not in self._adj_out[source_node]:
            return

        del self._adj_out[source_node][target_node]
        del self._adj_in[target_node][source_node]

        if not self.directed and source_node in self._adj_out[target_node]:
            del self._adj_out[target_node][source_node]
            del self._adj_in[source_node][target_node]


    def hasNode(self, node: Node | int | float | str) -> bool:
        return self._node_value(node) in self._nodes_by_value


    def hasEdge(self, source: Node | int | float | str, target: Node | int | float | str) -> bool:
        return self.getEdge(source, target) is not None


    def outgoingEdges(self, node_or_val) -> List[Edge]:
        node = self.getNode(node_or_val)
        if node is None:
            return []

        out_edges = [Edge(node, target, weight) for target, weight in self._adj_out[node].items()]
        return sorted(out_edges, key=self._edge_sort_key)


    def incomingEdges(self, node_or_val) -> List[Edge]:
        node = self.getNode(node_or_val)
        if node is None:
            return []

        in_edges = [Edge(source, node, weight) for source, weight in self._adj_in[node].items()]
        return sorted(in_edges, key=self._edge_sort_key)


    def incidentEdges(self, node_or_val) -> List[Edge]:
        return sorted(set(self.outgoingEdges(node_or_val) + self.incomingEdges(node_or_val)), key=self._edge_sort_key)


    @property
    def edges(self) -> list[tuple[int | float | str, int | float | str]]:
        pairs = [
            (source.id, target.id)
            for source, targets in self._adj_out.items()
            for target in targets
        ]
        return sorted(
            pairs,
            key=lambda pair: (
                0 if isinstance(pair[0], (int, float)) else 1,
                pair[0] if isinstance(pair[0], (int, float)) else str(pair[0]),
                0 if isinstance(pair[1], (int, float)) else 1,
                pair[1] if isinstance(pair[1], (int, float)) else str(pair[1]),
            ),
        )


    @property
    def nodes(self) -> list[int | float | str]:
        return sorted(
            self._nodes_by_value.keys(),
            key=lambda value: (0, value) if isinstance(value, (int, float)) else (1, str(value)),
        )


    def neighbours(self, node: Node | int | float | str) -> list[Node]:
        stored_node = self.getNode(node)
        if stored_node is None:
            return []
        return sorted(self._adj_out[stored_node], key=self._node_sort_key)


    @classmethod
    def convert_edge_list(cls, path, directed=False, weighted=False):
        graph = cls(directed=directed)
        with open(path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.split()
                if weighted:
                    source, target, weight = parts
                    graph.add_edge(source, target, float(weight))
                else:
                    source, target = parts
                    graph.add_edge(source, target)
        return graph


    def __str__(self) -> str:
        lines = [f"Directed: {self.directed}"]
        for node in self.allNodes():
            connected = self.neighbours(node)
            lines.append(f"{node}: {[str(neighbour) for neighbour in connected]}")
        return "\n".join(lines)
    
