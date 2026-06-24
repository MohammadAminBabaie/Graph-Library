"""
Graph Library — کتابخانه‌ی حرفه‌ای گراف پایتون

Licensed under Apache License 2.0

ویژگی‌های اصلی:
- Directed/Undirected graphs
- Weighted edges with names
- Multi-edges (parallel edges)
- Batch operations
- Advanced magic methods
- Matrix operations (numpy/scipy)
- Linear algebra (eigenvalues, determinant)
"""

from graph import Graph, Node, Edge, GraphError, NodeNotFoundError, EdgeNotFoundError, DuplicateNodeError
from graph_renderer import GraphRenderer, render_graph

try:
    from graph_advanced import GraphAdvanced, print_matrix_info, adjacency_matrix_from_graph
    HAS_ADVANCED = True
except ImportError:
    HAS_ADVANCED = False

__version__ = "1.1.0"
__author__ = "Graph Library Contributors"
__license__ = "Apache-2.0"
__url__ = "https://github.com/yourusername/graph-library"

if HAS_ADVANCED:
    __all__ = [
        "Graph", "Node", "Edge", "GraphRenderer", "render_graph",
        "GraphError", "NodeNotFoundError", "EdgeNotFoundError", "DuplicateNodeError",
        "GraphAdvanced", "print_matrix_info", "adjacency_matrix_from_graph",
    ]
else:
    __all__ = [
        "Graph", "Node", "Edge", "GraphRenderer", "render_graph",
        "GraphError", "NodeNotFoundError", "EdgeNotFoundError", "DuplicateNodeError",
    ]

__info__ = {
    "name": "Graph Library",
    "version": __version__,
    "description": "Professional Python graph data structure library",
    "author": __author__,
    "license": __license__,
    "url": __url__,
    "has_advanced": HAS_ADVANCED,
}
