"""
test_graph.py
=============
Unit tests for graph.py — Phase 1 (Revised)
Run with:  python -m pytest test_graph.py -v
"""

import pytest
from graph import (
    Graph,
    Node,
    Edge,
    GraphError,
    NodeNotFoundError,
    EdgeNotFoundError,
    DuplicateNodeError,
)


# ─────────────────────────────────────────────
#  Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def dg() -> Graph:
    """Small directed weighted graph used across many tests."""
    g = Graph(directed=True, name="TestDG")
    g.add_node("A", data=1, color="red")
    g.add_node("B", data=2)
    g.add_node("C", data=3)
    g.add_edge("A", "B", weight=2.0)
    g.add_edge("B", "C", weight=3.0)
    g.add_edge("A", "C", weight=5.0)
    return g


@pytest.fixture
def ug() -> Graph:
    """Small undirected graph."""
    g = Graph(directed=False, name="TestUG")
    g.add_edge("X", "Y", weight=1.0)
    g.add_edge("Y", "Z", weight=2.0)
    return g


# ─────────────────────────────────────────────
#  Node tests
# ─────────────────────────────────────────────

class TestNode:
    def test_creation(self):
        n = Node("id1", data=42, color="blue")
        assert n.node_id == "id1"
        assert n.data == 42
        assert n.get_attr("color") == "blue"

    def test_set_get_del_attr(self):
        n = Node("n")
        n.set_attr("x", 10)
        assert n.get_attr("x") == 10
        n.del_attr("x")
        assert n.get_attr("x") is None

    def test_del_missing_attr_raises(self):
        n = Node("n")
        with pytest.raises(KeyError):
            n.del_attr("nonexistent")

    def test_update_attrs_bulk(self):
        n = Node("n")
        n.update_attrs(a=1, b=2)
        assert n.attrs() == {"a": 1, "b": 2}

    def test_equality_and_hash(self):
        n1 = Node("A")
        n2 = Node("A")
        assert n1 == n2
        assert hash(n1) == hash(n2)
        assert n1 == "A"

    def test_repr(self):
        n = Node("Z", data=99)
        assert "Z" in repr(n)


# ─────────────────────────────────────────────
#  Edge tests
# ─────────────────────────────────────────────

class TestEdge:
    def test_creation(self):
        a, b = Node("A"), Node("B")
        e = Edge(a, b, weight=7.5, label="road")
        assert e.weight == 7.5
        assert e.get_attr("label") == "road"

    def test_reversed(self):
        a, b = Node("A"), Node("B")
        e = Edge(a, b, weight=4.0)
        r = e.reversed()
        assert r.src.node_id == "B"
        assert r.dst.node_id == "A"
        assert r.weight == 4.0

    def test_endpoints(self):
        a, b = Node("X"), Node("Y")
        e = Edge(a, b)
        assert e.endpoints() == ("X", "Y")

    def test_auto_edge_id(self):
        a, b = Node("A"), Node("B")
        e1, e2 = Edge(a, b), Edge(a, b)
        assert e1.edge_id != e2.edge_id


# ─────────────────────────────────────────────
#  Graph — node operations
# ─────────────────────────────────────────────

class TestGraphNodes:
    def test_add_and_get_node(self, dg):
        node = dg.get_node("A")
        assert node.node_id == "A"
        assert node.data == 1

    def test_add_node_idempotent(self, dg):
        n = dg.add_node("A")  # already exists
        assert n.node_id == "A"
        assert dg.order() == 3

    def test_add_node_strict_raises(self, dg):
        with pytest.raises(DuplicateNodeError):
            dg.add_node("A", strict=True)

    def test_remove_node_removes_edges(self, dg):
        dg.remove_node("A")
        assert not dg.has_node("A")
        assert not dg.has_edge("A", "B")
        assert not dg.has_edge("A", "C")

    def test_remove_missing_node_raises(self, dg):
        with pytest.raises(NodeNotFoundError):
            dg.remove_node("GHOST")

    def test_update_node(self, dg):
        dg.update_node("B", data=99, color="green")
        node = dg.get_node("B")
        assert node.data == 99
        assert node.get_attr("color") == "green"

    def test_has_node(self, dg):
        assert dg.has_node("A")
        assert not dg.has_node("Z")

    def test_contains_operator(self, dg):
        assert "B" in dg
        assert "Z" not in dg

    def test_len_operator(self, dg):
        assert len(dg) == 3

    def test_iter_operator(self, dg):
        ids = {n.node_id for n in dg}
        assert ids == {"A", "B", "C"}


