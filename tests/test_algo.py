from graphsys.algo import bfs, connected_components, dfs, dijkstra, path_exists
from graphsys.graph import Graph, Node


def test_bfs_expected_order():
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph = Graph(directed=True)
    graph.add_edge(a, b)
    graph.add_edge(a, c)

    result = bfs(graph, a)

    assert result == [a, b, c]


def test_bfs_returns_empty_list_for_missing_start():
    graph = Graph(directed=True)

    assert bfs(graph, Node("missing")) == []


def test_dfs_expected_order():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")

    graph = Graph(directed=True)
    graph.add_edge(a, b)
    graph.add_edge(a, c)
    graph.add_edge(b, d)

    result = dfs(graph, a)

    assert result == [a, b, d, c]


def test_path_exists_returns_true_for_reachable_node():
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph = Graph(directed=True)
    graph.add_edge(a, b)
    graph.add_edge(b, c)

    assert path_exists(graph, a, c) is True


def test_path_exists_returns_false_for_unreachable_node():
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph = Graph(directed=True)
    graph.add_edge(a, b)
    graph.add_node(c)

    assert path_exists(graph, a, c) is False


def test_dijkstra_returns_distances_and_previous_nodes():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")

    graph = Graph(directed=True)
    graph.add_edge(a, b, 1.0)
    graph.add_edge(a, c, 4.0)
    graph.add_edge(b, c, 2.0)
    graph.add_edge(c, d, 1.0)

    distances, previous = dijkstra(graph, a)

    assert distances[a] == 0.0
    assert distances[b] == 1.0
    assert distances[c] == 3.0
    assert distances[d] == 4.0
    assert previous[a] is None
    assert previous[b] == a
    assert previous[c] == b
    assert previous[d] == c


def test_dijkstra_marks_unreachable_nodes_as_infinite():
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph = Graph(directed=True)
    graph.add_edge(a, b, 2.0)
    graph.add_node(c)

    distances, previous = dijkstra(graph, a)

    assert distances[c] == float("inf")
    assert previous[c] is None


def test_connected_components_groups_disconnected_subgraphs():
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")
    e = Node("E")

    graph = Graph(directed=False)
    graph.add_edge(a, b)
    graph.add_edge(c, d)
    graph.add_node(e)

    result = connected_components(graph)

    assert result == [[a, b], [c, d], [e]]


def test_connected_components_uses_weak_connectivity_for_directed_graphs():
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph = Graph(directed=True)
    graph.add_edge(a, b)
    graph.add_edge(c, b)

    result = connected_components(graph)

    assert result == [[a, b, c]]
