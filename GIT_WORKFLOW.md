# Git Workflow Guide — Graph Library

Complete guide for branching strategy, tags, releases, and GitHub setup.

---

## 📋 Git Branching Strategy

### Recommended: Git Flow

```
main (production) ─────────────────────────────────────────
  │     ↑
  │     │ (merge & tag release)
  │     │
  ├─────┴─── release/v1.x branches (release prep)
  │
  ├─────────── develop (integration branch)
  │     ↑
  │     │ (merge feature branches here)
  │     │
  └─────┴─────┬────── feature/feature-name
              │
              ├────── feature/bfs-dfs
              ├────── feature/dijkstra
              ├────── feature/serialization
              │
              └────── bugfix/issue-xxx
```

### Branch Naming Convention

**Feature branches:**
```
feature/bfs-dfs-traversal
feature/dijkstra-algorithm
feature/graph-serialization
feature/visualization-improvement
```

**Bugfix branches:**
```
bugfix/node-creation-error
bugfix/edge-cache-corruption
bugfix/svg-rendering
```

**Release branches:**
```
release/v1.1.0
release/v2.0.0-beta
```

**Hotfix branches:**
```
hotfix/critical-bug-fix
hotfix/security-patch
```

---

## 🏷️ Tag & Release Strategy

### Semantic Versioning: MAJOR.MINOR.PATCH

```
v1.0.0  → First stable release
v1.1.0  → Feature addition (backwards compatible)
v1.0.1  → Bug fix (patch)
v2.0.0  → Breaking changes (major)
v1.0.0-alpha.1  → Alpha release
v1.0.0-beta.1   → Beta release
v1.0.0-rc.1     → Release candidate
```

### Release Timeline

```
Phase                   | Version        | Branch
─────────────────────────────────────────────────────
Current Stable          | v1.0.0        | main
─────────────────────────────────────────────────────
Phase 2 Development     | v1.1.0-dev    | develop
(BFS/DFS, algorithms)   |               |
─────────────────────────────────────────────────────
Phase 2 Release         | v1.1.0        | release/v1.1.0
─────────────────────────────────────────────────────
Phase 3 Planning        | v2.0.0-alpha  | develop
(Serialization)         |               |
─────────────────────────────────────────────────────
```

---

## 📝 Git Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
```
feat      → New feature
fix       → Bug fix
docs      → Documentation only
style     → Code style (no functional change)
refactor  → Code restructuring (no functional change)
perf      → Performance improvement
test      → Adding or updating tests
chore     → Maintenance (dependencies, configs)
ci        → CI/CD configuration
```

### Scope (optional)
```
core      → graph.py
render    → graph_renderer.py
examples  → examples.py
test      → test_graph.py
docs      → documentation
```

### Examples
```
feat(core): add multi-edge support
→ Good: Clear, specific, follows convention

fix(test): correct in_degree cache handling
→ Good: Identifies the issue and component

docs: add API reference
→ Good: Self-explanatory

refactor(core): optimize node lookup
→ Good: Type + scope + action
```

---

## 📦 Creating Releases on GitHub

### Step 1: Prepare Release Branch
```bash
# Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.1.0

# Update version numbers
# Update CHANGELOG.md
# Final testing and fixes
```

### Step 2: Merge to Main
```bash
# Switch to main and merge
git checkout main
git merge --no-ff release/v1.1.0

# Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0: Add Phase 2 algorithms"

# Push
git push origin main
git push origin v1.1.0
```

### Step 3: Create GitHub Release

**On GitHub UI:**

1. Go to Releases → Draft New Release
2. Choose tag: `v1.1.0`
3. Release title: `Graph Library v1.1.0 — Phase 2 Algorithms`
4. Fill release notes:

```markdown
## 🎉 Version 1.1.0 — Phase 2 Algorithms

### ✨ New Features
- BFS/DFS graph traversal
- Dijkstra shortest path algorithm
- Cycle detection
- Topological sort

### 🔧 Improvements
- Better error messages
- Performance optimizations
- Enhanced documentation

### 🐛 Bug Fixes
- Fixed in_degree cache bug
- Corrected SVG rendering
- Resolved multi-edge removal issue

### 📊 Statistics
- +150 lines of code
- +3 new algorithms
- +20 test cases
- +200 lines documentation

### 🙏 Thanks
Thanks to all contributors and users!

### 📥 Installation
```bash
pip install graph-library==1.1.0
```
or clone: `git clone --branch v1.1.0`

### 📖 Changelog
See [CHANGELOG.md](CHANGELOG.md) for full details
```

5. **Options:**
   - ✓ Pre-release (for alpha/beta)
   - ✓ Set as latest release (for stable)
   - ✓ Create discussion (engage community)

6. Click "Publish release"

---

## 📋 Files Needed for GitHub

### 1. `.gitignore` ✓ (Already created)

### 2. `CHANGELOG.md` (NEW)

Track changes by version:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Feature X
- Feature Y

### Changed
- Improved API

### Fixed
- Bug A

---

## [1.1.0] — 2025-06-20

### Added
- BFS/DFS traversal algorithms
- Dijkstra shortest path
- Cycle detection
- Topological sort

### Fixed
- In-degree cache corruption
- SVG rendering issues

---

## [1.0.0] — 2025-06-15