# ─────────────────────────────────────────────
#  Graph — edge operations
# ─────────────────────────────────────────────

class TestGraphEdges:
    def test_has_edge(self, dg):
        assert dg.has_edge("A", "B")
        assert not dg.has_edge("B", "A")

    def test_get_edges(self, dg):
        edges = dg.get_edges("A", "B")
        assert len(edges) == 1
        assert edges[0].weight == 2.0

    def test_multi_edge(self, dg):
        dg.add_edge("A", "B", weight=9.9)
        edges = dg.get_edges("A", "B")
        assert len(edges) == 2

    def test_remove_edge(self, dg):
        dg.remove_edge("A", "B")
        assert not dg.has_edge("A", "B")

    def test_remove_specific_edge_id(self, dg):
        e2 = dg.add_edge("A", "B", weight=9.9)
        dg.remove_edge("A", "B", edge_id=e2.edge_id)
        edges = dg.get_edges("A", "B")
        assert len(edges) == 1  # original still there

    def test_remove_missing_edge_raises(self, dg):
        with pytest.raises(EdgeNotFoundError):
            dg.remove_edge("C", "A")

    def test_self_loop(self):
        g = Graph()
        g.add_edge("A", "A", weight=1.0)
        assert g.has_edge("A", "A")
        assert g.size() == 1

    def test_auto_add_nodes_false_raises(self):
        g = Graph()
        with pytest.raises(NodeNotFoundError):
            g.add_edge("X", "Y", auto_add_nodes=False)


# ─────────────────────────────────────────────
#  Graph — degree & traversal
# ─────────────────────────────────────────────

class TestGraphDegree:
    def test_out_degree(self, dg):
        assert dg.out_degree("A") == 2
        assert dg.out_degree("C") == 0

    def test_in_degree(self, dg):
        assert dg.in_degree("A") == 0
        assert dg.in_degree("C") == 2

    def test_in_degree_cache_after_remove(self, dg):
        dg.remove_edge("A", "C")
        assert dg.in_degree("C") == 1

    def test_neighbors_directed(self, dg):
        nids = {n.node_id for n in dg.neighbors("A")}
        assert nids == {"B", "C"}

    def test_out_edges(self, dg):
        assert len(dg.out_edges("A")) == 2

    def test_in_edges(self, dg):
        assert len(dg.in_edges("C")) == 2

    def test_undirected_degree(self, ug):
        assert ug.degree("Y") == 2  # X-Y and Y-Z

    def test_undirected_neighbors_symmetric(self, ug):
        assert any(n.node_id == "X" for n in ug.neighbors("Y"))
        assert any(n.node_id == "Y" for n in ug.neighbors("X"))


# ─────────────────────────────────────────────
#  Graph — copy & subgraph
# ─────────────────────────────────────────────

class TestGraphCopy:
    def test_copy_is_independent(self, dg):
        g2 = dg.copy()
        g2.add_node("NEW")
        assert not dg.has_node("NEW")
        assert g2.order() == dg.order() + 1

    def test_copy_preserves_edges(self, dg):
        g2 = dg.copy()
        assert g2.has_edge("A", "B")
        assert g2.size() == dg.size()

    def test_subgraph(self, dg):
        sg = dg.subgraph(["A", "B"])
        assert sg.order() == 2
        assert sg.has_edge("A", "B")
        assert not sg.has_edge("A", "C")  # C not in subgraph

    def test_subgraph_missing_node_raises(self, dg):
        with pytest.raises(NodeNotFoundError):
            dg.subgraph(["A", "GHOST"])

    def test_clear(self, dg):
        dg.clear()
        assert dg.order() == 0
        assert dg.size() == 0


# ─────────────────────────────────────────────
#  Graph — iterators
# ─────────────────────────────────────────────

class TestGraphIterators:
    def test_nodes_iter(self, dg):
        assert len(list(dg.nodes())) == 3

    def test_edges_iter_directed(self, dg):
        assert len(list(dg.edges())) == 3

    def test_edges_iter_undirected_no_duplicates(self, ug):
        edge_list = list(ug.edges())
        assert len(edge_list) == 2  # X-Y and Y-Z, not their reverses

    def test_repr(self, dg):
        r = repr(dg)
        assert "Directed" in r
        assert "TestDG" in r
