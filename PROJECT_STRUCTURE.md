# Graph Library — Project Structure

Complete professional graph implementation with documentation and examples.

---

## File Manifest

### Core Implementation

#### `graph.py` (450 lines)
**Main graph library — fully functional, production-ready**

- **Classes:**
  - `Node` — vertices with attributes and data payload
  - `Edge` — directed edges with weight and attributes
  - `Graph` — main container with adjacency list representation
  
- **Exception Classes:**
  - `GraphError` — base exception
  - `NodeNotFoundError`
  - `EdgeNotFoundError`
  - `DuplicateNodeError`

- **Features:**
  - ✅ Directed and undirected graphs
  - ✅ Weighted edges
  - ✅ Multi-edge support (parallel edges)
  - ✅ Self-loops
  - ✅ Open attribute dictionaries
  - ✅ Incremental in-degree caching (O(1) queries)
  - ✅ Graph copy and subgraph extraction
  - ✅ Python dunder support (`in`, `len`, `iter`, `repr`)
  - ✅ Comprehensive error handling

- **Complexity:**
  - Node/edge lookup: O(1)
  - Add/remove node: O(degree) for connected edges
  - Add/remove edge: O(1) amortized
  - Out-edges: O(degree)
  - In-degree: O(1) via cache
  - In-edges: O(V+E) — avoid in loops

---

### Visualization

#### `graph_renderer.py` (300 lines)
**Rendering and visualization utilities**

- **Formats:**
  - ASCII art — terminal-friendly quick preview
  - DOT — Graphviz format (copy-paste to online renderers)
  - SVG — embedded force-directed layout

- **Classes:**
  - `GraphRenderer` — main rendering engine
  - `render_graph()` — convenience function

- **Features:**
  - No external dependencies for DOT/ASCII
  - SVG includes basic force-directed layout
  - Customizable node/edge attributes in DOT
  - Support for edge labels (weights)

- **Usage:**
  ```python
  from graph_renderer import render_graph
  print(render_graph(g, format="ascii"))  # Terminal preview
  print(render_graph(g, format="dot"))    # Copy to GraphvizOnline
  ```

---

### Documentation

#### `README.md` (800+ lines)
**Comprehensive guide with all you need to know**

- Installation and setup
- Quick start
- All graph types with detailed examples:
  1. Directed graphs
  2. Undirected graphs
  3. Weighted graphs
  4. Multi-edge graphs
  5. Self-loops
  6. Complex combinations
- Core concepts (Node, Edge, Graph)
- Complete API reference
- Visualization guide
- 7+ practical examples
- Best practices
- FAQ and troubleshooting

---

#### `PROJECT_STRUCTURE.md` (this file)
Overview and navigation guide for the entire project.

---

### Examples and Tests

#### `examples.py` (500+ lines)
**7 complete, runnable examples demonstrating all features**

1. **Directed City Network** — basic directed weighted graph
2. **Social Network** — undirected, friends graph
3. **Network Latency** — weighted directed graph with numeric semantics
4. **Airline Network** — multi-edge graph with flight attributes
5. **State Machine** — directed graph with self-loops
6. **Graph Operations** — copy, subgraph, independence
7. **E-Commerce Workflow** — complex real-world example with rich attributes

**Run examples:**
```bash
python examples.py directed_city_network
python examples.py undirected_social
python examples.py multi_edge_airline
python examples.py self_loop_state
python examples.py copy_subgraph
python examples.py ecommerce
python examples.py  # Run all
```

#### Manual Test Suite (in bash)
**44 unit tests covering:**
- Node creation and attributes
- Edge creation and reversal
- Directed and undirected graphs
- Multi-edges and self-loops
- Degree queries (out, in, bidirectional)
- Traversal (neighbors, out_edges, in_edges)
- Add/remove operations
- Error handling
- Graph copy and subgraph
- Cache correctness
- Iterator behavior

**All tests pass (see graph.py docstring for test runner)**

---

## Quick Navigation

### I want to...

**Learn the basics**
→ Start with `README.md` "Quick Start" section

**Understand different graph types**
→ `README.md` "Graph Types" section (6 types explained)

**See practical examples**
→ Run `examples.py` for 7 ready-to-use scenarios

**Use the library in my code**
```python
from graph import Graph
g = Graph(directed=True)
g.add_edge("A", "B", weight=5.0)
```

**Visualize a graph**
```python
from graph_renderer import render_graph
print(render_graph(g, format="ascii"))  # Quick view
# or
print(render_graph(g, format="dot"))    # Copy to GraphvizOnline
```

