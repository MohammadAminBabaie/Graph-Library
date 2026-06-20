# 📝 Commit Message Template

استفاده کن این template برای ایجاد clear، consistent commit messages.

---

## فرمت

```
<emoji> <type>(<scope>): <subject>

<body>

<footer>
```

---

## مثال‌های واقعی

### Type 1: Feature Addition
```
✨ feat(core): add name field to Edge class with auto-generation

- Add 'name' parameter to Edge.__init__()
- Auto-generate name as "{src_id}_{dst_id}" if not provided
- Update Edge.__repr__() to show name
- Update all Edge creation calls in Graph
- Backward compatible with existing code

Closes #45
Breaking-Changes: None
```

### Type 2: Bug Fix
```
🐛 fix(graph): correct in_degree cache corruption on edge removal

Previously, when removing edges, the in_degree cache was not
properly decremented, leading to incorrect degree queries.

- Fix _inc_in_degree() call in remove_edge()
- Add regression test case
- Verify all tests pass

Fixes #123
```

### Type 3: Documentation
```
📚 docs: add comprehensive DOT format guide

Create DOT_FORMAT_GUIDE.md with:
- Complete DOT syntax reference
- Node/edge/graph attribute tables
- Layout directions explained
- 5+ working examples
- Integration with Graph Library
- Best practices & tips

Related: #89
```

### Type 4: Packaging/Setup
```
🔧 chore: add Python packaging files

Add production-ready packaging infrastructure:
- pyproject.toml (modern setuptools config)
- setup.py + setup.cfg (backward compatibility)
- requirements.txt (dependencies)
- requirements-dev.txt (dev tools)
- MANIFEST.in (non-Python files)
- __init__.py (package initialization)

Ready for PyPI distribution
```

### Type 5: Refactoring
```
♻️ refactor(renderer): improve DOT export flexibility

- Rename to_dot() parameters for clarity
- Add show_node_labels parameter
- Add show_edge_labels parameter
- Support custom label formatters
- Maintain backward compatibility via defaults

Performance: No impact
Tests: All passing
```

---

## Types (با ایموجی)

| Type | Emoji | کاربرد |
|------|-------|--------|
| **feat** | ✨ | Feature جدید |
| **fix** | 🐛 | Bug fix |
| **docs** | 📚 | Documentation |
| **style** | 💄 | Code style (no logic change) |
| **refactor** | ♻️ | Code restructuring |
| **perf** | ⚡ | Performance improvement |
| **test** | 🧪 | Tests اضافه/بهبود |
| **chore** | 🔧 | Maintenance (deps, config) |
| **ci** | ⚙️ | CI/CD changes |
| **security** | 🔒 | Security fix |

---

## Scope (موضوع)

```
core       → graph.py (Graph, Node, Edge classes)
renderer   → graph_renderer.py
viewer     → graph_viewer.html
pkg        → Packaging & setup files
docs       → Documentation
tests      → Test files
```

---

## Subject (عنوان)

- ✓ Imperative mood: "add", "fix", "update" (نه "added", "fixed")
- ✓ Keep under 50 characters
- ✓ Don't capitalize first letter (بعد emoji)
- ✓ No period at end

**Examples:**
- ✓ `add name field to Edge class`
- ✓ `fix in_degree cache corruption`
- ✓ `update DOT export format`
- ✗ `Added name field`
- ✗ `Fix in_degree cache corruption.`

---

## Body (جزئیات)

شامل:
- **چرا** این تغییر ضروری بود
- **چی** تغییر کرد
- **چطور** تغییر انجام شد
- Reference به related issues
- Testing notes

**مثال:**
```
Previously, the Graph class did not support edge names, making
it difficult to label relationships meaningfully.

This commit adds:
- 'name' parameter to Edge class
- Auto-generation of names if not provided
- Proper handling in all Graph methods
- Examples in documentation

Fixes #45
Tests: All passing (44/44)
```

---

## Footer

```
Fixes #123              → Close issue
Closes #456             → Close issue
Related: #789           → Reference related issue
Breaking-Changes: ...   → Breaking changes
Reviewed-by: @user      → Code review
Co-authored-by: @user   → Collaboration
```

---

## نمونه کامل

```
✨ feat(core): add batch node/edge operations

Add bulk import/export methods for efficient graph construction:

- add_nodes(iterable) → bulk add Node objects
- add_edges(iterable) → bulk add Edge objects
- Performance improvement: ~50% faster for large graphs
- Backward compatible with existing API

Benefits:
- Easier programmatic graph creation
- Better performance for large imports
- Cleaner API for common operations

Example:
  nodes = [Node(i) for i in range(1000)]
  edges = [(Node(i), Node(i+1)) for i in range(999)]
  g.add_nodes(nodes)
  g.add_edges(edges)

Fixes #234
Related: #235, #236
Tests: All passing (48/48)
Breaking-Changes: None
```

---

## Checklist قبل Commit

- [ ] Code tested locally
- [ ] All tests passing
- [ ] Comments/docstrings updated
- [ ] No debug statements left
- [ ] Related docs updated
- [ ] CHANGELOG updated (اگه لازم)
- [ ] Commit message واضح و meaningful
- [ ] One logical change per commit

---

**Version:** 1.0  
**Last Updated:** June 16, 2025
