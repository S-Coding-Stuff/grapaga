# Grapaga

## Project Structure

```text
benchmarks/
  run_bfs.py
  run_dijkstra.py
main/
  __init__.py
  graph.py
  algo.py
  generators.py
  benchmarks.py
tests/
  test_graph.py
  test_algo.py
README.md
requirements.txt
```

## Setup

Install the project dependencies:

```bash
pip install -r requirements.txt
```

If you are using the local virtual environment:

```bash
./.venv/bin/pip install -r requirements.txt
```

## Running Tests

Run the full test suite from the project root:

```bash
./.venv/bin/python -m pytest -q
```

For more detailed output:

```bash
./.venv/bin/python -m pytest
```
