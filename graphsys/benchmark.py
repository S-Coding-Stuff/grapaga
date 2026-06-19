import time

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