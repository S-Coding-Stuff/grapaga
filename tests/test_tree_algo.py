import pytest

from graphsys.graph import Graph, Node
from graphsys.tree_algo import bfs_tree, dfs_tree, in_order, post_order, pre_order


def build_directed_binary_tree() -> Graph:
    tree = Graph(directed=True)
    tree.add_edge(0, 1)
    tree.add_edge(0, 2)
    tree.add_edge(1, 3)
    tree.add_edge(1, 4)
    tree.add_edge(2, 5)
    return tree


def test_pre_order_traverses_directed_tree_from_inferred_root():
    tree = build_directed_binary_tree()

    assert pre_order(tree) == [0, 1, 3, 4, 2, 5]


def test_post_order_traverses_directed_tree_from_inferred_root():
    tree = build_directed_binary_tree()

    assert post_order(tree) == [3, 4, 1, 5, 2, 0]


def test_in_order_traverses_binary_tree():
    tree = build_directed_binary_tree()

    assert in_order(tree) == [3, 1, 4, 0, 5, 2]


def test_bfs_tree_returns_node_values_in_level_order():
    tree = build_directed_binary_tree()

    assert bfs_tree(tree) == [0, 1, 2, 3, 4, 5]


def test_dfs_tree_returns_node_values_in_pre_order():
    tree = build_directed_binary_tree()

    assert dfs_tree(tree) == [0, 1, 3, 4, 2, 5]


def test_undirected_tree_requires_explicit_root_for_stable_traversal():
    tree = Graph()
    tree.add_edge("root", "left")
    tree.add_edge("root", "right")
    tree.add_edge("left", "leaf")

    assert pre_order(tree, "root") == ["root", "left", "leaf", "right"]
    assert bfs_tree(tree, "root") == ["root", "left", "right", "leaf"]


def test_in_order_rejects_non_binary_tree():
    tree = Graph(directed=True)
    tree.add_edge(0, 1)
    tree.add_edge(0, 2)
    tree.add_edge(0, 3)

    with pytest.raises(ValueError, match="binary trees"):
        in_order(tree)


def test_directed_tree_without_single_root_raises():
    tree = Graph(directed=True)
    tree.add_node(Node(1))
    tree.add_node(Node(2))

    with pytest.raises(ValueError, match="exactly one root"):
        pre_order(tree)
