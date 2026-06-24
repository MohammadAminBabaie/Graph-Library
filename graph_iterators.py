"""
graph_iterators.py - Advanced Iterator Patterns for Graphs

بخش‌های مختلفی را می‌توان iterate کرد:
- Nodes
- Edges  
- Neighbors
- Paths
- Cycles

Licensed under Apache License 2.0
"""

from __future__ import annotations
from typing import Iterator, Any, Optional, Set, List, Tuple
from graph import Graph, Node, Edge


# ══════════════════════════════════════════════════════════════════════════════
#  ITERATORS - روش‌های مختلف iteration
# ══════════════════════════════════════════════════════════════════════════════

class NodesIterator:
    """
    Iterator برای تکرار روی تمام nodes
    
    استفاده:
        for node in g.iter_nodes():
            print(node.node_id)
    """
    
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self._nodes = list(graph.nodes())
        self._index = 0
    
    def __iter__(self) -> NodesIterator:
        self._index = 0
        return self
    
    def __next__(self) -> Node:
        if self._index >= len(self._nodes):
            raise StopIteration
        node = self._nodes[self._index]
        self._index += 1
        return node
    
    def __len__(self) -> int:
        return len(self._nodes)
    
    def __repr__(self) -> str:
        return f"NodesIterator({len(self._nodes)} nodes)"


class EdgesIterator:
    """
    Iterator برای تکرار روی تمام edges
    
    استفاده:
        for edge in g.iter_edges():
            print(f"{edge.src.node_id} -> {edge.dst.node_id}")
    """
    
    def __init__(self, graph: Graph, weighted: bool = True) -> None:
        self.graph = graph
        self._edges = list(graph.edges())
        self._index = 0
        self.weighted = weighted
    
    def __iter__(self) -> EdgesIterator:
        self._index = 0
        return self
    
    def __next__(self) -> Edge:
        if self._index >= len(self._edges):
            raise StopIteration
        edge = self._edges[self._index]
        self._index += 1
        return edge
    
    def __len__(self) -> int:
        return len(self._edges)
    
    def __repr__(self) -> str:
        return f"EdgesIterator({len(self._edges)} edges)"


class NeighborsIterator:
    """
    Iterator برای neighbors یک node
    
    استفاده:
        for neighbor in g.iter_neighbors("A"):
            print(neighbor.node_id)
    """
    
    def __init__(self, graph: Graph, node_id: Any) -> None:
        self.graph = graph
        self.node_id = node_id
        self._neighbors = graph.neighbors(node_id)
        self._index = 0
    
    def __iter__(self) -> NeighborsIterator:
        self._index = 0
        return self
    
    def __next__(self) -> Node:
        if self._index >= len(self._neighbors):
            raise StopIteration
        neighbor = self._neighbors[self._index]
        self._index += 1
        return neighbor
    
    def __len__(self) -> int:
        return len(self._neighbors)


class OutEdgesIterator:
    """
    Iterator برای یال‌های خروجی یک node
    """
    
    def __init__(self, graph: Graph, node_id: Any) -> None:
        self.graph = graph
        self.node_id = node_id
        self._edges = graph.out_edges(node_id)
        self._index = 0
    
    def __iter__(self) -> OutEdgesIterator:
        self._index = 0
        return self
    
    def __next__(self) -> Edge:
        if self._index >= len(self._edges):
            raise StopIteration
        edge = self._edges[self._index]
        self._index += 1
        return edge
    
    def __len__(self) -> int:
        return len(self._edges)


class InEdgesIterator:
    """
    Iterator برای یال‌های ورودی یک node
    """
    
    def __init__(self, graph: Graph, node_id: Any) -> None:
        self.graph = graph
        self.node_id = node_id
        self._edges = graph.in_edges(node_id)
        self._index = 0
    
    def __iter__(self) -> InEdgesIterator:
        self._index = 0
        return self
    
    def __next__(self) -> Edge:
        if self._index >= len(self._edges):
            raise StopIteration
        edge = self._edges[self._index]
        self._index += 1
        return edge
    
    def __len__(self) -> int:
        return len(self._edges)


class DFSIterator:
    """
    Deep First Search Iterator
    
    استفاده:
        for node in g.iter_dfs(start="A"):
            print(node.node_id)
    """
    
    def __init__(self, graph: Graph, start: Any) -> None:
        self.graph = graph
        self.start = start
        self._stack = [start]
        self._visited: Set[Any] = set()
        self._result: List[Node] = []
        self._build_dfs()
    
    def _build_dfs(self) -> None:
        """BFS traversal"""
        stack = [self.start]
        visited: Set[Any] = set()
        
        while stack:
            node_id = stack.pop()
            if node_id in visited:
                continue
            
            visited.add(node_id)
            self._result.append(self.graph.get_node(node_id))
            
            # Add neighbors to stack
            for neighbor in reversed(self.graph.neighbors(node_id)):
                if neighbor.node_id not in visited:
                    stack.append(neighbor.node_id)
    
    def __iter__(self) -> DFSIterator:
        self._index = 0
        return self
    
    def __next__(self) -> Node:
        if self._index >= len(self._result):
            raise StopIteration
        node = self._result[self._index]
        self._index += 1
        return node
    
    def __len__(self) -> int:
        return len(self._result)


