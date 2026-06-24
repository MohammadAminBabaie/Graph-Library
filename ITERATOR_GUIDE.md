# 🔄 Iterator Patterns Guide

راهنمای کامل iteration روی Graph elements

---

## فهرست

1. [Node Iteration](#node-iteration)
2. [Edge Iteration](#edge-iteration)
3. [Neighbor Iteration](#neighbor-iteration)
4. [Traversal Iterators](#traversal-iterators)
5. [عملی Examples](#عملی-examples)

---

## Node Iteration

### روش ۱: `iter_nodes()`

```python
from graph import Graph
from graph_iterators import add_iterators_to_graph

add_iterators_to_graph()

g = Graph(directed=True)
g.add_edges([("A", "B"), ("B", "C")])

# تکرار روی nodes
for node in g.iter_nodes():
    print(node.node_id)
    print(node.data)
```

### روش ۲: Default Iteration

```python
# Default behavior: nodes
for node in g:
    print(node.node_id)
```

### روش ۳: List Comprehension

```python
# تمام node IDs
node_ids = [n.node_id for n in g.iter_nodes()]
print(node_ids)  # ['A', 'B', 'C']

# تمام nodes با filter
large_nodes = [n for n in g.iter_nodes() if n.data > 100]
```

---

## Edge Iteration

### روش ۱: `iter_edges()`

```python
# تکرار روی تمام edges
for edge in g.iter_edges():
    print(f"{edge.src.node_id} → {edge.dst.node_id}")
    print(f"  Weight: {edge.weight}")
    print(f"  Name: {edge.name}")
```

### روش ۲: بر اساس Node

```python
# یال‌های خروجی
for edge in g.iter_out_edges("A"):
    print(f"A → {edge.dst.node_id}")

# یال‌های ورودی
for edge in g.iter_in_edges("C"):
    print(f"{edge.src.node_id} → C")
```

### روش ۳: Filtering

```python
# فقط heavy edges
heavy_edges = [e for e in g.iter_edges() if e.weight > 5]

# فقط named edges
named_edges = [e for e in g.iter_edges() if e.name != ""]
```

---

## Neighbor Iteration

### روش ۱: `iter_neighbors()`

```python
# همسایه‌های یک node
for neighbor in g.iter_neighbors("A"):
    print(f"  {neighbor.node_id}")
```

### روش ۲: مع درجات

```python
for node in g.iter_nodes():
    neighbors = list(g.iter_neighbors(node.node_id))
    print(f"{node.node_id}: درجه {len(neighbors)}")
    for neighbor in neighbors:
        print(f"  - {neighbor.node_id}")
```

### روش ۳: Degree Queries

```python
# تمام nodes با حداقل 3 neighbors
popular = [n.node_id for n in g.iter_nodes() 
           if len(g.neighbors(n.node_id)) >= 3]
```

---

## Traversal Iterators

### DFS (Depth First Search)

```python
# DFS از node شروع می‌کند
for node in g.iter_dfs("A"):
    print(node.node_id, end=" → ")
print("END")

# Output: A → B → D → E → C → F → END
```

**خصوصیات DFS:**
- عمق‌اول جستجو
- Stack-based
- استفاده برای: cycles, topological sort

### BFS (Breadth First Search)

```python
# BFS از node شروع می‌کند
for node in g.iter_bfs("A"):
    print(node.node_id, end=" → ")
print("END")

# Output: A → B → C → D → E → F → END
```

**خصوصیات BFS:**
- عرض‌اول جستجو
- Queue-based
- استفاده برای: shortest path, level-by-level

---

## عملی Examples

### Example ۱: شمارش Elements

```python
from graph_iterators import count_iterations

# تعداد nodes
node_count = len(g.iter_nodes())

# تعداد edges
edge_count = len(g.iter_edges())

print(f"Nodes: {node_count}, Edges: {edge_count}")
```

### Example ۲: شبکه اجتماعی

```python
g = Graph(directed=False, name="Social Network")
g.add_edges([
    ("علی", "محمد"),
    ("علی", "فاطمه"),
    ("محمد", "حسن"),
    ("فاطمه", "زینب")
])

# دوستان هر نفر
for person in g.iter_nodes():
    friends = [f.node_id for f in g.iter_neighbors(person.node_id)]
    print(f"{person.node_id}: {friends}")

# مسیر از علی تا زینب
path = list(g.iter_bfs("علی"))
print(f"مسیر: {[n.node_id for n in path]}")
```

### Example ۳: Weighted Graph

```python
g = Graph(directed=True)
g.add_edges([
    ("A", "B", 5),
    ("B", "C", 3),
    ("A", "C", 10)
])

# تمام edges مرتب‌شده بر اساس وزن
sorted_edges = sorted(g.iter_edges(), key=lambda e: e.weight)
for edge in sorted_edges:
    print(f"{edge.src.node_id} → {edge.dst.node_id}: {edge.weight}")

# میانگین وزن
weights = [e.weight for e in g.iter_edges()]
avg_weight = sum(weights) / len(weights)
print(f"Average weight: {avg_weight}")
```

### Example ۴: Tree Traversal

```python
# درخت
g = Graph(directed=True)
g.add_edges([
    ("root", "left"),
    ("root", "right"),
    ("left", "ll"),
    ("left", "lr"),
    ("right", "rl")
])

# DFS - pre-order
print("Pre-order (DFS):")
for node in g.iter_dfs("root"):
    print(f"  {node.node_id}")

# BFS - level-order
print("\nLevel-order (BFS):")
for node in g.iter_bfs("root"):
    print(f"  {node.node_id}")
```

### Example ۵: Cycle Detection

```python
def has_cycle_dfs(g, start):
    """DFS برای detection cycle"""
    visited = set()
    path = set()
    
    def dfs(node_id):
        visited.add(node_id)
        path.add(node_id)
        
        for neighbor in g.iter_neighbors(node_id):
            if neighbor.node_id not in visited:
                if dfs(neighbor.node_id):
                    return True
            elif neighbor.node_id in path:
                return True
        
        path.remove(node_id)
        return False
    
    return dfs(start)

# استفاده
g = Graph(directed=True)
g.add_edges([("A", "B"), ("B", "C"), ("C", "A")])  # Cycle!
print(f"Cycle exists: {has_cycle_dfs(g, 'A')}")  # True
```

---

## Patterns & Tips

### ✅ بهترین روش‌ها

1. **استفاده از نام‌های واضح:**
   ```python
   for node in g.iter_nodes():  # ✓ واضح
       pass
   
   for n in g:  # ✗ مبهم
       pass
   ```

2. **Filtering سریع:**
   ```python
   # بهتر
   heavy = [e for e in g.iter_edges() if e.weight > 5]
   
   # نه
   heavy = []
   for e in g.iter_edges():
       if e.weight > 5:
           heavy.append(e)
   ```

3. **Reuse Iterators:**
   ```python
   iterator = g.iter_nodes()
   for node in iterator:
       process(node)
   # دوبار iterate کنید
   for node in iterator:
       process_again(node)
   ```

### ⚠️ نکات مهم

- **DFS vs BFS:**
  - DFS برای cycles و topological sort
  - BFS برای shortest path

- **Performance:**
  - Iterators lazy evaluation ندارند
  - کل graph بلافاصله loaded می‌شود

- **Modification:**
  - درحین iteration، graph تغییر ندهید

---

## API Reference

| Method | بازگشت | مثال |
|--------|--------|------|
| `iter_nodes()` | NodesIterator | `for n in g.iter_nodes()` |
| `iter_edges()` | EdgesIterator | `for e in g.iter_edges()` |
| `iter_neighbors(id)` | NeighborsIterator | `for n in g.iter_neighbors("A")` |
| `iter_out_edges(id)` | OutEdgesIterator | `for e in g.iter_out_edges("A")` |
| `iter_in_edges(id)` | InEdgesIterator | `for e in g.iter_in_edges("A")` |
| `iter_dfs(start)` | DFSIterator | `for n in g.iter_dfs("A")` |
| `iter_bfs(start)` | BFSIterator | `for n in g.iter_bfs("A")` |

---

## مثال کامل

```python
from graph import Graph
from graph_iterators import add_iterators_to_graph, print_traversal

# فعال کردن iterators
add_iterators_to_graph()

# ایجاد گراف
g = Graph(directed=True, name="شبکه")
g.add_edges([
    ("A", "B", 5),
    ("A", "C", 3),
    ("B", "D", 2),
    ("C", "D", 4),
    ("D", "E", 1)
])

print("=== Nodes ===")
for node in g.iter_nodes():
    print(f"  {node.node_id}")

print("\n=== Edges ===")
for edge in g.iter_edges():
    print(f"  {edge.src.node_id} → {edge.dst.node_id} ({edge.weight})")

print("\n=== Neighbors of A ===")
for neighbor in g.iter_neighbors("A"):
    print(f"  {neighbor.node_id}")

print("\n=== Traversals ===")
print_traversal(g, "A", "dfs")
print_traversal(g, "A", "bfs")
```

---

**Version:** 1.1.0  
**Status:** ✅ Complete  
**Tests:** 10/10 passing

