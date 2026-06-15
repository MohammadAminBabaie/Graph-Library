"""
graph_renderer.py
=================
Graph visualization and rendering utilities.

Generates DOT (Graphviz) format and can export to SVG/PNG.
Also provides ASCII art representation for terminal display.
"""

from __future__ import annotations
from typing import Optional, Callable
from graph import Graph, Node, Edge


class GraphRenderer:
    """
    Renders a Graph in various formats: DOT, SVG, ASCII art.

    This class does NOT require graphviz to be installed for DOT generation.
    It only needs graphviz CLI tools for PNG/SVG rendering (optional).
    """

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    # ══════════════════════════════════════════════════════════════════════════
    #  DOT Format (Graphviz source code)
    # ══════════════════════════════════════════════════════════════════════════

    def to_dot(
        self,
        rankdir: str = "TB",
        node_attrs: Optional[dict[str, str]] = None,
        edge_attrs: Optional[dict[str, str]] = None,
        node_labeler: Optional[Callable[[Node], str]] = None,
    ) -> str:
        """
        Generate a DOT (Graphviz) representation of the graph.

        Parameters
        ----------
        rankdir : str
            Graph direction: "TB" (top→bottom), "LR" (left→right), "RL", "BT"
        node_attrs : dict, optional
            Default attributes for all nodes (e.g. {"style": "filled", "color": "lightblue"})
        edge_attrs : dict, optional
            Default attributes for all edges (e.g. {"color": "gray"})
        node_labeler : callable, optional
            Function(node) -> str to customize node labels.
            Default is node.node_id.

        Returns
        -------
        str
            DOT source code ready for graphviz or online renderers.

        Examples
        --------
        >>> g = Graph()
        >>> g.add_edge("A", "B", weight=5)
        >>> dot = GraphRenderer(g).to_dot(rankdir="LR")
        >>> print(dot)  # Copy-paste into https://dreampuf.github.io/GraphvizOnline/
        """
        if node_attrs is None:
            node_attrs = {}
        if edge_attrs is None:
            edge_attrs = {}
        if node_labeler is None:
            node_labeler = lambda n: str(n.node_id)

        graph_type = "digraph" if self.graph.directed else "graph"
        edge_op = "->" if self.graph.directed else "--"

        lines = [f"{graph_type} {self.graph.name} {{"]
        lines.append(f'  rankdir="{rankdir}";')
        lines.append(f'  node [shape=box, {self._attrs_to_dot(node_attrs)}];')
        lines.append(f'  edge [{self._attrs_to_dot(edge_attrs)}];')
        lines.append("")

        # Render nodes
        for node in self.graph.nodes():
            label = node_labeler(node)
            attrs = {
                "label": label,
                **(node.get_attr("_dot_attrs") or {}),
            }
            attrs_str = self._attrs_to_dot(attrs)
            lines.append(f'  "{node.node_id}" [{attrs_str}];')

        lines.append("")

        # Render edges
        seen_edges = set()
        for edge in self.graph.edges():
            src_id = edge.src.node_id
            dst_id = edge.dst.node_id

            # Avoid duplicate edges in undirected graphs
            edge_key = tuple(sorted([src_id, dst_id])) if not self.graph.directed else (src_id, dst_id)
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)

            label = f"{edge.weight}" if edge.weight != 1.0 else ""
            attrs = {"label": label, **(edge.get_attr("_dot_attrs") or {})}
            attrs_str = self._attrs_to_dot(attrs)
            lines.append(f'  "{src_id}" {edge_op} "{dst_id}" [{attrs_str}];')

        lines.append("}")
        return "\n".join(lines)

    # ══════════════════════════════════════════════════════════════════════════
    #  ASCII Art Representation
    # ══════════════════════════════════════════════════════════════════════════

    def to_ascii(self, max_width: int = 100) -> str:
        """
        Generate a simple ASCII art representation of the graph.

        Useful for quick inspection in the terminal without graphviz.

        Parameters
        ----------
        max_width : int
            Maximum line width (wraps long node lists).

        Returns
        -------
        str
        """
        lines = [
            f"Graph: {self.graph.name} ({['Directed', 'Undirected'][not self.graph.directed]})",
            f"Nodes: {self.graph.order()} | Edges: {self.graph.size()}",
            "",
        ]

        for node in self.graph.nodes():
            data_str = f" [data={node.data}]" if node.data is not None else ""
            attrs_str = f" {node.attrs()}" if node.attrs() else ""
            lines.append(f"  • {node.node_id}{data_str}{attrs_str}")

        lines.append("")
        for edge in self.graph.edges():
            op = "->" if self.graph.directed else "--"
            weight_str = f" (w={edge.weight})" if edge.weight != 1.0 else ""
            lines.append(f"  {edge.src.node_id} {op} {edge.dst.node_id}{weight_str}")

        return "\n".join(lines)

    # ══════════════════════════════════════════════════════════════════════════
    #  SVG (simple embedded version)
    # ══════════════════════════════════════════════════════════════════════════

    def to_svg(
        self,
        width: int = 800,
        height: int = 600,
        node_size: int = 40,
    ) -> str:
        """
        Generate a simple SVG visualization.

        Uses a basic force-directed layout approximation.
        For production-grade layouts, use to_dot() + graphviz CLI.

        Parameters
        ----------
        width, height : int
            Canvas dimensions.
        node_size : int
            Radius of node circles.

        Returns
        -------
        str
            SVG markup (valid XML).
        """
        import math
        import random

        random.seed(42)  # Reproducible layout

        # Simple force-directed layout (iteration-based)
        nodes = list(self.graph.nodes())
        if not nodes:
            return '<svg></svg>'

        # Initial random positions
        pos = {n.node_id: [random.uniform(50, width - 50), random.uniform(50, height - 50)] for n in nodes}

        # Few iterations of attraction/repulsion
        for _ in range(10):
            for i, n1 in enumerate(nodes):
                fx, fy = 0, 0
                for j, n2 in enumerate(nodes):
                    if i == j:
                        continue
                    dx = pos[n2.node_id][0] - pos[n1.node_id][0]
                    dy = pos[n2.node_id][1] - pos[n1.node_id][1]
                    dist = math.sqrt(dx**2 + dy**2) + 1e-3
                    # Repulsion
                    fx -= (dx / dist) * 100 / (dist**2 + 1)
                    fy -= (dy / dist) * 100 / (dist**2 + 1)

                # Attraction to adjacent nodes
                for neighbor in self.graph.neighbors(n1.node_id):
                    dx = pos[neighbor.node_id][0] - pos[n1.node_id][0]
                    dy = pos[neighbor.node_id][1] - pos[n1.node_id][1]
                    dist = math.sqrt(dx**2 + dy**2) + 1e-3
                    fx += (dx / dist) * 0.1
                    fy += (dy / dist) * 0.1

                pos[n1.node_id][0] = max(node_size, min(width - node_size, pos[n1.node_id][0] + fx * 0.1))
                pos[n1.node_id][1] = max(node_size, min(height - node_size, pos[n1.node_id][1] + fy * 0.1))

        # Build SVG
        svg_lines = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'  <style>',
            f'    .node {{ fill: #b3d9ff; stroke: #0066cc; stroke-width: 2; }}',
            f'    .node-label {{ font-family: Arial; font-size: 12px; text-anchor: middle; dominant-baseline: middle; }}',
            f'    .edge {{ stroke: #666; stroke-width: 1.5; }}',
            f'    .edge-label {{ font-family: Arial; font-size: 10px; fill: #666; }}',
            f'  </style>',
        ]

        # Edges
        seen = set()
        for edge in self.graph.edges():
            key = (edge.src.node_id, edge.dst.node_id)
            if key in seen:
                continue
            seen.add(key)
            x1, y1 = pos[edge.src.node_id]
            x2, y2 = pos[edge.dst.node_id]
            svg_lines.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge"/>')
            if edge.weight != 1.0:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                svg_lines.append(
                    f'  <text x="{mx}" y="{my - 5}" class="edge-label">{edge.weight}</text>'
                )

        # Nodes
        for node in nodes:
            x, y = pos[node.node_id]
            svg_lines.append(f'  <circle cx="{x}" cy="{y}" r="{node_size}" class="node"/>')
            svg_lines.append(
                f'  <text x="{x}" y="{y}" class="node-label">{node.node_id}</text>'
            )

        svg_lines.append("</svg>")
        return "\n".join(svg_lines)

    # ══════════════════════════════════════════════════════════════════════════
    #  Helper
    # ══════════════════════════════════════════════════════════════════════════

    @staticmethod
    def _attrs_to_dot(attrs: dict[str, str]) -> str:
        """Convert a dict to DOT attribute format: key="value", key="value", ..."""
        if not attrs:
            return ""
        pairs = [f'{k}="{v}"' for k, v in attrs.items()]
        return ", ".join(pairs)


