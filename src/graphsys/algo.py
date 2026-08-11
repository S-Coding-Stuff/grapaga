from collections import deque
import heapq
from heapq import heappop, heappush
import itertools
from itertools import count
from typing import Callable, Dict, Iterable, Tuple, Any, List

from src.graphsys.graph import Graph, Node

def bfs(graph: Graph, start: Node) -> list:
    """Breadth First Search with Queue"""
    if not start or not graph.has_node(start):
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
    """DFS with Stack"""
    if not start or not graph.has_node(start):
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
    if not graph.has_node(start) or not graph.has_node(end):
        return False

    target_value = graph._node_value(end)

    for node in bfs(graph, start):
        if node.id == target_value:
            return True
    return False
    
    
def dijkstra(graph: Graph, start: Node) -> tuple[dict[Node, float], dict[Node, Node | None]]:
    if not graph.has_node(start):
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

def a_star(graph: Graph, start: Any, end: Any, heuristic) -> Tuple[List[Any], float]:
    """Return the best path from start to end using A* search."""

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
    ...
    
def connected_components(graph: Graph):
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
    ...
    

