"""
graph.py
========
Professional Graph Library — Phase 1 (Revised)

Design goals
------------
- Fully dynamic: nodes and edges can be added or removed at any time.
- Clean and principled: single-responsibility classes, consistent error handling.
- Performant: O(1) node lookup; cached in-degree; lazy edge deduplication.
- Extensible: open attribute dictionaries on every Node and Edge.
- Pythonic: supports `in`, `len`, `iter`, and `repr` everywhere.

Public API
----------
    Node(node_id, data, **attrs)
    Edge(src, dst, weight, **attrs)
    Graph(directed, name)
        .add_node / .remove_node / .has_node / .get_node / .update_node
        .add_edge / .remove_edge / .has_edge / .get_edges
        .neighbors / .out_edges / .in_edges
        .out_degree / .in_degree / .degree
        .nodes() / .edges()
        .order() / .size()
        .copy() / .subgraph(node_ids) / .clear()
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Iterator, Optional


# ══════════════════════════════════════════════════════════════════════════════
#  Exceptions
# ══════════════════════════════════════════════════════════════════════════════

class GraphError(Exception):
    """Base exception for all graph-related errors."""


class NodeNotFoundError(GraphError):
    def __init__(self, node_id: Any) -> None:
        super().__init__(f"Node not found: {node_id!r}")
        self.node_id = node_id


class EdgeNotFoundError(GraphError):
    def __init__(self, src_id: Any, dst_id: Any, edge_id: Optional[str] = None) -> None:
        detail = f" (edge_id={edge_id!r})" if edge_id else ""
        super().__init__(f"Edge not found: {src_id!r} -> {dst_id!r}{detail}")
        self.src_id = src_id
        self.dst_id = dst_id


class DuplicateNodeError(GraphError):
    def __init__(self, node_id: Any) -> None:
        super().__init__(f"Node already exists: {node_id!r}")
        self.node_id = node_id


# ══════════════════════════════════════════════════════════════════════════════
#  AttrMixin — shared attribute store for Node and Edge
# ══════════════════════════════════════════════════════════════════════════════

class AttrMixin:
    """
    Lightweight key-value attribute store.
    Allows any Node or Edge to carry arbitrary metadata.
    """

    def __init__(self) -> None:
        self._attrs: dict[str, Any] = {}

    def set_attr(self, key: str, value: Any) -> None:
        """Set a metadata attribute."""
        self._attrs[key] = value

    def get_attr(self, key: str, default: Any = None) -> Any:
        """Get a metadata attribute, returning *default* if missing."""
        return self._attrs.get(key, default)

    def del_attr(self, key: str) -> None:
        """Delete a metadata attribute. Raises KeyError if missing."""
        if key not in self._attrs:
            raise KeyError(f"Attribute not found: {key!r}")
        del self._attrs[key]

    def attrs(self) -> dict[str, Any]:
        """Return a shallow copy of all attributes."""
        return dict(self._attrs)

    def update_attrs(self, **kwargs: Any) -> None:
        """Bulk-update multiple attributes at once."""
        self._attrs.update(kwargs)


# ══════════════════════════════════════════════════════════════════════════════
#  Node
# ══════════════════════════════════════════════════════════════════════════════

class Node(AttrMixin):
    """
    A vertex in the graph.

    Parameters
    ----------
    node_id : Any hashable
        Unique identifier for this node.
    data : Any, optional
        Arbitrary user payload (object, dict, dataclass, …).
    **attrs :
        Initial metadata attributes (e.g. color="red", weight=3).

    Examples
    --------
    >>> n = Node("A", data={"population": 1_000_000}, color="blue")
    >>> n.get_attr("color")
    'blue'
    """

    __slots__ = ("node_id", "data", "_attrs")

    def __init__(self, node_id: Any, data: Any = None, **attrs: Any) -> None:
        super().__init__()
        self.node_id = node_id
        self.data = data
        self._attrs.update(attrs)

    # ── Dunder helpers ───────────────────────────────────────────────────────
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
#  Edge
# ══════════════════════════════════════════════════════════════════════════════

class Edge(AttrMixin):
    """
    A directed arc between two nodes.

    Parameters
    ----------
    src : Node
        Source (tail) node.
    dst : Node
        Destination (head) node.
    weight : float
        Numeric weight (default 1.0).
    edge_id : str, optional
        Unique identifier — auto-generated if omitted.
        Required to distinguish parallel edges (multi-graph).
    **attrs :
        Initial metadata attributes (e.g. capacity=100, label="road").

    Notes
    -----
    In an undirected Graph, a reverse shadow edge is stored automatically.
    Both the forward and reverse edge share the same base edge_id
    (the reverse is suffixed with ``_r``).
    """

    __slots__ = ("src", "dst", "weight", "edge_id", "_attrs")

    def __init__(
        self,
        src: Node,
        dst: Node,
        weight: float = 1.0,
        edge_id: Optional[str] = None,
        **attrs: Any,
    ) -> None:
        super().__init__()
        self.src = src
        self.dst = dst
        self.weight = weight
        self.edge_id: str = edge_id or str(uuid.uuid4())[:8]
        self._attrs.update(attrs)

    # ── Utilities ────────────────────────────────────────────────────────────
    def reversed(self) -> Edge:
        """Return a new Edge with src and dst swapped (same weight & attrs)."""
        return Edge(self.dst, self.src, self.weight, self.edge_id + "_r", **self._attrs)

    def endpoints(self) -> tuple[Any, Any]:
        """Return (src.node_id, dst.node_id)."""
        return (self.src.node_id, self.dst.node_id)

    # ── Dunder helpers ───────────────────────────────────────────────────────
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Edge):
            return self.edge_id == other.edge_id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.edge_id)

    def __repr__(self) -> str:
        return f"Edge({self.src.node_id!r} -> {self.dst.node_id!r}, w={self.weight}, id={self.edge_id!r})"


# ══════════════════════════════════════════════════════════════════════════════
#  Graph
# ══════════════════════════════════════════════════════════════════════════════

class Graph:
    """
    General-purpose graph supporting:

    - **Directed** or **Undirected** mode
    - **Weighted** edges
    - **Multi-edges** (parallel edges between the same pair of nodes)
    - **Self-loops** (edge from a node to itself)

    Internal representation
    -----------------------
    ``_nodes`` : dict[node_id -> Node]
        O(1) node lookup by id.
    ``_adj`` : dict[node_id -> list[Edge]]
        Adjacency list; for undirected graphs the reverse shadow edge is stored
        under the destination node so that ``out_edges`` works symmetrically.
    ``_in_degree_cache`` : dict[node_id -> int]
        Cached in-degree counter updated incrementally on every add/remove.
        Avoids O(V+E) scans for ``in_degree()``.

    Parameters
    ----------
    directed : bool
        ``True`` (default) for a digraph; ``False`` for an undirected graph.
    name : str
        Human-readable label for display / serialisation.
    """

    def __init__(self, directed: bool = True, name: str = "G") -> None:
        self.name = name
        self.directed = directed
        self._nodes: dict[Any, Node] = {}
        self._adj:   dict[Any, list[Edge]] = {}
        self._in_degree_cache: dict[Any, int] = {}

    # ══════════════════════════════════════════════════════════════════════════
    #  Internal helpers
    # ══════════════════════════════════════════════════════════════════════════

    def _require_node(self, node_id: Any) -> Node:
        """Return the node or raise NodeNotFoundError."""
        try:
            return self._nodes[node_id]
        except KeyError:
            raise NodeNotFoundError(node_id)

    def _inc_in_degree(self, node_id: Any, delta: int = 1) -> None:
        self._in_degree_cache[node_id] = self._in_degree_cache.get(node_id, 0) + delta

    # ══════════════════════════════════════════════════════════════════════════
    #  1. Node operations
    # ══════════════════════════════════════════════════════════════════════════

    def add_node(
        self,
        node_id: Any,
        data: Any = None,
        *,
        strict: bool = False,
        **attrs: Any,
    ) -> Node:
        """
        Add a node to the graph and return it.

        Parameters
        ----------
        node_id : Any hashable
            Unique identifier.
        data : Any, optional
            User payload.
        strict : bool
            If ``True``, raise ``DuplicateNodeError`` when the node already exists.
            Default is ``False`` (idempotent — existing node is returned as-is).
        **attrs :
            Metadata attributes for the new node.

        Returns
        -------
        Node

        Examples
        --------
        >>> g = Graph()
        >>> g.add_node("A", data=42, color="red")
        Node('A', data=42)
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

    def remove_node(self, node_id: Any) -> Node:
        """
        Remove a node and every edge incident to it.

        Returns
        -------
        Node
            The removed node (caller may inspect its data).

        Raises
        ------
        NodeNotFoundError
        """
        node = self._require_node(node_id)

        # Count how many in-edges we are about to delete (for cache correctness)
        for edge_list in self._adj.values():
            for e in edge_list:
                if e.dst.node_id == node_id:
                    self._inc_in_degree(node_id, -1)

        del self._nodes[node_id]
        del self._adj[node_id]
        del self._in_degree_cache[node_id]

        # Remove all edges pointing to this node from other adjacency lists
        for nid in self._adj:
            before = len(self._adj[nid])
            self._adj[nid] = [e for e in self._adj[nid] if e.dst.node_id != node_id]
            removed = before - len(self._adj[nid])
            if removed:
                self._inc_in_degree(node_id, 0)  # no-op: node already deleted

        return node

    def update_node(self, node_id: Any, data: Any = None, **attrs: Any) -> Node:
        """
        Update the data payload and/or attributes of an existing node.

        Parameters
        ----------
        node_id :
            Target node.
        data :
            New payload (``None`` leaves the existing payload unchanged).
        **attrs :
            Attributes to set or overwrite.

        Returns
        -------
        Node
        """
        node = self._require_node(node_id)
        if data is not None:
            node.data = data
        node.update_attrs(**attrs)
        return node

    def has_node(self, node_id: Any) -> bool:
        return node_id in self._nodes

    def get_node(self, node_id: Any) -> Node:
        return self._require_node(node_id)

    # ══════════════════════════════════════════════════════════════════════════
    #  2. Edge operations
    # ══════════════════════════════════════════════════════════════════════════

    def add_edge(
        self,
        src_id: Any,
        dst_id: Any,
        weight: float = 1.0,
        *,
        auto_add_nodes: bool = True,
        **attrs: Any,
    ) -> Edge:
        """
        Add a directed (or undirected) edge between two nodes.

        Parameters
        ----------
        src_id, dst_id :
            Node identifiers for the endpoints.
        weight : float
            Edge weight (default 1.0).
        auto_add_nodes : bool
            When ``True`` (default), missing nodes are created automatically.
            When ``False``, a ``NodeNotFoundError`` is raised instead.
        **attrs :
            Metadata attributes for the new edge.

        Returns
        -------
        Edge

        Examples
        --------
        >>> g = Graph()
        >>> g.add_edge("A", "B", weight=3.5, capacity=100)
        Edge('A' -> 'B', w=3.5, id=...)
        """
        if auto_add_nodes:
            self.add_node(src_id)
            self.add_node(dst_id)
        else:
            self._require_node(src_id)
            self._require_node(dst_id)

        src = self._nodes[src_id]
        dst = self._nodes[dst_id]

        edge = Edge(src, dst, weight, **attrs)
        self._adj[src_id].append(edge)
        self._inc_in_degree(dst_id)

        if not self.directed and src_id != dst_id:
            self._adj[dst_id].append(edge.reversed())
            self._inc_in_degree(src_id)

        return edge

    def remove_edge(
        self,
        src_id: Any,
        dst_id: Any,
        edge_id: Optional[str] = None,
    ) -> Edge:
        """
        Remove an edge and return it.

        Parameters
        ----------
        src_id, dst_id :
            Endpoints.
        edge_id : str, optional
            When provided, only the edge with this id is removed
            (essential for multi-graphs).  Otherwise the first
            matching edge is removed.

        Returns
        -------
        Edge
            The removed edge.

        Raises
        ------
        NodeNotFoundError, EdgeNotFoundError
        """
        self._require_node(src_id)

        removed_edge: Optional[Edge] = None
        new_list: list[Edge] = []

        for e in self._adj[src_id]:
            if removed_edge is None and e.dst.node_id == dst_id:
                if edge_id is None or e.edge_id == edge_id:
                    removed_edge = e
                    continue
            new_list.append(e)

        if removed_edge is None:
            raise EdgeNotFoundError(src_id, dst_id, edge_id)

        self._adj[src_id] = new_list
        self._inc_in_degree(dst_id, -1)

        if not self.directed and src_id != dst_id:
            rid = removed_edge.edge_id + "_r"
            self._adj[dst_id] = [e for e in self._adj[dst_id] if e.edge_id != rid]
            self._inc_in_degree(src_id, -1)

        return removed_edge

    def has_edge(self, src_id: Any, dst_id: Any) -> bool:
        """Return ``True`` if at least one edge exists from *src_id* to *dst_id*."""
        adj = self._adj.get(src_id)
        if adj is None:
            return False
        return any(e.dst.node_id == dst_id for e in adj)

    def get_edges(self, src_id: Any, dst_id: Any) -> list[Edge]:
        """
        Return all edges from *src_id* to *dst_id*.
        Returns an empty list when no edge exists (never raises).
        """
        adj = self._adj.get(src_id, [])
        return [e for e in adj if e.dst.node_id == dst_id]

    # ══════════════════════════════════════════════════════════════════════════
    #  3. Traversal helpers
    # ══════════════════════════════════════════════════════════════════════════

    def neighbors(self, node_id: Any) -> list[Node]:
        """Return deduplicated adjacent nodes (order = first-seen)."""
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
        """Return all outgoing edges from *node_id*."""
        self._require_node(node_id)
        return list(self._adj[node_id])

    def in_edges(self, node_id: Any) -> list[Edge]:
        """
        Return all edges whose destination is *node_id*.

        Note: O(V + E) scan — use sparingly on large graphs.
        For repeated in-edge queries, consider a reverse-adjacency index.
        """
        self._require_node(node_id)
        return [
            e
            for adj in self._adj.values()
            for e in adj
            if e.dst.node_id == node_id
        ]

    # ══════════════════════════════════════════════════════════════════════════
    #  4. Degree queries  (in_degree = O(1) via cache)
    # ══════════════════════════════════════════════════════════════════════════

    def out_degree(self, node_id: Any) -> int:
        self._require_node(node_id)
        return len(self._adj[node_id])

    def in_degree(self, node_id: Any) -> int:
        """O(1) — reads from the incremental cache."""
        self._require_node(node_id)
        return self._in_degree_cache.get(node_id, 0)

    def degree(self, node_id: Any) -> int:
        """
        Degree of a node.

        - Undirected: number of incident edges (self-loops counted once).
        - Directed: ``in_degree + out_degree``.
        """
        if self.directed:
            return self.in_degree(node_id) + self.out_degree(node_id)
        return self.out_degree(node_id)

    # ══════════════════════════════════════════════════════════════════════════
    #  5. Iterators
    # ══════════════════════════════════════════════════════════════════════════

    def nodes(self) -> Iterator[Node]:
        """Iterate over all nodes in insertion order."""
        return iter(self._nodes.values())

    def edges(self) -> Iterator[Edge]:
        """
        Iterate over every edge exactly once.

        For undirected graphs, shadow reverse edges (suffix ``_r``) are skipped
        so each physical edge is yielded only once.
        """
        seen: set[str] = set()
        for adj in self._adj.values():
            for e in adj:
                # Skip shadow reverse edges created for undirected graphs
                if e.edge_id.endswith("_r"):
                    continue
                if e.edge_id not in seen:
                    seen.add(e.edge_id)
                    yield e

    # ══════════════════════════════════════════════════════════════════════════
    #  6. Graph-level operations
    # ══════════════════════════════════════════════════════════════════════════

    def order(self) -> int:
        """Number of nodes (graph order)."""
        return len(self._nodes)

    def size(self) -> int:
        """Number of edges (graph size), counting undirected edges once."""
        return sum(1 for _ in self.edges())

    def clear(self) -> None:
        """Remove all nodes and edges, resetting the graph to empty."""
        self._nodes.clear()
        self._adj.clear()
        self._in_degree_cache.clear()

    def copy(self) -> Graph:
        """
        Return a shallow copy of this graph.

        Nodes and Edges are new objects; their ``.data`` payloads are
        *not* deep-copied (shared references are preserved).
        """
        g = Graph(directed=self.directed, name=self.name + "_copy")
        for node in self.nodes():
            g.add_node(node.node_id, node.data, **node.attrs())
        for edge in self.edges():
            g.add_edge(
                edge.src.node_id,
                edge.dst.node_id,
                edge.weight,
                auto_add_nodes=False,
                **edge.attrs(),
            )
        return g

    def subgraph(self, node_ids: Any) -> Graph:
        """
        Return a new graph induced by the given node ids.

        Only edges where *both* endpoints are in *node_ids* are included.

        Parameters
        ----------
        node_ids : iterable of node ids

        Returns
        -------
        Graph

        Raises
        ------
        NodeNotFoundError
            If any requested node id does not exist in this graph.
        """
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
                    auto_add_nodes=False,
                    **edge.attrs(),
                )
        return g

    # ══════════════════════════════════════════════════════════════════════════
    #  7. Python dunder interface
    # ══════════════════════════════════════════════════════════════════════════

    def __contains__(self, node_id: Any) -> bool:
        """Support ``node_id in graph`` syntax."""
        return node_id in self._nodes

    def __len__(self) -> int:
        """Return the number of nodes (``len(graph)``)."""
        return self.order()

    def __iter__(self) -> Iterator[Node]:
        """Iterate over nodes (``for node in graph``)."""
        return self.nodes()

    def __repr__(self) -> str:
        kind = "Directed" if self.directed else "Undirected"
        return (
            f"Graph(name={self.name!r}, type={kind}, "
            f"nodes={self.order()}, edges={self.size()})"
        )