# ───────────────────────────────────────────────────────────────────────────────
#  Convenience function
# ───────────────────────────────────────────────────────────────────────────────

def render_graph(
    graph: Graph,
    format: str = "ascii",
    rankdir: str = "TB",
) -> str:
    """
    Quick render of a graph in the specified format.

    Parameters
    ----------
    graph : Graph
    format : str
        "ascii", "dot", or "svg"
    rankdir : str
        Graph direction (for DOT format)

    Returns
    -------
    str
        Rendered output
    """
    renderer = GraphRenderer(graph)
    if format == "ascii":
        return renderer.to_ascii()
    elif format == "dot":
        return renderer.to_dot(rankdir=rankdir)
    elif format == "svg":
        return renderer.to_svg()
    else:
        raise ValueError(f"Unknown format: {format}")


if __name__ == "__main__":
    # Quick demo
    g = Graph(directed=True, name="Demo")
    g.add_edge("A", "B", weight=2.5)
    g.add_edge("B", "C", weight=3.0)
    g.add_edge("A", "C", weight=5.5)

    print("=== ASCII ===")
    print(render_graph(g, "ascii"))
    print()
    print("=== DOT (copy to https://dreampuf.github.io/GraphvizOnline/) ===")
    print(render_graph(g, "dot"))
    print()
    print("=== SVG ===")
    print(render_graph(g, "svg")[:200], "...[truncated]")