class BFSIterator:
    """
    Breadth First Search Iterator
    
    استفاده:
        for node in g.iter_bfs(start="A"):
            print(node.node_id)
    """
    
    def __init__(self, graph: Graph, start: Any) -> None:
        self.graph = graph
        self.start = start
        self._result: List[Node] = []
        self._index = 0
        self._build_bfs()
    
    def _build_bfs(self) -> None:
        """BFS traversal"""
        queue = [self.start]
        visited: Set[Any] = set()
        
        while queue:
            node_id = queue.pop(0)
            if node_id in visited:
                continue
            
            visited.add(node_id)
            self._result.append(self.graph.get_node(node_id))
            
            # Add neighbors to queue
            for neighbor in self.graph.neighbors(node_id):
                if neighbor.node_id not in visited:
                    queue.append(neighbor.node_id)
    
    def __iter__(self) -> BFSIterator:
        self._index = 0
        return self
    
    def __next__(self) -> Node:
        if self._index >= len(self._result):
            raise StopIteration
        node = self._result[self._index]
        self._index += 1
        return node
    
    def __len__(self) -> int:
        return len(self._result)


# ══════════════════════════════════════════════════════════════════════════════
#  EXTEND Graph CLASS
# ══════════════════════════════════════════════════════════════════════════════

def add_iterators_to_graph():
    """
    افزودن iterator methods به Graph class
    
    استفاده:
        add_iterators_to_graph()
        g = Graph()
        for node in g.iter_nodes():
            ...
    """
    
    def iter_nodes(self) -> NodesIterator:
        """بازگشت iterator برای تمام nodes"""
        return NodesIterator(self)
    
    def iter_edges(self) -> EdgesIterator:
        """بازگشت iterator برای تمام edges"""
        return EdgesIterator(self)
    
    def iter_neighbors(self, node_id: Any) -> NeighborsIterator:
        """بازگشت iterator برای neighbors یک node"""
        return NeighborsIterator(self, node_id)
    
    def iter_out_edges(self, node_id: Any) -> OutEdgesIterator:
        """بازگشت iterator برای یال‌های خروجی"""
        return OutEdgesIterator(self, node_id)
    
    def iter_in_edges(self, node_id: Any) -> InEdgesIterator:
        """بازگشت iterator برای یال‌های ورودی"""
        return InEdgesIterator(self, node_id)
    
    def iter_dfs(self, start: Any) -> DFSIterator:
        """بازگشت iterator برای DFS traversal"""
        return DFSIterator(self, start)
    
    def iter_bfs(self, start: Any) -> BFSIterator:
        """بازگشت iterator برای BFS traversal"""
        return BFSIterator(self, start)
    
    # افزودن methods به Graph
    Graph.iter_nodes = iter_nodes
    Graph.iter_edges = iter_edges
    Graph.iter_neighbors = iter_neighbors
    Graph.iter_out_edges = iter_out_edges
    Graph.iter_in_edges = iter_in_edges
    Graph.iter_dfs = iter_dfs
    Graph.iter_bfs = iter_bfs


# ══════════════════════════════════════════════════════════════════════════════
#  CONTEXT MANAGERS - روش‌های مختلفِ iteration
# ══════════════════════════════════════════════════════════════════════════════

class IterationMode:
    """
    Context manager برای تغییر mode iteration
    
    استفاده:
        g = Graph()
        
        # Default: nodes
        for item in g:
            print(item.node_id)
        
        # با IterationMode: edges
        with g.mode("edges"):
            for edge in g:
                print(edge)
    """
    
    def __init__(self, graph: Graph, mode: str = "nodes") -> None:
        self.graph = graph
        self.mode = mode
        self._original_iter = None
    
    def __enter__(self):
        # Store original __iter__
        self._original_iter = self.graph.__iter__
        
        if self.mode == "edges":
            self.graph.__iter__ = lambda: self.graph.iter_edges().__iter__()
        elif self.mode == "nodes":
            self.graph.__iter__ = lambda: self.graph.iter_nodes().__iter__()
        
        return self.graph
    
    def __exit__(self, *args):
        # Restore original __iter__
        if self._original_iter:
            self.graph.__iter__ = self._original_iter


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def print_traversal(graph: Graph, start: Any, method: str = "bfs") -> None:
    """چاپ traversal"""
    if method == "bfs":
        iterator = graph.iter_bfs(start)
    elif method == "dfs":
        iterator = graph.iter_dfs(start)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    print(f"\n{method.upper()} Traversal from '{start}':")
    path = " → ".join([node.node_id for node in iterator])
    print(f"  {path}")


def count_iterations(graph: Graph, item_type: str = "nodes") -> int:
    """تعداد items در iteration"""
    if item_type == "nodes":
        return len(graph.iter_nodes())
    elif item_type == "edges":
        return len(graph.iter_edges())
    else:
        raise ValueError(f"Unknown type: {item_type}")