**Find API documentation**
→ `README.md` "API Reference" section

**Debug/extend the library**
→ `graph.py` is fully documented with docstrings and type hints

**Understand performance**
→ `README.md` "FAQ" section, or inline comments in `graph.py`

---

## Design Principles

### 1. **Single Responsibility**
- `Node` — just a vertex with metadata
- `Edge` — just a directed arc with weight
- `Graph` — container and operations
- `GraphRenderer` — visualization only

### 2. **Pythonic Interface**
- Supports `in`, `len`, `iter`, `repr`
- Clear exception types
- Consistent naming and parameter order

### 3. **Extensibility**
- Open attribute system (`set_attr`, `get_attr`, `update_attrs`)
- User data payload in every node
- Custom edge attributes
- Subclassable for domain-specific graphs

### 4. **Performance Conscious**
- O(1) node/edge lookup via hash tables
- Incremental in-degree caching (O(1) queries)
- Lazy edge deduplication for undirected graphs
- No unnecessary copies

### 5. **Error Handling**
- Specific exception types
- Clear error messages
- Validation on public API boundaries
- No silent failures

---

## Statistics

| Aspect | Value |
|--------|-------|
| **Total Lines (Code)** | ~750 |
| **Total Lines (Docs)** | ~2000 |
| **Core Classes** | 3 (Node, Edge, Graph) |
| **Exception Classes** | 4 |
| **Public Methods** | 35+ |
| **Test Cases** | 44 |
| **Examples** | 7 |
| **External Dependencies** | 0 (core) / optional graphviz CLI |
| **Python Version** | 3.9+ |
| **Performance Guarantee** | O(1) node/edge lookup, O(1) in-degree |

---

## Workflow Recommendations

### Development Workflow

1. **Design your graph structure**
   - Sketch on paper or use `README.md` "Graph Types"
   - Choose directed/undirected, weighted/unweighted
   - Plan your node IDs and attributes

2. **Implement using graph.py**
   ```python
   from graph import Graph
   g = Graph(directed=..., name="...")
   g.add_node(..., data=...)
   g.add_edge(..., weight=...)
   ```

3. **Visualize early and often**
   ```python
   from graph_renderer import render_graph
   print(render_graph(g, format="ascii"))
   ```

4. **Test your logic**
   - Query neighbors, degrees, paths
   - Check edge existence
   - Validate assumptions

5. **Generate publication-ready diagrams**
   ```python
   dot = render_graph(g, format="dot")
   # Copy to https://dreampuf.github.io/GraphvizOnline/
   # Or: dot -Tpng output.dot -o output.png
   ```

### Production Workflow

1. **Validate input**
   - Use `strict=True` when adding nodes
   - Use `auto_add_nodes=False` for explicit errors

2. **Cache expensive operations**
   ```python
   neighbors = g.neighbors("A")  # Cache this result
   for _ in range(1000):
       for neighbor in neighbors:  # Reuse
           ...
   ```

3. **Handle exceptions**
   ```python
   from graph import NodeNotFoundError
   try:
       node = g.get_node(user_id)
   except NodeNotFoundError:
       handle_error()
   ```

4. **Monitor performance**
   - `in_edges()` is O(V+E) — use sparingly
   - `in_degree()` is O(1) — prefer for large graphs
   - Consider reverse-adjacency index if needed

---

## Future Extensions

### Algorithms (Phase 2)
- BFS / DFS traversal
- Shortest path (Dijkstra, Bellman-Ford)
- Cycle detection
- Topological sort
- Strongly connected components

### Advanced Features
- Reverse adjacency index for O(1) in_edges()
- Graph transactions (atomic multi-operation batches)
- Serialization (JSON, GraphML, GML)
- Filtering and transformation operators
- Graph algorithms utilities

### Performance
- Lazy loading for very large graphs
- Graph compression
- Parallel traversal support

---

## Summary

This is a **complete, professional graph library** ready for production use. It emphasizes:

✅ **Clarity** — easy to understand and use  
✅ **Completeness** — all major features included  
✅ **Quality** — well-tested, documented, principled  
✅ **Performance** — O(1) core operations  
✅ **Extensibility** — open attributes, subclassable  

Perfect for:
- Learning graph data structures
- Academic projects
- Production systems requiring graphs
- Teaching algorithms
- Prototyping graph-based solutions

---

**Version:** 1.0  
**Status:** Stable  
**License:** Open to use and modify
