"""
graph_iteration_modes.py - Elegant Iteration Modes

دو راه برای iteration:

روش ۱: Properties
   for node in g.nodes:
   for edge in g.edges:

روش ۲: Context Managers
   with g.iter_edges():
       for item in g:

روش ۳: Subscripting
   for node in g[:]:              # nodes
   for edge in g[...]:            # edges

Licensed under Apache License 2.0
"""

from __future__ import annotations
from typing import Iterator, Union
from graph import Graph, Node, Edge


# ══════════════════════════════════════════════════════════════════════════════
#  ELEGANT ITERATION MODES
# ══════════════════════════════════════════════════════════════════════════════

class IterableView:
    """
    یک view برای iteration
    
    استفاده:
        view = IterableView(graph, "nodes")
        for item in view:
            process(item)
    """
    
    def __init__(self, graph: Graph, mode: str = "nodes") -> None:
        self.graph = graph
        self.mode = mode  # "nodes" یا "edges"
        self._cache = None
    
    def __iter__(self) -> Iterator:
        """تکرار بر اساس mode"""
        if self.mode == "nodes":
            return iter(self.graph.nodes())
        elif self.mode == "edges":
            return iter(self.graph.edges())
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
    
    def __len__(self) -> int:
        """تعداد items"""
        if self.mode == "nodes":
            return self.graph.order()
        elif self.mode == "edges":
            return self.graph.size()
        else:
            return 0
    
    def __repr__(self) -> str:
        count = len(self)
        return f"IterableView({self.mode}, {count} items)"
    
    def filter(self, predicate):
        """فیلتر کردن items"""
        return [item for item in self if predicate(item)]
    
    def map(self, func):
        """تبدیل items"""
        return [func(item) for item in self]


class IterationContext:
    """
    Context Manager برای تغییر iteration mode
    
    استفاده:
        with g.iter_edges() as edges:
            for edge in edges:
                process(edge)
        
        # یا
        
        with g.iter_edges():
            for edge in g:
                process(edge)
    """
    
    def __init__(self, graph: Graph, mode: str = "nodes") -> None:
        self.graph = graph
        self.mode = mode
        self._original_iter = None
        self._original_next = None
    
    def __enter__(self):
        """فعال کردن mode"""
        # ذخیره original
        self._original_iter = self.graph.__iter__
        
        # تغییر __iter__ بر اساس mode
        if self.mode == "nodes":
            self.graph.__iter__ = lambda: iter(self.graph.nodes())
        elif self.mode == "edges":
            self.graph.__iter__ = lambda: iter(self.graph.edges())
        
        return self.graph
    
    def __exit__(self, *args):
        """بازگردانی به حالت اصلی"""
        if self._original_iter:
            self.graph.__iter__ = self._original_iter


# ══════════════════════════════════════════════════════════════════════════════
#  EXTEND GRAPH WITH ELEGANT PROPERTIES
# ══════════════════════════════════════════════════════════════════════════════

def add_iteration_modes_to_graph():
    """
    افزودن iteration modes به Graph class
    
    استفاده:
        add_iteration_modes_to_graph()
        
        # حالا می‌توانید استفاده کنید:
        for node in g.nodes:
            print(node.node_id)
        
        for edge in g.edges:
            print(edge.src.node_id, "→", edge.dst.node_id)
    """
    
    def get_nodes_view(self) -> IterableView:
        """Property برای nodes view"""
        return IterableView(self, "nodes")
    
    def get_edges_view(self) -> IterableView:
        """Property برای edges view"""
        return IterableView(self, "edges")
    
    def iter_nodes_context(self) -> IterationContext:
        """Context manager برای nodes"""
        return IterationContext(self, "nodes")
    
    def iter_edges_context(self) -> IterationContext:
        """Context manager برای edges"""
        return IterationContext(self, "edges")
    
    def get_item(self, key):
        """Subscripting support"""
        if key == ...:  # Ellipsis برای edges
            return IterableView(self, "edges")
        elif key == slice(None):  # [:] برای nodes
            return IterableView(self, "nodes")
        elif isinstance(key, slice):
            # دیگر slices
            if key.start is None and key.stop is None:
                return IterableView(self, "nodes")
        else:
            # node access by ID
            return self.get_node(key)
    
    # افزودن properties
    Graph.nodes = property(get_nodes_view)
    Graph.edges = property(get_edges_view)
    
    # افزودن methods
    Graph.iter_nodes = iter_nodes_context
    Graph.iter_edges = iter_edges_context
    Graph.__getitem__ = get_item


