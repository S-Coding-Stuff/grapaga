"""Handles acyclic graph traversal algorithms, specifically for trees."""

from collections import deque
from graphsys.graph import Graph, Node


def _resolve_root(tree: Graph, root=None) -> Node | None:
    if root is not None:
        return tree.get_node(root)

    nodes = tree.all_nodes()
    if not nodes:
        return None

    if not tree.directed:
        return nodes[0]

    roots = [node for node in nodes if not tree.incoming_edges(node)]
    if len(roots) != 1:
        raise ValueError("Directed tree traversal requires exactly one root node.")
    return roots[0]


def _children(tree: Graph, node: Node, parent: Node | None = None) -> list[Node]:
    neighbours = tree.neighbours(node)
    if tree.directed or parent is None:
        return neighbours
    return [neighbour for neighbour in neighbours if neighbour != parent]


def in_order(tree: Graph, root=None) -> list[int | float | str]:
    start = _resolve_root(tree, root)
    if start is None:
        return []

    def traverse(node: Node, parent: Node | None = None) -> list[int | float | str]:
        children = _children(tree, node, parent)
        if len(children) > 2:
            raise ValueError("In-order traversal is only defined for binary trees.")

        result: list[int | float | str] = []
        if children:
            result.extend(traverse(children[0], node))
        result.append(node.id)
        if len(children) == 2:
            result.extend(traverse(children[1], node))
        return result

    return traverse(start)


def post_order(tree: Graph, root=None) -> list[int | float | str]:
    start = _resolve_root(tree, root)
    if start is None:
        return []

    def traverse(node: Node, parent: Node | None = None) -> list[int | float | str]:
        result: list[int | float | str] = []
        for child in _children(tree, node, parent):
            result.extend(traverse(child, node))
        result.append(node.id)
        return result

    return traverse(start)


def pre_order(tree: Graph, root=None) -> list[int | float | str]:
    start = _resolve_root(tree, root)
    if start is None:
        return []

    def traverse(node: Node, parent: Node | None = None) -> list[int | float | str]:
        result = [node.id]
        for child in _children(tree, node, parent):
            result.extend(traverse(child, node))
        return result

    return traverse(start)


def bfs_tree(tree: Graph, root=None) -> list[int | float | str]:
    start = _resolve_root(tree, root)
    if start is None:
        return []

    visited = {start}
    queue = deque([(start, None)])
    result: list[int | float | str] = []

    while queue:
        node, parent = queue.popleft()
        result.append(node.id)

        for child in _children(tree, node, parent):
            if child in visited:
                continue
            visited.add(child)
            queue.append((child, node))

    return result


def dfs_tree(tree: Graph, root=None) -> list[int | float | str]:
    start = _resolve_root(tree, root)
    if start is None:
        return []

    visited = set()
    stack = [(start, None)]
    result: list[int | float | str] = []

    while stack:
        node, parent = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        result.append(node.id)

        children = _children(tree, node, parent)
        for child in reversed(children):
            if child not in visited:
                stack.append((child, node))

    return result
