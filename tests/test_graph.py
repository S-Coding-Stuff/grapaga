from graphsys.graph import Edge, Graph, Node


def test_add_node():
    graph = Graph()
    a = Node("A")

    graph.add_node(a)

    assert graph.has_node(a) is True


def test_has_node_accepts_raw_value():
    graph = Graph()
    a = Node("A")
    graph.add_node(a)

    assert graph.has_node("A") is True


def test_add_edge_adds_both_nodes():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")

    graph.add_edge(a, b)

    assert graph.has_node(a) is True
    assert graph.has_node(b) is True


def test_get_node_returns_stored_node_for_value():
    graph = Graph()
    a = Node("A")
    graph.add_node(a)

    assert graph.get_node("A") == a


def test_get_node_returns_none_for_missing_value():
    graph = Graph()

    assert graph.get_node("missing") is None


def test_get_edge_returns_edge_object():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.add_edge(a, b, 2.5)

    edge = graph.get_edge(a, b)

    assert edge == Edge(a, b, 2.5)


def test_has_edge_returns_true_for_existing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.add_edge(a, b)

    assert graph.has_edge(a, b) is True
    assert graph.has_edge("A", "B") is True


def test_has_edge_returns_false_for_missing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.add_node(a)
    graph.add_node(b)

    assert graph.has_edge(a, b) is False


def test_outgoing_edges_returns_sorted_edges():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")
    one = Node(1)

    graph.add_edge(a, c, 5.0)
    graph.add_edge(a, b, 2.0)
    graph.add_edge(a, one, 1.0)

    result = graph.outgoing_edges(a)

    assert result == [
        Edge(a, one, 1.0),
        Edge(a, b, 2.0),
        Edge(a, c, 5.0),
    ]


def test_neighbours_returns_target_nodes_in_sorted_order():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")
    one = Node(1)

    graph.add_edge(a, c)
    graph.add_edge(a, b)
    graph.add_edge(a, one)

    assert graph.neighbours(a) == [one, b, c]


def test_all_nodes_returns_sorted_node_objects():
    graph = Graph()
    graph.add_node(Node("B"))
    graph.add_node(Node(2))
    graph.add_node(Node("A"))
    graph.add_node(Node(1))

    assert graph.all_nodes() == [Node(1), Node(2), Node("A"), Node("B")]


def test_edges_returns_all_edges_as_sorted_tuples():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph.add_edge(a, c)
    graph.add_edge(a, b)

    assert graph.edges == [("A", "B"), ("A", "C")]


def test_count_returns_node_and_edge_totals():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph.add_edge(a, b)
    graph.add_node(c)

    assert graph.count == {"Nodes": 3, "Edges": 1}


def test_remove_edge_removes_existing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.add_edge(a, b)

    graph.remove_edge(a, b)

    assert graph.get_edge(a, b) is None


def test_remove_edge_ignores_missing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.add_node(a)
    graph.add_node(b)

    graph.remove_edge(a, b)

    assert graph.get_edge(a, b) is None


def test_remove_node_removes_node_and_connected_edges():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")
    graph.add_edge(a, b)
    graph.add_edge(c, a)

    graph.remove_node(a)

    assert graph.has_node(a) is False
    assert graph.get_edge(a, b) is None
    assert graph.get_edge(c, a) is None


def test_directed_graph_does_not_add_reverse_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.add_edge(a, b)

    assert graph.get_edge(a, b) == Edge(a, b, 1.0)
    assert graph.get_edge(b, a) is None


def test_undirected_graph_adds_reverse_edge():
    graph = Graph(directed=False)
    a = Node("A")
    b = Node("B")
    graph.add_edge(a, b)

    assert graph.get_edge(a, b) == Edge(a, b, 1.0)
    assert graph.get_edge(b, a) == Edge(b, a, 1.0)
