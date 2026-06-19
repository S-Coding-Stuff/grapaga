from graphsys.graph import Graph, Node
import random

def random_graph(n, m, directed=False, seed=0):
    random.seed(seed)
    graph = Graph(directed=directed)
    
    nodes = [Node(i) for i in range(n)]
    for node in nodes:
        graph.addNode(node)
    
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
        graph.addEdge(nodes[u], nodes[v])
    return graph
