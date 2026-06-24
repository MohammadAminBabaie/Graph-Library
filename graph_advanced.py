"""
graph_advanced.py - Advanced Graph Operations

Features:
- Intersection & Union operations
- Adjacency Matrix
- Eigenvalues & Determinant
- Advanced Magic Methods

Licensed under Apache License 2.0
"""

from __future__ import annotations
from typing import Optional, Any
import numpy as np
from scipy.linalg import det, eig

from graph import Graph, Node, Edge


class GraphAdvanced(Graph):
    """
    Graph با عملیات پیشرفته و matrix operations
    
    ویژگی‌های اضافی:
    - اشتراک و اجتماع گراف‌ها
    - ماتریس مجاورت
    - مقادیر ویژه و determinant
    - Magic methods پیشرفته
    """

    # ══════════════════════════════════════════════════════════════════════════
    #  SET OPERATIONS: INTERSECTION & UNION
    # ══════════════════════════════════════════════════════════════════════════

    def intersection(self, other: Graph) -> GraphAdvanced:
        """
        اشتراک دو گراف
        
        شامل:
        - تنها گره‌هایی که در هر دو وجود دارند
        - تنها یال‌هایی که در هر دو وجود دارند
        
        Parameters
        ----------
        other : Graph
            گراف دوم
            
        Returns
        -------
        GraphAdvanced
            گراف حاصل اشتراک
            
        Example
        -------
        >>> g1.intersection(g2)  # تنها مشترک‌ها
        """
        result = GraphAdvanced(directed=self.directed, name=f"{self.name}∩{other.name}")
        
        # گره‌های مشترک
        common_nodes = set(self._nodes.keys()) & set(other._nodes.keys())
        for node_id in common_nodes:
            node = self._nodes[node_id]
            result.add_node(node_id, node.data, **node.attrs())
        
        # یال‌های مشترک
        for edge in self.edges():
            if other.has_edge(edge.src.node_id, edge.dst.node_id):
                result.add_edge(
                    edge.src.node_id,
                    edge.dst.node_id,
                    edge.weight,
                    edge.name,
                    auto_add_nodes=False,
                    **edge.attrs()
                )
        
        return result

    def union(self, other: Graph) -> GraphAdvanced:
        """
        اجتماع دو گراف
        
        شامل:
        - تمام گره‌ها از هر دو
        - تمام یال‌ها از هر دو
        
        Parameters
        ----------
        other : Graph
            گراف دوم
            
        Returns
        -------
        GraphAdvanced
            گراف حاصل اجتماع
            
        Example
        -------
        >>> g1.union(g2)  # اجتماع کامل
        """
        result = GraphAdvanced(directed=self.directed, name=f"{self.name}∪{other.name}")
        
        # تمام گره‌ها
        all_node_ids = set(self._nodes.keys()) | set(other._nodes.keys())
        for node_id in all_node_ids:
            if node_id in self._nodes:
                node = self._nodes[node_id]
                result.add_node(node_id, node.data, **node.attrs())
            else:
                node = other._nodes[node_id]
                result.add_node(node_id, node.data, **node.attrs())
        
        # تمام یال‌ها
        added_edges = set()
        for edge in self.edges():
            key = (edge.src.node_id, edge.dst.node_id, edge.edge_id)
            if key not in added_edges:
                result.add_edge(
                    edge.src.node_id,
                    edge.dst.node_id,
                    edge.weight,
                    edge.name,
                    auto_add_nodes=False,
                    **edge.attrs()
                )
                added_edges.add(key)
        
        for edge in other.edges():
            key = (edge.src.node_id, edge.dst.node_id, edge.edge_id)
            if key not in added_edges:
                result.add_edge(
                    edge.src.node_id,
                    edge.dst.node_id,
                    edge.weight,
                    edge.name,
                    auto_add_nodes=False,
                    **edge.attrs()
                )
                added_edges.add(key)
        
        return result

    # ══════════════════════════════════════════════════════════════════════════
    #  MAGIC METHODS: OPERATORS
    # ══════════════════════════════════════════════════════════════════════════

    def __and__(self, other: Graph) -> GraphAdvanced:
        """تقاطع (اشتراک) - g1 & g2"""
        return self.intersection(other)

    def __or__(self, other: Graph) -> GraphAdvanced:
        """اتحاد (اجتماع) - g1 | g2"""
        return self.union(other)

    def __xor__(self, other: Graph) -> GraphAdvanced:
        """تفاوت متقارن - g1 ^ g2"""
        union = self.union(other)
        intersection = self.intersection(other)
        return union - intersection

    def __eq__(self, other: Any) -> bool:
        """برابری دو گراف"""
        if not isinstance(other, Graph):
            return False
        
        if self.order() != other.order() or self.size() != other.size():
            return False
        
        for node in self.nodes():
            if not other.has_node(node.node_id):
                return False
        
        for edge in self.edges():
            if not other.has_edge(edge.src.node_id, edge.dst.node_id):
                return False
        
        return True

    def __ne__(self, other: Any) -> bool:
        """عدم برابری"""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Hash گراف (بر اساس nodes و edges)"""
        node_tuple = tuple(sorted([n.node_id for n in self.nodes()]))
        edge_tuple = tuple(sorted([(e.src.node_id, e.dst.node_id) for e in self.edges()]))
        return hash((node_tuple, edge_tuple))

    def __getitem__(self, node_id: Any) -> Node:
        """دسترسی به گره با indexing - g[node_id]"""
        return self.get_node(node_id)

    def __setitem__(self, node_id: Any, data: Any) -> None:
        """تنظیم data گره - g[node_id] = data"""
        if self.has_node(node_id):
            self.get_node(node_id).data = data
        else:
            self.add_node(node_id, data)

    def __delitem__(self, node_id: Any) -> None:
        """حذف گره - del g[node_id]"""
        self.remove_node(node_id)

    # ══════════════════════════════════════════════════════════════════════════
    #  MATRIX OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def adjacency_matrix(self, weighted: bool = True, include_self_loops: bool = True) -> np.ndarray:
        """
        ماتریس مجاورت گراف
        
        Parameters
        ----------
        weighted : bool
            اگر True، وزن یال استفاده می‌شود
        include_self_loops : bool
            اگر True، حلقه‌های خودی شامل می‌شود
            
        Returns
        -------
        np.ndarray
            ماتریس مجاورت (n × n)
            
        Example
        -------
        >>> g = GraphAdvanced(directed=True)
        >>> g.add_edges([("A", "B", 5), ("B", "C", 3)])
        >>> matrix = g.adjacency_matrix()
        >>> print(matrix)
        """
        nodes = sorted([n.node_id for n in self.nodes()])
        n = len(nodes)
        node_to_idx = {node_id: i for i, node_id in enumerate(nodes)}
        
        # ماتریس صفر
        matrix = np.zeros((n, n), dtype=float)
        
        # پر کردن ماتریس
        for edge in self.edges():
            i = node_to_idx[edge.src.node_id]
            j = node_to_idx[edge.dst.node_id]
            
            # Skip خود یال اگر نخواستید
            if i == j and not include_self_loops and edge.src.node_id == edge.dst.node_id:
                continue
            
            value = edge.weight if weighted else 1.0
            matrix[i, j] = value
            
            # اگر غیر جهت‌دار، symmetric
            if not self.directed:
                matrix[j, i] = value
        
        return matrix

    def laplacian_matrix(self) -> np.ndarray:
        """
        ماتریس Laplacian (L = D - A)
        
        D: ماتریس درجه
        A: ماتریس مجاورت
        
        Returns
        -------
        np.ndarray
            ماتریس Laplacian
        """
        adj = self.adjacency_matrix(weighted=False)
        n = len(adj)
        
        # ماتریس درجه
        degree = np.diag(np.sum(adj, axis=1))
        
        # Laplacian
        return degree - adj

    def degree_matrix(self) -> np.ndarray:
        """
        ماتریس درجه (قطری)
        
        Returns
        -------
        np.ndarray
            ماتریس درجه (n × n)
        """
        nodes = sorted([n.node_id for n in self.nodes()])
        degrees = [self.degree(n) for n in nodes]
        return np.diag(degrees)

    # ══════════════════════════════════════════════════════════════════════════
    #  LINEAR ALGEBRA OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def determinant(self) -> float:
        """
        محاسبه determinant ماتریس مجاورت
        
        Returns
        -------
        float
            Determinant
            
        Example
        -------
        >>> det = g.determinant()
        >>> print(f"Determinant: {det}")
        """
        if self.order() == 0:
            return 0.0
        
        matrix = self.adjacency_matrix()
        return float(det(matrix))

    def eigenvalues(self) -> np.ndarray:
        """
        مقادیر ویژه ماتریس مجاورت
        
        Returns
        -------
        np.ndarray
            آرایه مقادیر ویژه
            
        Example
        -------
        >>> eigenvals = g.eigenvalues()
        >>> print(eigenvals)
        """
        if self.order() == 0:
            return np.array([])
        
        matrix = self.adjacency_matrix()
        eigenvalues, _ = eig(matrix)
        return np.sort(eigenvalues.real)[::-1]  # نزولی ترتیب

    def eigenvectors(self) -> tuple[np.ndarray, np.ndarray]:
        """
        مقادیر و بردارهای ویژه
        
        Returns
        -------
        tuple
            (eigenvalues, eigenvectors)
            
        Example
        -------
        >>> vals, vecs = g.eigenvectors()
        >>> print(vals, vecs)
        """
        if self.order() == 0:
            return np.array([]), np.array([])
        
        matrix = self.adjacency_matrix()
        eigenvalues, eigenvectors = eig(matrix)
        
        # ترتیب نزولی
        idx = np.argsort(eigenvalues.real)[::-1]
        
        return eigenvalues[idx].real, eigenvectors[:, idx].real

    def spectral_radius(self) -> float:
        """
        بزرگ‌ترین مقدار ویژه (spectral radius)
        
        Returns
        -------
        float
            Spectral radius
        """
        if self.order() == 0:
            return 0.0
        
        eigenvalues = self.eigenvalues()
        return float(np.max(np.abs(eigenvalues)))

    def trace(self) -> float:
        """
        Trace ماتریس مجاورت (مجموع عناصر قطری)
        
        Returns
        -------
        float
            Trace
        """
        matrix = self.adjacency_matrix()
        return float(np.trace(matrix))

    def rank(self) -> int:
        """
        رتبه ماتریس مجاورت
        
        Returns
        -------
        int
            رتبه
        """
        if self.order() == 0:
            return 0
        
        matrix = self.adjacency_matrix()
        return int(np.linalg.matrix_rank(matrix))

    # ══════════════════════════════════════════════════════════════════════════
    #  MATRIX STATISTICS
    # ══════════════════════════════════════════════════════════════════════════

    def matrix_stats(self) -> dict[str, Any]:
        """
        آمارهای ماتریس
        
        Returns
        -------
        dict
            آمارهای مختلف
        """
        if self.order() == 0:
            return {}
        
        matrix = self.adjacency_matrix()
        eigenvalues = self.eigenvalues()
        
        return {
            "shape": matrix.shape,
            "determinant": float(det(matrix)),
            "trace": float(np.trace(matrix)),
            "rank": int(np.linalg.matrix_rank(matrix)),
            "spectral_radius": float(np.max(np.abs(eigenvalues))),
            "min_eigenvalue": float(np.min(eigenvalues)),
            "max_eigenvalue": float(np.max(eigenvalues)),
            "frobenius_norm": float(np.linalg.norm(matrix, 'fro')),
            "condition_number": float(np.linalg.cond(matrix)) if np.linalg.matrix_rank(matrix) == len(matrix) else float('inf'),
        }

    # ══════════════════════════════════════════════════════════════════════════
    #  STRING REPRESENTATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def __repr__(self) -> str:
        """نمایش کامل گراف"""
        kind = "جهت‌دار" if self.directed else "بدون‌جهت"
        return (
            f"GraphAdvanced(name={self.name!r}, type={kind}, "
            f"nodes={self.order()}, edges={self.size()}, "
            f"λ_max={self.spectral_radius():.2f})"
        )

    def __str__(self) -> str:
        """نمایش ساده"""
        return f"{self.name} ({self.order()} nodes, {self.size()} edges)"


# ══════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def adjacency_matrix_from_graph(g: Graph, weighted: bool = True) -> np.ndarray:
    """Helper function برای دریافت ماتریس مجاورت"""
    if isinstance(g, GraphAdvanced):
        return g.adjacency_matrix(weighted=weighted)
    
    # برای Graph عادی
    nodes = sorted([n.node_id for n in g.nodes()])
    n = len(nodes)
    node_to_idx = {node_id: i for i, node_id in enumerate(nodes)}
    
    matrix = np.zeros((n, n), dtype=float)
    for edge in g.edges():
        i = node_to_idx[edge.src.node_id]
        j = node_to_idx[edge.dst.node_id]
        value = edge.weight if weighted else 1.0
        matrix[i, j] = value
        if not g.directed:
            matrix[j, i] = value
    
    return matrix


def print_matrix_info(g: GraphAdvanced) -> None:
    """چاپ اطلاعات ماتریس"""
    print("\n" + "="*70)
    print(f"📊 اطلاعات ماتریس: {g.name}")
    print("="*70)
    
    stats = g.matrix_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key:20s}: {value:12.4f}")
        elif isinstance(value, tuple):
            print(f"  {key:20s}: {value}")
        else:
            print(f"  {key:20s}: {value}")
    
    print("="*70 + "\n")

