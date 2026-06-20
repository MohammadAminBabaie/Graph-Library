"""
مثال‌های کامل - تمام ویژگی‌های Graph Library

Licensed under Apache License 2.0
"""

from graph import Graph, Node, Edge
from graph_renderer import render_graph


def example_1_basic():
    """مثال 1: گراف پایه‌ای"""
    print("=" * 70)
    print("مثال 1: گراف پایه‌ای جهت‌دار")
    print("=" * 70)
    
    g = Graph(directed=True, name="شهرهای ایران")
    g.add_edge("تهران", "قم", weight=140, name="بزرگراه")
    g.add_edge("قم", "اصفهان", weight=240, name="جاده‌ی اصلی")
    g.add_edge("تهران", "اصفهان", weight=410, name="بزرگراه")
    
    print(render_graph(g, format="ascii"))
    print()


def example_2_batch_operations():
    """مثال 2: عملیات دسته‌ای"""
    print("=" * 70)
    print("مثال 2: افزودن دسته‌ای گره‌ها و یال‌ها")
    print("=" * 70)
    
    g = Graph(directed=False, name="شبکه‌ی اجتماعی")
    
    # افزودن دسته‌ای گره‌ها
    names = ["علی", "فاطمه", "محمد", "زینب"]
    g.add_nodes([Node(name) for name in names])
    
    # افزودن دسته‌ای یال‌ها
    edges = [
        ("علی", "فاطمه"),
        ("علی", "محمد"),
        ("فاطمه", "زینب"),
        ("محمد", "زینب")
    ]
    g.add_edges(edges)
    
    print(render_graph(g, format="ascii"))
    print(f"\nتعداد گره‌ها و یال‌ها: {len(g)}")
    print()


def example_3_edge_names():
    """مثال 3: نام‌دهی یال‌ها"""
    print("=" * 70)
    print("مثال 3: یال‌های نام‌دار و وزن‌دار")
    print("=" * 70)
    
    g = Graph(directed=True, name="شبکه‌ی کامپیوتری")
    g.add_edge("سرور۱", "سرور۲", weight=10, name="اتصال اصلی")
    g.add_edge("سرور۲", "پایگاه‌داده", weight=5, name="درخواست")
    g.add_edge("پایگاه‌داده", "سرور۲", weight=5, name="جواب")
    
    print(render_graph(g, format="ascii"))
    print("\nیال‌های با نام:")
    for edge in g.edges():
        print(f"  {edge.src.node_id} → {edge.dst.node_id}: {edge.name} (وزن={edge.weight})")
    print()


def example_4_update_operations():
    """مثال 4: اپدیت گره‌ها و یال‌ها"""
    print("=" * 70)
    print("مثال 4: اپدیت ویژگی‌ها")
    print("=" * 70)
    
    g = Graph(directed=True)
    g.add_edge("A", "B", weight=1.0)
    print(f"قبل: {g.get_edges('A', 'B')[0]}")
    
    # اپدیت یال
    g.update_edge("A", "B", weight=5.0, name="مسیر بهبود‌یافته")
    print(f"بعد: {g.get_edges('A', 'B')[0]}")
    print()


def example_5_graph_operations():
    """مثال 5: عملیات گراف (جمع، تفریق)"""
    print("=" * 70)
    print("مثال 5: Merge و تفریق گراف‌ها")
    print("=" * 70)
    
    g1 = Graph(directed=True, name="شبکه۱")
    g1.add_edge("A", "B")
    g1.add_edge("B", "C")
    
    g2 = Graph(directed=True, name="شبکه۲")
    g2.add_edge("C", "D")
    g2.add_edge("D", "E")
    
    # Merge
    g_merged = g1 + g2
    print(f"Merge: {g1.name} + {g2.name} = {g_merged.name}")
    print(f"گره‌ها: {g_merged.order()}, یال‌ها: {g_merged.size()}")
    
    # تفریق
    g_sub = g_merged - g2
    print(f"\nتفریق: {g_merged.name} - {g2.name}")
    print(f"گره‌های باقی‌مانده: {[n.node_id for n in g_sub.nodes()]}")
    print()


