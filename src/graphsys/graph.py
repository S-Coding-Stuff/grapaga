from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Node:
    """Represent an immutable graph node.

    :param id: Numeric or string node identifier.
    :type id: int | float | str
    :param label: Optional descriptive label; defaults to None.
    :type label: str | None

    Dataclass equality and hashing include both id and label. Graph lookup
    uses only id and preserves the first node inserted for an identifier.
    """

    id: int | float | str  # ID
    label: str | None = None  # Optional label - good for visualisation or classification tasks

    def __str__(self) -> str:
        """Return the node identifier as text.

        :returns: String representation of the identifier.
        :rtype: str
        """
        return str(self.id)


@dataclass(frozen=True)
class Edge:
    """Represent an immutable weighted edge.

    :param source: Source node.
    :type source: Node
    :param target: Target node.
    :type target: Node
    :param weight: Edge weight; defaults to 1.0.
    :type weight: float
    :param label: Optional descriptive label; defaults to None.
    :type label: str | None
    """

    source: Node
    target: Node
    weight: float = 1.0
    label: str | None = None  # Optional label - good for visualisation or classification tasks

    def __str__(self) -> str:
        """Format the edge endpoints and weight.

        :returns: Text in the form source -> target (weight).
        :rtype: str
        """
        return f"{self.source} -> {self.target} ({self.weight})"


