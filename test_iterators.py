"""
تست‌های Iterator

Licensed under Apache License 2.0
"""

import sys
from graph import Graph
from graph_iterators import (
    add_iterators_to_graph,
    NodesIterator, EdgesIterator, NeighborsIterator,
    DFSIterator, BFSIterator
)

# فعال کردن iterators
add_iterators_to_graph()


def test_nodes_iterator():
    """تست NodesIterator"""
    print("\n🔵 تست NodesIterator")
    
    g = Graph(directed=True)
    g.add_nodes(["A", "B", "C"])
    
    iterator = g.iter_nodes()
    assert len(iterator) == 3, "تعداد nodes نادرست"
    
    nodes = list(iterator)
    assert len(nodes) == 3, "تعداد nodes در iteration نادرست"
    
    print("  ✅ NodesIterator")


def test_edges_iterator():
    """تست EdgesIterator"""
    print("\n🟠 تست EdgesIterator")
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D")])
    
    iterator = g.iter_edges()
    assert len(iterator) == 3, "تعداد edges نادرست"
    
    edges = list(iterator)
    assert len(edges) == 3, "تعداد edges در iteration نادرست"
    
    print("  ✅ EdgesIterator")


def test_neighbors_iterator():
    """تست NeighborsIterator"""
    print("\n🟡 تست NeighborsIterator")
    
    g = Graph(directed=False)
    g.add_edges([("A", "B"), ("A", "C"), ("A", "D")])
    
    neighbors = g.iter_neighbors("A")
    assert len(neighbors) == 3, "تعداد neighbors نادرست"
    
    neighbor_list = list(neighbors)
    assert len(neighbor_list) == 3, "تعداد neighbors در iteration نادرست"
    
    print("  ✅ NeighborsIterator")


def test_out_edges_iterator():
    """تست Out Edges Iterator"""
    print("\n🟢 تست OutEdgesIterator")
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("A", "C"), ("B", "D")])
    
    out_edges = g.iter_out_edges("A")
    assert len(out_edges) == 2, "تعداد out_edges نادرست"
    
    print("  ✅ OutEdgesIterator")


def test_in_edges_iterator():
    """تست In Edges Iterator"""
    print("\n🔵 تست InEdgesIterator")
    
    g = Graph(directed=True)
    g.add_edges([("A", "D"), ("B", "D"), ("C", "D")])
    
    in_edges = g.iter_in_edges("D")
    assert len(in_edges) == 3, "تعداد in_edges نادرست"
    
    print("  ✅ InEdgesIterator")


def test_dfs_iterator():
    """تست DFS Iterator"""
    print("\n🟠 تست DFSIterator")
    
    g = Graph(directed=True)
    g.add_edges([
        ("A", "B"), ("A", "C"),
        ("B", "D"), ("C", "E")
    ])
    
    dfs = g.iter_dfs("A")
    assert len(dfs) == 5, "تعداد DFS nodes نادرست"
    
    nodes = list(dfs)
    assert nodes[0].node_id == "A", "DFS از A شروع نشده"
    
    print("  ✅ DFSIterator")


def test_bfs_iterator():
    """تست BFS Iterator"""
    print("\n🟡 تست BFSIterator")
    
    g = Graph(directed=True)
    g.add_edges([
        ("A", "B"), ("A", "C"),
        ("B", "D"), ("C", "E")
    ])
    
    bfs = g.iter_bfs("A")
    assert len(bfs) == 5, "تعداد BFS nodes نادرست"
    
    nodes = list(bfs)
    assert nodes[0].node_id == "A", "BFS از A شروع نشده"
    
    # BFS level by level: A, B-C, D-E
    assert nodes[1].node_id in ["B", "C"], "BFS order غلط"
    
    print("  ✅ BFSIterator")


def test_iteration_multiple_times():
    """تست تکرار iteration"""
    print("\n🟢 تست تکرار Iteration")
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("B", "C")])
    
    iterator = g.iter_nodes()
    
    # اولین بار
    nodes1 = list(iterator)
    assert len(nodes1) == 3, "اولین iteration نادرست"
    
    # دوبار
    nodes2 = list(iterator)
    assert len(nodes2) == 3, "دوم iteration نادرست"
    
    print("  ✅ تکرار Iterator")


def test_filtering():
    """تست filtering"""
    print("\n🔵 تست Filtering")
    
    g = Graph(directed=True)
    g.add_edges([
        ("A", "B", 1),
        ("B", "C", 5),
        ("C", "D", 2)
    ])
    
    # فقط heavy edges
    heavy = [e for e in g.iter_edges() if e.weight > 2]
    assert len(heavy) == 1, "filtering نادرست"
    assert heavy[0].weight == 5, "وزن غلط"
    
    print("  ✅ Filtering")


def test_iteration_with_default():
    """تست default iteration"""
    print("\n🟠 تست Default Iteration")
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("B", "C")])
    
    # default: nodes
    default_items = list(g)
    assert len(default_items) == 3, "default iteration نادرست"
    
    print("  ✅ Default Iteration (Nodes)")


def main():
    print("\n" + "="*70)
    print("🧪 تست‌های Iterator")
    print("="*70)
    
    tests = [
        test_nodes_iterator,
        test_edges_iterator,
        test_neighbors_iterator,
        test_out_edges_iterator,
        test_in_edges_iterator,
        test_dfs_iterator,
        test_bfs_iterator,
        test_iteration_multiple_times,
        test_filtering,
        test_iteration_with_default,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"✅ {passed}/{len(tests)} تست گذاشت")
    if failed > 0:
        print(f"❌ {failed} تست ناموفق")
    print("="*70 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
