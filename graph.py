"""
graph.py - Complete Implementation
Professional Graph Library with all features

Licensed under Apache License 2.0

Features:
- Directed/Undirected graphs
- Weighted edges with names
- Multi-edges (parallel edges)
- Self-loops
- Batch operations (add_nodes, add_edges)
- Advanced graph operations (__add__, __sub__, complement)
- Enhanced __contains__ for edges and subgraphs
- Full attribute system
"""

from __future__ import annotations

import uuid
from typing import Any, Iterator, Optional, Union


# ══════════════════════════════════════════════════════════════════════════════
#  EXCEPTIONS
# ══════════════════════════════════════════════════════════════════════════════

class GraphError(Exception):
    """استثنای پایه برای تمام خطاهای مرتبط با گراف"""


class NodeNotFoundError(GraphError):
    def __init__(self, node_id: Any) -> None:
        super().__init__(f"گره پیدا نشد: {node_id!r}")
        self.node_id = node_id


class EdgeNotFoundError(GraphError):
    def __init__(self, src_id: Any, dst_id: Any, edge_id: Optional[str] = None) -> None:
        detail = f" (edge_id={edge_id!r})" if edge_id else ""
        super().__init__(f"یال پیدا نشد: {src_id!r} -> {dst_id!r}{detail}")
        self.src_id = src_id
        self.dst_id = dst_id


class DuplicateNodeError(GraphError):
    def __init__(self, node_id: Any) -> None:
        super().__init__(f"گره از قبل وجود دارد: {node_id!r}")
        self.node_id = node_id


# ══════════════════════════════════════════════════════════════════════════════
#  ATTRIBUTE MIXIN
# ══════════════════════════════════════════════════════════════════════════════

class AttrMixin:
    """ذخیره‌سازی ویژگی‌های کلید-مقدار برای Node و Edge"""

    def __init__(self) -> None:
        self._attrs: dict[str, Any] = {}

    def set_attr(self, key: str, value: Any) -> None:
        """تنظیم یک ویژگی متاداتا"""
        self._attrs[key] = value

    def get_attr(self, key: str, default: Any = None) -> Any:
        """دریافت یک ویژگی، بازگشت مقدار پیش‌فرض اگر موجود نباشد"""
        return self._attrs.get(key, default)

    def del_attr(self, key: str) -> None:
        """حذف یک ویژگی"""
        if key not in self._attrs:
            raise KeyError(f"ویژگی پیدا نشد: {key!r}")
        del self._attrs[key]

    def attrs(self) -> dict[str, Any]:
        """بازگشت کپی تمام ویژگی‌ها"""
        return dict(self._attrs)

    def update_attrs(self, **kwargs: Any) -> None:
        """اپدیت دسته‌ای چندین ویژگی"""
        self._attrs.update(kwargs)


# ══════════════════════════════════════════════════════════════════════════════
#  NODE CLASS
# ══════════════════════════════════════════════════════════════════════════════

class Node(AttrMixin):
    """
    یک رأس (گره) در گراف
    
    Parameters
    ----------
    node_id : Any hashable
        شناسه منحصر به فرد
    data : Any, optional
        بار کاربری دلخواه
    **attrs
        ویژگی‌های متاداتا اولیه
    """

    __slots__ = ("node_id", "data", "_attrs")

    def __init__(self, node_id: Any, data: Any = None, **attrs: Any) -> None:
        super().__init__()
        self.node_id = node_id
        self.data = data
        self._attrs.update(attrs)

    def __hash__(self) -> int:
        return hash(self.node_id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return self.node_id == other

    def __repr__(self) -> str:
        extra = f", data={self.data!r}" if self.data is not None else ""
        return f"Node({self.node_id!r}{extra})"


# ══════════════════════════════════════════════════════════════════════════════
#  EDGE CLASS
# ══════════════════════════════════════════════════════════════════════════════

class Edge(AttrMixin):
    """
    یک یال (کمان) بین دو گره
    
    Parameters
    ----------
    src : Node
        گره منبع
    dst : Node
        گره مقصد
    weight : float
        وزن یال (پیش‌فرض 1.0)
    name : str, optional
        نام قابل خواندن یال (مثال: "مسیر اصلی")
        اگر ارائه نشود، به صورت "{src_id}_{dst_id}" تولید می‌شود
    edge_id : str, optional
        شناسه منحصر به فرد - اگر ارائه نشود، تولید می‌شود
    **attrs
        ویژگی‌های متاداتا
    """

    __slots__ = ("src", "dst", "weight", "name", "edge_id", "_attrs")

    def __init__(
        self,
        src: Node,
        dst: Node,
        weight: float = 1.0,
        name: Optional[str] = None,
        edge_id: Optional[str] = None,
        **attrs: Any,
    ) -> None:
        super().__init__()
        self.src = src
        self.dst = dst
        self.weight = weight
        self.name: str = name or f"{src.node_id}_{dst.node_id}"
        self.edge_id: str = edge_id or str(uuid.uuid4())[:8]
        self._attrs.update(attrs)

    def reversed(self) -> Edge:
        """بازگشت یک یال جدید با src و dst معکوس"""
        reversed_name = f"{self.name}_rev" if not self.name.endswith("_rev") else self.name
        return Edge(
            self.dst,
            self.src,
            self.weight,
            name=reversed_name,
            edge_id=self.edge_id + "_r",
            **self._attrs
        )

    def endpoints(self) -> tuple[Any, Any]:
        """بازگشت (src.node_id, dst.node_id)"""
        return (self.src.node_id, self.dst.node_id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Edge):
            return self.edge_id == other.edge_id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.edge_id)

    def __repr__(self) -> str:
        return f"Edge({self.src.node_id!r} -> {self.dst.node_id!r}, name={self.name!r}, w={self.weight})"


