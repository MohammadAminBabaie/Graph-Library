# Graph Library — Complete Guide

Professional Python graph data structure library with support for directed/undirected, weighted, multi-edge, and self-loop graphs.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Graph Types](#graph-types)
4. [Core Concepts](#core-concepts)
5. [API Reference](#api-reference)
6. [Visualization](#visualization)
7. [Examples](#examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Installation

### Requirements
- Python 3.9+
- No external dependencies (graph.py is standalone)
- Optional: `graphviz` CLI tool for rendering (not Python module)

### Setup
```bash
# Copy the graph module to your project
cp graph.py /path/to/your/project/

# Import in your code
from graph import Graph, Node, Edge
```

---

## Quick Start

### Minimal Example
```python
from graph import Graph

# Create a directed graph
g = Graph(directed=True)

# Add nodes
g.add_node("A")
g.add_node("B")
g.add_node("C")

# Add edges
g.add_edge("A", "B", weight=10.0)
g.add_edge("B", "C", weight=20.0)
g.add_edge("A", "C", weight=25.0)

# Query the graph
print(g)  # Graph(name='G', type=Directed, nodes=3, edges=3)
print(g.neighbors("A"))  # [Node('B'), Node('C')]
```

### Visualization
```python
from graph_renderer import render_graph

# Quick ASCII preview
print(render_graph(g, format="ascii"))

# DOT format (copy to online renderer)
dot_code = render_graph(g, format="dot")
```

---

## Graph Types

### 1. Directed Graph

A directed graph where edges have a direction (A → B is different from B → A).

**Use cases:** Page rankings, traffic networks, dependencies, state machines.

```python
from graph import Graph

g = Graph(directed=True, name="WebLinks")

# Add web pages and links
g.add_node("wikipedia.org")
g.add_node("github.com")
g.add_node("google.com")

g.add_edge("wikipedia.org", "github.com")     # wiki → github
g.add_edge("github.com", "google.com")        # github → google
g.add_edge("google.com", "wikipedia.org")     # google → wiki (loop)

# Query
print(f"From Wikipedia, you can reach: {[n.node_id for n in g.neighbors('wikipedia.org')]}")
# Output: ['github.com']

print(f"In-degree of google.com: {g.in_degree('google.com')}")
# Output: 1 (only github links to it)
```

### 2. Undirected Graph

Edges are bidirectional; A -- B means you can go both directions.

**Use cases:** Social networks, road networks, molecular structures, communication networks.

```python
g = Graph(directed=False, name="SocialNetwork")

g.add_edge("Alice", "Bob")
g.add_edge("Bob", "Charlie")
g.add_edge("Alice", "Charlie")

# Both directions work automatically
print(g.has_edge("Alice", "Bob"))   # True
print(g.has_edge("Bob", "Alice"))   # True (automatic!)

# All neighbors are symmetric
print(g.neighbors("Bob"))  # [Node('Alice'), Node('Charlie')]
```

### 3. Weighted Graph

Edges carry numeric weights (costs, distances, probabilities, capacities).

**Use cases:** Shortest paths, network flows, distance matrices.

```python
g = Graph(directed=True, name="CityNetwork")

# Cities with distances
g.add_node("Berlin")
g.add_node("Munich")
g.add_node("Hamburg")

g.add_edge("Berlin", "Munich", weight=585.0)   # km
g.add_edge("Berlin", "Hamburg", weight=289.0)
g.add_edge("Munich", "Hamburg", weight=779.0)

for edge in g.edges():
    print(f"{edge.src.node_id} -> {edge.dst.node_id}: {edge.weight} km")

# Output:
# Berlin -> Munich: 585.0 km
# Berlin -> Hamburg: 289.0 km
# Munich -> Hamburg: 779.0 km
```

### 4. Multi-Edge Graph

Multiple independent edges between the same pair of nodes.

**Use cases:** Transportation networks (multiple routes), parallel communications, redundancy.

```python
g = Graph(directed=True, name="Roads")

g.add_node("CityA")
g.add_node("CityB")

# Three different routes between the cities
route1 = g.add_edge("CityA", "CityB", weight=100.0, type="highway")
route2 = g.add_edge("CityA", "CityB", weight=150.0, type="local_road")
route3 = g.add_edge("CityA", "CityB", weight=120.0, type="scenic_route")

# Retrieve all edges
edges = g.get_edges("CityA", "CityB")
print(f"Routes available: {len(edges)}")  # 3

# Remove a specific edge
g.remove_edge("CityA", "CityB", edge_id=route1.edge_id)

edges = g.get_edges("CityA", "CityB")
print(f"Routes remaining: {len(edges)}")  # 2
```

### 5. Self-Loop

An edge from a node to itself.

**Use cases:** State transitions, reflexive relations, self-references.

```python
g = Graph(directed=True, name="StateMachine")

g.add_node("Waiting")
g.add_node("Running")
g.add_node("Error")

# State transitions
g.add_edge("Waiting", "Running")
g.add_edge("Running", "Waiting")
g.add_edge("Running", "Error")
g.add_edge("Error", "Waiting")

# Self-loop: Error state can recover to itself (retries)
g.add_edge("Error", "Error", weight=0.5)

print(f"Self-loops from Error: {g.get_edges('Error', 'Error')}")
```

### 6. Weighted + Multi-Edge (Combination)

Combine features for complex real-world scenarios.

```python
g = Graph(directed=True, name="AirlineNetwork")

# Airports
airports = ["JFK", "LAX", "ORD", "DFW"]
for airport in airports:
    g.add_node(airport, data={"type": "airport"})

# Multiple flights (different times, airlines, aircraft)
g.add_edge("JFK", "LAX", weight=5.5, airline="United", aircraft="Boeing777")
g.add_edge("JFK", "LAX", weight=5.5, airline="American", aircraft="Airbus350")
g.add_edge("JFK", "ORD", weight=2.5, airline="Delta", aircraft="Boeing737")

# Check all JFK → LAX flights
flights = g.get_edges("JFK", "LAX")
print(f"JFK → LAX: {len(flights)} flights")
for f in flights:
    print(f"  - {f.get_attr('airline')} ({f.get_attr('aircraft')})")
```

---

## Core Concepts

### Node

A vertex in the graph with:
- **node_id**: Unique identifier (any hashable type: str, int, tuple, ...)
- **data**: Optional user payload (object, dict, list, ...)
- **attributes**: Arbitrary metadata (color, label, weight, custom fields, ...)

```python
from graph import Node

# Simple node
n1 = Node("A")

# Node with data
n2 = Node("UserID_42", data={"name": "Alice", "age": 30})

# Node with attributes
n3 = Node("City", data="Berlin", color="blue", population=3_700_000)

# Access/modify attributes
n3.set_attr("visited", True)
print(n3.get_attr("visited"))  # True
print(n3.get_attr("missing", default="N/A"))  # N/A
```

### Edge

A directed arc from source to destination with:
- **src / dst**: Source and destination nodes
- **weight**: Numeric weight (default 1.0)
- **edge_id**: Unique ID (auto-generated or provided; required for multi-edges)
- **attributes**: Metadata (capacity, label, color, ...)

```python
from graph import Edge, Node

a, b = Node("A"), Node("B")

# Simple edge
e1 = Edge(a, b)

# Weighted edge
e2 = Edge(a, b, weight=10.5)

# Edge with attributes
e3 = Edge(a, b, weight=10.5, capacity=100, color="red")

# Access
print(e3.endpoints())  # ('A', 'B')
print(e3.get_attr("capacity"))  # 100

# Reverse (for undirected graphs)
e_rev = e3.reversed()
print(e_rev.src.node_id, "->", e_rev.dst.node_id)  # B -> A
```

### Graph

The container holding all nodes and edges. Supports:
- Directed or undirected
- Weighted or unweighted
- Single or multi-edge
- Self-loops

```python
from graph import Graph

# Directed
dg = Graph(directed=True, name="MyDiGraph")

# Undirected
ug = Graph(directed=False, name="MyUndirected")

# Query
print(dg.order())  # number of nodes
print(dg.size())   # number of edges
print(dg.directed)  # True
```

---

## API Reference

### Node

```python
# Creation
n = Node(node_id, data=None, **attrs)

# Attribute access
n.set_attr(key, value)
n.get_attr(key, default=None)
n.del_attr(key)
n.attrs()  # dict copy of all attributes
n.update_attrs(**kwargs)

# Equality / hashing
n == other_node
hash(n)

# String representation
repr(n)
```

### Edge

```python
# Creation
e = Edge(src, dst, weight=1.0, edge_id=None, **attrs)

# Utilities
e.reversed()  # new Edge with swapped endpoints
e.endpoints()  # (src.node_id, dst.node_id)

# Attribute access (same as Node)
e.set_attr, e.get_attr, e.del_attr, e.attrs(), e.update_attrs()
```

### Graph

#### Node Operations

```python
# Add
node = g.add_node(node_id, data=None, strict=False, **attrs)
# strict=True raises DuplicateNodeError if node exists; False is idempotent

# Remove
removed_node = g.remove_node(node_id)  # raises NodeNotFoundError if missing

# Query
g.has_node(node_id)
g.get_node(node_id)
g.update_node(node_id, data=None, **attrs)

# Iteration
for node in g.nodes():
    ...
```

#### Edge Operations

```python
# Add
edge = g.add_edge(src_id, dst_id, weight=1.0, auto_add_nodes=True, **attrs)
# auto_add_nodes=True creates missing nodes; False raises NodeNotFoundError

# Remove
removed_edge = g.remove_edge(src_id, dst_id, edge_id=None)
# edge_id selects a specific edge (for multi-edges)

# Query
g.has_edge(src_id, dst_id)
g.get_edges(src_id, dst_id)  # list, possibly multiple

# Iteration
for edge in g.edges():
    ...
```

#### Traversal

```python
# Adjacent nodes
g.neighbors(node_id)  # deduped, preserves order

# Edges
g.out_edges(node_id)  # all outgoing
g.in_edges(node_id)   # all incoming (O(V+E) — avoid in loops)
```

#### Degree

```python
g.out_degree(node_id)  # number of outgoing edges
g.in_degree(node_id)   # number of incoming edges (O(1) via cache)
g.degree(node_id)      # in + out for directed; incident edges for undirected
```

#### Graph-Level

```python
g.order()          # number of nodes
g.size()           # number of edges (undirected edges counted once)

g.clear()          # remove all nodes and edges

g.copy()           # shallow copy (independent structure)
g.subgraph(node_ids)  # induced subgraph
```

#### Python Dunder Support

```python
len(g)             # same as g.order()
node_id in g       # same as g.has_node()
for node in g:     # iterate nodes
    ...
repr(g)            # human-readable summary
```

#### Metadata

```python
g.directed         # bool
g.name             # str
g._nodes           # dict[node_id -> Node] (internal; read-only for production)
g._adj             # dict[node_id -> list[Edge]] (internal)
```

---

## Visualization

### ASCII Art (Quick Preview)

No dependencies. Print in terminal for fast inspection.

```python
from graph_renderer import render_graph

g = Graph()
g.add_edge("A", "B", weight=5)
g.add_edge("B", "C", weight=3)

print(render_graph(g, format="ascii"))
```

Output:
```
Graph: G (Directed)
Nodes: 3 | Edges: 2

  • A
  • B
  • C

  A -> B (w=5)
  B -> C (w=3)
```

### DOT Format (Graphviz)

Generate source code for professional rendering.

```python
from graph_renderer import GraphRenderer

g = Graph(directed=True, name="WebGraph")
g.add_edge("A", "B", weight=2.5)
g.add_edge("B", "C", weight=3.0)

dot = GraphRenderer(g).to_dot(rankdir="LR")
print(dot)
```

Copy the output to:
- https://dreampuf.github.io/GraphvizOnline/
- https://gravizo.com/
- Local: `dot -Tpng output.dot -o output.png`

### SVG (Embedded)

Simple force-directed layout for embedding in HTML.

```python
svg = GraphRenderer(g).to_svg(width=800, height=600, node_size=40)
# Save to file or embed in HTML
with open("graph.svg", "w") as f:
    f.write(svg)
```

---

## Examples

### Example 1: Social Network

Friends graph (undirected, unweighted).

```python
from graph import Graph
from graph_renderer import render_graph

g = Graph(directed=False, name="Friends")

friends = [
    ("Alice", "Bob"),
    ("Bob", "Charlie"),
    ("Alice", "Charlie"),
    ("Charlie", "David"),
    ("David", "Eve"),
    ("Eve", "Alice"),
]

for a, b in friends:
    g.add_edge(a, b)

print(render_graph(g, format="ascii"))

# Compute some stats
for person in ["Alice", "Bob", "Charlie"]:
    print(f"{person} has {g.degree(person)} friends")
```

### Example 2: City Distances (Weighted Directed)

Find shortest path candidates.

```python
g = Graph(directed=True, name="CityDistances")

cities = ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"]
for city in cities:
    g.add_node(city, data={"country": "Germany"})

routes = [
    ("Berlin", "Munich", 585),
    ("Berlin", "Hamburg", 289),
    ("Hamburg", "Cologne", 390),
    ("Cologne", "Frankfurt", 180),
    ("Frankfurt", "Munich", 365),
]

for src, dst, distance in routes:
    g.add_edge(src, dst, weight=distance)

print(render_graph(g, format="ascii"))
```

### Example 3: State Machine

Directed graph with self-loops.

```python
g = Graph(directed=True, name="ProcessStateMachine")

states = ["Idle", "Running", "Paused", "Error", "Shutdown"]
for state in states:
    g.add_node(state)

transitions = [
    ("Idle", "Running"),
    ("Running", "Paused"),
    ("Paused", "Running"),
    ("Running", "Error"),
    ("Error", "Idle"),
    ("Error", "Error", 0.5),  # self-loop for retries
    ("Running", "Shutdown"),
]

for t in transitions:
    if len(t) == 3:
        g.add_edge(t[0], t[1], weight=t[2])
    else:
        g.add_edge(t[0], t[1])

print(render_graph(g, format="ascii"))

# Find all possible exit states from Running
running_neighbors = g.neighbors("Running")
print(f"Running can transition to: {[n.node_id for n in running_neighbors]}")
```

### Example 4: Multi-Edge Airline Network

Real-world complexity.

```python
g = Graph(directed=True, name="Airlines")

airports = ["JFK", "LAX", "ORD", "ATL"]
for airport in airports:
    g.add_node(airport)

flights = [
    ("JFK", "LAX", 5.5, "UA", "B777"),
    ("JFK", "LAX", 5.5, "AA", "A350"),
    ("JFK", "ORD", 2.5, "UA", "B737"),
    ("LAX", "ORD", 4.0, "DL", "B767"),
    ("ORD", "ATL", 2.0, "DL", "B737"),
]

for src, dst, hours, airline, aircraft in flights:
    g.add_edge(
        src, dst,
        weight=hours,
        airline=airline,
        aircraft=aircraft,
    )

# Find all options for JFK → LAX
jfk_lax = g.get_edges("JFK", "LAX")
print(f"JFK → LAX: {len(jfk_lax)} flights")
for flight in jfk_lax:
    airline = flight.get_attr("airline")
    aircraft = flight.get_attr("aircraft")
    print(f"  {airline} {aircraft} ({flight.weight}h)")
```

### Example 5: Copy & Subgraph

Graph slicing and comparison.

```python
g = Graph(directed=True, name="Original")

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "D")
g.add_edge("A", "D")

# Full copy (independent)
g2 = g.copy()
g2.add_node("E")
print(f"Original has {g.order()} nodes; Copy has {g2.order()} nodes")

# Subgraph induced by certain nodes
sub = g.subgraph(["A", "B", "C"])
print(f"Subgraph order: {sub.order()}, size: {sub.size()}")

# Check which edges remain
print(f"A → B in subgraph? {sub.has_edge('A', 'B')}")
print(f"A → D in subgraph? {sub.has_edge('A', 'D')}")  # False (D not in subgraph)
```

---

## Best Practices

### 1. **Use Meaningful Node Identifiers**

```python
# Good
g.add_node("user_123")
g.add_node("order_456")

# Also good: tuples
g.add_node(("user", 123))

# Avoid generic IDs unless necessary
g.add_node(0)  # What does "0" represent?
```

### 2. **Leverage `data` for Payloads**

```python
# Store complex objects in data, attributes for metadata
user_node = g.add_node(
    "user_1",
    data={"name": "Alice", "email": "alice@example.com"},
    verified=True,
    signup_date="2024-01-01"
)
```

### 3. **Use `weight` for Numeric Semantics**

```python
# weight = semantically meaningful numeric value
g.add_edge("A", "B", weight=2.5)  # distance, cost, probability, time, etc.

# For non-numeric properties, use attributes
g.add_edge("A", "B", weight=1.0, relationship_type="colleague", since="2020")
```

### 4. **Cache Results for Large Graphs**

```python
# ✓ Good: compute once, reuse
neighbors_of_a = g.neighbors("A")
for neighbor in neighbors_of_a:
    # Use pre-computed list multiple times
    ...

# ✗ Avoid: recompute every loop
for _ in range(1000):
    neighbors = g.neighbors("A")  # O(degree) each time
```

### 5. **Use `auto_add_nodes=False` for Type Safety**

```python
# ✓ Explicit error if nodes don't exist
g.add_edge("A", "B", auto_add_nodes=False)

# ✗ Silent creation (prone to typos)
g.add_edge("A", "Bb")  # Oops, created a typo node
```

### 6. **Handle Exceptions Gracefully**

```python
from graph import NodeNotFoundError, EdgeNotFoundError, DuplicateNodeError

try:
    g.get_node("missing")
except NodeNotFoundError:
    print("Node not found")

try:
    g.add_node("existing", strict=True)
except DuplicateNodeError:
    print("Node already exists")
```

### 7. **Visualize During Development**

```python
# Quick ASCII check before long computations
print(render_graph(g, format="ascii"))

# Generate DOT for formal documentation
dot_code = GraphRenderer(g).to_dot(rankdir="LR")
# Save or share with team
```

### 8. **Use Subgraph for Analysis**

```python
# Analyze a subset without modifying the original
important_nodes = [n for n in g.nodes() if n.get_attr("priority") == "high"]
important_graph = g.subgraph([n.node_id for n in important_nodes])
```

---

## Troubleshooting

### "NodeNotFoundError" when adding edge

**Cause:** `auto_add_nodes=False` and nodes don't exist.

**Solution:**
```python
# Option 1: Allow auto-creation
g.add_edge("A", "B")  # auto_add_nodes=True (default)

# Option 2: Create nodes first
g.add_node("A")
g.add_node("B")
g.add_edge("A", "B", auto_add_nodes=False)
```

### Multi-edge edges seem to disappear

**Cause:** Using `remove_edge()` without `edge_id` removes only the first matching edge.

**Solution:**
```python
# To remove a specific edge, save its edge_id
e1 = g.add_edge("A", "B", weight=10)
e2 = g.add_edge("A", "B", weight=20)

g.remove_edge("A", "B", edge_id=e1.edge_id)  # Remove only e1
```

### "in_degree cache corruption"

**Cause:** Direct manipulation of `_adj` (internal data structure).

**Solution:** Always use public API:
```python
# ✓ Correct
g.remove_edge("A", "B")

# ✗ Never do this
g._adj["A"].clear()
```

### Performance issues on large graphs

**Cause:** Calling `in_edges()` repeatedly (O(V+E) scan).

**Solution:**
```python
# Cache the result
in_edges_of_b = g.in_edges("B")

# Avoid
for i in range(1000):
    in_edges = g.in_edges("B")  # Recomputes every time
```

### Subgraph raises "NodeNotFoundError"

**Cause:** Requesting a node ID that doesn't exist in the original graph.

**Solution:**
```python
# Verify nodes exist first
node_ids = ["A", "B", "C"]
for nid in node_ids:
    if not g.has_node(nid):
        print(f"Node {nid} not found!")
    
sub = g.subgraph(node_ids)
```

---

## Advanced: Extending the Library

### Custom Node Subclass

```python
class PersonNode(Node):
    def __init__(self, node_id, name, age):
        super().__init__(node_id, data={"name": name, "age": age})
    
    @property
    def name(self):
        return self.data["name"]

# Use it
person = PersonNode("user_1", "Alice", 30)
```

### Custom Graph Subclass

```python
class WeightedDAG(Graph):
    """Directed Acyclic Graph (no cycle checking here, but architectural intent)."""
    
    def __init__(self, name="DAG"):
        super().__init__(directed=True, name=name)
```

---

## FAQ

**Q: Can I use non-string node IDs?**
A: Yes! Any hashable type works: integers, tuples, even custom objects (if they define `__hash__`).

**Q: Is this thread-safe?**
A: No. For multi-threaded use, add external locking or use immutable snapshots.

**Q: How do I export to other formats?**
A: Use `GraphRenderer.to_dot()` and convert with graphviz CLI, or extend the renderer.

**Q: What's the performance complexity?**
A: Node/edge lookup: O(1). Out-edges: O(degree). In-degree: O(1) cached. In-edges: O(V+E).

---

## License

Free to use and modify. Attribution appreciated.

---

**Version:** 1.0  
**Last Updated:** 2025-01-XX  
**Maintainer:** Graph Library Community
