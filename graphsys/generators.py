from graphsys.graph import Graph, Node
import random

def complete_graph(n: int, 
                   m: int,
                   directed: bool = False, 
                   seed: int = 0) -> Graph:
    ...
    
def generate_grid(n: int, m: int, seed: int = 0) -> Graph:
    ...

def tree_graph(num_nodes: int, directed: bool = False, seed=0):
    """Directed, acyclic, must be n-1 edges, connected"""
    random.seed(seed)
    graph = Graph(directed=directed)
    nodes = [Node(i) for i in range(num_nodes)]
    for node in nodes:
        graph.add_node(node)
    
    for i in range(1, num_nodes):
        parent_node_idx = random.randrange(i)
        graph.add_edge(nodes[parent_node_idx], nodes[i])
    return graph

def random_graph(n: int, m: int, directed: bool=False, seed=0) -> Graph:
    random.seed(seed)
    graph = Graph(directed=directed)
    
    nodes = [Node(i) for i in range(n)]
    for node in nodes:
        graph.add_node(node)
    
    max_edges = n*(n-1) if directed else n*(n-1)//2
    if m > max_edges:
        raise ValueError(f"m must be less than or equal to {max_edges} for n={n}, directed={directed}")
    
    edges = set()
    
    while len(edges) < m:
        u = random.randrange(n)
        v = random.randrange(n)
    
        if u == v:
            continue
        
        edge = (u,v) if directed else tuple(sorted((u,v)))
        if edge in edges:
            continue
        
        edges.add(edge)
        graph.add_edge(nodes[u], nodes[v])
    return graph
