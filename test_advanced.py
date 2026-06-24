"""
تست‌های GraphAdvanced

Licensed under Apache License 2.0
"""

import sys
import numpy as np
from graph_advanced import GraphAdvanced, print_matrix_info


def test_magic_methods():
    """تست magic methods"""
    print("\n🔵 تست Magic Methods")
    
    g1 = GraphAdvanced(directed=True, name="G1")
    g1.add_edges([("A", "B"), ("B", "C")])
    
    g2 = GraphAdvanced(directed=True, name="G2")
    g2.add_edges([("B", "C"), ("C", "D")])
    
    # اشتراک (B و C مشترک)
    g_and = g1 & g2
    assert g_and.order() == 2, "اشتراک: تعداد گره‌ها (B, C)"
    print("  ✅ اشتراک (&)")
    
    # اجتماع
    g_or = g1 | g2
    assert g_or.order() == 4, "اجتماع: تعداد گره‌ها"
    print("  ✅ اجتماع (|)")
    
    # برابری
    g3 = GraphAdvanced(directed=True, name="G3")
    g3.add_edges([("A", "B"), ("B", "C")])
    assert g1 == g3, "برابری"
    print("  ✅ برابری (==)")
    
    # indexing
    g = GraphAdvanced(directed=True)
    g.add_node("X", data=10)
    assert g["X"].data == 10, "indexing"
    print("  ✅ Indexing ([])")


def test_intersection():
    """تست اشتراک"""
    print("\n🟠 تست Intersection")
    
    g1 = GraphAdvanced(directed=False)
    g1.add_edges([("A", "B"), ("B", "C"), ("A", "C")])
    
    g2 = GraphAdvanced(directed=False)
    g2.add_edges([("B", "C"), ("C", "D")])
    
    result = g1.intersection(g2)
    assert "B" in result and "C" in result, "گره‌های مشترک"
    assert "A" not in result, "گره‌های غیرمشترک"
    print(f"  ✅ اشتراک: {result.order()} گره، {result.size()} یال")


def test_union():
    """تست اجتماع"""
    print("\n🟡 تست Union")
    
    g1 = GraphAdvanced(directed=False)
    g1.add_edges([("A", "B")])
    
    g2 = GraphAdvanced(directed=False)
    g2.add_edges([("C", "D")])
    
    result = g1.union(g2)
    assert result.order() == 4, "اجتماع: تعداد گره‌ها"
    assert result.size() == 2, "اجتماع: تعداد یال‌ها"
    print(f"  ✅ اجتماع: {result.order()} گره، {result.size()} یال")


def test_adjacency_matrix():
    """تست ماتریس مجاورت"""
    print("\n🟢 تست Adjacency Matrix")
    
    g = GraphAdvanced(directed=True)
    g.add_edges([("A", "B", 2), ("B", "C", 3)])
    
    matrix = g.adjacency_matrix(weighted=True)
    assert matrix.shape == (3, 3), "اندازه ماتریس"
    assert matrix[0, 1] == 2, "وزن یال A→B"
    print(f"  ✅ ماتریس مجاورت: {matrix.shape}")
    
    # بدون وزن
    matrix_unweighted = g.adjacency_matrix(weighted=False)
    assert matrix_unweighted[0, 1] == 1, "بدون وزن"
    print("  ✅ ماتریس بدون وزن")


def test_laplacian():
    """تست ماتریس Laplacian"""
    print("\n🔵 تست Laplacian Matrix")
    
    g = GraphAdvanced(directed=False)
    g.add_edges([("A", "B"), ("B", "C"), ("C", "A")])
    
    laplacian = g.laplacian_matrix()
    assert laplacian.shape == (3, 3), "اندازه"
    print(f"  ✅ Laplacian Matrix: {laplacian.shape}")


