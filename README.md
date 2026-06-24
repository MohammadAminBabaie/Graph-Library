# 📊 Graph Library v1.1.0

Professional Python graph data structure library with advanced features.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green)
![Tests Passing](https://img.shields.io/badge/Tests-62%2F62%20passing-brightgreen)

---

## ✨ ویژگی‌ها

### 📌 ویژگی‌های اصلی
- ✅ **Directed & Undirected graphs**
- ✅ **Weighted edges** with custom names
- ✅ **Multi-edges** (parallel edges supported)
- ✅ **Self-loops** support
- ✅ **Rich attributes** for nodes and edges
- ✅ **Batch operations** (add_nodes, add_edges)
- ✅ **Graph operations** (+, -, &, |, ^)
- ✅ **Zero external dependencies** for core

### 🔬 ویژگی‌های پیشرفته (با numpy/scipy)
- ✅ **Magic methods** (&, |, ^, [], ==, hash())
- ✅ **Set operations** (intersection, union, symmetric difference)
- ✅ **Adjacency matrices** (weighted/unweighted)
- ✅ **Laplacian matrices**
- ✅ **Eigenvalues & eigenvectors**
- ✅ **Determinant calculation**
- ✅ **Spectral radius**
- ✅ **Matrix statistics** (rank, trace, condition number)

### 📈 رندرینگ
- ✅ **ASCII** preview
- ✅ **DOT** (Graphviz)
- ✅ **SVG** (force-directed layout)
- ✅ **JSON** (for web viewer)

### 🎨 Web Viewer
- ✅ **Interactive HTML5 canvas**
- ✅ **Node dragging**
- ✅ **Zoom & pan**
- ✅ **DOT import/export**
- ✅ **JSON import/export**

---

## 🚀 نصب سریع

```bash
# Core (بدون dependencies بیرونی)
pip install -e .

# Advanced (با numpy و scipy)
pip install -e ".[dev]"
```

---

## 💡 استفاده سریع

### Basic Graph

```python
from graph import Graph

g = Graph(directed=True)
g.add_edges([("A", "B", 5), ("B", "C", 3)])

print(g.order(), g.size())  # 3, 2
print(g["A"])               # Node('A')
```

### Advanced Operations

```python
from graph_advanced import GraphAdvanced

g = GraphAdvanced(directed=False)
g.add_edges([("A", "B"), ("B", "C"), ("C", "A")])

# Magic methods
g1 & g2  # intersection
g1 | g2  # union

# Matrix operations
matrix = g.adjacency_matrix()
eigenvalues = g.eigenvalues()
spectral = g.spectral_radius()
```

### Visualization

```python
from graph_renderer import render_graph

# ASCII
print(render_graph(g, format="ascii"))

# DOT
dot_code = render_graph(g, format="dot", rankdir="LR")
g.save_to_dot("graph.dot")

# JSON
json_data = render_graph(g, format="json")
```

---

## 📊 API مرجع

### Graph Class

```python
g = Graph(directed=True)

# Node operations
g.add_node("A")
g.add_nodes([Node("B"), Node("C")])
g.remove_node("A")
g.has_node("B")
g.get_node("C")
g.update_node("A", data=10)

# Edge operations
g.add_edge("A", "B", weight=5, name="route")
g.add_edges([("B", "C"), ("C", "A")])
g.remove_edge("A", "B")
g.update_edge("A", "B", weight=10)
g.has_edge("B", "C")
g.get_edges("A", "B")

# Queries
g.order()           # تعداد گره‌ها
g.size()            # تعداد یال‌ها
g.num_edges("A", "B")
g.neighbors("A")
g.out_degree("A")
g.in_degree("B")
g.degree("C")

# Operations
g.copy()
g.subgraph(["A", "B"])
g.complement()

# Advanced
g1 + g2    # merge
g1 - g2    # remove
g + Node("X")
"A" in g   # membership
```

### GraphAdvanced Class

```python
g = GraphAdvanced(directed=False)

# Magic methods
g1 & g2         # intersection
g1 | g2         # union
g1 ^ g2         # symmetric difference
g1 == g2        # equality
hash(g)         # hashable
g["A"]          # indexing
del g["A"]      # deletion

# Set operations
g.intersection(other)
g.union(other)

# Matrices
g.adjacency_matrix(weighted=True)
g.laplacian_matrix()
g.degree_matrix()

# Linear algebra
g.determinant()
g.eigenvalues()
g.eigenvectors()
g.spectral_radius()
g.rank()
g.trace()
g.matrix_stats()
```

---

## 📚 مثال‌ها

### 10 مثال پایه‌ای

```bash
python examples.py           # تمام مثال‌ها
python examples.py 1         # مثال اول
python examples.py 5         # مثال پنجم
```

### 10 مثال پیشرفته

```bash
python examples_advanced.py           # تمام مثال‌ها
python examples_advanced.py 1         # مثال اول
python examples_advanced.py 7         # آمارهای ماتریس
```

---

## 🧪 تست‌ها

```bash
# تست‌های اصلی
python test_graph.py
# نتیجه: ✅ 50/50 passing

# تست‌های پیشرفته
python test_advanced.py
# نتیجه: ✅ 12/12 passing
```

---

## 📖 مستندات

- `INSTALLATION.md` — نصب و راه‌اندازی
- `ADVANCED_GUIDE.md` — راهنمای ویژگی‌های پیشرفته
- `DOT_FORMAT_GUIDE.md` — فرمت DOT کامل
- `VISUALIZATION.md` — راهنمای رندرینگ
- `PROJECT_RULES.md` — قوانین توسعه
- `CONTRIBUTING.md` — نحوه‌ی مشارکت

---

## 📦 نیازمندی‌ها

### Core
- Python 3.9+
- ✅ No external dependencies

### Advanced (Optional)
- numpy >= 1.21.0
- scipy >= 1.7.0

### Development (Optional)
- mypy, black, flake8, pylint
- pytest, pytest-cov
- sphinx, sphinx-rtd-theme

---

## 🎯 مثال کامل

```python
from graph_advanced import GraphAdvanced, print_matrix_info
from graph_renderer import render_graph

# گراف ایجاد کنید
g = GraphAdvanced(directed=False, name="شبکه")
g.add_edges([
    ("A", "B", 1), ("B", "C", 2),
    ("C", "D", 1), ("D", "A", 2),
    ("A", "C", 3)
])

# نمایش
print(render_graph(g, format="ascii"))

# تحلیل
print_matrix_info(g)

# عملیات
print(f"Spectral Radius: {g.spectral_radius():.4f}")
print(f"Eigenvalues: {g.eigenvalues()}")

# اشتراک و اجتماع
g2 = GraphAdvanced(directed=False)
g2.add_edges([("C", "D"), ("D", "E")])

common = g & g2
all_nodes = g | g2
print(f"مشترک: {common.order()} گره")
print(f"اجتماع: {all_nodes.order()} گره")
```

---

## 🔄 Magic Methods

```python
# Intersection
result = g1 & g2

# Union
result = g1 | g2

# Symmetric difference
result = g1 ^ g2

# Equality
if g1 == g2:
    print("Same graphs")

# Indexing
node = g["node_id"]
g["node_id"] = data
del g["node_id"]

# Iteration
for node in g:
    print(node)

# Length
print(len(g))  # تعداد گره‌ها
print(g.counts())  # (nodes, edges)

# Hash
graph_set = {g1, g2}

# Membership
if "A" in g:
    print("Node exists")
```

---

## 🏗️ معماری

```
graph/
├── graph.py                 # کلاس‌های اصلی
├── graph_renderer.py        # رندرینگ
├── graph_advanced.py        # ویژگی‌های پیشرفته
├── graph_viewer.html        # web viewer
├── examples.py              # 10 مثال
├── examples_advanced.py     # 10 مثال پیشرفته
├── test_graph.py            # 50 تست
└── test_advanced.py         # 12 تست
```

---

## 📊 اعدادوشمار

| Metric | Value |
|--------|-------|
| **Total lines of code** | 3,500+ |
| **Total documentation** | 10,000+ |
| **Test cases** | 62 |
| **Features** | 50+ |
| **External dependencies** | 0 (core) |
| **Python version** | 3.9+ |

---

## 🎓 اصول پروژه

1. ✅ **Dynamic Design** — انعطاف‌پذیری
2. ✅ **Continuous Improvement** — بهتری دائمی
3. ✅ **Clean Code** — PEP 8 + SOLID
4. ✅ **Type Hints** — نوع‌شناسی کامل
5. ✅ **Perfect Tests** — 62/62 passing
6. ✅ **Documentation** — جامع و واضح
7. ✅ **Zero deps** — مستقل (core)
8. ✅ **Apache 2.0** — لایسنس آزاد

---

## 🚀 آماده برای

✅ **Production** — درخت راه‌حل صنعتی  
✅ **GitHub** — منتشر کردن  
✅ **PyPI** — توزیع  
✅ **Research** — تحقیقات  

---

## 📞 پشتیبانی

- 📖 مستندات: `README.md`
- 🎓 مثال‌ها: `examples.py`, `examples_advanced.py`
- 🧪 تست‌ها: `test_graph.py`, `test_advanced.py`
- 🔧 نصب: `INSTALLATION.md`

---

## 📜 لایسنس

Apache License 2.0 — آزادانه استفاده کنید

---

**Version:** 1.1.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2025  
**Maintainer:** Graph Library Contributors

