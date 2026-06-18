from main.graph import Edge, Graph, Node


def test_add_node():
    graph = Graph()
    a = Node("A")

    graph.addNode(a)

    assert graph.hasNode(a) is True


def test_has_node_accepts_raw_value():
    graph = Graph()
    a = Node("A")
    graph.addNode(a)

    assert graph.hasNode("A") is True


def test_add_edge_adds_both_nodes():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")

    graph.addEdge(a, b)

    assert graph.hasNode(a) is True
    assert graph.hasNode(b) is True


def test_get_node_returns_stored_node_for_value():
    graph = Graph()
    a = Node("A")
    graph.addNode(a)

    assert graph.getNode("A") == a


def test_get_node_returns_none_for_missing_value():
    graph = Graph()

    assert graph.getNode("missing") is None


def test_get_edge_returns_edge_object():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.addEdge(a, b, 2.5)

    edge = graph.getEdge(a, b)

    assert edge == Edge(a, b, 2.5)


def test_has_edge_returns_true_for_existing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.addEdge(a, b)

    assert graph.hasEdge(a, b) is True
    assert graph.hasEdge("A", "B") is True


def test_has_edge_returns_false_for_missing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.addNode(a)
    graph.addNode(b)

    assert graph.hasEdge(a, b) is False


def test_outgoing_edges_returns_sorted_edges():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")
    one = Node(1)

    graph.addEdge(a, c, 5.0)
    graph.addEdge(a, b, 2.0)
    graph.addEdge(a, one, 1.0)

    result = graph.outgoingEdges(a)

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

    graph.addEdge(a, c)
    graph.addEdge(a, b)
    graph.addEdge(a, one)

    assert graph.neighbours(a) == [one, b, c]


def test_all_nodes_returns_sorted_node_objects():
    graph = Graph()
    graph.addNode(Node("B"))
    graph.addNode(Node(2))
    graph.addNode(Node("A"))
    graph.addNode(Node(1))

    assert graph.allNodes() == [Node(1), Node(2), Node("A"), Node("B")]


def test_edges_returns_all_edges_as_sorted_tuples():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph.addEdge(a, c)
    graph.addEdge(a, b)

    assert graph.edges == [("A", "B"), ("A", "C")]


def test_count_returns_node_and_edge_totals():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")

    graph.addEdge(a, b)
    graph.addNode(c)

    assert graph.count() == {"Nodes": 3, "Edges": 1}


def test_remove_edge_removes_existing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.addEdge(a, b)

    graph.removeEdge(a, b)

    assert graph.getEdge(a, b) is None


def test_remove_edge_ignores_missing_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.addNode(a)
    graph.addNode(b)

    graph.removeEdge(a, b)

    assert graph.getEdge(a, b) is None


def test_remove_node_removes_node_and_connected_edges():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    c = Node("C")
    graph.addEdge(a, b)
    graph.addEdge(c, a)

    graph.removeNode(a)

    assert graph.hasNode(a) is False
    assert graph.getEdge(a, b) is None
    assert graph.getEdge(c, a) is None


def test_directed_graph_does_not_add_reverse_edge():
    graph = Graph(directed=True)
    a = Node("A")
    b = Node("B")
    graph.addEdge(a, b)

    assert graph.getEdge(a, b) == Edge(a, b, 1.0)
    assert graph.getEdge(b, a) is None


def test_undirected_graph_adds_reverse_edge():
    graph = Graph(directed=False)
    a = Node("A")
    b = Node("B")
    graph.addEdge(a, b)

    assert graph.getEdge(a, b) == Edge(a, b, 1.0)
    assert graph.getEdge(b, a) == Edge(b, a, 1.0)
