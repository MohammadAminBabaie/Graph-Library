# Graph Visualization Guide

Complete guide to all visualization options available in the Graph Library.

---

## 🎨 Visualization Options

### 1. ASCII Art (Terminal)

**Best for:** Quick preview, headless environments, terminal applications

**Advantages:**
- No dependencies
- Works everywhere
- Quick to render
- Self-documenting

**Usage:**
```python
from graph_renderer import render_graph

g = Graph(directed=True)
g.add_edge("A", "B", weight=5)
g.add_edge("B", "C", weight=3)

# Quick preview in terminal
print(render_graph(g, format="ascii"))
```

**Output:**
```
Graph: G (Directed)
Nodes: 3 | Edges: 2

  • A
  • B
  • C

  A -> B (w=5)
  B -> C (w=3)
```

---

### 2. DOT Format (Graphviz)

**Best for:** Professional diagrams, publication, detailed layout control

**Advantages:**
- Industry standard
- Highly customizable
- Multiple output formats (PNG, PDF, SVG)
- Fine-grained control

**Usage:**
```python
from graph_renderer import render_graph

g = Graph(directed=True)
g.add_edge("A", "B", weight=5)
g.add_edge("B", "C", weight=3)

# Generate DOT code
dot_code = render_graph(g, format="dot", rankdir="LR")

# Save to file
with open("graph.dot", "w") as f:
    f.write(dot_code)

# Render with Graphviz CLI (requires graphviz installed)
# dot -Tpng graph.dot -o graph.png
# dot -Tpdf graph.dot -o graph.pdf
# dot -Tsvg graph.dot -o graph.svg
```

