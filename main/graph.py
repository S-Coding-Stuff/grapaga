from dataclasses import dataclass
from typing import List

"""Node Class"""
@dataclass(frozen=True)
class Node:
    """Node setup to simply hold data."""
    element: int | float | str

    def __str__(self) -> str:
        return str(self.element)


"""Edges Class"""
@dataclass(frozen=True)
class Edge:
    source: Node
    target: Node
    weight: float = 1.0

    def __str__(self) -> str:
        return f"{self.source} -> {self.target} ({self.weight})"


"""Graph Class"""
class Graph:
    def __init__(self, directed: bool = False):
        self.directed = directed
        self._nodes: set[Node] = set()
        self._edges: set[Edge] = set()

    @staticmethod
    def _node_value(node: Node | int | float | str) -> int | float | str:
        return node.element if isinstance(node, Node) else node

    @staticmethod
    def _edge_sort_key(edge: Edge) -> tuple[int, int | float | str, float]:
        return (
            0 if isinstance(edge.target.element, (int, float)) else 1,
            edge.target.element if isinstance(edge.target.element, (int, float)) else str(edge.target.element),
            edge.weight,
        )
    
    
    @staticmethod
    def _node_sort_key(node: Node) -> tuple[int, int | float | str, float]:
        return (
            0 if isinstance(node.element, (int, float)) else 1,
                node.element if isinstance(node.element, (int, float)) else str(node.element),
            )
          
    
    def allNodes(self) -> list[Node]:
        return sorted(
            self._nodes,
            key=lambda node: (
                0 if isinstance(node.element, (int, float)) else 1,
                node.element if isinstance(node.element, (int, float)) else str(node.element),
            )
        )
    
    def count(self) -> dict:
        """Returns a count of Nodes and Edges (Connected Components later)"""
        return {"Nodes": len(self.nodes), "Edges": len(self.edges)}
        # TODO - Add in connected component count
        
    def addEdge(self, u: Node, v:Node, weight:float=1.0) -> None:
        self._nodes.add(u)
        self._nodes.add(v)
        edge = Edge(u, v, weight)
        self._edges.add(edge)
        
        if not self.directed:
            reverseEdge = Edge(v, u, weight)
            self._edges.add(reverseEdge)
    
    def addNode(self, node:Node) -> None:
        """Simply adding nodes to the graph object."""
        self._nodes.add(node)
        
    def getNode(self, node_or_val) -> Node | None:
        val = self._node_value(node_or_val)
        for node in self.allNodes():
            if node.element == val:
                return node
        return None
    
    def getEdge(self, source, target) -> Edge | None:
        source_node = self.getNode(source)
        target_node = self.getNode(target)
        
        if source_node is None or target_node is None:
            return None
        
        for edge in self._edges:
            if edge.source == source_node and edge.target == target_node:
                return edge
        return None
    
    def removeNode(self, node: Node) -> None:
        my_node = self.getNode(node)
        if my_node is None:
            return
        edges_remove = []
        for edge in self._edges:
            if edge.source == my_node or edge.target == my_node:
                edges_remove.append(edge)
        for edge in edges_remove:
            self._edges.remove(edge)
        self._nodes.remove(my_node)
        
    def removeEdge(self, source, target) -> None:
        my_edge = self.getEdge(source, target)
        if my_edge is None:
            return
        self._edges.remove(my_edge)
        
        
    def hasNode(self, node: Node | int | float | str) -> bool:
        """Check if a graph has a given node"""
        node_val = self._node_value(node)
        for existing_node in self._nodes:
            if existing_node.element == node_val:
                return True
        return False
    
    def hasEdge(self, source: Node | int | float | str, target: Node | int | float | str) -> bool:
        """Checks if an edge exists, source and target are u and v (maths!)."""
        return self.getEdge(source, target) is not None
    
    def outgoingEdges(self, node_or_val) -> List[Edge]:
        node = self.getNode(node_or_val)
        
        if node is None:
            return []
        out_edges = []
        for edge in self._edges:
            if edge.source == node:
                out_edges.append(edge)
        return sorted(out_edges, key=self._edge_sort_key)
        
    def incomingEdges(self, node_or_val) -> List[Edge]:
        node = self.getNode(node_or_val)
        
        if node is None:
            return []
        in_edges = []
        for edge in self._edges:
            if edge.target == node:
                in_edges.append(edge)

        return sorted(in_edges, key=self._edge_sort_key)
        
    def incidentEdges(self, node_or_val) -> List[Edge]:
        outgoing = self.outgoingEdges(node_or_val)
        incoming = self.incomingEdges(node_or_val)

        return sorted(set(outgoing + incoming), key=self._edge_sort_key)
    
    @property
    def edges(self) -> list[tuple[int | float | str, int | float | str]]:
        return sorted(
            [(edge.source.element, edge.target.element) for edge in self._edges],
            key=lambda pair: (
                0 if isinstance(pair[0], (int, float)) else 1,
                pair[0] if isinstance(pair[0], (int, float)) else str(pair[0]),
                0 if isinstance(pair[1], (int, float)) else 1,
                pair[1] if isinstance(pair[1], (int, float)) else str(pair[1]),
            ),
        )
    
    @property
    def nodes(self) -> list[int | float | str]:
        return sorted(
            [node.element for node in self.allNodes()],
            key=lambda x: (0, x) if isinstance(x, (int, float)) else (1, str(x)),
        )
    
    
    def neighbours(self, node: Node | int | float | str) -> list[Node]:
        node_val = self._node_value(node)
        result = []
        for edge in self.outgoingEdges(node_val):
            result.append(edge.target)
        return sorted(
            result,
            key=lambda x: (
                0 if isinstance(x.element, (int, float)) else 1,
                x.element if isinstance(x.element, (int, float)) else str(x.element),
            ),
        )
        
    @classmethod
    def convert_edge_list(cls, path, directed=False, weighted=False):
        graph = cls(directed=directed)
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if weighted:
                    source, target, weight = parts
                    graph.addEdge(source, target, weight)
                else:
                    source, target = parts
                    graph.addEdge(source, target)
        return graph
    
    def __str__(self) -> str:
        lines = [f"Directed: {self.directed}"]
        for node in self.allNodes(): 
            connected = self.neighbours(node)
            lines.append(f"{node}: {[str(n) for n in connected]}") 
        return "\n".join(lines)
    
