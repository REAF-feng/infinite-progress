# Day 22：列表进阶——排序、查找、列表推导式

---

## 🎯 本节课学习目标

- 掌握列表的排序和反转
- 学会在列表中查找元素
- 认识列表推导式（简洁创建列表的技巧）

---

## 📖 知识点讲解

### 1. 排序

```python
列表.sort()                # 从小到大排序，直接修改原列表
列表.sort(reverse=True)    # 从大到小排序
sorted(列表)               # 返回一个新排序列表，原列表不变
```

### 2. 查找

```python
元素 in 列表               # 检查元素是否在列表中，返回True/False
列表.index(元素)           # 查找元素的索引位置，找不到会报错
列表.count(元素)           # 统计元素出现了几次
```

### 3. 列表推导式（⭐Python特色技能）

一种快速创建列表的简洁写法：

```python
# 传统写法
squares = []
for i in range(1, 11):
    squares.append(i ** 2)

# 列表推导式（一行搞定！）
squares = [i ** 2 for i in range(1, 11)]
# 结果：[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

---

## 💻 课堂演示代码

```python
# ========== 排序 ==========

nums = [5, 2, 8, 1, 9, 3]
print("原列表：", nums)

nums.sort()                         # 升序排序
print("升序：", nums)                # [1, 2, 3, 5, 8, 9]

nums.sort(reverse=True)             # 降序排序
print("降序：", nums)                # [9, 8, 5, 3, 2, 1]

# sorted()不改变原列表
original = [3, 1, 4, 1, 5]
new_list = sorted(original)
print("原列表不变：", original)      # [3, 1, 4, 1, 5]
print("新排序列表：", new_list)      # [1, 1, 3, 4, 5]

# ========== 反转 ==========

nums = [1, 2, 3, 4, 5]
nums.reverse()                      # 反转列表
print("反转后：", nums)              # [5, 4, 3, 2, 1]

# ========== 查找 ==========

fruits = ["苹果", "香蕉", "橘子", "香蕉", "葡萄"]

print("苹果在列表里吗？", "苹果" in fruits)        # True
print("西瓜在列表里吗？", "西瓜" in fruits)        # False
print("香蕉出现了几次？", fruits.count("香蕉"))    # 2
print("橘子的位置：", fruits.index("橘子"))        # 2

# ========== 列表推导式 ==========

# 生成1到10的平方
squares = [x ** 2 for x in range(1, 11)]
print("1~10的平方：", squares)

# 带条件过滤：只保留偶数
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [n for n in numbers if n % 2 == 0]
print("偶数：", evens)              # [2, 4, 6, 8, 10]

# 字符串处理
names = ["alice", "bob", "charlie"]
upper_names = [name.upper() for name in names]
print("大写：", upper_names)        # ["ALICE", "BOB", "CHARLIE"]

# ========== 其他常用操作 ==========

# max, min, sum
scores = [85, 92, 78, 66, 95]
print("最高分：", max(scores))       # 95
print("最低分：", min(scores))       # 66
print("总分：", sum(scores))         # 416

# 列表合并
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b                           # 合并
print("合并：", c)                   # [1, 2, 3, 4, 5, 6]

# 列表复制（注意！）
original = [1, 2, 3]
# copied = original    # ❌ 这样不是复制，是指向同一个列表！
copied = original.copy()  # ✅ 这才是真正的复制
copied[0] = 999
print("原列表：", original)          # [1, 2, 3]  没被影响！
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `.sort()` | 直接对原列表排序，`reverse=True`降序 |
| 2 | `sorted()` | 返回新列表，原列表不变 |
| 3 | `in` | 检查元素是否在列表中 |
| 4 | `.index()` | 查位置，找不到会报错 |
| 5 | 列表推导式 | `[表达式 for 变量 in 序列 if 条件]` |
| 6 | `max()` `min()` `sum()` | 最大值、最小值、求和 |
| 7 | `.copy()` | 真正复制，`=`只是贴标签 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出运行结果**
```python
nums = [3, 1, 4, 1, 5, 9, 2]
print(max(nums))          # ______
print(nums.count(1))      # ______
print(7 in nums)          # ______
```

**题2：补全列表推导式——生成1~20中所有奇数的平方**
```python
result = [______ for x in range(1, 21) ______ x % 2 == 1]
```

---

### 【进阶实操题】

**题3：成绩排名系统**
让用户输入5个学生的姓名和成绩，用两个列表分别存储。然后按成绩从高到低排序显示排名。提示：需要同时排序姓名和成绩，保持对应关系。

**题4：购物清单价格统计**
用一个列表存储商品名，另一个列表存储对应价格。写程序：显示所有商品、计算总价、找到最贵和最便宜的商品。

---

### 【拓展思考题】

**题5：用列表推导式生成素数列表**
用一行列表推导式（可以嵌套if）生成2~100之间的所有质数。提示：`all()` 函数可以判断一个序列是否全为True。

---

> 🎉 排序和推导式是你Python进阶的必备技能！
