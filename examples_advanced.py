"""
مثال‌های پیشرفته - GraphAdvanced
۱۰ مثال برای تمام ویژگی‌های پیشرفته

Licensed under Apache License 2.0
"""

import numpy as np
from graph_advanced import GraphAdvanced, print_matrix_info


def example_1_magic_methods():
    """مثال ۱: Magic Methods - &, |, ^, [], =="""
    print("\n" + "="*70)
    print("مثال ۱: Magic Methods")
    print("="*70)
    
    g1 = GraphAdvanced(directed=True, name="گراف۱")
    g1.add_edges([("A", "B"), ("B", "C"), ("A", "C")])
    
    g2 = GraphAdvanced(directed=True, name="گراف۲")
    g2.add_edges([("B", "C"), ("C", "D"), ("B", "D")])
    
    print("\nگراف۱:", g1)
    print("گراف۲:", g2)
    
    # اشتراک (intersection) - &
    g_and = g1 & g2
    print(f"\nاشتراک (g1 & g2): {g_and.order()} گره، {g_and.size()} یال")
    
    # اجتماع (union) - |
    g_or = g1 | g2
    print(f"اجتماع (g1 | g2): {g_or.order()} گره، {g_or.size()} یال")
    
    # تفاوت متقارن (symmetric difference) - ^
    g_xor = g1 ^ g2
    print(f"تفاوت متقارن (g1 ^ g2): {g_xor.order()} گره، {g_xor.size()} یال")
    
    # برابری
    g3 = GraphAdvanced(directed=True, name="کپی")
    g3.add_edges([("A", "B"), ("B", "C"), ("A", "C")])
    print(f"\ng1 == g3؟ {g1 == g3}")
    print(f"g1 == g2؟ {g1 == g2}")


def example_2_indexing():
    """مثال ۲: Indexing - g[node_id]"""
    print("\n" + "="*70)
    print("مثال ۲: Indexing و Subscripting")
    print("="*70)
    
    g = GraphAdvanced(directed=True, name="شهرها")
    g.add_node("تهران", data={"population": 8_000_000})
    g.add_node("قم", data={"population": 1_000_000})
    
    # دسترسی
    print("\nدسترسی به داده‌ها:")
    print(f"  g['تهران'].data = {g['تهران'].data}")
    print(f"  g['قم'].data = {g['قم'].data}")
    
    # تعیین
    g['تهران'] = {"population": 9_000_000, "capital": True}
    print(f"\nبعد از تغییر:")
    print(f"  g['تهران'].data = {g['تهران'].data}")
    
    # حذف
    print("\nحذف گره:")
    del g['قم']
    print(f"  تعداد گره‌ها بعد از حذف: {g.order()}")


def example_3_adjacency_matrix():
    """مثال ۳: ماتریس مجاورت"""
    print("\n" + "="*70)
    print("مثال ۳: ماتریس مجاورت")
    print("="*70)
    
    g = GraphAdvanced(directed=True, name="شبکه")
    g.add_edges([
        ("A", "B", 5),
        ("B", "C", 3),
        ("A", "C", 10),
        ("C", "A", 2)
    ])
    
    print(f"\nگراف: {g}")
    print("گره‌ها: A, B, C")
    print("یال‌ها: A→B(5), B→C(3), A→C(10), C→A(2)")
    
    # ماتریس وزن‌دار
    matrix_weighted = g.adjacency_matrix(weighted=True)
    print("\n📊 ماتریس مجاورت (وزن‌دار):")
    print(matrix_weighted)
    
    # ماتریس بدون وزن
    matrix_unweighted = g.adjacency_matrix(weighted=False)
    print("\n📊 ماتریس مجاورت (بدون وزن):")
    print(matrix_unweighted)
    
    # ماتریس Laplacian
    laplacian = g.laplacian_matrix()
    print("\n📊 ماتریس Laplacian:")
    print(laplacian)


def example_4_determinant():
    """مثال ۴: Determinant"""
    print("\n" + "="*70)
    print("مثال ۴: محاسبه Determinant")
    print("="*70)
    
    g = GraphAdvanced(directed=True, name="مثال")
    g.add_edges([
        ("A", "B", 1),
        ("B", "A", 1),
        ("B", "C", 2),
        ("C", "B", 2)
    ])
    
    print(f"\nگراف: {g}")
    det_value = g.determinant()
    print(f"Determinant: {det_value:.4f}")
    
    # مثال دیگر
    g2 = GraphAdvanced(directed=False, name="مثلث")
    g2.add_edges([("A", "B"), ("B", "C"), ("C", "A")])
    print(f"\nگراف دوم (مثلث): {g2}")
    print(f"Determinant: {g2.determinant():.4f}")


def example_5_eigenvalues():
    """مثال ۵: مقادیر ویژه"""
    print("\n" + "="*70)
    print("مثال ۵: مقادیر ویژه و Spectral Radius")
    print("="*70)
    
    g = GraphAdvanced(directed=False, name="شبکه")
    g.add_edges([
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A"),
        ("A", "C")
    ])
    
    print(f"\nگراف: {g}")
    
    eigenvalues = g.eigenvalues()
    print(f"\nمقادیر ویژه:")
    for i, ev in enumerate(eigenvalues):
        print(f"  λ_{i+1} = {ev:.4f}")
    
    spectral = g.spectral_radius()
    print(f"\nSpectral Radius (بزرگ‌ترین |λ|): {spectral:.4f}")


