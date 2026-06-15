# Contributing to Graph Library

We appreciate your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and professional. We welcome contributors from all backgrounds.

## How to Contribute

### Reporting Issues

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and environment

### Suggesting Features

Have an idea? Open an issue with:
- Clear description of the feature
- Why it would be useful
- Potential use cases
- Code examples if applicable

### Submitting Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/graph-library.git
   cd graph-library
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/my-feature
   # or
   git checkout -b fix/bug-description
   ```

3. **Make your changes**
   - Follow the code style (see below)
   - Write clear, documented code
   - Add tests for new features
   - Update documentation

4. **Test your changes**
   ```bash
   python test_graph.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: description"
   git commit -m "Fix: description"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/my-feature
   ```

## Code Style

### Python Style

- **Follow PEP 8** (mostly)
- **Use type hints** throughout
- **Clear variable names** (no single-letter except iterators)
- **Docstrings** on all public methods
- **Comments** for complex logic

Example:
```python
def add_edge(
    self,
    src_id: Any,
    dst_id: Any,
    weight: float = 1.0,
    *,
    auto_add_nodes: bool = True,
    **attrs: Any,
) -> Edge:
    """
    Add an edge to the graph.

    Parameters
    ----------
    src_id, dst_id : Any
        Node identifiers
    weight : float
        Edge weight (default 1.0)
    auto_add_nodes : bool
        Create missing nodes automatically
    **attrs :
        Edge attributes

    Returns
    -------
    Edge
        The newly created edge
    """
```

### Documentation

- **Clear, concise docstrings**
- **Type hints on all parameters**
- **Examples in docstrings**
- **Markdown formatting** for complex docs

## Areas for Contribution

### High Priority

- [ ] **Phase 2 Algorithms**
  - BFS/DFS traversal
  - Shortest path (Dijkstra, Bellman-Ford)
  - Cycle detection
  - Topological sort
  - Strongly connected components

- [ ] **Graph Serialization**
  - JSON export/import
  - GraphML format
  - GML format

### Medium Priority

- [ ] **Performance**
  - Reverse adjacency index
  - Graph compression
  - Lazy loading

- [ ] **Visualization**
  - Additional layout algorithms
  - Better SVG rendering
  - 3D visualization

### Low Priority

- [ ] **Examples**
  - More real-world use cases
  - Educational tutorials
  - Algorithm walkthroughs

- [ ] **Documentation**
  - API extensions
  - Performance guides
  - Comparison with other libraries

## Testing

### New Features

For every new feature, include tests:

```python
def test_my_new_feature():
    g = Graph()
    # Setup
    g.add_node("A")
    
    # Test
    result = g.my_new_feature("A")
    
    # Assert
    assert result is not None
    assert result == expected_value
```

### Running Tests

```bash
# Manual test runner (no pytest needed)
python test_graph.py

# Or run specific test file
python -m pytest test_graph.py -v
```

## Review Process

1. **Code Review** — We'll review for:
   - Correctness
   - Performance
   - Code style
   - Documentation
   - Test coverage

2. **Feedback** — We may request changes

3. **Merge** — Once approved, your PR will be merged!

## Development Setup

```bash
# Clone
git clone https://github.com/yourusername/graph-library.git
cd graph-library

# Install (development)
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Run tests
python test_graph.py

# Run examples
python examples.py

# Read docs
cat README.md
```

## Questions?

- **Documentation** — See [README.md](README.md)
- **Issues** — Open a GitHub issue
- **Discussions** — GitHub Discussions (if enabled)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Graph Library! 🎉