**Online Rendering:**
1. Copy the DOT code
2. Paste into [GraphvizOnline](https://dreampuf.github.io/GraphvizOnline/)
3. Adjust layout direction (rankdir)
4. Download as PNG/PDF/SVG

**Layout Directions:**
- `TB` — Top to Bottom (default)
- `LR` — Left to Right
- `RL` — Right to Left
- `BT` — Bottom to Top

**Customization:**
```python
from graph_renderer import GraphRenderer

renderer = GraphRenderer(g)
dot_code = renderer.to_dot(
    rankdir="LR",
    node_attrs={"shape": "ellipse", "color": "lightblue"},
    edge_attrs={"color": "gray"}
)
```

---

### 3. SVG (Static Web)

**Best for:** Web embedding, static diagrams, blog posts

**Advantages:**
- Web-friendly
- Scalable
- Embeddable in HTML
- Self-contained

**Usage:**
```python
from graph_renderer import render_graph

g = Graph(directed=True)
g.add_edge("A", "B", weight=5)
g.add_edge("B", "C", weight=3)

# Generate SVG
svg_code = render_graph(g, format="svg")

# Save to file
with open("graph.svg", "w") as f:
    f.write(svg_code)

# Embed in HTML
html = f"""
<html>
<body>
    {svg_code}
</body>
</html>
"""
```

**Embed in HTML:**
```html
<figure>
    <svg>
        <!-- SVG content here -->
    </svg>
    <figcaption>My Graph</figcaption>
</figure>
```

---

### 4. JSON (Interactive Web Viewer) ⭐ NEW!

**Best for:** Interactive exploration, presentations, dynamic analysis

**Advantages:**
- Beautiful UI
- Drag & drop nodes
- Zoom & pan
- Real-time statistics
- No server needed
- Fully standalone

**Usage:**

#### Step 1: Export to JSON
```python
from graph_renderer import render_graph

g = Graph(directed=True)
g.add_node("A", data={"type": "input"})
g.add_node("B", data={"type": "process"})
g.add_node("C", data={"type": "output"})

g.add_edge("A", "B", weight=5)
g.add_edge("B", "C", weight=3)

# Export graph to JSON
json_data = render_graph(g, format="json")

# Save to file
with open("mygraph.json", "w") as f:
    f.write(json_data)

# Or get JSON as string
print(json_data)
```

#### Step 2: Open Interactive Viewer
1. Open `graph_viewer.html` in a web browser
2. Click the "Load JSON" button
3. Select your JSON file
4. Interact with the graph!

#### JSON Format:
```json
{
  "name": "MyGraph",
  "directed": true,
  "nodes": [
    {
      "id": "A",
      "label": "A",
      "data": {"type": "input"},
      "attrs": {}
    },
    ...
  ],
  "edges": [
    {
      "source": "A",
      "target": "B",
      "weight": 5,
      "label": "5",
      "attrs": {}
    },
    ...
  ]
}
```

**Features:**

| Feature | Description |
|---------|-------------|
| 🎯 Node Dragging | Click and drag any node to reposition |
| 🔍 Zoom | Scroll to zoom in/out (50% - 200%) |
| 📍 Pan | Click-drag background to move view |
| 📊 Statistics | Real-time node & edge count |
| 💾 Export | Download modified graph as JSON |
| 🔄 Reset | Return to original layout |
| 🎨 Beautiful UI | Professional dark-themed interface |

---

## 📊 Comparison Table

| Feature | ASCII | DOT | SVG | JSON/Web |
|---------|-------|-----|-----|----------|
| **Setup** | None | Graphviz CLI | None | Browser |
| **Interactivity** | None | None | None | Full |
| **Drag Nodes** | ❌ | ❌ | ❌ | ✅ |
| **Zoom/Pan** | ❌ | ❌ | ❌ | ✅ |
| **Publication Quality** | ❌ | ✅ | ✅ | ✅ |
| **Customization** | Limited | Extensive | Limited | Good |
| **File Size** | Tiny | Small | Medium | Small |
| **Load Time** | Instant | Fast | Fast | Fast |
| **Dependencies** | None | Graphviz | None | None |

---

## 🚀 Workflow Examples

### Workflow 1: Quick Terminal Preview
```python
from graph_renderer import render_graph

g = Graph()
# ... build your graph ...

# Quick ASCII check
print(render_graph(g, format="ascii"))
```

### Workflow 2: Professional Publication
```python
from graph_renderer import render_graph

g = Graph()
# ... build your graph ...

# Generate publication-ready DOT
dot = render_graph(g, format="dot", rankdir="LR")

# Either:
# a) Use online renderer: paste into GraphvizOnline
# b) Use CLI: dot -Tpdf graph.dot -o graph.pdf
```

### Workflow 3: Interactive Exploration
```python
from graph_renderer import render_graph

g = Graph()
# ... build your graph ...

# Export to JSON
json_data = render_graph(g, format="json")
with open("mygraph.json", "w") as f:
    f.write(json_data)

# Open graph_viewer.html in browser and load mygraph.json
```

### Workflow 4: Web Integration
```python
from graph_renderer import render_graph

g = Graph()
# ... build your graph ...

# Get SVG for embedding
svg = render_graph(g, format="svg", width=1000, height=600)

# Embed in HTML/website
html = f"""
<div class="graph-container">
    {svg}
</div>
"""
```

---

## 💡 Tips & Tricks

### Tip 1: Large Graphs
For very large graphs (1000+ nodes):
- Use JSON/web viewer with pruning
- Export subgraph to JSON
- Use DOT with `rankdir="LR"` for better readability

### Tip 2: Styling Nodes/Edges in DOT
```python
from graph_renderer import GraphRenderer

g = Graph()
# ... build graph ...

# Custom node attributes
node_attrs = {
    "shape": "ellipse",
    "color": "lightblue",
    "style": "filled"
}

# Custom edge attributes
edge_attrs = {
    "color": "gray",
    "penwidth": "2"
}

renderer = GraphRenderer(g)
dot = renderer.to_dot(node_attrs=node_attrs, edge_attrs=edge_attrs)
```

### Tip 3: Different Layouts in DOT
```python
# Different layout directions
dot_tb = render_graph(g, format="dot", rankdir="TB")  # Top to Bottom
dot_lr = render_graph(g, format="dot", rankdir="LR")  # Left to Right
dot_rl = render_graph(g, format="dot", rankdir="RL")  # Right to Left
dot_bt = render_graph(g, format="dot", rankdir="BT")  # Bottom to Top

# Try different ones to find the best for your graph
```

### Tip 4: Export Multiple Formats
```python
from graph_renderer import render_graph

g = Graph()
# ... build graph ...

# Get all formats at once
formats = {
    "ascii": render_graph(g, format="ascii"),
    "dot": render_graph(g, format="dot"),
    "svg": render_graph(g, format="svg"),
    "json": render_graph(g, format="json")
}

# Save each to a file
for fmt, content in formats.items():
    with open(f"graph.{fmt}", "w") as f:
        f.write(content)
```

---

## 🔗 External Tools

### Graphviz Online
- **URL:** https://dreampuf.github.io/GraphvizOnline/
- **Use:** Paste DOT code, get instant visualization
- **Download:** PNG, PDF, SVG, JSON
- **Features:** Adjustable layout, styling

### Gravizo
- **URL:** https://gravizo.com/
- **Use:** Embed Graphviz diagrams directly in Markdown
- **Format:** URL-based DOT embedding
- **Perfect for:** GitHub READMEs

### Graph Online
- **URL:** https://graphonline.ru/
- **Use:** Visual graph editor
- **Format:** Supports multiple formats
- **Features:** Full graph editor

---

## 📚 References

- [Graphviz Documentation](https://graphviz.org/)
- [DOT Language Reference](https://graphviz.org/doc/info/lang.html)
- [SVG Specification](https://www.w3.org/TR/SVG/)
- [D3.js (for advanced web visualization)](https://d3js.org/)

---

## ✅ Choosing the Right Format

```
Need quick preview?
  → ASCII

Need professional diagram?
  → DOT (via Graphviz) + PDF export

Need to embed in website?
  → SVG

Need interactive exploration?
  → JSON + graph_viewer.html ⭐

Need all formats?
  → Generate all (see Tip 4)
```

---

**Version:** 1.0  
**Last Updated:** June 16, 2025  
**Status:** Complete visualization guide
