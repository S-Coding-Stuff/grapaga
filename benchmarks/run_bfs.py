from graphsys.algo import bfs
from graphsys.benchmark import benchmark_algo, save_benchmark, save_results
from graphsys.generators import random_graph
from graphsys.graph import Node

g_size = [(1_000, 5_000), (5_000, 10_000), (10_000, 50_000)]

cases = g_size if isinstance(g_size, list) else [g_size]
directed = False
seed = 42

rows = []
for n, m in cases:
    print()
    print("=" * 40)
    print(f"Random Graph: n={n}, m={m}")
    graph = random_graph(n, m, directed=directed, seed=seed)
    benchmark_algo("Breadth First Search", bfs, graph, Node(0))
    print("=" * 40)
    row = save_benchmark("BFS", bfs, graph, Node(0))
    rows.append(row)
    
save_results("results/bfs_py.csv", rows)
