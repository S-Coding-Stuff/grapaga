import csv

from graphsys.benchmark import benchmark_algo, save_benchmark, save_results
from graphsys.graph import Graph


def test_benchmark_forwards_arguments_and_returns_result(capsys):
    graph = Graph()
    graph.add_edge("a", "b")
    calls = []

    def algorithm(received_graph, start, *, limit):
        calls.append((received_graph, start, limit))
        return [start]

    result, elapsed = benchmark_algo("example", algorithm, graph, "a", limit=2)
    assert result == ["a"]
    assert elapsed >= 0
    assert calls == [(graph, "a", 2)]
    assert "example" in capsys.readouterr().out


def test_saved_benchmark_contains_graph_metadata_and_timing():
    graph = Graph(directed=True)
    graph.add_edge("a", "b")
    calls = []

    def algorithm(received_graph):
        calls.append(received_graph)

    row = save_benchmark("example", algorithm, graph)
    assert calls == [graph]
    assert row["algorithm"] == "example"
    assert row["nodes"] == 2
    assert row["edges"] == 1
    assert row["time_seconds"] >= 0


def test_save_results_creates_directory_and_overwrites_csv(tmp_path):
    path = tmp_path / "nested" / "results.csv"
    rows = [{"algorithm": "test, with comma", "nodes": 2, "edges": 1, "time_seconds": 0.25}]
    save_results(path, rows)
    save_results(path, rows)
    with path.open(newline="") as file:
        assert list(csv.DictReader(file)) == [
            {"algorithm": "test, with comma", "nodes": "2", "edges": "1", "time_seconds": "0.25"}
        ]
