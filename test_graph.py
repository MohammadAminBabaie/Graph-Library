"""
تست‌های واحدی برای Graph Library

Licensed under Apache License 2.0
اجرا: python test_graph.py
"""

import sys
from graph import Graph, Node, Edge, GraphError, NodeNotFoundError, EdgeNotFoundError, DuplicateNodeError


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def test(self, name: str, condition: bool, message: str = ""):
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            print(f"  ❌ {name}")
            if message:
                print(f"     {message}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*70}")
        print(f"نتایج: {self.passed}/{total} تست گذاشت")
        print(f"{'='*70}\n")
        return self.failed == 0


def test_node_creation():
    print("\n🔵 تست‌های Node")
    runner = TestRunner()
    
    node = Node("A")
    runner.test("ایجاد گره", node.node_id == "A")
    
    node = Node("B", data={"value": 10})
    runner.test("گره با data", node.data["value"] == 10)
    
    node = Node("C", color="red")
    runner.test("گره با attributes", node.get_attr("color") == "red")
    
    return runner.summary()


def test_edge_creation():
    print("\n🟠 تست‌های Edge")
    runner = TestRunner()
    
    n1, n2 = Node("A"), Node("B")
    edge = Edge(n1, n2)
    runner.test("ایجاد یال", edge.src.node_id == "A")
    runner.test("نام خودکار یال", edge.name == "A_B")
    
    edge = Edge(n1, n2, weight=5.0, name="مسیر")
    runner.test("یال با نام کاستم", edge.name == "مسیر")
    runner.test("وزن یال", edge.weight == 5.0)
    
    reversed_edge = edge.reversed()
    runner.test("یال معکوس", reversed_edge.src.node_id == "B")
    runner.test("نام معکوس", "rev" in reversed_edge.name)
    
    return runner.summary()


def test_graph_basic():
    print("\n🟢 تست‌های Graph - پایه‌ای")
    runner = TestRunner()
    
    g = Graph(directed=True)
    runner.test("گراف جهت‌دار", g.directed == True)
    
    g.add_node("A")
    runner.test("افزودن گره", g.has_node("A"))
    runner.test("تعداد گره", g.order() == 1)
    
    g.add_edge("A", "B")
    runner.test("افزودن یال و گره خودکار", g.has_node("B"))
    runner.test("تعداد یال", g.num_edges() == 1)
    
    return runner.summary()


def test_graph_batch_operations():
    print("\n🟡 تست‌های Graph - عملیات دسته‌ای")
    runner = TestRunner()
    
    g = Graph(directed=True)
    
    nodes = [Node(f"Node{i}") for i in range(3)]
    g.add_nodes(nodes)
    runner.test("افزودن دسته‌ای گره‌ها", g.order() == 3)
    
    edges = [("Node0", "Node1"), ("Node1", "Node2")]
    g.add_edges(edges)
    runner.test("افزودن دسته‌ای یال‌ها", g.num_edges() == 2)
    
    e = Edge(g.get_node("Node0"), g.get_node("Node2"), name="مسیر مستقیم")
    g.add_edge_direct(e)
    runner.test("افزودن Edge مستقیم", g.num_edges("Node0", "Node2") == 1)
    
    return runner.summary()


def test_graph_update():
    print("\n🔵 تست‌های Graph - اپدیت")
    runner = TestRunner()
    
    g = Graph(directed=True)
    g.add_edge("A", "B", weight=1.0)
    
    g.update_edge("A", "B", weight=5.0)
    runner.test("اپدیت وزن", g.get_edges("A", "B")[0].weight == 5.0)
    
    g.update_edge("A", "B", name="نام جدید")
    runner.test("اپدیت نام", g.get_edges("A", "B")[0].name == "نام جدید")
    
    return runner.summary()