class Graph:
    """Store a directed or undirected weighted graph.

    Node identifiers are unique within a graph. Undirected edges are stored
    in both adjacency directions, except self-loops, which are stored once.
    Numeric identifiers sort before string identifiers.

    :ivar directed: Whether edges have a direction.
    :vartype directed: bool
    """

    def __init__(self, directed: bool = False):
        """Initialize an empty graph.

        :param directed: Whether to store directed edges; defaults to False.
        :type directed: bool
        :returns: None.
        :rtype: None
        """
        self.directed = directed
        self._nodes_by_value: dict[int | float | str, Node] = {}
        self._adj_out: dict[Node, dict[Node, float]] = {}
        self._adj_in: dict[Node, dict[Node, float]] = {}

        # Data features for each node and edge
        self._node_features: dict[Node, np.ndarray] = {}
        self._edge_features: dict[tuple[Node, Node], np.ndarray] = {}

    @staticmethod
    def _node_value(node: Node | int | float | str) -> int | float | str:
        """Extract a node identifier.

        :param node: Node or node ID to resolve.
        :type node: Node | int | float | str
        :returns: The node ID, or the supplied raw identifier.
        :rtype: int | float | str
        """
        return node.id if isinstance(node, Node) else node

    @staticmethod
    def _edge_sort_key(edge: Edge) -> tuple[int, int | float | str, float]:
        """Build an ordering key for an edge.

        :param edge: Edge to order.
        :type edge: Edge
        :returns: Target type group, target ID, and weight; numeric IDs precede strings.
        :rtype: tuple[int, int | float | str, float]
        """
        return (
            0 if isinstance(edge.target.id, (int, float)) else 1,
            edge.target.id if isinstance(edge.target.id, (int, float)) else str(edge.target.id),
            edge.weight,
        )

    @staticmethod
    def _node_sort_key(node: Node) -> tuple[int, int | float | str]:
        """Build an ordering key for a node.

        :param node: Node to order.
        :type node: Node
        :returns: Type group and identifier; numeric IDs precede strings.
        :rtype: tuple[int, int | float | str]
        """
        return (
            0 if isinstance(node.id, (int, float)) else 1,
            node.id if isinstance(node.id, (int, float)) else str(node.id),
        )

    def _coerce_node(self, node_or_val: Node | int | float | str) -> Node:
        """Resolve or insert a node by identifier.

        An existing node is preserved even if the supplied label differs.

        :param node_or_val: Node or node ID to resolve.
        :type node_or_val: Node | int | float | str
        :returns: Existing stored node, or the newly inserted node.
        :rtype: Node
        """
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
        """Return all stored nodes in sorted order.

        :returns: Nodes ordered numerically first, then by string identifier.
        :rtype: list[Node]
        """
        return sorted(self._nodes_by_value.values(), key=self._node_sort_key)

    @property
    def count(self) -> dict:
        """Return node and stored adjacency entry counts.

        An undirected edge contributes two entries; a self-loop contributes one.

        :returns: Counts under the keys Nodes and Edges.
        :rtype: dict[str, int]
        """
        return {
            "Nodes": len(self._nodes_by_value),
            "Edges": sum(len(targets) for targets in self._adj_out.values()),
        }

    def add_edge(
        self, u: Node | int | float | str, v: Node | int | float | str, weight: float = 1.0
    ) -> None:
        """Insert or update an edge and ensure both endpoints exist.

        Existing edge weights are replaced. Undirected graphs also update the
        reverse adjacency. Weights are not validated.

        :param u: Source node or node ID.
        :type u: Node | int | float | str
        :param v: Target node or node ID.
        :type v: Node | int | float | str
        :param weight: Weight to store; defaults to 1.0.
        :type weight: float
        :returns: None.
        :rtype: None
        """
        source = self._coerce_node(u)
        target = self._coerce_node(v)
        self._adj_out[source][target] = weight
        self._adj_in[target][source] = weight

        if not self.directed:
            self._adj_out[target][source] = weight
            self._adj_in[source][target] = weight

    def add_node(self, node: Node | int | float | str) -> None:
        """Insert a node unless its identifier is already stored.

        Preserve the original stored node and label when its ID already exists.

        :param node: Node or node ID to resolve.
        :type node: Node | int | float | str
        :returns: None.
        :rtype: None
        """
        self._coerce_node(node)

    def get_node(self, node_or_val) -> Node | None:
        """Look up a stored node by identifier.

        :param node_or_val: Node or node ID to resolve.
        :type node_or_val: Node | int | float | str
        :returns: Stored node, or None if the identifier is absent.
        :rtype: Node | None
        """
        return self._nodes_by_value.get(self._node_value(node_or_val))

    def get_edge(self, source, target) -> Edge | None:
        """Look up an edge between two endpoints.

        :param source: Source node or node ID.
        :type source: Node | int | float | str
        :param target: Target node or node ID.
        :type target: Node | int | float | str
        :returns: Edge with stored endpoints and weight, or None if absent.
        :rtype: Edge | None
        """
        source_node = self.get_node(source)
        target_node = self.get_node(target)

        if source_node is None or target_node is None:
            return None

        weight = self._adj_out[source_node].get(target_node)
        if weight is None:
            return None
        return Edge(source_node, target_node, weight)

    def remove_node(self, node: Node | int | float | str) -> None:
        """Remove a node and its incoming and outgoing adjacency entries.

        Do nothing if the node is absent.

        :param node: Node or node ID to resolve.
        :type node: Node | int | float | str
        :returns: None.
        :rtype: None
        """
        stored_node = self.get_node(node)
        if stored_node is None:
            return

        for target in list(self._adj_out[stored_node]):
            del self._adj_in[target][stored_node]
        for source in list(self._adj_in[stored_node]):
            del self._adj_out[source][stored_node]

        del self._adj_out[stored_node]
        del self._adj_in[stored_node]
        del self._nodes_by_value[stored_node.id]

    def remove_edge(self, source, target) -> None:
        """Remove an edge between two endpoints.

        Also remove the reverse adjacency in undirected graphs. Do nothing
        if either endpoint or the edge is absent.

        :param source: Source node or node ID.
        :type source: Node | int | float | str
        :param target: Target node or node ID.
        :type target: Node | int | float | str
        :returns: None.
        :rtype: None
        """
        source_node = self.get_node(source)
        target_node = self.get_node(target)

        if source_node is None or target_node is None:
            return

        if target_node not in self._adj_out[source_node]:
            return

        del self._adj_out[source_node][target_node]
        del self._adj_in[target_node][source_node]

        if not self.directed and source_node in self._adj_out[target_node]:
            del self._adj_out[target_node][source_node]
            del self._adj_in[source_node][target_node]

    def has_node(self, node: Node | int | float | str) -> bool:
        """Check whether a node identifier is stored.

        :param node: Node or node ID to resolve.
        :type node: Node | int | float | str
        :returns: Whether the identifier exists.
        :rtype: bool
        """
        return self._node_value(node) in self._nodes_by_value

    def has_edge(self, source: Node | int | float | str, target: Node | int | float | str) -> bool:
        """Check whether an edge exists between two endpoints.

        :param source: Source node or node ID.
        :type source: Node | int | float | str
        :param target: Target node or node ID.
        :type target: Node | int | float | str
        :returns: Whether the edge exists.
        :rtype: bool
        """
        return self.get_edge(source, target) is not None

    def outgoing_edges(self, node_or_val) -> list[Edge]:
        """Return edges leaving a node.

        :param node_or_val: Node or node ID to resolve.
        :type node_or_val: Node | int | float | str
        :returns: Edges sorted by target type group, target ID, then weight; empty if absent.
        :rtype: list[Edge]
        """
        node = self.get_node(node_or_val)
        if node is None:
            return []

        out_edges = [Edge(node, target, weight) for target, weight in self._adj_out[node].items()]
        return sorted(out_edges, key=self._edge_sort_key)

    def incoming_edges(self, node_or_val) -> list[Edge]:
        """Return edges entering a node.

        All returned edges share a target. Equal-weight ties preserve adjacency
        insertion order; edges are not sorted by source identifier.

        :param node_or_val: Node or node ID to resolve.
        :type node_or_val: Node | int | float | str
        :returns: Edges sorted by target type group, target ID, then weight; empty if absent.
        :rtype: list[Edge]
        """
        node = self.get_node(node_or_val)
        if node is None:
            return []

        in_edges = [Edge(source, node, weight) for source, weight in self._adj_in[node].items()]
        return sorted(in_edges, key=self._edge_sort_key)

    def incident_edges(self, node_or_val) -> list[Edge]:
        """Return distinct incoming and outgoing edges for a node.

        A self-loop appears once. Ordering among equal sort keys is unspecified.

        :param node_or_val: Node or node ID to resolve.
        :type node_or_val: Node | int | float | str
        :returns: Edges sorted by target type group, target ID, then weight; empty if absent.
        :rtype: list[Edge]
        """
        return sorted(
            set(self.outgoing_edges(node_or_val) + self.incoming_edges(node_or_val)),
            key=self._edge_sort_key,
        )

    @property
    def edges(self) -> list[tuple[int | float | str, int | float | str]]:
        """Return all stored source and target identifier pairs.

        Weights are omitted. Undirected non-loop edges appear in both directions.

        :returns: Pairs sorted by source and then target, with numeric IDs before strings.
        :rtype: list[tuple[int | float | str, int | float | str]]
        """
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
        """Return all node identifiers in sorted order.

        :returns: Numeric identifiers followed by string identifiers, sorted within each group.
        :rtype: list[int | float | str]
        """
        return sorted(
            self._nodes_by_value.keys(),
            key=lambda value: (0, value) if isinstance(value, (int, float)) else (1, str(value)),
        )

    def neighbours(self, node: Node | int | float | str) -> list[Node]:
        """Return the outgoing neighbours of a node.

        :param node: Node or node ID to resolve.
        :type node: Node | int | float | str
        :returns: Stored neighbours in node sort order, or an empty list if absent.
        :rtype: list[Node]
        """
        stored_node = self.get_node(node)
        if stored_node is None:
            return []
        return sorted(self._adj_out[stored_node], key=self._node_sort_key)

    @classmethod
    def convert_edge_list(cls, path, directed=False, weighted=False):
        """Load a graph from a whitespace-delimited edge-list file.

        Ignore blank lines and lines whose stripped text begins with #. Each
        remaining line must contain two columns, or three when weighted is True.
        Repeated edges replace earlier weights. Unweighted edges use weight 1.0.

        :param path: Path to the input text file.
        :type path: str | os.PathLike
        :param directed: Whether the resulting graph is directed; defaults to False.
        :type directed: bool
        :param weighted: Whether each line has a third weight column; defaults to False.
        :type weighted: bool
        :returns: Graph with string node IDs and float weights for weighted input.
        :rtype: Graph
        :raises OSError: The file cannot be opened or read.
        :raises ValueError: A row has an incorrect column count or an invalid float weight.
        """
        graph = cls(directed=directed)
        with open(path) as file:
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
        """Format graph direction and sorted adjacency lists.

        :returns: Multiline graph description with each node and its outgoing neighbours.
        :rtype: str
        """
        lines = [f"Directed: {self.directed}"]
        for node in self.all_nodes():
            connected = self.neighbours(node)
            lines.append(f"{node}: {[str(neighbour) for neighbour in connected]}")
        return "\n".join(lines)