# ══════════════════════════════════════════════════════════════════════════════
#  GRAPH CLASS - COMPLETE VERSION
# ══════════════════════════════════════════════════════════════════════════════

class Graph:
    """
    گراف جامع با پشتیبانی:
    - گراف جهت‌دار/بدون‌جهت
    - یال‌های وزن‌دار با نام
    - یال‌های متوازی (multi-edge)
    - حلقه‌های خودی
    - عملیات دسته‌ای
    - عملیات پیشرفته (جمع، تفریق، مکمل)
    """

    def __init__(self, directed: bool = True, name: str = "G") -> None:
        """
        ایجاد گراف جدید
        
        Parameters
        ----------
        directed : bool
            True برای گراف جهت‌دار، False برای بدون‌جهت
        name : str
            نام گراف
        """
        self.directed = directed
        self.name = name
        self._nodes: dict[Any, Node] = {}
        self._adj: dict[Any, list[Edge]] = {}
        self._in_degree_cache: dict[Any, int] = {}

    # ══════════════════════════════════════════════════════════════════════════
    #  NODE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def add_node(
        self, node_id: Any, data: Any = None, *, strict: bool = False, **attrs: Any
    ) -> Node:
        """
        اضافه کردن یک گره
        
        Parameters
        ----------
        node_id : Any hashable
            شناسه گره
        data : Any, optional
            بار کاربری
        strict : bool
            اگر True، exception اگر گره موجود باشد
        **attrs
            ویژگی‌های متاداتا
        """
        if node_id in self._nodes:
            if strict:
                raise DuplicateNodeError(node_id)
            return self._nodes[node_id]

        node = Node(node_id, data, **attrs)
        self._nodes[node_id] = node
        self._adj[node_id] = []
        self._in_degree_cache[node_id] = 0
        return node

    def add_nodes(self, nodes: Any) -> None:
        """اضافه کردن دسته‌ای از گره‌ها (Node objects یا node_ids)"""
        for node in nodes:
            if isinstance(node, Node):
                self.add_node(node.node_id, node.data, **node.attrs())
            else:
                self.add_node(node)

    def add_node_direct(self, node: Node) -> Node:
        """اضافه کردن یک شیء Node به طور مستقیم"""
        return self.add_node(node.node_id, node.data, **node.attrs())

    def remove_node(self, node_id: Any) -> Node:
        """حذف یک گره و تمام یال‌های مرتبط"""
        self._require_node(node_id)
        node = self._nodes.pop(node_id)
        
        # حذف یال‌های خروجی
        for edge in list(self._adj[node_id]):
            self._inc_in_degree(edge.dst.node_id, -1)
            if not self.directed:
                self._inc_in_degree(node_id, -1)
        del self._adj[node_id]
        
        # حذف یال‌های ورودی
        for other_id in list(self._adj.keys()):
            self._adj[other_id] = [
                e for e in self._adj[other_id]
                if e.dst.node_id != node_id
            ]
        
        del self._in_degree_cache[node_id]
        return node

    def has_node(self, node_id: Any) -> bool:
        """بررسی وجود گره"""
        return node_id in self._nodes

    def get_node(self, node_id: Any) -> Node:
        """دریافت شیء Node"""
        if node_id not in self._nodes:
            raise NodeNotFoundError(node_id)
        return self._nodes[node_id]

    def update_node(self, node_id: Any, data: Any = None, **attrs: Any) -> Node:
        """اپدیت یک گره"""
        node = self.get_node(node_id)
        if data is not None:
            node.data = data
        node.update_attrs(**attrs)
        return node

    # ══════════════════════════════════════════════════════════════════════════
    #  EDGE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def add_edge(
        self,
        src_id: Any,
        dst_id: Any,
        weight: float = 1.0,
        name: Optional[str] = None,
        *,
        auto_add_nodes: bool = True,
        **attrs: Any,
    ) -> Edge:
        """اضافه کردن یک یال"""
        if auto_add_nodes:
            self.add_node(src_id)
            self.add_node(dst_id)
        else:
            self._require_node(src_id)
            self._require_node(dst_id)

        edge = Edge(self._nodes[src_id], self._nodes[dst_id], weight, name, **attrs)
        self._adj[src_id].append(edge)
        self._inc_in_degree(dst_id, 1)

        if not self.directed:
            reverse = edge.reversed()
            self._adj[dst_id].append(reverse)
            self._inc_in_degree(src_id, 1)

        return edge

    def add_edges(self, edges: Any) -> None:
        """اضافه کردن دسته‌ای از یال‌ها"""
        for edge in edges:
            if isinstance(edge, Edge):
                self.add_edge_direct(edge)
            elif isinstance(edge, (tuple, list)) and len(edge) >= 2:
                src, dst = edge[0], edge[1]
                weight = edge[2] if len(edge) > 2 else 1.0
                self.add_edge(src, dst, weight)

    def add_edge_direct(self, edge: Edge) -> Edge:
        """اضافه کردن یک شیء Edge به طور مستقیم"""
        src_id, dst_id = edge.endpoints()
        return self.add_edge(
            src_id, dst_id, edge.weight, edge.name,
            auto_add_nodes=True, **edge.attrs()
        )

    def remove_edge(self, src_id: Any, dst_id: Any, edge_id: Optional[str] = None) -> Edge:
        """حذف یک یال"""
        self._require_node(src_id)
        self._require_node(dst_id)

        adj = self._adj[src_id]
        target_idx = -1

        if edge_id is None:
            for i, e in enumerate(adj):
                if e.dst.node_id == dst_id:
                    target_idx = i
                    break
        else:
            for i, e in enumerate(adj):
                if e.dst.node_id == dst_id and e.edge_id == edge_id:
                    target_idx = i
                    break

        if target_idx == -1:
            raise EdgeNotFoundError(src_id, dst_id, edge_id)

        removed = adj.pop(target_idx)
        self._inc_in_degree(dst_id, -1)

        if not self.directed:
            self._inc_in_degree(src_id, -1)
            reverse_adj = self._adj[dst_id]
            for i, e in enumerate(reverse_adj):
                if e.dst.node_id == src_id and e.edge_id == removed.edge_id + "_r":
                    reverse_adj.pop(i)
                    break

        return removed

    def update_edge(
        self, src_id: Any, dst_id: Any, edge_id: Optional[str] = None, **attrs: Any
    ) -> Edge:
        """اپدیت یک یال"""
        edges = self.get_edges(src_id, dst_id)
        if not edges:
            raise EdgeNotFoundError(src_id, dst_id, edge_id)

        target_edge = None
        if edge_id is None:
            target_edge = edges[0]
        else:
            for e in edges:
                if e.edge_id == edge_id:
                    target_edge = e
                    break

        if target_edge is None:
            raise EdgeNotFoundError(src_id, dst_id, edge_id)

        if "weight" in attrs:
            target_edge.weight = attrs.pop("weight")
        if "name" in attrs:
            target_edge.name = attrs.pop("name")
        target_edge.update_attrs(**attrs)

        return target_edge

    def has_edge(self, src_id: Any, dst_id: Any) -> bool:
        """بررسی وجود یال"""
        return len(self.get_edges(src_id, dst_id)) > 0

    def get_edges(self, src_id: Any, dst_id: Any) -> list[Edge]:
        """دریافت تمام یال‌های بین دو گره"""
        if src_id not in self._nodes:
            return []
        adj = self._adj.get(src_id, [])
        return [e for e in adj if e.dst.node_id == dst_id]

    # ══════════════════════════════════════════════════════════════════════════
    #  TRAVERSAL
    # ══════════════════════════════════════════════════════════════════════════

    def neighbors(self, node_id: Any) -> list[Node]:
        """گره‌های مجاور (بدون تکرار)"""
        self._require_node(node_id)
        seen: set[Any] = set()
        result: list[Node] = []
        for e in self._adj[node_id]:
            nid = e.dst.node_id
            if nid not in seen:
                seen.add(nid)
                result.append(e.dst)
        return result

    def out_edges(self, node_id: Any) -> list[Edge]:
        """تمام یال‌های خروجی"""
        self._require_node(node_id)
        return list(self._adj[node_id])

    def in_edges(self, node_id: Any) -> list[Edge]:
        """تمام یال‌های ورودی (O(V+E))"""
        self._require_node(node_id)
        return [
            e for adj in self._adj.values()
            for e in adj
            if e.dst.node_id == node_id
        ]

    # ══════════════════════════════════════════════════════════════════════════
    #  DEGREE QUERIES
    # ══════════════════════════════════════════════════════════════════════════

    def out_degree(self, node_id: Any) -> int:
        """درجه‌ی خروجی"""
        self._require_node(node_id)
        return len(self._adj[node_id])

    def in_degree(self, node_id: Any) -> int:
        """درجه‌ی ورودی (O(1) via cache)"""
        self._require_node(node_id)
        return self._in_degree_cache.get(node_id, 0)

    def degree(self, node_id: Any) -> int:
        """درجه کل"""
        self._require_node(node_id)
        if self.directed:
            return self.in_degree(node_id) + self.out_degree(node_id)
        else:
            return self.out_degree(node_id)

    # ══════════════════════════════════════════════════════════════════════════
    #  ITERATORS
    # ══════════════════════════════════════════════════════════════════════════

    def nodes(self) -> Iterator[Node]:
        """تکرار روی تمام گره‌ها"""
        return iter(self._nodes.values())

    def edges(self) -> Iterator[Edge]:
        """تکرار روی تمام یال‌ها (هر کدام یک بار)"""
        seen: set[str] = set()
        for adj in self._adj.values():
            for e in adj:
                if e.edge_id.endswith("_r"):
                    continue
                if e.edge_id not in seen:
                    seen.add(e.edge_id)
                    yield e

    # ══════════════════════════════════════════════════════════════════════════
    #  GRAPH METRICS
    # ══════════════════════════════════════════════════════════════════════════

    def order(self) -> int:
        """تعداد گره‌ها"""
        return len(self._nodes)

    def size(self) -> int:
        """تعداد یال‌ها"""
        return sum(1 for _ in self.edges())

    def num_edges(self, src_id: Any = None, dst_id: Any = None) -> int:
        """تعداد یال‌ها (کل یا بین دو گره)"""
        if src_id is not None and dst_id is not None:
            return len(self.get_edges(src_id, dst_id))
        return self.size()

    # ══════════════════════════════════════════════════════════════════════════
    #  GRAPH OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def clear(self) -> None:
        """خالی کردن گراف"""
        self._nodes.clear()
        self._adj.clear()
        self._in_degree_cache.clear()

    def copy(self) -> Graph:
        """کپی گراف"""
        g = Graph(directed=self.directed, name=self.name + "_copy")
        for node in self.nodes():
            g.add_node(node.node_id, node.data, **node.attrs())
        for edge in self.edges():
            g.add_edge(
                edge.src.node_id,
                edge.dst.node_id,
                edge.weight,
                edge.name,
                auto_add_nodes=False,
                **edge.attrs(),
            )
        return g

    def subgraph(self, node_ids: Any) -> Graph:
        """زیرگراف ایجاد شده توسط گره‌های داده شده"""
        ids = set(node_ids)
        for nid in ids:
            self._require_node(nid)

        g = Graph(directed=self.directed, name=self.name + "_sub")
        for nid in ids:
            node = self._nodes[nid]
            g.add_node(nid, node.data, **node.attrs())

        for edge in self.edges():
            if edge.src.node_id in ids and edge.dst.node_id in ids:
                g.add_edge(
                    edge.src.node_id,
                    edge.dst.node_id,
                    edge.weight,
                    edge.name,
                    auto_add_nodes=False,
                    **edge.attrs(),
                )
        return g

    def complement(self) -> Graph:
        """گراف مکمل (یال‌های موجود حذف، یال‌های ناموجود اضافه)"""
        comp = Graph(directed=self.directed, name=self.name + "_complement")
        
        # اضافه کردن تمام گره‌ها
        for node in self.nodes():
            comp.add_node(node.node_id, node.data, **node.attrs())
        
        # اضافه کردن یال‌های مکمل
        for src in self.nodes():
            for dst in self.nodes():
                # بدون خود یال برای undirected، با خود یال برای directed
                if self.directed:
                    if src.node_id == dst.node_id:
                        continue
                else:
                    if src.node_id >= dst.node_id:
                        continue
                
                if not self.has_edge(src.node_id, dst.node_id):
                    comp.add_edge(src.node_id, dst.node_id, auto_add_nodes=False)
        
        return comp

    # ══════════════════════════════════════════════════════════════════════════
    #  GRAPH OPERATIONS: ADD, SUB
    # ══════════════════════════════════════════════════════════════════════════

    def __add__(self, other: Union[Graph, Node, Edge]) -> Graph:
        """
        جمع دو گراف (Merge) یا اضافه کردن Node/Edge
        
        g1 + g2 = Merge کردن گراف‌ها (اتحاد)
        g + node = اضافه کردن گره
        g + edge = اضافه کردن یال
        """
        if isinstance(other, Graph):
            # Merge دو گراف
            result = self.copy()
            for node in other.nodes():
                result.add_node(node.node_id, node.data, **node.attrs())
            for edge in other.edges():
                result.add_edge(
                    edge.src.node_id,
                    edge.dst.node_id,
                    edge.weight,
                    edge.name,
                    **edge.attrs(),
                )
            return result
        elif isinstance(other, Node):
            result = self.copy()
            result.add_node_direct(other)
            return result
        elif isinstance(other, Edge):
            result = self.copy()
            result.add_edge_direct(other)
            return result
        return NotImplemented

    def __sub__(self, other: Union[Graph, Node, Edge]) -> Graph:
        """
        تفریق گراف‌ها یا حذف Node/Edge
        
        g1 - g2 = حذف گره‌ها و یال‌هایی که در g2 هستند
        g - node = حذف گره
        g - edge = حذف یال
        """
        if isinstance(other, Graph):
            result = self.copy()
            # حذف گره‌هایی که در هر دو وجود دارند
            for node in other.nodes():
                if result.has_node(node.node_id):
                    result.remove_node(node.node_id)
            return result
        elif isinstance(other, Node):
            result = self.copy()
            if result.has_node(other.node_id):
                result.remove_node(other.node_id)
            return result
        elif isinstance(other, Edge):
            result = self.copy()
            src_id, dst_id = other.endpoints()
            try:
                result.remove_edge(src_id, dst_id, other.edge_id)
            except EdgeNotFoundError:
                pass
            return result
        return NotImplemented

    # ══════════════════════════════════════════════════════════════════════════
    #  DUNDER METHODS
    # ══════════════════════════════════════════════════════════════════════════

    def __contains__(self, item: Any) -> bool:
        """
        بررسی عضویت
        
        گره_id in g → بررسی وجود گره
        edge in g → بررسی وجود یال
        graph_sub in g → بررسی subgraph بودن
        """
        if isinstance(item, Node):
            return self.has_node(item.node_id)
        elif isinstance(item, Edge):
            return self.has_edge(item.src.node_id, item.dst.node_id)
        elif isinstance(item, Graph):
            # بررسی اینکه item یک subgraph است
            for node in item.nodes():
                if not self.has_node(node.node_id):
                    return False
            for edge in item.edges():
                if not self.has_edge(edge.src.node_id, edge.dst.node_id):
                    return False
            return True
        else:
            return self.has_node(item)

    def __len__(self) -> tuple[int, int]:
        """بازگشت (تعداد_گره‌ها, تعداد_یال‌ها)"""
        return (self.order(), self.size())

    def __iter__(self) -> Iterator[Node]:
        """تکرار روی گره‌ها"""
        return self.nodes()

    def __repr__(self) -> str:
        kind = "جهت‌دار" if self.directed else "بدون‌جهت"
        return (
            f"Graph(نام={self.name!r}, نوع={kind}, "
            f"گره‌ها={self.order()}, یال‌ها={self.size()})"
        )

    # ══════════════════════════════════════════════════════════════════════════
    #  PRIVATE HELPERS
    # ══════════════════════════════════════════════════════════════════════════

    def _require_node(self, node_id: Any) -> None:
        """بررسی وجود گره، exception اگر نباشد"""
        if node_id not in self._nodes:
            raise NodeNotFoundError(node_id)

    def _inc_in_degree(self, node_id: Any, delta: int) -> None:
        """اپدیت cache درجه‌ی ورودی"""
        self._in_degree_cache[node_id] = self._in_degree_cache.get(node_id, 0) + delta
