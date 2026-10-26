import pytest

from graphsys.graph import Graph


@pytest.mark.parametrize("weighted", [False, True])
@pytest.mark.parametrize("directed", [False, True])
def test_load_edge_list_with_comments_whitespace_and_string_ids(tmp_path, weighted, directed):
    path = tmp_path / "edges.txt"
    content = "  # comment\n\n  0\tA  2.5\nA B 0\n" if weighted else " # comment\n\n0\tA\n A B \n"
    path.write_text(content)
    graph = Graph.convert_edge_list(path, directed=directed, weighted=weighted)

    assert graph.nodes == ["0", "A", "B"]
    assert graph.get_edge("0", "A").weight == (2.5 if weighted else 1)
    assert graph.get_edge("A", "B").weight == (0 if weighted else 1)
    assert graph.has_edge("A", "0") is (not directed)


@pytest.mark.parametrize(
    "content, weighted", [("A", False), ("A B C", False), ("A B", True), ("A B nope", True)]
)
def test_malformed_edge_list_raises(tmp_path, content, weighted):
    path = tmp_path / "invalid.txt"
    path.write_text(content)
    with pytest.raises(ValueError):
        Graph.convert_edge_list(path, weighted=weighted)


def test_empty_edge_list(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("# no edges\n\n")
    assert Graph.convert_edge_list(path).count == {"Nodes": 0, "Edges": 0}


def test_missing_edge_list(tmp_path):
    with pytest.raises(FileNotFoundError):
        Graph.convert_edge_list(tmp_path / "missing.txt")
