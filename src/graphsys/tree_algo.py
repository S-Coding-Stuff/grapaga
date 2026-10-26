"""Handles acyclic graph traversal algorithms, specifically for trees."""

from collections import deque
from graphsys.graph import Graph, Node


def _resolve_root(tree: Graph, root=None) -> Node | None:
    """Resolve an explicit root or infer a default root.

    Without an explicit root, select the first sorted node for undirected
    graphs, or the unique node with no incoming edges for directed graphs.

    :param tree: Graph whose root is needed.
    :type tree: Graph
    :param root: Root node or ID; None requests inference.
    :type root: Node | int | float | str | None
    :returns: Stored root, or None for an empty graph or absent explicit root.
    :rtype: Node | None
    :raises ValueError: A nonempty directed graph has no unique inferred root.
    """
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
    """Return sorted outgoing neighbours, excluding an undirected parent.

    :param tree: Graph containing the node.
    :type tree: Graph
    :param node: Node whose children are needed.
    :type node: Node
    :param parent: Parent to exclude in undirected graphs; defaults to None.
    :type parent: Node | None
    :returns: Neighbour nodes, excluding parent only when the graph is undirected.
    :rtype: list[Node]
    """
    neighbours = tree.neighbours(node)
    if tree.directed or parent is None:
        return neighbours
    return [neighbour for neighbour in neighbours if neighbour != parent]


def in_order(tree: Graph, root=None) -> list[int | float | str]:
    """Traverse a tree in in-order order.

    Infer a unique incoming-edge-free root for directed trees, or use the
    first sorted node for undirected trees. An explicit root restricts the
    traversal to its reachable subtree. Consider children in sorted node order.
    Assume a valid acyclic tree; cycles are not detected.
    Treat the first child as left and the second as right; a sole child is left.

    :param tree: Tree to traverse.
    :type tree: Graph
    :param root: Explicit root, or None to infer one; defaults to None.
    :type root: Node | int | float | str | None
    :returns: Node IDs in traversal order; empty for an empty tree or absent explicit root.
    :rtype: list[int | float | str]
    :raises ValueError: A nonempty directed graph has no unique inferred root.
    :raises ValueError: A visited node has more than two children.
    """
    start = _resolve_root(tree, root)
    if start is None:
        return []

    def traverse(node: Node, parent: Node | None = None) -> list[int | float | str]:
        """Collect one subtree in in-order order.

        Use the enclosing tree. Assume an acyclic tree.

        :param node: Root of the subtree.
        :type node: Node
        :param parent: Parent to exclude for undirected trees; defaults to None.
        :type parent: Node | None
        :returns: Subtree node IDs in traversal order.
        :rtype: list[int | float | str]
        :raises ValueError: A visited node has more than two children.
        """
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
    """Traverse a tree in post-order order.

    Infer a unique incoming-edge-free root for directed trees, or use the
    first sorted node for undirected trees. An explicit root restricts the
    traversal to its reachable subtree. Consider children in sorted node order.
    Assume a valid acyclic tree; cycles are not detected.

    :param tree: Tree to traverse.
    :type tree: Graph
    :param root: Explicit root, or None to infer one; defaults to None.
    :type root: Node | int | float | str | None
    :returns: Node IDs in traversal order; empty for an empty tree or absent explicit root.
    :rtype: list[int | float | str]
    :raises ValueError: A nonempty directed graph has no unique inferred root.
    """
    start = _resolve_root(tree, root)
    if start is None:
        return []

    def traverse(node: Node, parent: Node | None = None) -> list[int | float | str]:
        """Collect one subtree in post-order order.

        Use the enclosing tree. Assume an acyclic tree.

        :param node: Root of the subtree.
        :type node: Node
        :param parent: Parent to exclude for undirected trees; defaults to None.
        :type parent: Node | None
        :returns: Subtree node IDs in traversal order.
        :rtype: list[int | float | str]
        """
        result: list[int | float | str] = []
        for child in _children(tree, node, parent):
            result.extend(traverse(child, node))
        result.append(node.id)
        return result

    return traverse(start)


def pre_order(tree: Graph, root=None) -> list[int | float | str]:
    """Traverse a tree in pre-order order.

    Infer a unique incoming-edge-free root for directed trees, or use the
    first sorted node for undirected trees. An explicit root restricts the
    traversal to its reachable subtree. Consider children in sorted node order.
    Assume a valid acyclic tree; cycles are not detected.

    :param tree: Tree to traverse.
    :type tree: Graph
    :param root: Explicit root, or None to infer one; defaults to None.
    :type root: Node | int | float | str | None
    :returns: Node IDs in traversal order; empty for an empty tree or absent explicit root.
    :rtype: list[int | float | str]
    :raises ValueError: A nonempty directed graph has no unique inferred root.
    """
    start = _resolve_root(tree, root)
    if start is None:
        return []

    def traverse(node: Node, parent: Node | None = None) -> list[int | float | str]:
        """Collect one subtree in pre-order order.

        Use the enclosing tree. Assume an acyclic tree.

        :param node: Root of the subtree.
        :type node: Node
        :param parent: Parent to exclude for undirected trees; defaults to None.
        :type parent: Node | None
        :returns: Subtree node IDs in traversal order.
        :rtype: list[int | float | str]
        """
        result = [node.id]
        for child in _children(tree, node, parent):
            result.extend(traverse(child, node))
        return result

    return traverse(start)


def bfs_tree(tree: Graph, root=None) -> list[int | float | str]:
    """Traverse a tree in breadth-first order.

    Infer a unique incoming-edge-free root for directed trees, or use the
    first sorted node for undirected trees. An explicit root restricts the
    traversal to its reachable subtree. Consider children in sorted node order.
    Track visited nodes to avoid repeated visits; tree validity is not checked.

    :param tree: Tree to traverse.
    :type tree: Graph
    :param root: Explicit root, or None to infer one; defaults to None.
    :type root: Node | int | float | str | None
    :returns: Node IDs in traversal order; empty for an empty tree or absent explicit root.
    :rtype: list[int | float | str]
    :raises ValueError: A nonempty directed graph has no unique inferred root.
    """
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
    """Traverse a tree in depth-first order.

    Infer a unique incoming-edge-free root for directed trees, or use the
    first sorted node for undirected trees. An explicit root restricts the
    traversal to its reachable subtree. Consider children in sorted node order.
    Track visited nodes to avoid repeated visits; tree validity is not checked.

    :param tree: Tree to traverse.
    :type tree: Graph
    :param root: Explicit root, or None to infer one; defaults to None.
    :type root: Node | int | float | str | None
    :returns: Node IDs in traversal order; empty for an empty tree or absent explicit root.
    :rtype: list[int | float | str]
    :raises ValueError: A nonempty directed graph has no unique inferred root.
    """
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
