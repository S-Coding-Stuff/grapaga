import time
import csv
import os

def benchmark_algo(name, algo, graph, *args, **kwargs):
    start = time.perf_counter()
    result = algo(graph, *args, **kwargs)
    end = time.perf_counter()
    
    elapsed = end - start
    
    print(f"Algorithm: {name}")
    print(f"Nodes: {graph.count['Nodes']}")
    print(f"Edges: {graph.count['Edges']}")
    print(f"Time: {elapsed:.4f} seconds")
    
    return result, elapsed

def save_benchmark(name, algo, graph, *args, **kwargs):
    start = time.perf_counter()
    result = algo(graph, *args, **kwargs)
    end = time.perf_counter()
    
    return {
        "algorithm": name,
        "nodes": graph.count['Nodes'],
        "edges": graph.count['Edges'],
        "time_seconds": end - start
    }
    
def save_results(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["algorithm", "nodes", "edges", "time_seconds"])
        writer.writeheader()
        writer.writerows(rows)