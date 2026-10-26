from graphsys.algo import a_star
from graphsys.graph import Node
from graphsys.benchmark import benchmark_algo, save_benchmark, save_results
from graphsys.generators import random_graph

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
    benchmark_algo("A-Star Algorithm", a_star, graph, Node(0), Node(max(n - 1, 0)),
                   lambda current, goal: 0.0)
    print("=" * 40)
    row = save_benchmark("A-star", a_star, graph, Node(0), Node(max(n - 1, 0)),
                         lambda current, goal: 0.0)
    rows.append(row)

save_results("results/a_star_py.csv", rows)
