# Day 34：函数进阶技巧——装饰器与递归入门

---

## 🎯 本节课学习目标

- 理解递归思想（函数调用自己）
- 认识装饰器的基本概念（⭐拓展）
- 写几个经典的递归问题

---

## 📖 知识点讲解

### 1. 递归——函数调用自己

**生活类比：** 俄罗斯套娃。打开一个娃娃，里面还有一个娃娃，再打开里面又有一个……直到最小的那个打不开为止。

```python
def countdown(n):
    if n <= 0:          # 终止条件（最重要！没有就会死循环）
        print("发射！")
        return
    print(n)
    countdown(n - 1)    # 自己调用自己

countdown(5)
# 输出：5 4 3 2 1 发射！
```

**递归三要素：**
1. **终止条件**（什么时候停下来）—— 最重要！
2. **递推关系**（每次怎么变小）
3. **调用自身**

### 2. 递归经典例子

```python
# 阶乘：5! = 5×4×3×2×1
def factorial(n):
    if n <= 1:           # 终止条件
        return 1
    return n * factorial(n - 1)   # n! = n × (n-1)!

# 斐波那契数列：1,1,2,3,5,8,13,...
def fibonacci(n):
    if n <= 2:           # 终止条件
        return 1
    return fibonacci(n-1) + fibonacci(n-2)
```

### 3. 装饰器入门（⭐拓展选学）

装饰器是一个函数，它能"包裹"另一个函数，在不修改原函数的情况下增加额外功能。就像给手机加个保护壳，手机功能不变，但多了保护。

```python
# 一个极简装饰器
def my_decorator(func):
    def wrapper():
        print("===== 开始 =====")
        func()
        print("===== 结束 =====")
    return wrapper

@my_decorator            # 用@符号使用装饰器
def say_hello():
    print("你好世界！")

say_hello()
# 输出：
# ===== 开始 =====
# 你好世界！
# ===== 结束 =====
```

---

## 💻 课堂演示代码

```python
# ========== 递归：阶乘 ==========

def factorial(n):
    """计算n的阶乘 n! = n × (n-1) × ... × 1"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

for i in range(1, 8):
    print(f"{i}! = {factorial(i)}")

# ========== 递归：反转字符串 ==========

def reverse_string(s):
    """递归反转字符串"""
    if len(s) <= 1:        # 空串或单字符，直接返回
        return s
    return reverse_string(s[1:]) + s[0]   # 把第一个字符放最后

print(reverse_string("hello"))   # olleh

# ========== 递归：汉诺塔问题 ==========

def hanoi(n, source, target, auxiliary):
    """
    n个盘子从source柱移到target柱，借助auxiliary柱
    规则：每次只能移一个，大的不能压小的
    """
    if n == 1:
        print(f"把盘子从{source}移到{target}")
        return
    hanoi(n - 1, source, auxiliary, target)   # 先把n-1个移到辅助柱
    print(f"把盘子从{source}移到{target}")     # 移动最大的
    hanoi(n - 1, auxiliary, target, source)   # 再把n-1个移到目标柱

print("=== 汉诺塔（3个盘子）===")
hanoi(3, "A", "C", "B")

# ========== 递归 vs 循环 ==========

# 用循环求1+2+...+n
def sum_loop(n):
    total = 0
    for i in range(1, n+1):
        total += i
    return total

# 用递归求1+2+...+n
def sum_recursive(n):
    if n <= 1:
        return 1
    return n + sum_recursive(n - 1)

print(f"循环法：{sum_loop(100)}")
print(f"递归法：{sum_recursive(100)}")
# 结果一样，但递归更直观！不过递归太深会报错。

# ========== 装饰器示例：计时器 ==========
import time

def timer(func):
    """计算函数运行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱ {func.__name__} 运行了 {end-start:.4f} 秒")
        return result
    return wrapper

@timer
def slow_function():
    total = 0
    for i in range(10000000):
        total += i
    return total

# result = slow_function()
# 输出：⏱ slow_function 运行了 0.5234 秒
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | 递归 | 函数自己调用自己，必须有终止条件 |
| 2 | 终止条件 | 递归最重要的一步，否则死循环 |
| 3 | 递推关系 | 大问题拆成小问题，如 n! = n×(n-1)! |
| 4 | 递归风险 | 层级太深会超过递归限制（默认约1000层） |
| 5 | 装饰器 `@` | 不修改原函数的情况下增加功能（选学） |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出运行结果**
```python
def mystery(n):
    if n == 0:
        return 0
    return n + mystery(n - 2)

print(mystery(6))    # ______
```

**题2：补全递归函数——计算x的n次方**
```python
def power(x, n):
    if n == 0:
        return ______     # 任何数的0次方=1
    return x * power(______, ______)
```

---

### 【进阶实操题】

**题3：递归计算最大公约数**
用递归实现辗转相除法求最大公约数：`gcd(a,b) = gcd(b, a%b)`，当b=0时返回a。

**题4：递归列出目录结构**
给定一个嵌套列表模拟目录结构（如 `["dir1", ["file1", "file2"], "file3"]`），用递归函数打印出缩进的目录树结构。

---

### 【拓展思考题】

**题5：用递归解决"八皇后"简化版**
在一个4×4棋盘上放4个皇后，要求它们不互相攻击（不在同一行、同一列、同一斜线）。用递归+回溯法找出一种解法。提示：用列表存储每行皇后的列位置。

---

> 🎉 递归是编程思维的一次跃升，初学有点难但值得攻克！
