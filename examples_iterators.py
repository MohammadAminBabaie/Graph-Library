"""
مثال‌های Iterator Patterns

Licensed under Apache License 2.0
"""

from graph import Graph
from graph_iterators import add_iterators_to_graph, print_traversal


# اولین، iterators را فعال کنید
add_iterators_to_graph()


def example_1_nodes_iteration():
    """مثال ۱: تکرار روی Nodes"""
    print("\n" + "="*70)
    print("مثال ۱: تکرار روی Nodes")
    print("="*70)
    
    g = Graph(directed=True, name="شبکه")
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D")])
    
    print("\nروش ۱: استفاده از iter_nodes()")
    for node in g.iter_nodes():
        print(f"  • {node.node_id}")
    
    print("\nروش ۲: استفاده از __iter__() - default")
    for node in g:
        print(f"  • {node.node_id}")
    
    print(f"\nتعداد nodes: {len(g.iter_nodes())}")


def example_2_edges_iteration():
    """مثال ۲: تکرار روی Edges"""
    print("\n" + "="*70)
    print("مثال ۲: تکرار روی Edges")
    print("="*70)
    
    g = Graph(directed=True, name="شبکه")
    g.add_edges([
        ("A", "B", 5, "route1"),
        ("B", "C", 3, "route2"),
        ("C", "D", 2, "route3")
    ])
    
    print("\nتمام Edges:")
    for edge in g.iter_edges():
        print(f"  {edge.src.node_id} → {edge.dst.node_id}: {edge.name} (w={edge.weight})")
    
    print(f"\nتعداد edges: {len(g.iter_edges())}")


def example_3_neighbors_iteration():
    """مثال ۳: تکرار روی Neighbors"""
    print("\n" + "="*70)
    print("مثال ۳: تکرار روی Neighbors")
    print("="*70)
    
    g = Graph(directed=False, name="شبکه اجتماعی")
    g.add_edges([
        ("علی", "محمد"),
        ("علی", "فاطمه"),
        ("علی", "حسن"),
        ("محمد", "فاطمه")
    ])
    
    print("\nدوستان علی:")
    for neighbor in g.iter_neighbors("علی"):
        print(f"  • {neighbor.node_id}")
    
    print("\nدوستان محمد:")
    for neighbor in g.iter_neighbors("محمد"):
        print(f"  • {neighbor.node_id}")


def example_4_out_edges():
    """مثال ۴: یال‌های خروجی"""
    print("\n" + "="*70)
    print("مثال ۴: یال‌های خروجی یک Node")
    print("="*70)
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("A", "C"), ("A", "D"), ("B", "C")])
    
    print("\nیال‌های خروجی A:")
    for edge in g.iter_out_edges("A"):
        print(f"  A → {edge.dst.node_id}")
    
    print("\nیال‌های خروجی B:")
    for edge in g.iter_out_edges("B"):
        print(f"  B → {edge.dst.node_id}")


def example_5_in_edges():
    """مثال ۵: یال‌های ورودی"""
    print("\n" + "="*70)
    print("مثال ۵: یال‌های ورودی یک Node")
    print("="*70)
    
    g = Graph(directed=True)
    g.add_edges([("A", "D"), ("B", "D"), ("C", "D")])
    
    print("\nیال‌های ورودی D:")
    for edge in g.iter_in_edges("D"):
        print(f"  {edge.src.node_id} → D")


def example_6_dfs_traversal():
    """مثال ۶: DFS Traversal"""
    print("\n" + "="*70)
    print("مثال ۶: DFS (Depth First Search)")
    print("="*70)
    
    g = Graph(directed=True)
    g.add_edges([
        ("A", "B"), ("A", "C"),
        ("B", "D"), ("B", "E"),
        ("C", "F"), ("D", "G")
    ])
    
    print("\nدرخت:")
    print("      A")
    print("     / \\")
    print("    B   C")
    print("   / \\   \\")
    print("  D   E   F")
    print(" /")
    print("G")
    
    print("\nDFS از A:")
    for node in g.iter_dfs("A"):
        print(f"  {node.node_id}", end=" → ")
    print("END")


def example_7_bfs_traversal():
    """مثال ۷: BFS Traversal"""
    print("\n" + "="*70)
    print("مثال ۷: BFS (Breadth First Search)")
    print("="*70)
    
    g = Graph(directed=True)
    g.add_edges([
        ("A", "B"), ("A", "C"),
        ("B", "D"), ("B", "E"),
        ("C", "F"), ("D", "G")
    ])
    
    print("\nBFS از A:")
    for node in g.iter_bfs("A"):
        print(f"  {node.node_id}", end=" → ")
    print("END")
    
    print("\n\nمقایسه:")
    print_traversal(g, "A", "dfs")
    print_traversal(g, "A", "bfs")


