# پروژه قوانین — Graph Library

تمام قوانین و اصول طراحی و توسعه این پروژه

---

## 📋 قوانین کاملی که تا حالا تعریف شدند

### ۱. **دینامیک بودن پروژه و کد** 🔄
- پروژه باید هر وقت تغییر کند، تطبیق پذیر باشد
- نودها و یال‌ها می‌تونند هر وقت اضافه یا حذف بشن
- ویژگی‌ها و متاداتا دینامیکی هستند
- Graph copy، subgraph extraction، و manipulations آزادانه ممکن

### ۲. **پیشنهادهای بهبود و بهتر شدن داده بشه** 💡
- هر کد جدید با تجزیه و تحلیل بهبود ارائه بشه
- فعال‌ترین نقاط برای بهینه‌سازی پیشنهاد بشن
- جایی‌های ضعیف و بدطراحی‌ها شناسایی و اصلاح بشن
- بهتری‌های performance و readability همیشه بررسی شن

### ۳. **تمیز و روی اصول نوشته شه** ✨
- PEP 8 compliance
- Single-responsibility principle
- Clean code principles
- SOLID principles (جایی‌که قابل اعمال)
- DRY (Don't Repeat Yourself)
- Type hints همه‌جا
- Comprehensive docstrings
- Self-documenting code

### ۴. **سعی بر استفاده از تمام ابزارهای موجود** 🛠️
- هر ابزار و feature‌ی که برای بهتری استفاده شود
- Best practices از کمیونیتی و استاندارد‌ها
- Exception handling جامع
- Caching و optimization techniques
- Type system (mypy compatible)

### ۵. **کمال‌گرایی رعایت بشه** 🎯
- اول‌اولی‌ها: Correctness > Performance > Elegance
- هیچ quick-and-dirty solutions
- Comprehensive test coverage
- Edge cases covered
- Error handling complete
- Documentation thorough

### ۶. **تمام چیز انگلیسی باشه** 🌐
- **همه کدها:** Variable names, function names, comments, docstrings
- **تمام داکومنت‌ها:** README، CHANGELOG، CONTRIBUTING، guides
- **تمام error messages و logs**
- **نظرات و توضیحات inline**
- هیچ کد فارسی در خود فایل‌های پایتون

### ۷. **هماهنگی در تمام بخش‌های پروژه** 🔗 [**NEW**]
- **هر تغییر موازی در همه جاها اعمال بشه**
  - API تغییر کرد → Examples update بشن
  - Edge case پیدا شد → Tests update بشن
  - کلاس رفرکتور شد → Docstrings update بشن
  - نسخه increment شد → CHANGELOG update بشن
  
- **پروژه همیشه consistent و هماهنگ باشه**
  - اگه README میگه functionality X وجود داره، واقعاً وجود داشته باشه
  - اگه code X می‌کنه، docstring هم بگه X
  - اگه example Y استفاده می‌کنه، API support کنه
  - تمام اصول در تمام بخش‌ها اعمال بشن

- **چیکلیست برای هر change:**
  - [ ] کد اصلی تغییر کرد
  - [ ] Docstrings update شدند
  - [ ] Tests اضافه/اپدیت شدند
  - [ ] Examples اپدیت شدند (اگه لازم)
  - [ ] README/Documentation اپدیت شد (اگه لازم)
  - [ ] CHANGELOG اپدیت شد
  - [ ] Type hints درست هستند
  - [ ] تمام tests pass می‌کنند

### ۸. **پرسش قبل از فرض** ❓ [**NEW**]
- **اگه چیزی نمی‌دونم یا uncertainty هست:**
  - قبل از اینکه خودم guess کنم، ازت می‌پرسم
  - اگه specification غیر واضح هست، می‌پرسم
  - اگه implementation choice دو راهه است، ازت می‌پرسم
  - اگه مطمئن نیستم that's the requirement، می‌پرسم

- **نه اینطور:**
  - "شاید میخوای اینطوری..."
  - "فکر کنم این درسته..."
  - "معمولاً اینطوری میشه..."

- **بلکه اینطور:**
  - "تایید می‌کنی که..."
  - "الزامات این feature: ... منطقی؟"
  - "بین این دو option، کدوم بهتره؟"

### ۹. **تمرکز روی برآورده کردن خواسته‌ی کاربر** 🎯 [**NEW**]
- **Execution-first**: انجام کار جلو می‌رود، سپس بهبود
- **User requirements are king**: خواسته‌ی کاربر > best practices (اگه conflict)
- **Direct delivery**: مستقیم اونچی‌ رو بدم که خواسته‌ای
- **Efficient focus**: وقت و انرژی رو روی اینکه خاسته‌ای کاملاً انجام شه بزار
- **No over-engineering**: فقط اونچی که لازم، نه "شاید اینجا هم خوب باشه"

---

## 🎯 خلاصه (تمام قوانین یک‌نگاه)

```
1️⃣  Dynamic        → پروژه انعطاف‌پذیر و قابل تغییر
2️⃣  Improvement    → ہمیشہ بہتری پیشنہاد کن
3️⃣  Clean Code     → اصول clean code + principles
4️⃣  Tools          → تمام ابزارهای موجود استفاده
5️⃣  Perfection     → کمال‌گرایی در execution
6️⃣  English        → تمام چیز انگلیسی
7️⃣  Consistency    → تغییرات موازی در همه جا [NEW]
8️⃣  Ask First      → پرسش قبل از فرض [NEW]
9️⃣  Execution      → تمرکز روی خواسته‌ی کاربر [NEW]
```

---

## ✅ Consistency Checklist

هر تغییر باید این مراحل را داشته باشد:

### Phase 1: Understand
- [ ] متوجه دقیق requirement
- [ ] مشخص scope change
- [ ] شناسایی affected areas

### Phase 2: Implement
- [ ] Core functionality (graph.py / relevant module)
- [ ] Type hints (اگه نیاز)
- [ ] Error handling
- [ ] Edge cases

### Phase 3: Test
- [ ] Unit tests اضافه/اپدیت
- [ ] Manual testing
- [ ] تمام tests pass

### Phase 4: Document
- [ ] Docstrings update
- [ ] README update (اگه API change)
- [ ] Examples update (اگه behavior change)
- [ ] CHANGELOG update

### Phase 5: Verify
- [ ] تمام اصول اعمال شدند؟
- [ ] Consistency همه‌جا؟
- [ ] پروژه هماهنگ؟
- [ ] هیچ inconsistency نیست؟

---

## 🔍 Consistency Examples

### مثال 1: نام Method تغییر کرد

اگه `add_node()` رو `create_node()` تغییر بدی:

```
❌ WRONG:
  • graph.py میں rename کردی
  • examples.py اپدیت نکردی
  • README اپدیت نکردی
  → کاربران confused می‌شند!

✅ CORRECT:
  • graph.py میں rename کردی
  • تمام examples.py calls update کردی
  • README API section update کردی
  • CHANGELOG add کردی
  • Tests اپدیت کردی
  → همه جا consistent!
```

### مثال 2: نیا Feature اضافه کردی

اگه `find_path()` method add کردی:

```
❌ WRONG:
  • graph.py میں code نوشتی
  • Documentation ننوشتی
  • Examples نسازی
  • Tests نسازی
  → Half-baked implementation

✅ CORRECT:
  • graph.py میں code نوشتی (full docstring)
  • Unit tests نوشتی (edge cases)
  • Example code نوشتی
  • README میں document کردی
  • CHANGELOG add کردی
  → Production-ready feature
```

### مثال 3: Bug Fix کردی

اگه `in_degree` cache bug fix کردی:

```
❌ WRONG:
  • graph.py fix کردی
  • Test نوشتی
  • تمام! commit کردی
  → شاید جای دیگه هم bug ہے

✅ CORRECT:
  • Root cause شناسایی کردی
  • graph.py fix کردی
  • Test نوشتی (regression prevention)
  • Similar cases search کردی (کاش جای دیگه bug نباشه)
  • CHANGELOG document کردی
  • README مثال add کردی (اگه لازم)
  → Bulletproof fix
```

---

## 📚 References & Standards

### Code Style
- **PEP 8**: https://pep8.org/
- **Type Hints**: https://docs.python.org/3/library/typing.html
- **Docstring Format**: NumPy style

### Git
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Git Flow**: https://nvie.com/posts/a-successful-git-branching-model/
- **Semantic Versioning**: https://semver.org/

### Best Practices
- **SOLID Principles**: Single, Open/Closed, Liskov, Interface, Dependency
- **Clean Code**: Robert C. Martin (Uncle Bob)
- **Testing**: 100% coverage for core, edge cases covered

---

## 🎯 Decision Making Framework

وقتی تغییر میخوای انجام بدی:

```
1. مطمئنی که متوجه requirement؟
   → اگه نه: STOP → ازم پرس

2. اثر این change روی پروژه چیه؟
   → شامل کدوم modules؟
   → شامل کدوم documentation؟
   → شامل کدوم examples؟

3. تمام affected areas رو:
   → Code
   → Tests
   → Docs
   → Examples

4. Verify consistency:
   → README compatible؟
   → Examples working؟
   → All tests pass؟

5. Only then commit ✓
```

---

## ⚠️ Anti-Patterns (نکنم‌ها)

```
❌ Code change بدون test
❌ Feature بدون documentation
❌ Example بدون working code
❌ Bug fix بدون root cause analysis
❌ Docstring update بدون README update
❌ CHANGELOG forget کردن
❌ Code comment بدون English
❌ Variable name با اختصار غیر clear
❌ Copy-paste code (DRY violation)
❌ Guess کردن instead of asking
```

---

## 📊 Quality Metrics

هر commit/change باید:

```
✓ تمام tests pass (44/44 minimum)
✓ Type hints complete
✓ Docstrings complete
✓ No code duplication (DRY)
✓ Error handling comprehensive
✓ Documentation updated
✓ Examples working
✓ CHANGELOG updated
✓ Consistency check passed
✓ No breaking changes (unless major version)
```

---

## 🎉 Success Criteria

اینکه change "done" محسوب بشه:

1. ✅ **Functional**: Code کار می‌کنه correctness
2. ✅ **Tested**: Unit tests exist + pass
3. ✅ **Documented**: Docstrings + README + Examples
4. ✅ **Consistent**: تمام parts synchronized
5. ✅ **Clean**: Following all code principles
6. ✅ **Verified**: No regressions, all metrics pass

---

## 📝 Commit Checklist Template

هر commit قبل‌تر:

```markdown
## Commit: [Type] [Scope]: [Message]

### Changes
- [ ] Code implemented
- [ ] Type hints added
- [ ] Error handling
- [ ] Edge cases covered

### Testing
- [ ] Unit tests added/updated
- [ ] All tests pass (44/44)
- [ ] Manual testing done

### Documentation
- [ ] Docstrings updated
- [ ] README updated (if API change)
- [ ] Examples updated (if behavior change)
- [ ] CHANGELOG updated

### Quality
- [ ] Code follows PEP 8
- [ ] No code duplication
- [ ] Type hints complete
- [ ] Consistency verified

### Ready? → COMMIT ✓
```

---

**Version**: 2.0 (مع اضافات جدید)  
**Last Updated**: فقط‌الآن  
**Status**: تمام‌ترین تعریف قوانین