def example_6_complement():
    """مثال 6: گراف مکمل"""
    print("=" * 70)
    print("مثال 6: گراف مکمل")
    print("=" * 70)
    
    g = Graph(directed=False, name="شبکه")
    g.add_edges([("A", "B"), ("B", "C")])
    
    comp = g.complement()
    print(f"گراف اصلی:")
    print(render_graph(g, format="ascii"))
    print(f"\nگراف مکمل:")
    print(render_graph(comp, format="ascii"))
    print()


def example_7_subgraph():
    """مثال 7: زیرگراف"""
    print("=" * 70)
    print("مثال 7: استخراج زیرگراف")
    print("=" * 70)
    
    g = Graph(directed=True, name="گراف_کل")
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])
    
    sub = g.subgraph(["A", "B", "C"])
    print(f"گراف اصلی: {g.order()} گره، {g.size()} یال")
    print(f"زیرگراف: {sub.order()} گره، {sub.size()} یال")
    print(f"گره‌های زیرگراف: {[n.node_id for n in sub.nodes()]}")
    print()


def example_8_contains():
    """مثال 8: بررسی عضویت"""
    print("=" * 70)
    print("مثال 8: بررسی وجود گره، یال و زیرگراف")
    print("=" * 70)
    
    g = Graph(directed=True, name="شبکه")
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    
    # بررسی گره
    print(f"'A' در گراف؟ {'A' in g}")
    print(f"'D' در گراف؟ {'D' in g}")
    
    # بررسی یال
    e = Edge(g.get_node("A"), g.get_node("B"))
    print(f"یال A→B در گراف؟ {e in g}")
    
    # بررسی زیرگراف
    sub = g.subgraph(["A", "B"])
    print(f"زیرگراف {{A,B}} یک زیرگراف است؟ {sub in g}")
    print()


def example_9_json_export():
    """مثال 9: صادرات JSON"""
    print("=" * 70)
    print("مثال 9: صادرات گراف به JSON")
    print("=" * 70)
    
    g = Graph(directed=True, name="نمونه")
    g.add_edge("A", "B", weight=5, name="اتصال")
    g.add_edge("B", "C", weight=3, name="رابط")
    
    json_data = render_graph(g, format="json")
    print("JSON (۲۰۰ کاراکتر اول):")
    print(json_data[:200] + "...")
    print()


def example_10_dot_export():
    """مثال 10: صادرات DOT"""
    print("=" * 70)
    print("مثال 10: صادرات گراف به DOT")
    print("=" * 70)
    
    g = Graph(directed=True, name="شبکه")
    g.add_edge("A", "B", weight=5, name="بزرگراه")
    g.add_edge("B", "C", weight=3, name="جاده")
    
    from graph_renderer import GraphRenderer
    renderer = GraphRenderer(g)
    dot = renderer.to_dot(rankdir="LR", show_edge_labels=True)
    print("DOT (۲۰۰ کاراکتر اول):")
    print(dot[:200] + "...")
    print("\nنکته: این DOT را در GraphvizOnline.com بسته‌بندی کنید")
    print()


# فهرست مثال‌ها
EXAMPLES = {
    "1": example_1_basic,
    "2": example_2_batch_operations,
    "3": example_3_edge_names,
    "4": example_4_update_operations,
    "5": example_5_graph_operations,
    "6": example_6_complement,
    "7": example_7_subgraph,
    "8": example_8_contains,
    "9": example_9_json_export,
    "10": example_10_dot_export,
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
        print("اجرای تمام مثال‌ها...\n")
        for i in range(1, 11):
            EXAMPLES[str(i)]()
        print("\n✅ تمام مثال‌ها اجرا شدند!")
        print("\nبرای اجرای مثال خاص:")
        print("  python examples.py 1")
        print("  python examples.py 5")
        print("  و غیره...")
