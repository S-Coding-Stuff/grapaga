import csv
import os
import time


def benchmark_algo(name, algo, graph, *args, **kwargs):
    """Time one algorithm execution and print a summary.

    Algorithm exceptions propagate to the caller. The graph is not copied,
    so mutations made by the algorithm remain visible.

    :param name: Label for the benchmark.
    :type name: str
    :param algo: Algorithm called with graph followed by args and kwargs.
    :type algo: Callable[..., Any]
    :param graph: Graph passed to the algorithm.
    :type graph: Graph
    :param args: Additional positional arguments forwarded to the algorithm.
    :type args: Any
    :param kwargs: Additional keyword arguments forwarded to the algorithm.
    :type kwargs: Any
    :returns: Algorithm result and elapsed time in seconds.
    :rtype: tuple[Any, float]
    """
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
    """Time one algorithm execution and create a benchmark record.

    Discard the algorithm result. Read graph counts after execution. This
    function does not write a file. Algorithm exceptions propagate.

    :param name: Label for the benchmark.
    :type name: str
    :param algo: Algorithm called with graph followed by args and kwargs.
    :type algo: Callable[..., Any]
    :param graph: Graph passed to the algorithm.
    :type graph: Graph
    :param args: Additional positional arguments forwarded to the algorithm.
    :type args: Any
    :param kwargs: Additional keyword arguments forwarded to the algorithm.
    :type kwargs: Any
    :returns: Record with algorithm, nodes, edges, and time_seconds keys.
    :rtype: dict[str, str | int | float]
    """
    start = time.perf_counter()
    algo(graph, *args, **kwargs)
    end = time.perf_counter()

    return {
        "algorithm": name,
        "nodes": graph.count["Nodes"],
        "edges": graph.count["Edges"],
        "time_seconds": end - start,
    }


def save_results(path, rows):
    """Write benchmark records to a CSV file, replacing existing contents.

    Create missing parent directories and write a header even for empty rows.
    Missing fields are written empty; unexpected record keys raise ValueError.

    :param path: Output path containing a nonempty parent directory.
    :type path: str | os.PathLike
    :param rows: Records using algorithm, nodes, edges, and time_seconds keys.
    :type rows: Iterable[dict[str, Any]]
    :returns: None.
    :rtype: None
    :raises OSError: A directory cannot be created or the output cannot be written.
    :raises ValueError: A record contains keys outside the CSV field names.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["algorithm", "nodes", "edges", "time_seconds"])
        writer.writeheader()
        writer.writerows(rows)