### Added
- Initial release
- Core graph data structure
- Visualization (ASCII, DOT, SVG)
- Comprehensive documentation
```

### 3. `.github/workflows/` (NEW - Optional CI/CD)

**Test on every push:**

`.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Run tests
      run: python test_graph.py
```

### 4. `.github/ISSUE_TEMPLATE/` (NEW)

**Bug Report Template:**

`.github/ISSUE_TEMPLATE/bug_report.md`:
```markdown
---
name: Bug report
about: Report a bug
---

## Description
Clear description of the bug.

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- Python version:
- OS:
- Graph Library version:

## Code Example
```python
# Minimal code to reproduce
```

## Additional Context
Any other context.
```

**Feature Request Template:**

`.github/ISSUE_TEMPLATE/feature_request.md`:
```markdown
---
name: Feature request
about: Suggest an idea
---

## Description
Clear description of the feature.

## Motivation
Why is this needed?

## Proposed Solution
How should it work?

## Example Usage
```python
# How users would use this feature
```

## Alternatives
Other approaches considered.
```

### 5. `.github/pull_request_template.md` (NEW)

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement

## Related Issue
Closes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Added new tests
- [ ] All tests passing
- [ ] Tested on Python 3.9+

## Documentation
- [ ] Updated README
- [ ] Added docstrings
- [ ] Added examples

## Checklist
- [ ] Code follows style guidelines
- [ ] No new warnings
- [ ] Added/updated tests
- [ ] Documentation updated
```

---

## 🔄 Workflow Example

### Creating a Feature

```bash
# 1. Start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/bfs-dfs-traversal

# 3. Make changes
# ... write code, tests, docs ...

# 4. Commit frequently
git add graph.py
git commit -m "feat(core): implement BFS traversal"

git add test_graph.py
git commit -m "test(core): add BFS test cases"

git add examples.py
git commit -m "docs(examples): add BFS example"

# 5. Push to GitHub
git push origin feature/bfs-dfs-traversal

# 6. Create Pull Request on GitHub
# → Describe changes
# → Link to issues
# → Request reviewers
# → Wait for approval

# 7. After merge, delete local branch
git checkout develop
git pull origin develop
git branch -d feature/bfs-dfs-traversal
```

### Releasing Version 1.1.0

```bash
# 1. Create release branch
git checkout -b release/v1.1.0 develop

# 2. Update version (in code/docs)
# Version number in docstrings, README, etc.

# 3. Update CHANGELOG.md
# List all features, fixes, improvements

# 4. Final testing
python test_graph.py
python examples.py

# 5. Commit
git commit -am "Release v1.1.0"

# 6. Merge to main
git checkout main
git merge --no-ff release/v1.1.0

# 7. Tag
git tag -a v1.1.0 -m "Release v1.1.0: Phase 2 Algorithms"

# 8. Merge back to develop
git checkout develop
git merge --no-ff release/v1.1.0

# 9. Push everything
git push origin main develop
git push origin v1.1.0

# 10. Create GitHub Release (via web UI)
# Copy CHANGELOG section into release notes
```

---

## 📊 GitHub Repository Settings

### Branch Protection Rules

**For main branch:**
- ✓ Require pull request reviews (min. 1)
- ✓ Require status checks to pass
- ✓ Require branches to be up to date
- ✓ Include administrators

**For develop branch:**
- ✓ Require pull request reviews (min. 1)
- ✓ Require status checks to pass

### Labels

Create these labels for issues:

```
🐛 bug           → Something broken
✨ enhancement   → New feature
📚 documentation → Docs improvement
🚀 performance   → Speed/optimization
❓ question      → Need clarification
help wanted      → Looking for contributors
good first issue → For beginners
blocked          → Waiting for something
approved         → Ready to work on
in progress      → Currently being worked on
```

### Milestones

Create milestones for versions:

```
v1.1.0 (Phase 2 Algorithms)
v2.0.0 (Phase 3 - Serialization)
v1.0.x (Bugfixes)
```

### Protected Tags

Protect version tags:
- Pattern: `v*`
- Requires branch to be up to date

---

## 🔗 Automatic Deployments (Optional)

If you want auto-deployment to PyPI:

`.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Build
      run: |
        python -m pip install build
        python -m build
    
    - name: Publish
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

---

## 📈 Recommended Initial Tags

```bash
# Create initial tag for v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0: Initial stable release"
git push origin v1.0.0

# Create development markers
git tag -a v1.1.0-planning -m "Planning for v1.1.0"
git tag -a v2.0.0-planning -m "Planning for v2.0.0"
```

---

## ✅ Final Checklist

Before pushing to GitHub:

- [ ] All tests passing (44/44)
- [ ] Code follows PEP 8 + type hints
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] .gitignore configured
- [ ] LICENSE present
- [ ] CONTRIBUTING.md present
- [ ] No sensitive data in commits
- [ ] Commit messages follow convention
- [ ] Branch names are clear

After creating GitHub repository:

- [ ] Set main branch as default
- [ ] Enable branch protection for main/develop
- [ ] Create issue templates
- [ ] Create PR template
- [ ] Set up labels
- [ ] Create milestones
- [ ] Add repository description
- [ ] Add topics (tags)
- [ ] Enable Discussions (optional)
- [ ] Enable Pages (optional)
- [ ] Create first Release from v1.0.0 tag

---

## 📚 References

- [Git Branching Strategy](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning](https://semver.org/)
- [Commit Message Convention](https://www.conventionalcommits.org/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

