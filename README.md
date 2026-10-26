# Grapaga

A Python learning project for graph algorithms, graph neural networks, testing, and CI/CD. The graph utilities are usable; the GNN experiments are still under development.

## Features

- Directed and undirected graphs with `Node` and `Edge` dataclasses.
- Node and edge insertion, removal, lookup, and adjacency queries.
- Weighted and unweighted edge-list loading.
- Breadth-first search, depth-first search, reachability, Dijkstra, and A*.
- Connected components, using weak connectivity for directed graphs.
- Pre-order, in-order, post-order, breadth-first, and depth-first tree traversals.
- Random graph and tree generators, plus CSV benchmark utilities.
- Experimental GraphSAGE, PPI data loaders, training, and micro-F1 evaluation code.

## Setup

Python 3.10 or newer is required. Run commands from the repository root.

Create and activate a virtual environment on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with `.venv\Scripts\Activate.ps1`.

Install the project with development tools:

```bash
python -m pip install -e ".[dev]"
```

Other installation options:

```bash
# Core graph package and NumPy only
python -m pip install -e .

# Include PyTorch, PyTorch Geometric, and development tools
python -m pip install -e ".[dev,gnn]"
```

Dependencies and optional groups are declared in `pyproject.toml`. The separate `requirements.txt` contains pinned dependencies, including additional scientific packages and GNN dependencies:

```bash
python -m pip install -r requirements.txt
```

Installing the GNN dependencies does not resolve the code issues listed under current limitations.

## Graph usage

Install the package before using `graphsys` imports; `src/` is the source directory.

```python
from graphsys.graph import Graph, Node
from graphsys.algo import a_star, bfs, dfs, dijkstra

graph = Graph(directed=True)
a, b, c = Node("A"), Node("B"), Node("C")
graph.add_edge(a, b, 1.0)
graph.add_edge(b, c, 2.5)
graph.add_edge(a, c, 5.0)

print(graph.nodes)  # ["A", "B", "C"]
print(bfs(graph, a))
print(dfs(graph, a))

distances, previous = dijkstra(graph, a)
print(distances[c])  # 3.5

path, cost = a_star(graph, a, c, heuristic=lambda node, goal: 0.0)
print(path, cost)  # ["A", "B", "C"] 3.5
```

BFS, DFS, and Dijkstra accept raw node IDs or `Node` objects and resolve them to the graph’s stored nodes. A* returns node IDs in its path; BFS and DFS return `Node` objects. Use nonnegative edge weights for Dijkstra and A*. A zero heuristic makes A* behave as a uniform-cost search.

### Edge-list files

```python
from graphsys.graph import Graph

graph = Graph.convert_edge_list("edges.txt", directed=True, weighted=True)
```

A weighted file has one edge per line:

```text
A B 1.5
B C 2.0
```

For an unweighted file, omit the third column and pass `weighted=False`. Blank lines and lines beginning with `#` are ignored. Node IDs loaded from files are strings.

### Tree traversal

```python
from graphsys.graph import Graph
from graphsys.tree_algo import pre_order, bfs_tree

tree = Graph(directed=True)
tree.add_edge("root", "left")
tree.add_edge("root", "right")

print(pre_order(tree))  # ["root", "left", "right"]
print(bfs_tree(tree))   # ["root", "left", "right"]
```

Directed trees infer their root from the single node with no incoming edges. Pass an explicit root for undirected trees. In-order traversal supports at most two children per node; child order follows sorted node IDs, with no separate left/right designation. Supply valid trees: recursive traversals do not detect cycles.

## Development checks

Install the `dev` extra before running these commands:

```bash
# Run the test suite
python -m pytest -q

# Measure graph package coverage, including branches
python -m pytest --cov --cov-report=term-missing

# Check lint and formatting
python -m ruff check .
python -m ruff format --check .

# Build a wheel and source distribution in dist/
python -m build
```

Tests cover graph operations, graph algorithms, tree traversals, edge-list loading, generators, and benchmark utilities. GNN code does not yet have dedicated tests. Coverage is configured for `graphsys` only. Lint and formatting checks may report existing issues; no CI workflow is checked in yet.

## Benchmarks

Run benchmarks as modules from the repository root:

```bash
python -m benchmarks.run_bfs
python -m benchmarks.run_dijkstra
python -m benchmarks.run_a_star
```

Each script defines graph sizes and a random seed, prints timings, and writes a CSV under `results/`. Running a script overwrites its corresponding results file. The generated graphs use default unit edge weights, and the A* benchmark uses a zero heuristic.

These are exploratory timings: the scripts execute algorithms separately for console output and CSV recording, and do not yet aggregate repeated measurements. Importing a benchmark module also executes it.

## GNN experiments

The `src/gnnsys/` directory contains:

- `models.py`: GraphSAGE, an unfinished GCN, and a NumPy message-passing prototype.
- `data.py`: PPI train, validation, and test dataset loaders, defaulting to `data/ppi`.
- `train.py`: a training configuration, training loop, and command-line argument parser.
- `eval.py`: multi-label micro-F1 evaluation and logit prediction.
- `config.yaml`: an experimental configuration that is not currently loaded by training.
- `convert.py`: a placeholder for conversion utilities.

The training code targets GraphSAGE on PPI, while the YAML describes a GCN experiment with different defaults. Treat the YAML as a draft rather than an active training configuration. GNN imports and training are currently blocked by the issues below.

## Project structure

```text
benchmarks/             # BFS, Dijkstra, and A* benchmark scripts
results/                # Recorded benchmark CSV files
src/
  graphsys/             # Graph structures, algorithms, generators, benchmarks
  gnnsys/               # Experimental GNN models, data, training, and evaluation
tests/                  # Graph and tree tests
LICENSE
README.md
pyproject.toml          # Package metadata, dependency groups, and tool settings
requirements.txt        # Pinned dependency list
```

The `data/` directory is ignored by Git and may be created when datasets are downloaded.

## Current limitations

- `gnnsys/__init__.py` and `train.py` import `build_graphsage_for_dataset`, which is not yet defined in `models.py`.
- `GCN` has no forward implementation, and `convert.py` is empty.
- `detect_cycle`, `top_sort`, `complete_graph`, and `generate_grid` are placeholders.
- Edge weights are not validated for shortest-path algorithm requirements.
- Automated CI and release workflows are not yet configured.

## Contributing

Keep changes focused, add regression tests for bug fixes, and run the relevant development checks before submitting a pull request. Include a description of the behavior changed and the checks performed.

## License

MIT. See [LICENSE](LICENSE).
