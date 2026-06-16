"""
graph_renderer.py

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

================================================================================
Graph Visualization and Rendering Utilities

Generates DOT (Graphviz) format, SVG, ASCII art, and JSON for interactive web
visualization.
================================================================================
"""

from __future__ import annotations

import json
import math
import random
from typing import Any, Callable, Optional

from graph import Graph, Node, Edge


class GraphRenderer:
    """
    Renders a Graph in various formats: DOT, SVG, ASCII art, and JSON.

    Supports:
    - ASCII art (terminal preview)
    - DOT format (Graphviz)
    - SVG (embedded with force-directed layout)
    - JSON (for interactive web visualization)
    """

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    # ══════════════════════════════════════════════════════════════════════════
    #  JSON Export (for interactive web visualization)
    # ══════════════════════════════════════════════════════════════════════════

    def to_json(self) -> str:
        """
        Export graph to JSON format for interactive web visualization.

        Returns
        -------
        str
            JSON string with nodes and edges information
        """
        nodes_list = []
        edges_list = []

        # Export nodes
        for node in self.graph.nodes():
            nodes_list.append({
                "id": str(node.node_id),
                "label": str(node.node_id),
                "data": node.data,
                "attrs": node.attrs(),
            })

        # Export edges
        seen = set()
        for edge in self.graph.edges():
            src_id = str(edge.src.node_id)
            dst_id = str(edge.dst.node_id)
            key = (src_id, dst_id, edge.edge_id)

            if key not in seen:
                seen.add(key)
                edges_list.append({
                    "source": src_id,
                    "target": dst_id,
                    "weight": edge.weight,
                    "label": f"{edge.weight}" if edge.weight != 1.0 else "",
                    "attrs": edge.attrs(),
                })

        return json.dumps({
            "name": self.graph.name,
            "directed": self.graph.directed,
            "nodes": nodes_list,
            "edges": edges_list,
        }, indent=2)

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
            Default attributes for all nodes
        edge_attrs : dict, optional
            Default attributes for all edges
        node_labeler : callable, optional
            Function(node) -> str to customize node labels

        Returns
        -------
        str
            DOT source code
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
        Generate ASCII art representation of the graph.

        Parameters
        ----------
        max_width : int
            Maximum line width

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
        Generate SVG visualization with force-directed layout.

        Parameters
        ----------
        width, height : int
            Canvas dimensions
        node_size : int
            Node radius

        Returns
        -------
        str
            SVG markup
        """
        random.seed(42)
        nodes = list(self.graph.nodes())
        if not nodes:
            return '<svg></svg>'

        pos = {n.node_id: [random.uniform(50, width - 50), random.uniform(50, height - 50)] for n in nodes}

        # Force-directed layout iterations
        for _ in range(10):
            for i, n1 in enumerate(nodes):
                fx, fy = 0, 0
                for j, n2 in enumerate(nodes):
                    if i == j:
                        continue
                    dx = pos[n2.node_id][0] - pos[n1.node_id][0]
                    dy = pos[n2.node_id][1] - pos[n1.node_id][1]
                    dist = math.sqrt(dx**2 + dy**2) + 1e-3
                    fx -= (dx / dist) * 100 / (dist**2 + 1)
                    fy -= (dy / dist) * 100 / (dist**2 + 1)

                for neighbor in self.graph.neighbors(n1.node_id):
                    dx = pos[neighbor.node_id][0] - pos[n1.node_id][0]
                    dy = pos[neighbor.node_id][1] - pos[n1.node_id][1]
                    dist = math.sqrt(dx**2 + dy**2) + 1e-3
                    fx += (dx / dist) * 0.1
                    fy += (dy / dist) * 0.1

                pos[n1.node_id][0] = max(node_size, min(width - node_size, pos[n1.node_id][0] + fx * 0.1))
                pos[n1.node_id][1] = max(node_size, min(height - node_size, pos[n1.node_id][1] + fy * 0.1))

        svg_lines = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<style>',
            f'  .node {{ fill: #b3d9ff; stroke: #0066cc; stroke-width: 2; }}',
            f'  .node-label {{ font-family: Arial; font-size: 12px; text-anchor: middle; dominant-baseline: middle; }}',
            f'  .edge {{ stroke: #666; stroke-width: 1.5; }}',
            f'  .edge-label {{ font-family: Arial; font-size: 10px; fill: #666; }}',
            f'</style>',
        ]

        seen = set()
        for edge in self.graph.edges():
            key = (edge.src.node_id, edge.dst.node_id)
            if key in seen:
                continue
            seen.add(key)
            x1, y1 = pos[edge.src.node_id]
            x2, y2 = pos[edge.dst.node_id]
            svg_lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge"/>')
            if edge.weight != 1.0:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                svg_lines.append(f'<text x="{mx}" y="{my - 5}" class="edge-label">{edge.weight}</text>')

        for node in nodes:
            x, y = pos[node.node_id]
            svg_lines.append(f'<circle cx="{x}" cy="{y}" r="{node_size}" class="node"/>')
            svg_lines.append(f'<text x="{x}" y="{y}" class="node-label">{node.node_id}</text>')

        svg_lines.append("</svg>")
        return "\n".join(svg_lines)

    # ══════════════════════════════════════════════════════════════════════════
    #  Helper
    # ══════════════════════════════════════════════════════════════════════════

    @staticmethod
    def _attrs_to_dot(attrs: dict[str, str]) -> str:
        """Convert dict to DOT attribute format."""
        if not attrs:
            return ""
        pairs = [f'{k}="{v}"' for k, v in attrs.items()]
        return ", ".join(pairs)


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
        "ascii", "dot", "svg", or "json"
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
    elif format == "json":
        return renderer.to_json()
    else:
        raise ValueError(f"Unknown format: {format}")


if __name__ == "__main__":
    from graph import Graph

    g = Graph(directed=True, name="Demo")
    g.add_edge("A", "B", weight=2.5)
    g.add_edge("B", "C", weight=3.0)
    g.add_edge("A", "C", weight=5.5)

    print("=== ASCII ===")
    print(render_graph(g, "ascii"))
    print()
    print("=== DOT ===")
    print(render_graph(g, "dot")[:200])
    print()
    print("=== JSON ===")
    print(render_graph(g, "json"))