# ══════════════════════════════════════════════════════════════════════════════
#  CONVENIENCE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def setup_elegant_iteration():
    """
    تنظیم کامل iteration modes
    
    بعد از اجرا می‌توانید استفاده کنید:
    
    # روش ۱: Properties
    for node in g.nodes:
        pass
    
    for edge in g.edges:
        pass
    
    # روش ۲: Context managers
    with g.iter_edges():
        for item in g:  # items اینجا edges هستند
            pass
    
    # روش ۳: Subscripting
    for node in g[:]:
        pass
    
    for edge in g[...]:
        pass
    """
    add_iteration_modes_to_graph()
    return "✅ Elegant iteration modes activated!"


# ══════════════════════════════════════════════════════════════════════════════
#  ADVANCED FEATURES
# ══════════════════════════════════════════════════════════════════════════════

class QueryBuilder:
    """
    Query builder برای graph queries
    
    استفاده:
        q = QueryBuilder(g)
        heavy_edges = q.edges().filter(lambda e: e.weight > 5).map(lambda e: e.name)
    """
    
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self._data = None
    
    def nodes(self) -> QueryBuilder:
        """انتخاب nodes"""
        self._data = IterableView(self.graph, "nodes")
        return self
    
    def edges(self) -> QueryBuilder:
        """انتخاب edges"""
        self._data = IterableView(self.graph, "edges")
        return self
    
    def filter(self, predicate) -> QueryBuilder:
        """فیلتر کردن"""
        if self._data is None:
            raise ValueError("Select nodes or edges first!")
        self._data = [item for item in self._data if predicate(item)]
        return self
    
    def map(self, func) -> QueryBuilder:
        """تبدیل"""
        if self._data is None:
            raise ValueError("Select nodes or edges first!")
        self._data = [func(item) for item in self._data]
        return self
    
    def limit(self, n: int) -> QueryBuilder:
        """محدود کردن"""
        if self._data is None:
            raise ValueError("Select nodes or edges first!")
        self._data = self._data[:n]
        return self
    
    def get(self) -> list:
        """دریافت نتایج"""
        if self._data is None:
            raise ValueError("Select nodes or edges first!")
        return list(self._data) if isinstance(self._data, list) else list(self._data)
    
    def __iter__(self):
        """تکرار روی نتایج"""
        if self._data is None:
            raise ValueError("Select nodes or edges first!")
        return iter(self._data) if isinstance(self._data, list) else iter(self._data)
    
    def __repr__(self) -> str:
        if self._data is None:
            return "QueryBuilder(empty)"
        return f"QueryBuilder({len(list(self._data)) if isinstance(self._data, list) else 'data'} items)"


# ══════════════════════════════════════════════════════════════════════════════
#  EXAMPLE HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def print_nodes(graph: Graph, title: str = "Nodes") -> None:
    """چاپ تمام nodes"""
    print(f"\n{title}:")
    for node in graph.nodes:
        print(f"  • {node.node_id} (data={node.data})")


def print_edges(graph: Graph, title: str = "Edges") -> None:
    """چاپ تمام edges"""
    print(f"\n{title}:")
    for edge in graph.edges:
        print(f"  {edge.src.node_id} → {edge.dst.node_id} ({edge.name}, w={edge.weight})")


def print_graph_summary(graph: Graph) -> None:
    """خلاصه گراف"""
    print(f"\n{'='*50}")
    print(f"Graph: {graph.name}")
    print(f"{'='*50}")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges)}")
    print_nodes(graph)
    print_edges(graph)
    print(f"{'='*50}")

