"""Regression tests for graph identity, mutation, traversal, and shortest paths."""

import pytest

from graphsys.algo import a_star, bfs, connected_components, dfs, dijkstra, path_exists
from graphsys.graph import Edge, Graph, Node


@pytest.mark.parametrize("directed", [False, True])
def test_edge_update_keeps_adjacency_consistent(directed):
    graph = Graph(directed=directed)
    graph.add_edge("a", "b", 4)
    graph.add_edge("a", "b", 0)

    assert graph.outgoing_edges("a") == [Edge(Node("a"), Node("b"), 0)]
    assert graph.incoming_edges("b") == [Edge(Node("a"), Node("b"), 0)]
    assert graph.count["Edges"] == (1 if directed else 2)
    if not directed:
        assert graph.get_edge("b", "a").weight == 0


@pytest.mark.parametrize("directed", [False, True])
@pytest.mark.parametrize("operation", ["remove_edge", "remove_node"])
def test_self_loop_can_be_removed(directed, operation):
    graph = Graph(directed=directed)
    graph.add_edge("a", "a")
    assert len(graph.incident_edges("a")) == 1

    if operation == "remove_edge":
        graph.remove_edge("a", "a")
        assert graph.has_node("a")
    else:
        graph.remove_node("a")
        assert not graph.has_node("a")
    assert graph.edges == []
    assert graph.incoming_edges("a") == []
    assert graph.outgoing_edges("a") == []


@pytest.mark.parametrize("directed", [False, True])
def test_remove_node_cleans_neighbour_adjacency(directed):
    graph = Graph(directed=directed)
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")
    graph.add_edge("a", "c", 3)
    graph.remove_node("b")
    graph.remove_node("missing")

    assert graph.nodes == ["a", "c"]
    assert all(
        edge.source.id != "b" and edge.target.id != "b"
        for node in graph.all_nodes()
        for edge in graph.incident_edges(node)
    )
    assert graph.get_edge("a", "c").weight == 3


def test_duplicate_node_id_preserves_original_node():
    graph = Graph()
    original = Node("a", label="original")
    graph.add_node(original)
    graph.add_node(Node("a", label="replacement"))
    graph.add_edge("a", "b")

    assert graph.get_node("a") is original
    assert graph.get_edge("a", "b").source is original
    assert graph.count["Nodes"] == 2


@pytest.mark.parametrize("traversal", [bfs, dfs])
@pytest.mark.parametrize("start", [0, Node(0), Node(0, label="alternate")])
def test_traversal_normalizes_start_and_visits_cycles_once(traversal, start):
    graph = Graph(directed=True)
    graph.add_edge(0, 0)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.add_node(3)

    assert traversal(graph, start) == [Node(0), Node(1), Node(2)]


@pytest.mark.parametrize("traversal", [bfs, dfs])
def test_traversal_empty_and_missing_start(traversal):
    assert traversal(Graph(), Node("missing")) == []


def test_reachability_respects_direction_and_identity():
    graph = Graph(directed=True)
    graph.add_edge(0, 1)
    assert path_exists(graph, 0, 1)
    assert path_exists(graph, 0, 0)
    assert not path_exists(graph, 1, 0)
    assert not path_exists(graph, 0, "missing")


@pytest.mark.parametrize("start", [0, Node(0), Node(0, label="alternate")])
def test_dijkstra_normalizes_start_and_handles_ties_and_stale_entries(start):
    graph = Graph(directed=True)
    for source, target, weight in [
        (0, "a", 8),
        (0, 1, 1),
        (0, "b", 1),
        (1, "a", 1),
        ("a", "goal", 0),
    ]:
        graph.add_edge(source, target, weight)
    graph.add_node("isolated")

    distances, previous = dijkstra(graph, start)

    assert distances == {
        Node(0): 0,
        Node(1): 1,
        Node("a"): 2,
        Node("b"): 1,
        Node("goal"): 2,
        Node("isolated"): float("inf"),
    }
    assert previous[Node("a")] == Node(1)
    assert previous[Node("goal")] == Node("a")
    assert previous[Node(0)] is None
    assert previous[Node("isolated")] is None


def test_dijkstra_missing_start():
    assert dijkstra(Graph(), Node("missing")) == ({}, {})


def test_a_star_with_consistent_nonzero_heuristic():
    graph = Graph(directed=True)
    graph.add_edge("a", "b", 2)
    graph.add_edge("b", "goal", 2)
    graph.add_edge("a", "goal", 7)
    estimates = {"a": 4, "b": 2, "goal": 0}
    path, cost = a_star(graph, "a", "goal", lambda node, goal: estimates[node.id])
    assert path == ["a", "b", "goal"]
    assert cost == 4


def test_a_star_existing_but_unreachable_goal():
    graph = Graph(directed=True)
    graph.add_edge("a", "b")
    graph.add_node("goal")
    assert a_star(graph, "a", "goal", lambda node, goal: 0) == ([], float("inf"))


def test_components_empty_and_self_loop():
    assert connected_components(Graph()) == []
    graph = Graph()
    graph.add_edge(0, 0)
    graph.add_node(1)
    assert connected_components(graph) == [[Node(0)], [Node(1)]]
