# Day 28：列表字典高级技巧——lambda、解包与推导式进阶

---

## 🎯 本节课学习目标

- 理解 `lambda` 匿名函数（为函数做准备）
- 掌握列表/字典的进阶推导式
- 学会 zip 和 enumerate 等实用函数

---

## 📖 知识点讲解

### 1. lambda —— 一次性小函数

`lambda` 是定义一个"只用一次的小函数"的简写方式。

```python
# 传统写法
def add(x):
    return x + 10

# lambda写法（一行搞定）
lambda x: x + 10
```

常用于 `sort()` 的 `key` 参数和 `max()`/`min()`：
```python
students.sort(key=lambda s: s["总分"])     # 按总分排序
max(students, key=lambda s: s["语文"])      # 找语文最高分
```

### 2. enumerate() —— 同时获得索引和值

```python
for index, value in enumerate(["a", "b", "c"]):
    print(index, value)
# 0 a
# 1 b
# 2 c
```

### 3. zip() —— 拉链函数

把多个列表"拉"在一起，一一配对：

```python
names = ["张三", "李四", "王五"]
ages = [20, 25, 30]
list(zip(names, ages))   # [("张三",20), ("李四",25), ("王五",30)]
```

---

## 💻 课堂演示代码

```python
# ========== lambda 排序 ==========

students = [
    {"name": "张三", "语文": 85, "数学": 92},
    {"name": "李四", "语文": 90, "数学": 88},
    {"name": "王五", "语文": 76, "数学": 95},
]

# 按语文成绩降序排序
students.sort(key=lambda s: s["语文"], reverse=True)
for s in students:
    print(f"{s['name']} 语文{s['语文']} 数学{s['数学']}")

# 找数学最高分
best_math = max(students, key=lambda s: s["数学"])
print(f"\n数学最高：{best_math['name']} ({best_math['数学']}分)")

# ========== enumerate 编号 ==========

fruits = ["苹果", "香蕉", "橘子", "葡萄"]
print("编号 水果")
for i, fruit in enumerate(fruits, start=1):   # 编号从1开始
    print(f" {i}. {fruit}")

# ========== zip 配对 ==========

names = ["张三", "李四", "王五"]
scores = [85, 92, 78]
cities = ["北京", "上海", "广州"]

for name, score, city in zip(names, scores, cities):
    print(f"{name}来自{city}，考了{score}分")

# 快速创建字典
name_score_dict = dict(zip(names, scores))
print("姓名→成绩字典：", name_score_dict)    # {"张三":85, "李四":92, "王五":78}

# ========== 字典推导式 ==========

# 把列表变成字典
words = ["apple", "banana", "cherry"]
len_dict = {word: len(word) for word in words}
print("单词→长度：", len_dict)               # {"apple":5, "banana":6, "cherry":6}

# 条件过滤
scores = {"张三": 85, "李四": 92, "王五": 78, "赵六": 55}
passed = {name: score for name, score in scores.items() if score >= 60}
print("及格的：", passed)                    # {"张三":85, "李四":92, "王五":78}

# 键值互换
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print("互换后：", swapped)                   # {1:"a", 2:"b", 3:"c"}

# ========== 列表解包（*） ==========

a, *b, c = [1, 2, 3, 4, 5]
print(f"a={a}, b={b}, c={c}")               # a=1, b=[2,3,4], c=5

first, *rest = "hello"
print(f"首字母={first}, 剩余={rest}")        # 首字母=h, 剩余=['e','l','l','o']

# 合并多个列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]                  # [1, 2, 3, 4, 5, 6]
print("合并：", combined)
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `lambda 参数: 表达式` | 一次性的小函数，常用于sort的key |
| 2 | `enumerate(列表, start)` | 遍历同时获得索引和值 |
| 3 | `zip(a, b, c)` | 多个列表一一配对 |
| 4 | 字典推导式 | `{k: v for k,v in 字典.items() if 条件}` |
| 5 | `a, *b, c = 列表` | 解包，`*`收集剩余元素 |
| 6 | `[*a, *b]` | 合并多个列表的简洁写法 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出运行结果**
```python
a = [1, 2, 3]
b = ["a", "b", "c"]
print(list(zip(a, b)))       # ______

nums = [5, 2, 8, 1]
nums.sort(key=lambda x: -x)  # ______（降序排列）
```

**题2：补全代码**
```python
# 用字典推导式把列表变成 {元素: 元素长度} 的字典
words = ["hello", "world", "python"]
result = {______: ______ for w in words}
```

---

### 【进阶实操题】

**题3：多维度排序**
有一组学生数据（列表套字典），先按班级排序，同一班级内按成绩降序。用lambda实现。

**题4：合并两个报表**
两个列表分别存储了学号和姓名、学号和成绩。用zip和字典把它们合并成完整的学号→姓名→成绩的数据结构。

---

### 【拓展思考题】

**题5：用列表推导式和zip实现矩阵转置**
有一个3×3的矩阵（嵌套列表），用一行代码实现转置（行列互换）。
```python
matrix = [[1,2,3], [4,5,6], [7,8,9]]
# 转置后：[[1,4,7], [2,5,8], [3,6,9]]
```

---

> 🎉 这些高级技巧能大幅提升你的代码简洁度！
