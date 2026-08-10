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

def a_star(graph: Graph, start: Any, end: Any, h) -> Tuple[List[Node], float, Dict[str, int]]:
    start_node = graph.get_node(start)
    end_node = graph.get_node(end)
    g_scores = {node: float("inf") for node in graph.all_nodes()}
    f_scores = {node: float("inf") for node in graph.all_nodes()}
    prev_nodes = {node: None for node in graph.all_nodes()}
    
    g_scores[start_node] = 0.0
    f_scores[start_node] = h(start_node, end_node)

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
    

