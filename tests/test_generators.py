import pytest

from graphsys.algo import bfs
from graphsys.generators import random_graph, tree_graph
from graphsys.graph import Node


@pytest.mark.parametrize("directed", [False, True])
@pytest.mark.parametrize("n,m", [(0, 0), (1, 0), (6, 0), (6, 7), (6, 15)])
def test_random_graph_size_and_edge_invariants(directed, n, m):
    graph = random_graph(n, m, directed=directed, seed=42)
    assert graph.nodes == list(range(n))
    assert graph.count["Edges"] == m * (1 if directed else 2)
    assert all(source != target for source, target in graph.edges)
    if not directed:
        assert all(graph.has_edge(target, source) for source, target in graph.edges)


@pytest.mark.parametrize("directed,m", [(False, 7), (True, 13)])
def test_random_graph_rejects_too_many_edges(directed, m):
    with pytest.raises(ValueError, match="m must"):
        random_graph(4, m, directed=directed)


@pytest.mark.parametrize("generator, args", [(random_graph, (10, 15)), (tree_graph, (10,))])
def test_generators_reproduce_graph_for_same_seed(generator, args):
    first = generator(*args, seed=123)
    second = generator(*args, seed=123)
    assert first.nodes == second.nodes
    assert first.edges == second.edges


@pytest.mark.parametrize("directed", [False, True])
@pytest.mark.parametrize("n", [0, 1, 12])
def test_generated_tree_connected_and_has_expected_edges(directed, n):
    tree = tree_graph(n, directed=directed, seed=42)
    assert tree.nodes == list(range(n))
    assert tree.count["Edges"] == max(0, n - 1) * (1 if directed else 2)
    if n:
        assert set(bfs(tree, Node(0))) == set(tree.all_nodes())
    if directed:
        assert tree.incoming_edges(0) == []
        assert all(len(tree.incoming_edges(node)) == 1 for node in range(1, n))
