from collections import deque
from heapq import heappop, heappush
from itertools import count

from main.graph import Graph, Node, Edge

def bfs(graph: Graph, start: Node) -> list:
    """Breadth First Search with Queue"""
    if not start or not graph.hasNode(start):
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
    if not start or not graph.hasNode(start):
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
    if not graph.hasNode(start) or not graph.hasNode(end):
        return False

    target_value = graph._node_value(end)

    for node in bfs(graph, start):
        if node.element == target_value:
            return True
    return False
    
    
def dijkstra(graph: Graph, start: Node) -> tuple[dict[Node, float], dict[Node, Node | None]]:
    if not graph.hasNode(start):
        return {}, {}

    distances = {node: float("inf") for node in graph.allNodes()}
    previous = {node: None for node in graph.allNodes()}
    distances[start] = 0.0

    queue_order = count()
    priority_queue = [(0.0, next(queue_order), start)]

    while priority_queue:
        current_distance, _, current_node = heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for edge in graph.outgoingEdges(current_node):
            neighbour = edge.target
            new_distance = current_distance + edge.weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_node
                heappush(priority_queue, (new_distance, next(queue_order), neighbour))

    return distances, previous

def a_star(graph: Graph, start):
    ...

def detect_cycle(graph: Graph):
    ...
    
def connected_components(graph: Graph):
    components = []
    visited = set()

    for start_node in graph.allNodes():
        if start_node in visited:
            continue

        component = []
        stack = [start_node]
        visited.add(start_node)

        while stack:
            node = stack.pop()
            component.append(node)

            for edge in graph.incidentEdges(node):
                neighbour = edge.target if edge.source == node else edge.source
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append(neighbour)

        components.append(sorted(component, key=graph._node_sort_key))

    return components, len(component)

def top_sort(graph: Graph):
    ...