def test_graph_operations():
    print("\n🟠 تست‌های Graph - عملیات (جمع/تفریق)")
    runner = TestRunner()
    
    g1 = Graph(directed=True, name="G1")
    g1.add_edges([("A", "B"), ("B", "C")])
    
    g2 = Graph(directed=True, name="G2")
    g2.add_edges([("C", "D")])
    
    g_merged = g1 + g2
    runner.test("Merge گراف‌ها", g_merged.order() == 4)
    runner.test("Merge یال‌ها", g_merged.size() == 3)
    
    g_sub = g_merged - g1
    runner.test("تفریق گراف‌ها", g_sub.order() < g_merged.order())
    
    g_node = g1 + Node("X")
    runner.test("افزودن Node", g_node.has_node("X"))
    
    return runner.summary()


def test_graph_len():
    print("\n🟡 تست‌های Graph - len()")
    runner = TestRunner()
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D")])
    
    runner.test("len() بازگشت int", isinstance(len(g), int))
    runner.test("len() تعداد گره‌ها", len(g) == 4)
    
    result = g.counts()
    runner.test("counts() تعداد یال‌ها", result[1] == 3)
    
    return runner.summary()


def test_graph_contains():
    print("\n🟢 تست‌های Graph - __contains__")
    runner = TestRunner()
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("B", "C")])
    
    runner.test("گره در گراف", "A" in g)
    runner.test("گره خارج گراف", "D" not in g)
    
    edge = g.get_edges("A", "B")[0]
    runner.test("یال در گراف", edge in g)
    
    sub = g.subgraph(["A", "B"])
    runner.test("زیرگراف در گراف", sub in g)
    
    return runner.summary()


def test_graph_complement():
    print("\n🔵 تست‌های Graph - مکمل")
    runner = TestRunner()
    
    g = Graph(directed=False, name="Original")
    g.add_edges([("A", "B"), ("B", "C")])
    
    comp = g.complement()
    runner.test("مکمل دارای تمام گره‌ها", comp.order() == g.order())
    runner.test("مکمل یال‌های بیشتر دارد", comp.size() >= g.size())
    
    return runner.summary()


def test_graph_degree():
    print("\n🟠 تست‌های Graph - درجات")
    runner = TestRunner()
    
    g = Graph(directed=True)
    g.add_edges([("A", "B"), ("A", "C"), ("B", "C")])
    
    runner.test("out_degree", g.out_degree("A") == 2)
    runner.test("in_degree", g.in_degree("C") == 2)
    runner.test("درجه کل (directed)", g.degree("B") == 2)
    
    return runner.summary()


def test_errors():
    print("\n🟡 تست‌های خطاها")
    runner = TestRunner()
    
    g = Graph(directed=True)
    g.add_node("A")
    g.add_node("B")
    
    try:
        g.get_node("NotExist")
        runner.test("NodeNotFoundError", False)
    except NodeNotFoundError:
        runner.test("NodeNotFoundError", True)
    
    try:
        g.remove_edge("A", "Z")
        runner.test("EdgeNotFoundError", False)
    except NodeNotFoundError:
        runner.test("EdgeNotFoundError", True)
    
    try:
        g.add_node("A", strict=True)
        runner.test("DuplicateNodeError", False)
    except DuplicateNodeError:
        runner.test("DuplicateNodeError", True)
    
    return runner.summary()


def main():
    print("\n" + "="*70)
    print("🧪 تست‌های Graph Library")
    print("="*70)
    
    results = [
        test_node_creation(),
        test_edge_creation(),
        test_graph_basic(),
        test_graph_batch_operations(),
        test_graph_update(),
        test_graph_operations(),
        test_graph_len(),
        test_graph_contains(),
        test_graph_complement(),
        test_graph_degree(),
        test_errors(),
    ]
    
    print("\n" + "="*70)
    total_passed = sum(1 for r in results if r)
    total_tests = len(results)
    print(f"✅ {total_passed}/{total_tests} بخش تست گذاشت")
    print("="*70 + "\n")
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