def example_6_eigenvectors():
    """مثال ۶: بردارهای ویژه"""
    print("\n" + "="*70)
    print("مثال ۶: بردارهای ویژه")
    print("="*70)
    
    g = GraphAdvanced(directed=False, name="مربع")
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])
    
    print(f"\nگراف (مربع): {g}")
    
    eigenvalues, eigenvectors = g.eigenvectors()
    print(f"\nمقادیر ویژه: {eigenvalues}")
    print(f"\nبردارهای ویژه (۳ اول):")
    for i in range(min(3, len(eigenvalues))):
        print(f"  v_{i+1} = {eigenvectors[:, i]}")


def example_7_matrix_statistics():
    """مثال ۷: آمارهای ماتریس"""
    print("\n" + "="*70)
    print("مثال ۷: آمارهای ماتریس")
    print("="*70)
    
    g = GraphAdvanced(directed=False, name="شبکه پیچیده")
    g.add_edges([
        ("A", "B"), ("B", "C"), ("C", "D"),
        ("D", "A"), ("A", "C"), ("B", "D"),
        ("B", "E"), ("E", "D")
    ])
    
    print_matrix_info(g)


def example_8_rank_and_trace():
    """مثال ۸: Rank و Trace"""
    print("\n" + "="*70)
    print("مثال ۸: Rank و Trace")
    print("="*70)
    
    g = GraphAdvanced(directed=True, name="شبکه")
    g.add_edges([
        ("A", "B"), ("B", "C"),
        ("A", "C"), ("C", "D"),
        ("D", "B")
    ])
    
    print(f"\nگراف: {g}")
    print(f"Trace (مجموع قطر): {g.trace():.4f}")
    print(f"Rank (رتبه): {g.rank()}")
    
    matrix = g.adjacency_matrix()
    print(f"\nماتریس مجاورت ({matrix.shape[0]}×{matrix.shape[1]}):")
    print(matrix.astype(int))


def example_9_intersection_union():
    """مثال ۹: اشتراک و اجتماع عملی"""
    print("\n" + "="*70)
    print("مثال ۹: اشتراک و اجتماع - کاربرد عملی")
    print("="*70)
    
    # شبکه‌های اجتماعی
    g1 = GraphAdvanced(directed=False, name="دوستان_علی")
    g1.add_edges([
        ("علی", "محمد"),
        ("علی", "فاطمه"),
        ("محمد", "فاطمه")
    ])
    
    g2 = GraphAdvanced(directed=False, name="دوستان_حسن")
    g2.add_edges([
        ("حسن", "فاطمه"),
        ("حسن", "محمد"),
        ("فاطمه", "محمد")
    ])
    
    print("\nشبکه علی:", g1)
    for edge in g1.edges():
        print(f"  {edge.src.node_id} -- {edge.dst.node_id}")
    
    print("\nشبکه حسن:", g2)
    for edge in g2.edges():
        print(f"  {edge.src.node_id} -- {edge.dst.node_id}")
    
    # دوستان مشترک
    common = g1 & g2
    print(f"\nدوستان مشترک ({common.order()} نفر، {common.size()} یال):")
    for node in common.nodes():
        print(f"  {node.node_id}")
    
    # تمام دوستان
    all_friends = g1 | g2
    print(f"\nتمام دوستان ({all_friends.order()} نفر، {all_friends.size()} یال):")
    for node in all_friends.nodes():
        print(f"  {node.node_id}")


def example_10_all_features():
    """مثال ۱۰: تمام ویژگی‌ها در یک مثال"""
    print("\n" + "="*70)
    print("مثال ۱۰: تمام ویژگی‌ها")
    print("="*70)
    
    g = GraphAdvanced(directed=False, name="شبکه_کامل")
    g.add_edges([
        ("A", "B", 1), ("B", "C", 2),
        ("C", "D", 1), ("D", "A", 2),
        ("A", "C", 3)
    ])
    
    print(f"\n📊 گراف: {g}")
    print(f"repr: {repr(g)}")
    
    print(f"\n🔢 ویژگی‌های عددی:")
    print(f"  تعداد گره‌ها: {g.order()}")
    print(f"  تعداد یال‌ها: {g.size()}")
    print(f"  Determinant: {g.determinant():.4f}")
    print(f"  Spectral Radius: {g.spectral_radius():.4f}")
    print(f"  Trace: {g.trace():.4f}")
    print(f"  Rank: {g.rank()}")
    
    print(f"\n📈 مقادیر ویژه:")
    eigenvals = g.eigenvalues()
    for i, ev in enumerate(eigenvals):
        print(f"  λ_{i+1} = {ev:.4f}")
    
    print(f"\n✅ کامل!")


# فهرست مثال‌ها
EXAMPLES = {
    "1": example_1_magic_methods,
    "2": example_2_indexing,
    "3": example_3_adjacency_matrix,
    "4": example_4_determinant,
    "5": example_5_eigenvalues,
    "6": example_6_eigenvectors,
    "7": example_7_matrix_statistics,
    "8": example_8_rank_and_trace,
    "9": example_9_intersection_union,
    "10": example_10_all_features,
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
        print("🎓 مثال‌های GraphAdvanced")
        print("="*70)
        print("\nاستفاده: python examples_advanced.py [شماره]")
        print("مثال: python examples_advanced.py 1")
        print("\nمثال‌های موجود:")
        print("  1. Magic Methods (&, |, ^, ==)")
        print("  2. Indexing (g[node_id])")
        print("  3. Adjacency Matrix")
        print("  4. Determinant")
        print("  5. Eigenvalues")
        print("  6. Eigenvectors")
        print("  7. Matrix Statistics")
        print("  8. Rank & Trace")
        print("  9. Intersection & Union (عملی)")
        print("  10. تمام ویژگی‌ها")
        print("\n یا برای اجرای تمام مثال‌ها:")
        print("  for i in 1 2 3 4 5 6 7 8 9 10; do python examples_advanced.py $i; done")
