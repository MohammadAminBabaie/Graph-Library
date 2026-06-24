# 📚 راهنمای GraphAdvanced - عملیات پیشرفته

## فهرست مطالب

1. [نصب و راه‌اندازی](#نصب)
2. [Magic Methods](#magic-methods)
3. [عملیات Set](#set-operations)
4. [ماتریس مجاورت](#adjacency-matrix)
5. [جبر خطی](#linear-algebra)
6. [مثال‌های عملی](#examples)

---

## نصب

```bash
pip install -e ".[advanced]"

# یا دستی
pip install numpy scipy
```

---

## Magic Methods

### اشتراک (Intersection) - `&`

```python
from graph_advanced import GraphAdvanced

g1 = GraphAdvanced(directed=True)
g1.add_edges([("A", "B"), ("B", "C"), ("A", "C")])

g2 = GraphAdvanced(directed=True)
g2.add_edges([("B", "C"), ("C", "D")])

# اشتراک - تنها گره‌ها و یال‌های مشترک
g_common = g1 & g2
# نتیجه: B, C گره‌ها و B→C یال
```

### اجتماع (Union) - `|`

```python
# اجتماع - تمام گره‌ها و یال‌ها
g_all = g1 | g2
# نتیجه: A, B, C, D گره‌ها و تمام یال‌ها
```

### تفاوت متقارن - `^`

```python
# تفاوت متقارن - عناصری که تنها در یکی وجود دارند
g_diff = g1 ^ g2
```

### برابری - `==`

```python
g3 = GraphAdvanced(directed=True)
g3.add_edges([("A", "B"), ("B", "C"), ("A", "C")])

if g1 == g3:
    print("گراف‌ها یکسان هستند")
```

### Indexing - `[]`

```python
g = GraphAdvanced(directed=True)
g.add_node("تهران", data={"population": 8_000_000})

# دسترسی
print(g["تهران"].data)

# تعیین
g["تهران"] = {"population": 9_000_000}

# حذف
del g["تهران"]
```

### Hashing - `hash()`

```python
g1 = GraphAdvanced(directed=True)
g1.add_edges([("A", "B")])

# گراف‌ها را می‌توان در set قرار داد
graph_set = {g1}
```

---

## Set Operations

### Intersection - اشتراک

```python
g1 = GraphAdvanced(directed=False)
g1.add_edges([("A", "B"), ("B", "C"), ("A", "C")])

g2 = GraphAdvanced(directed=False)
g2.add_edges([("B", "C"), ("C", "D")])

# گره‌های مشترک: B, C
# یال‌های مشترک: B-C
common = g1.intersection(g2)

# یا
common = g1 & g2
```

### Union - اجتماع

```python
# تمام گره‌ها: A, B, C, D
# تمام یال‌ها: A-B, B-C, A-C, C-D
union = g1.union(g2)

# یا
union = g1 | g2
```

---

## Adjacency Matrix

### ماتریس مجاورت وزن‌دار

```python
g = GraphAdvanced(directed=True)
g.add_edges([
    ("A", "B", 5),
    ("B", "C", 3),
    ("A", "C", 10)
])

# ماتریس با وزن‌ها
matrix = g.adjacency_matrix(weighted=True)
print(matrix)

# Output:
# [[0  5 10]
#  [0  0  3]
#  [0  0  0]]
```

### ماتریس بدون وزن

```python
# ماتریس بدون وزن (0 یا 1)
matrix = g.adjacency_matrix(weighted=False)

# Output:
# [[0 1 1]
#  [0 0 1]
#  [0 0 0]]
```

### ماتریس Laplacian

```python
# L = D - A
# D: ماتریس درجه
# A: ماتریس مجاورت
laplacian = g.laplacian_matrix()
```

### ماتریس درجه

```python
# ماتریس قطری درجه‌ها
degree_matrix = g.degree_matrix()
```

---

## Linear Algebra

### Determinant

```python
g = GraphAdvanced(directed=True)
g.add_edges([("A", "B"), ("B", "A")])

det = g.determinant()
print(f"Determinant: {det}")
```

### مقادیر ویژه (Eigenvalues)

```python
g = GraphAdvanced(directed=False)
g.add_edges([("A", "B"), ("B", "C"), ("C", "A")])

# مقادیر ویژه
eigenvalues = g.eigenvalues()
print(f"λ: {eigenvalues}")

# Spectral Radius (بزرگ‌ترین |λ|)
spectral = g.spectral_radius()
print(f"Spectral Radius: {spectral}")
```

### بردارهای ویژه (Eigenvectors)

```python
eigenvalues, eigenvectors = g.eigenvectors()

print("مقادیر ویژه:", eigenvalues)
print("بردارهای ویژه:")
print(eigenvectors)
```

### Rank و Trace

```python
# رتبه ماتریس
rank = g.rank()

# مجموع عناصر قطری
trace = g.trace()
```

### آمارهای کامل

```python
stats = g.matrix_stats()

for key, value in stats.items():
    print(f"{key}: {value}")

# خروجی:
# shape: (3, 3)
# determinant: 0.0
# trace: 0.0
# rank: 2
# spectral_radius: 2.0
# min_eigenvalue: -1.0
# max_eigenvalue: 2.0
# frobenius_norm: 2.449...
# condition_number: inf
```

---

## مثال‌های عملی

### مثال ۱: تحلیل شبکه اجتماعی

```python
from graph_advanced import GraphAdvanced

# دوستان علی
g1 = GraphAdvanced(directed=False, name="دوستان_علی")
g1.add_edges([
    ("علی", "محمد"),
    ("علی", "فاطمه"),
    ("محمد", "فاطمه")
])

# دوستان حسن
g2 = GraphAdvanced(directed=False, name="دوستان_حسن")
g2.add_edges([
    ("حسن", "فاطمه"),
    ("حسن", "محمد"),
    ("فاطمه", "محمد")
])

# دوستان مشترک
common = g1 & g2
print(f"دوستان مشترک: {[n.node_id for n in common.nodes()]}")

# تمام دوستان
all_friends = g1 | g2
print(f"تمام دوستان: {all_friends.order()} نفر")
```

### مثال ۲: تحلیل شبکه

```python
g = GraphAdvanced(directed=False, name="شبکه")
g.add_edges([
    ("A", "B"), ("B", "C"), ("C", "D"),
    ("D", "A"), ("A", "C"), ("B", "D")
])

# ویژگی‌های شبکه
stats = g.matrix_stats()

spectral = stats["spectral_radius"]
print(f"Spectral Radius (تراکم شبکه): {spectral}")

cond_num = stats["condition_number"]
print(f"Condition Number: {cond_num}")

eigenvals = g.eigenvalues()
print(f"مقادیر ویژه: {eigenvals}")
```

### مثال ۳: مقایسه گراف‌ها

```python
# دو شبکه مختلف
g1 = GraphAdvanced(directed=False, name="شبکه_ستاره")
g1.add_edges([("A", "B"), ("A", "C"), ("A", "D")])

g2 = GraphAdvanced(directed=False, name="شبکه_حلقه")
g2.add_edges([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])

# مقایسه spectral radius
spec1 = g1.spectral_radius()
spec2 = g2.spectral_radius()

print(f"Spectral Radius شبکه ستاره: {spec1}")
print(f"Spectral Radius شبکه حلقه: {spec2}")

if spec1 > spec2:
    print("شبکه ستاره متراکم‌تر است")
else:
    print("شبکه حلقه متراکم‌تر است")
```

---

## خصوصیات پیشرفته

### ماتریس مجاورت بدون حلقه خودی

```python
matrix = g.adjacency_matrix(include_self_loops=False)
```

### نمایش ماتریس

```python
import numpy as np

g = GraphAdvanced(directed=True)
g.add_edges([("A", "B", 2), ("B", "C", 3)])

matrix = g.adjacency_matrix()
print("ماتریس مجاورت:")
print(matrix)

print(f"\nاندازه: {matrix.shape}")
print(f"نوع: {matrix.dtype}")
```

---

## استفاده در کاربردهای واقعی

### تحلیل شبکه انتقال

```python
# شبکه توزیع برق
power_grid = GraphAdvanced(directed=False, name="شبکه_برق")
power_grid.add_edges([
    ("نیروگاه", "سالن_۱"),
    ("سالن_۱", "بخش_۱"),
    ("سالن_۱", "بخش_۲"),
    ("بخش_۱", "مصرف_کننده_۱"),
])

# تحلیل
spectral = power_grid.spectral_radius()
print(f"کارایی شبکه (Spectral Radius): {spectral}")
```

### رتبه‌بندی صفحات‌وب

```python
# شبکه لینک‌های وب
web = GraphAdvanced(directed=True, name="وب_گراف")
web.add_edges([
    ("صفحه_A", "صفحه_B"),
    ("صفحه_B", "صفحه_C"),
    ("صفحه_C", "صفحه_A"),
])

# مقادیر ویژه برای PageRank
eigenvals, eigenvecs = web.eigenvectors()
```

---

## نکات مهم

### ⚠️ نکات

1. **ماتریس بزرگ:** برای گراف‌های بزرگ، محاسبه eigenvalues می‌تواند کند باشد
2. **گراف‌های پیچیده:** برای جزئیات بیشتر، scipy مستندات را بخوانید
3. **دقت عددی:** مقادیر eigenvalues ممکن است کوچک خطاهای عددی داشته باشند

---

## مثال کامل

```python
from graph_advanced import GraphAdvanced, print_matrix_info

# گراف ایجاد کنید
g = GraphAdvanced(directed=False, name="مثال_کامل")
g.add_edges([
    ("A", "B", 1),
    ("B", "C", 2),
    ("C", "D", 1),
    ("D", "A", 2),
    ("A", "C", 3)
])

# نمایش اطلاعات
print(f"گراف: {g}")
print_matrix_info(g)

# عملیات
print(f"\nDeterminant: {g.determinant():.4f}")
print(f"Spectral Radius: {g.spectral_radius():.4f}")
print(f"Rank: {g.rank()}")
print(f"Trace: {g.trace():.4f}")

# مقادیر ویژه
eigenvals = g.eigenvalues()
print(f"\nمقادیر ویژه:")
for i, ev in enumerate(eigenvals):
    print(f"  λ_{i+1} = {ev:.4f}")
```

---

## تابع‌های مفید

```python
# Intersection
g_common = g1 & g2

# Union
g_all = g1 | g2

# Symmetric Difference
g_diff = g1 ^ g2

# Indexing
node = g["node_id"]
g["node_id"] = new_data
del g["node_id"]

# Matrices
matrix = g.adjacency_matrix()
laplacian = g.laplacian_matrix()
degree = g.degree_matrix()

# Linear Algebra
det = g.determinant()
eigenvalues = g.eigenvalues()
eigenvalues, eigenvectors = g.eigenvectors()
spectral = g.spectral_radius()
rank = g.rank()
trace = g.trace()

# Statistics
stats = g.matrix_stats()
```

---

## منابع

- NumPy: https://numpy.org/
- SciPy: https://scipy.org/
- Graph Theory: https://en.wikipedia.org/wiki/Graph_theory
- Spectral Graph Theory: https://en.wikipedia.org/wiki/Spectral_graph_theory

---

**نسخه:** 1.1.0  
**آخرین به‌روزرسانی:** 2025  
**لایسنس:** Apache 2.0