def example_8_iteration_patterns():
    """مثال ۸: الگوهای مختلف Iteration"""
    print("\n" + "="*70)
    print("مثال ۸: الگوهای Iteration")
    print("="*70)
    
    g = Graph(directed=False)
    g.add_edges([("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")])
    
    print("\nالگو ۱: تمام nodes")
    nodes_list = [n.node_id for n in g.iter_nodes()]
    print(f"  {nodes_list}")
    
    print("\nالگو ۲: تمام edges")
    edges_list = [(e.src.node_id, e.dst.node_id) for e in g.iter_edges()]
    print(f"  {edges_list}")
    
    print("\nالگو ۳: برای هر node، neighbors")
    for node in g.iter_nodes():
        neighbors = [n.node_id for n in g.iter_neighbors(node.node_id)]
        print(f"  {node.node_id}: {neighbors}")
    
    print("\nالگو ۴: برای هر edge، weight")
    for edge in g.iter_edges():
        print(f"  {edge.src.node_id}-{edge.dst.node_id}: w={edge.weight}")


def example_9_filtering_iteration():
    """مثال ۹: Filtering During Iteration"""
    print("\n" + "="*70)
    print("مثال ۹: Filtering During Iteration")
    print("="*70)
    
    g = Graph(directed=True)
    g.add_edges([
        ("A", "B", 1),
        ("A", "C", 5),
        ("B", "D", 2),
        ("C", "D", 3),
        ("D", "E", 1)
    ])
    
    print("\nتمام edges:")
    all_edges = list(g.iter_edges())
    for edge in all_edges:
        print(f"  {edge.src.node_id} → {edge.dst.node_id}: w={edge.weight}")
    
    print("\nفقط edges با weight > 1:")
    heavy_edges = [e for e in g.iter_edges() if e.weight > 1]
    for edge in heavy_edges:
        print(f"  {edge.src.node_id} → {edge.dst.node_id}: w={edge.weight}")
    
    print("\nNodes با بیش از 1 neighbor:")
    for node in g.iter_nodes():
        neighbors = list(g.iter_neighbors(node.node_id))
        if len(neighbors) > 1:
            print(f"  {node.node_id}: {[n.node_id for n in neighbors]}")


def example_10_complex_traversal():
    """مثال ۱۰: Traversal پیچیده"""
    print("\n" + "="*70)
    print("مثال ۱۰: Traversal پیچیده (Social Network)")
    print("="*70)
    
    # شبکه اجتماعی
    g = Graph(directed=False, name="Social Network")
    g.add_edges([
        ("علی", "محمد"),
        ("علی", "فاطمه"),
        ("محمد", "حسن"),
        ("فاطمه", "زینب"),
        ("حسن", "زینب"),
        ("زینب", "سارا")
    ])
    
    print("\nتمام افراد:")
    for person in g.iter_nodes():
        print(f"  {person.node_id}")
    
    print("\nتمام رابطه‌ها:")
    for edge in g.iter_edges():
        print(f"  {edge.src.node_id} ↔ {edge.dst.node_id}")
    
    print("\nدوستان هر نفر:")
    for person in g.iter_nodes():
        friends = [f.node_id for f in g.iter_neighbors(person.node_id)]
        print(f"  {person.node_id}: {friends}")
    
    print("\nBFS از علی (تا دو درجه):")
    bfs_nodes = list(g.iter_bfs("علی"))
    print(f"  {[n.node_id for n in bfs_nodes]}")


# فهرست
EXAMPLES = {
    "1": example_1_nodes_iteration,
    "2": example_2_edges_iteration,
    "3": example_3_neighbors_iteration,
    "4": example_4_out_edges,
    "5": example_5_in_edges,
    "6": example_6_dfs_traversal,
    "7": example_7_bfs_traversal,
    "8": example_8_iteration_patterns,
    "9": example_9_filtering_iteration,
    "10": example_10_complex_traversal,
}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        num = sys.argv[1]
        if num in EXAMPLES:
            EXAMPLES[num]()
        else:
            print(f"مثال {num} پیدا نشد")
    else:
        print("\n" + "="*70)
        print("🔄 Iterator Examples")
        print("="*70)
        print("\nاستفاده: python examples_iterators.py [شماره]")
        print("مثال: python examples_iterators.py 1")
        print("\nمثال‌های موجود:")
        print("  1. Nodes iteration")
        print("  2. Edges iteration")
        print("  3. Neighbors iteration")
        print("  4. Out edges")
        print("  5. In edges")
        print("  6. DFS traversal")
        print("  7. BFS traversal")
        print("  8. Iteration patterns")
        print("  9. Filtering iteration")
        print("  10. Complex traversal")
        print("\nیا برای اجرای تمام:")
        print("  for i in 1 2 3 4 5 6 7 8 9 10; do python examples_iterators.py $i; done")
