# 📦 نصب و راه‌اندازی

## ۱. نیازمندی‌های سیستم

```bash
# Python 3.9 یا بالاتر
python --version  # باید 3.9+ باشد
```

## ۲. نصب Graph Library

### گزینه A: از کد منبع (توسعه)

```bash
# کلون کردن
git clone https://github.com/yourusername/graph-library.git
cd graph-library

# نصب در حالت توسعه
pip install -e .

# یا اگه development tools می‌خواهید
pip install -e ".[dev]"
```

### گزینه B: نصب مستقیم

```bash
pip install graph-library
```

## ۳. بررسی نصب

```bash
# تست کنید
python -c "from graph import Graph; print('✅ نصب شد!')"
```

## ۴ استفاده سریع

```python
from graph import Graph

# گراف ایجاد کنید
g = Graph(directed=True)

# گره‌ها و یال‌ها اضافه کنید
g.add_edge("A", "B", weight=5)
g.add_edge("B", "C", weight=3)

# نمایش
from graph_renderer import render_graph
print(render_graph(g, format="ascii"))
```

## ۵. چند فایل مهم

- `graph.py` — کلاس‌های اصلی (Graph, Node, Edge)
- `graph_renderer.py` — رندرینگ (ASCII, DOT, SVG, JSON)
- `graph_viewer.html` — نمایش‌دهنده‌ی تعاملی
- `examples.py` — ۱۰ مثال کامل
- `test_graph.py` — تست‌های واحدی

## ۶. اجرای مثال‌ها

```bash
# تمام مثال‌ها
python examples.py

# یک مثال خاص
python examples.py 1
python examples.py 5
```

## ۷. تست‌ها

```bash
# اجرای تمام تست‌ها
python test_graph.py

# باید نتیجه: ✅ تست‌ها گذاشتند
```

## ۸. ابزارهای توسعه (اختیاری)

```bash
# نصب کامل برای توسعه
pip install -e ".[dev]"

# یا دستی
pip install mypy black flake8 pylint pytest sphinx
```

### اجرای linters

```bash
# Type checking
mypy graph.py

# Format
black graph.py

# Lint
flake8 graph.py
pylint graph.py
```

## ۹. مستندات

- `README.md` — مستندات اصلی
- `VISUALIZATION.md` — راهنمای رندرینگ
- `DOT_FORMAT_GUIDE.md` — فرمت DOT کامل
- `CONTRIBUTING.md` — نحوه‌ی مشارکت

## ۱۰. نمایش‌دهنده‌ی تعاملی

```bash
# یک JSON تولید کنید
python -c "
from graph import Graph
from graph_renderer import render_graph

g = Graph(directed=True)
g.add_edge('A', 'B', weight=5)
g.add_edge('B', 'C', weight=3)

json_data = render_graph(g, format='json')
with open('graph.json', 'w') as f:
    f.write(json_data)
"

# سپس graph_viewer.html را در مرورگر باز کنید
# و graph.json را بارگذاری کنید
```

## ۱۱. مشکلات رایج

### مشکل: "ModuleNotFoundError: No module named 'graph'"

**حل:**
```bash
# اطمینان حاصل کنید که در درستگاه هستید
cd graph-library

# یا نصب کنید
pip install -e .
```

### مشکل: Python نسخه قدیمی

**حل:**
```bash
# بروزرسانی کنید
python3 -m pip install --upgrade pip
# یا استفاده از Python 3.9+
python3.9 -m pip install -e .
```

### مشکل: اجازه‌های نصب

**حل:**
```bash
# استفاده از --user
pip install --user -e .

# یا virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate  # Windows
pip install -e .
```

## ۱۲. دستورات مفید

```bash
# نمایش اطلاعات نصب شده
pip show graph-library

# اپدیت
pip install --upgrade graph-library

# حذف
pip uninstall graph-library
```

## 📚 منابع

- [Documentation](README.md)
- [Examples](examples.py)
- [Tests](test_graph.py)
- [GitHub](https://github.com/yourusername/graph-library)

---

**موفق باشید!** 🚀
