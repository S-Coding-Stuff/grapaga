# Grapaga

Lightweight graph data structures and algorithms in Python, with an early-stage `gnnsys` package for graph neural network experiments.

## What is implemented

- `graphsys.graph`
  - `Node` and `Edge` dataclasses
  - `Graph` with directed and undirected modes
  - Node and edge insertion, removal, lookup, and adjacency queries
  - Edge-list file loading via `Graph.convert_edge_list(...)`
- `graphsys.algo`
  - Breadth-first search (`bfs`)
  - Depth-first search (`dfs`)
  - Reachability check (`path_exists`)
  - Dijkstra shortest paths (`dijkstra`)
  - Connected components (`connected_components`)
- `gnnsys.models`
  - `GCN` built with PyTorch Geometric
  - `LinkPredictionModel` built on top of the GCN encoder

## Project structure

```text
benchmarks/
  run_bfs.py
  run_dijkstra.py
ggnsys/
  __init__.py
  config.yaml
  models.py
  train.py
graphsys/
  __init__.py
  graph.py
  algo.py
  generators.py
  benchmark.py
  tree_algo.py
tests/
  test_graph.py
  test_algo.py
README.md
requirements.txt
```

## Setup

Install the current Python dependencies:

```bash
pip install -r requirements.txt
```

If you are using the local virtual environment:

```bash
./.venv/bin/pip install -r requirements.txt
```

Note: `requirements.txt` currently includes the core test dependencies only. The `gnnsys` models also require PyTorch and PyTorch Geometric, which are not listed there yet.

## Usage

Basic graph construction:

```python
from graphsys.graph import Graph, Node

graph = Graph(directed=True)
a = Node("A")
b = Node("B")
c = Node("C")

graph.add_edge(a, b, 1.0)
graph.add_edge(b, c, 2.5)

print(graph.nodes)
print(graph.edges)
```

Run traversal and shortest-path algorithms:

```python
from graphsys.algo import bfs, dfs, dijkstra

print(bfs(graph, a))
print(dfs(graph, a))

distances, previous = dijkstra(graph, a)
print(distances[c])
```

Load from an edge list file:

```python
from graphsys.graph import Graph

graph = Graph.convert_edge_list("path/to/edges.txt", directed=True, weighted=False)
```

Unweighted edge list format:

```text
A B
B C
```

Weighted edge list format:

```text
A B 1.5
B C 2.0
```

## Running tests

Run the full test suite from the project root:

```bash
./.venv/bin/python -m pytest -q
```

Or without a virtual environment-specific path:

```bash
python -m pytest -q
```

## Benchmarks

The repository includes small benchmark entry points for BFS and Dijkstra:

```bash
python benchmarks/run_bfs.py
python benchmarks/run_dijkstra.py
```

Existing benchmark outputs are stored in `results/`.

## Current limitations

- `gnnsys/train.py`, `gnnsys/eval.py`, and `gnnsys/convert.py` are placeholders at the moment.
- `a_star`, `detect_cycle`, and `top_sort` in `graphsys.algo` are declared but not implemented yet.
- The GNN stack depends on packages that are not currently declared in `requirements.txt`.
