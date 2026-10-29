import random

from graphsys.graph import Graph, Node


def complete_graph(n: int, m: int, directed: bool = False, seed: int = 0) -> Graph:
    """Reserve an entry point for complete-graph generation.

    This function is a placeholder despite its Graph return annotation.

    :param n: Unused size parameter; semantics are not implemented.
    :type n: int
    :param m: Unused size parameter; semantics are not implemented.
    :type m: int
    :param directed: Unused direction flag; defaults to False.
    :type directed: bool
    :param seed: Unused random seed; defaults to zero.
    :type seed: int
    :returns: None; no graph is generated.
    :rtype: None
    """
    ...


def generate_grid(n: int, m: int, seed: int = 0) -> Graph:
    """Reserve an entry point for grid generation.

    This function is a placeholder despite its Graph return annotation.

    :param n: Unused size parameter; semantics are not implemented.
    :type n: int
    :param m: Unused size parameter; semantics are not implemented.
    :type m: int
    :param seed: Unused random seed; defaults to zero.
    :type seed: int
    :returns: None; no graph is generated.
    :rtype: None
    """
    ...


def tree_graph(num_nodes: int, directed: bool = False, seed=0):
    """Generate a tree by attaching each new node to an earlier node.

    Reset the global random state. For positive sizes, produce num_nodes - 1
    logical edges. Undirected graphs store both adjacency directions.

    :param num_nodes: Number of nodes, with integer IDs starting at zero.
    :type num_nodes: int
    :param directed: Whether edges point from parent to child; defaults to False.
    :type directed: bool
    :param seed: Seed for the global random generator; defaults to zero.
    :type seed: int
    :returns: Generated tree; nonpositive node counts produce an empty graph.
    :rtype: Graph
    """
    random.seed(seed)
    graph = Graph(directed=directed)
    nodes = [Node(i) for i in range(num_nodes)]
    for node in nodes:
        graph.add_node(node)

    for i in range(1, num_nodes):
        parent_node_idx = random.randrange(i)
        graph.add_edge(nodes[parent_node_idx], nodes[i])
    return graph


def random_graph(n: int, m: int, directed: bool = False, seed=0) -> Graph:
    """Generate a random graph without duplicate edges or self-loops.

    Reset the global random state. Undirected edges are stored in both
    directions. Negative sizes are not explicitly validated. Rejection
    sampling may become slow near the maximum edge count.

    :param n: Nonnegative node count; IDs range from zero to n - 1.
    :type n: int
    :param m: Nonnegative logical edge count.
    :type m: int
    :param directed: Whether edges are directed; defaults to False.
    :type directed: bool
    :param seed: Seed for the global random generator; defaults to zero.
    :type seed: int
    :returns: Graph containing the requested nodes and logical edges for valid sizes.
    :rtype: Graph
    :raises ValueError: m exceeds n * (n - 1), or half that limit when undirected.
    """
    random.seed(seed)
    graph = Graph(directed=directed)

    nodes = [Node(i) for i in range(n)]
    for node in nodes:
        graph.add_node(node)

    max_edges = n * (n - 1) if directed else n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(
            f"m must be less than or equal to {max_edges} for n={n}, directed={directed}"
        )

    edges = set()

    while len(edges) < m:
        u = random.randrange(n)
        v = random.randrange(n)

        if u == v:
            continue

        edge = (u, v) if directed else tuple(sorted((u, v)))
        if edge in edges:
            continue

        edges.add(edge)
        graph.add_edge(nodes[u], nodes[v])
    return graph
