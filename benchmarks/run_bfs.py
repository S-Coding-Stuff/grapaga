from graphsys.algo import bfs
from graphsys.benchmark import benchmark_algo
from graphsys.generators import random_graph
from graphsys.graph import Node

g_size = [(1_000, 5_000)]

cases = g_size if isinstance(g_size, list) else [g_size]

for n, m in cases:
    print()
    print("=" * 40)
    print(f"Random Graph: n={n}, m={m}")
    graph = random_graph(n, m, directed=False, seed=42)
    benchmark_algo("Breadth First Search", bfs, graph, Node(0))
    print("=" * 40)