def test_determinant():
    """تست Determinant"""
    print("\n🟠 تست Determinant")
    
    g = GraphAdvanced(directed=True)
    g.add_edges([("A", "B"), ("B", "A")])
    
    det = g.determinant()
    assert isinstance(det, (int, float, np.number)), "نوع Determinant"
    print(f"  ✅ Determinant: {det:.4f}")


def test_eigenvalues():
    """تست مقادیر ویژه"""
    print("\n🟡 تست Eigenvalues")
    
    g = GraphAdvanced(directed=False)
    g.add_edges([("A", "B"), ("B", "C"), ("C", "A")])
    
    eigenvals = g.eigenvalues()
    assert len(eigenvals) == 3, "تعداد مقادیر ویژه"
    assert np.isreal(eigenvals).all() or np.isreal(eigenvals).any(), "نوع eigenvalues"
    print(f"  ✅ Eigenvalues: {[f'{e:.2f}' for e in eigenvals]}")
    
    # Spectral radius
    spectral = g.spectral_radius()
    assert spectral >= 0, "Spectral radius"
    print(f"  ✅ Spectral Radius: {spectral:.4f}")


def test_eigenvectors():
    """تست بردارهای ویژه"""
    print("\n🟢 تست Eigenvectors")
    
    g = GraphAdvanced(directed=False)
    g.add_edges([("A", "B"), ("B", "C")])
    
    eigenvals, eigenvecs = g.eigenvectors()
    assert len(eigenvals) == 3, "تعداد مقادیر ویژه"
    assert eigenvecs.shape == (3, 3), "اندازه بردارهای ویژه"
    print(f"  ✅ Eigenvectors: {eigenvecs.shape}")


def test_matrix_stats():
    """تست آمارهای ماتریس"""
    print("\n🔵 تست Matrix Statistics")
    
    g = GraphAdvanced(directed=False)
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])
    
    stats = g.matrix_stats()
    assert "determinant" in stats, "determinant در stats"
    assert "trace" in stats, "trace در stats"
    assert "rank" in stats, "rank در stats"
    print(f"  ✅ Stats: {len(stats)} متریک")


def test_rank_and_trace():
    """تست Rank و Trace"""
    print("\n🟠 تست Rank & Trace")
    
    g = GraphAdvanced(directed=True)
    g.add_edges([("A", "B"), ("B", "C")])
    
    rank = g.rank()
    trace = g.trace()
    assert isinstance(rank, int), "نوع rank"
    assert isinstance(trace, (int, float, np.number)), "نوع trace"
    print(f"  ✅ Rank: {rank}, Trace: {trace:.4f}")


def test_degree_matrix():
    """تست ماتریس درجه"""
    print("\n🟡 تست Degree Matrix")
    
    g = GraphAdvanced(directed=False)
    g.add_edges([("A", "B"), ("A", "C"), ("B", "C")])
    
    deg_matrix = g.degree_matrix()
    assert deg_matrix.shape == (3, 3), "اندازه"
    assert np.all(np.diag(np.diag(deg_matrix)) == deg_matrix), "قطری"
    print(f"  ✅ Degree Matrix: {deg_matrix.shape}")


def test_empty_graph():
    """تست گراف خالی"""
    print("\n🟢 تست Empty Graph")
    
    g = GraphAdvanced(directed=True)
    
    assert g.determinant() == 0.0, "determinant گراف خالی"
    assert len(g.eigenvalues()) == 0, "eigenvalues گراف خالی"
    print("  ✅ گراف خالی: معالجه شد")


def main():
    print("\n" + "="*70)
    print("🧪 تست‌های GraphAdvanced")
    print("="*70)
    
    tests = [
        test_magic_methods,
        test_intersection,
        test_union,
        test_adjacency_matrix,
        test_laplacian,
        test_determinant,
        test_eigenvalues,
        test_eigenvectors,
        test_matrix_stats,
        test_rank_and_trace,
        test_degree_matrix,
        test_empty_graph,
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
