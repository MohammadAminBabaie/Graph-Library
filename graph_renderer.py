"""
graph_renderer.py - تمام فرمت‌های رندرینگ

Licensed under Apache License 2.0

فرمت‌های پشتیبانی شده:
- ASCII (پیش‌نمایش ترمینال)
- DOT (Graphviz)
- SVG (وب)
- JSON (Interactive viewer)
"""

from __future__ import annotations

import json
import math
import random
from typing import Any, Callable, Optional

from graph import Graph, Node, Edge


class GraphRenderer:
    """رندرینگ گراف در قالب‌های مختلف"""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    # ══════════════════════════════════════════════════════════════════════════
    #  JSON Export (برای web viewer)
    # ══════════════════════════════════════════════════════════════════════════

    def to_json(self) -> str:
        """صادرات گراف به JSON"""
        nodes_list = []
        edges_list = []

        for node in self.graph.nodes():
            nodes_list.append({
                "id": str(node.node_id),
                "label": str(node.node_id),
                "data": node.data,
                "attrs": node.attrs(),
            })

        seen = set()
        for edge in self.graph.edges():
            src_id = str(edge.src.node_id)
            dst_id = str(edge.dst.node_id)
            key = (src_id, dst_id, edge.edge_id)

            if key not in seen:
                seen.add(key)
                label = f"{edge.name}({edge.weight})" if edge.weight != 1.0 else edge.name
                edges_list.append({
                    "source": src_id,
                    "target": dst_id,
                    "name": edge.name,
                    "weight": edge.weight,
                    "label": label,
                    "attrs": edge.attrs(),
                })

        return json.dumps({
            "name": self.graph.name,
            "directed": self.graph.directed,
            "nodes": nodes_list,
            "edges": edges_list,
        }, indent=2)

    # ══════════════════════════════════════════════════════════════════════════
    #  DOT Format with save/load
    # ══════════════════════════════════════════════════════════════════════════

    def to_dot(
        self,
        rankdir: str = "TB",
        show_node_labels: bool = True,
        show_edge_labels: bool = True,
        node_attrs: Optional[dict[str, str]] = None,
        edge_attrs: Optional[dict[str, str]] = None,
        node_labeler: Optional[Callable[[Node], str]] = None,
    ) -> str:
        """
        صادرات گراف به فرمت DOT
        
        Parameters
        ----------
        rankdir : str
            جهت: TB, LR, BT, RL
        show_node_labels : bool
            نمایش لیبل گره‌ها
        show_edge_labels : bool
            نمایش لیبل یال‌ها (نام و وزن)
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

        # گره‌ها
        for node in self.graph.nodes():
            label = node_labeler(node) if show_node_labels else ""
            attrs = {"label": label} if show_node_labels else {}
            attrs.update(node.get_attr("_dot_attrs") or {})
            attrs_str = self._attrs_to_dot(attrs)
            lines.append(f'  "{node.node_id}" [{attrs_str}];')

        lines.append("")

        # یال‌ها
        seen_edges = set()
        for edge in self.graph.edges():
            src_id = edge.src.node_id
            dst_id = edge.dst.node_id

            edge_key = tuple(sorted([src_id, dst_id])) if not self.graph.directed else (src_id, dst_id)
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)

            if show_edge_labels:
                label = f"{edge.name}({edge.weight})"
            else:
                label = ""
            
            attrs = {"label": label} if show_edge_labels else {}
            attrs.update(edge.get_attr("_dot_attrs") or {})
            attrs_str = self._attrs_to_dot(attrs)
            lines.append(f'  "{src_id}" {edge_op} "{dst_id}" [{attrs_str}];')

        lines.append("}")
        return "\n".join(lines)

    def save_to_dot(self, filename: str, **kwargs: Any) -> None:
        """ذخیره‌ی گراف به فایل DOT"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_dot(**kwargs))

    @staticmethod
    def load_from_dot(filename: str) -> Graph:
        """لود کردن گراف از فایل DOT - تحت ساخت"""
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        # تحلیل ساده DOT
        is_directed = "digraph" in content
        g = Graph(directed=is_directed)
        
        # استخراج گره‌ها (ساده)
        import re
        node_pattern = r'"([^"]+)"'
        nodes = set(re.findall(node_pattern, content))
        for node_id in nodes:
            g.add_node(node_id)
        
        # استخراج یال‌ها
        edge_pattern = r'"([^"]+)"\s*(?:->|--)\s*"([^"]+)"'
        edges = re.findall(edge_pattern, content)
        for src, dst in edges:
            if src in nodes and dst in nodes:
                g.add_edge(src, dst, auto_add_nodes=False)
        
        return g

    # ══════════════════════════════════════════════════════════════════════════
    #  ASCII Art
    # ══════════════════════════════════════════════════════════════════════════

    def to_ascii(self, max_width: int = 100) -> str:
        """نمایش ASCII"""
        kind = "جهت‌دار" if self.graph.directed else "بدون‌جهت"
        lines = [
            f"Graph: {self.graph.name} ({kind})",
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
            label = f" [{edge.name}]" if edge.name else ""
            weight_str = f" (w={edge.weight})" if edge.weight != 1.0 else ""
            lines.append(f"  {edge.src.node_id} {op} {edge.dst.node_id}{label}{weight_str}")

        return "\n".join(lines)

    # ══════════════════════════════════════════════════════════════════════════
    #  SVG
    # ══════════════════════════════════════════════════════════════════════════

    def to_svg(self, width: int = 800, height: int = 600, node_size: int = 40) -> str:
        """تولید SVG"""
        random.seed(42)
        nodes = list(self.graph.nodes())
        if not nodes:
            return '<svg></svg>'

        pos = {n.node_id: [random.uniform(50, width - 50), random.uniform(50, height - 50)] for n in nodes}

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
            '<style>',
            '.node { fill: #b3d9ff; stroke: #0066cc; stroke-width: 2; }',
            '.node-label { font-family: Arial; font-size: 12px; text-anchor: middle; dominant-baseline: middle; }',
            '.edge { stroke: #666; stroke-width: 1.5; }',
            '.edge-label { font-family: Arial; font-size: 10px; fill: #666; }',
            '</style>',
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
                svg_lines.append(f'<text x="{mx}" y="{my - 5}" class="edge-label">{edge.name}({edge.weight})</text>')

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
        """تبدیل dict به فرمت DOT"""
        if not attrs:
            return ""
        pairs = [f'{k}="{v}"' for k, v in attrs.items()]
        return ", ".join(pairs)


def render_graph(
    graph: Graph,
    format: str = "ascii",
    rankdir: str = "TB",
    **kwargs: Any
) -> str:
    """
    رندرینگ سریع گراف
    
    Parameters
    ----------
    graph : Graph
    format : str
        "ascii", "dot", "svg", or "json"
    rankdir : str
        جهت (برای DOT)
    **kwargs
        پارامتر‌های اضافی
    """
    renderer = GraphRenderer(graph)
    if format == "ascii":
        return renderer.to_ascii()
    elif format == "dot":
        return renderer.to_dot(rankdir=rankdir, **kwargs)
    elif format == "svg":
        return renderer.to_svg(**kwargs)
    elif format == "json":
        return renderer.to_json()
    else:
        raise ValueError(f"فرمت نامعلوم: {format}")
