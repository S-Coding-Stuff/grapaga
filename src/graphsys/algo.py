from collections import deque
from heapq import heappop, heappush
from itertools import count
from typing import Any

from graphsys.graph import Graph, Node


def bfs(graph: Graph, start: Node) -> list:
    """Traverse reachable nodes in breadth-first order.

    Follow outgoing edges in directed graphs and consider neighbours in
    sorted order. Each stored node is returned at most once.

    :param graph: Graph to traverse.
    :type graph: Graph
    :param start: Starting node or node ID, resolved to the stored node.
    :type start: Node | int | float | str
    :returns: Stored nodes in traversal order, including start, or an empty
        list if start is absent.
    :rtype: list[Node]
    """
    start = graph.get_node(start)
    if start is None:
        return []

    queue = deque([start])
    visited = set()
    visited.add(start)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.neighbours(node):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order


def dfs(graph: Graph, start: Node) -> list:
    """Traverse reachable nodes using a depth-first stack traversal.

    Follow outgoing edges in directed graphs. Push neighbours in reverse
    sorted order and mark them visited when pushed. Each stored node is
    returned at most once.

    :param graph: Graph to traverse.
    :type graph: Graph
    :param start: Starting node or node ID, resolved to the stored node.
    :type start: Node | int | float | str
    :returns: Stored nodes in traversal order, including start, or an empty
        list if start is absent.
    :rtype: list[Node]
    """
    start = graph.get_node(start)
    if start is None:
        return []
    stack = [start]
    visited = set()
    visited.add(start)
    order = []
    while stack:
        node = stack.pop()
        order.append(node)
        for neighbour in reversed(graph.neighbours(node)):
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)
    return order


def path_exists(graph, start: Node, end: Node):
    """Check whether end is reachable from start.

    Follow outgoing edges in directed graphs. Identical endpoints are
    reachable when the node exists in the graph.

    :param graph: Graph to search.
    :type graph: Graph
    :param start: Starting node or node ID.
    :type start: Node | int | float | str
    :param end: Target node or node ID.
    :type end: Node | int | float | str
    :returns: Whether a route exists; False if either endpoint is absent.
    :rtype: bool
    """
    if not graph.has_node(start) or not graph.has_node(end):
        return False

    target_value = graph._node_value(end)

    for node in bfs(graph, start):
        if node.id == target_value:
            return True
    return False


def dijkstra(graph: Graph, start: Node) -> tuple[dict[Node, float], dict[Node, Node | None]]:
    """Compute shortest-path distances using Dijkstra's algorithm.

    Follow outgoing edges in directed graphs. Edge weights must be finite
    and nonnegative; this precondition is not validated.

    :param graph: Weighted graph to search.
    :type graph: Graph
    :param start: Starting node or node ID, resolved to the stored node.
    :type start: Node | int | float | str
    :returns: A pair of distance and predecessor dictionaries keyed by stored
        nodes. Unreachable nodes have infinite distance and no predecessor.
        The start has distance zero and no predecessor. Both dictionaries
        are empty if start is absent.
    :rtype: tuple[dict[Node, float], dict[Node, Node | None]]
    """
    start = graph.get_node(start)
    if start is None:
        return {}, {}

    distances = {node: float("inf") for node in graph.all_nodes()}
    previous = {node: None for node in graph.all_nodes()}
    distances[start] = 0.0

    queue_order = count()
    priority_queue = [(0.0, next(queue_order), start)]

    while priority_queue:
        current_distance, _, current_node = heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for edge in graph.outgoing_edges(current_node):
            neighbour = edge.target
            new_distance = current_distance + edge.weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_node
                heappush(priority_queue, (new_distance, next(queue_order), neighbour))

    return distances, previous


def a_star(graph: Graph, start: Any, end: Any, heuristic) -> tuple[list[Any], float]:
    """Search for a shortest path using A*.

    Follow outgoing edges in directed graphs. Shortest-path guarantees
    require finite, nonnegative weights and a consistent heuristic that is
    zero at the goal, since processed nodes are not reopened. These
    preconditions are not validated. A zero heuristic is supported.

    :param graph: Weighted graph to search.
    :type graph: Graph
    :param start: Starting node or node ID.
    :type start: Node | int | float | str
    :param end: Target node or node ID.
    :type end: Node | int | float | str
    :param heuristic: Estimate of remaining cost, called with the stored
        current node and goal node.
    :type heuristic: Callable[[Node, Node], float]
    :returns: A pair containing the path of node IDs and its total cost.
        Missing endpoints or an unreachable goal produce an empty path and
        infinite cost. Identical stored endpoints produce a single-node
        path with zero cost.
    :rtype: tuple[list[int | float | str], float]
    """
    start_node = graph.get_node(start)
    end_node = graph.get_node(end)

    if start_node is None or end_node is None:
        return [], float("inf")

    if start_node == end_node:
        return [start_node.id], 0.0

    g_score = {start_node: 0.0}
    previous = {}
    processed = set()
    queue_order = count()

    heap = [(heuristic(start_node, end_node), next(queue_order), start_node)]

    while heap:
        _, _, current = heappop(heap)

        if current in processed:
            continue

        if current == end_node:
            path_nodes = [current]
            while path_nodes[-1] in previous:
                path_nodes.append(previous[path_nodes[-1]])
            path_nodes.reverse()
            return [node.id for node in path_nodes], g_score[current]

        processed.add(current)

        for edge in graph.outgoing_edges(current):
            neighbour = edge.target
            tentative_cost = g_score[current] + edge.weight

            if tentative_cost < g_score.get(neighbour, float("inf")):
                g_score[neighbour] = tentative_cost
                previous[neighbour] = current
                heappush(
                    heap,
                    (tentative_cost + heuristic(neighbour, end_node), next(queue_order), neighbour),
                )

    return [], float("inf")


def detect_cycle(graph: Graph):
    """Reserve an entry point for cycle detection.

    This function is not implemented and does not inspect the graph.

    :param graph: Graph intended for cycle detection.
    :type graph: Graph
    :returns: None; this does not indicate whether a cycle exists.
    :rtype: None
    """
    ...


def connected_components(graph: Graph):
    """Find the connected components of a graph.

    Use weak connectivity for directed graphs by following incoming and
    outgoing edges. Sort nodes within each component using the graph's node
    ordering, and discover components in sorted node order.

    :param graph: Graph whose components are required.
    :type graph: Graph
    :returns: Components containing stored Node objects, including singleton
        components for isolated nodes. An empty graph produces an empty list.
    :rtype: list[list[Node]]
    """
    components = []
    visited = set()

    for start_node in graph.all_nodes():
        if start_node in visited:
            continue

        component = []
        stack = [start_node]
        visited.add(start_node)

        while stack:
            node = stack.pop()
            component.append(node)

            for edge in graph.incident_edges(node):
                neighbour = edge.target if edge.source == node else edge.source
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append(neighbour)

        components.append(sorted(component, key=graph._node_sort_key))

    return components


def top_sort(graph: Graph):
    """Reserve an entry point for topological sorting.

    This function is not implemented. It does not inspect the graph or
    validate that it is directed and acyclic.

    :param graph: Graph intended for topological sorting.
    :type graph: Graph
    :returns: None; no ordering is computed.
    :rtype: None
    """
    ...
