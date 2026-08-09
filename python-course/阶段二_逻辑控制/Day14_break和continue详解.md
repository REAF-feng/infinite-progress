# Day 14：break和continue——精准控制循环

---

## 🎯 本节课学习目标

- 彻底搞懂break（跳出）和continue（跳过）的区别
- 学会在for和while中使用它们
- 理解`for...else`的特殊用法

---

## 📖 知识点讲解

### 1. break 和 continue 的区别

**生活类比：吃一串葡萄🍇**

- **break**：吃到一颗坏的，整串葡萄不吃了，直接扔掉走人（**整个循环结束**）
- **continue**：吃到一颗坏的，吐掉这颗，继续吃下一颗（**跳过本轮，循环继续**）

```
循环: 第1颗 → 第2颗 → 第3颗(坏) → 第4颗 → 第5颗

用continue:  吃1, 吃2, 吐3, 吃4, 吃5   ← 跳过坏的继续吃
用break:    吃1, 吃2, 碰到坏的, 不吃了  ← 直接结束
```

### 2. for...else —— 循环的彩蛋

Python有个特殊语法：`for...else`。**当循环正常结束（没被break打断）时，会执行else里的代码。** 如果被break打断了，else不执行。

```python
for item in 序列:
    if 条件:
        break        # 被打断，else不执行
else:
    正常结束才执行    # 没break才走到这里
```

这常用于"查找"场景：找到了就break，一直没找到就执行else。

---

## 💻 课堂演示代码

```python
# ========== break：找到就退出 ==========

print("=== break示例：找第一个能被7整除的数 ===")
for num in range(30, 50):
    if num % 7 == 0:
        print(f"找到了！{num} 能被7整除")
        break                    # 找到一个就不找了
    print(f"{num} 不能被7整除，继续找...")

# ========== continue：跳过不合条件的 ==========

print()
print("=== continue示例：只打印奇数 ===")
for num in range(1, 11):
    if num % 2 == 0:            # 偶数
        continue                 # 跳过偶数，不打印
    print(num, end=" ")          # 只打印奇数
print()

# ========== for...else：查找失败时执行 ==========

print()
print("=== 查找质数（只能被1和自己整除的数）===")

# 判断29是不是质数
n = 29
for i in range(2, n):          # 从2到n-1
    if n % i == 0:
        print(f"{n} 不是质数，能被{i}整除")
        break                    # 找到因数，不是质数
else:
    print(f"{n} 是质数")         # 没找到任何因数，是质数

# ========== 综合实战：过滤名单 ==========

print()
print("=== 成绩筛选 ===")
scores = [85, 42, 91, 67, 55, 78, 33, 95]

# 任务1：找到第一个不及格的分数
print("查找第一个不及格分数：")
for s in scores:
    if s < 60:
        print(f"第一个不及格：{s}")
        break

# 任务2：只显示及格的分数
print("所有及格分数：", end=" ")
for s in scores:
    if s < 60:
        continue                 # 不及格就跳过
    print(s, end=" ")
print()

# ========== while中的break和continue ==========

print()
count = 0
while count < 10:
    count = count + 1
    if count == 3:
        continue                 # 跳过3
    if count == 8:
        break                    # 到8就停
    print(count, end=" ")
# 输出：1 2 4 5 6 7
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `break` | 直接结束整个循环，后面的都不跑了 |
| 2 | `continue` | 跳过本轮，继续下一轮 |
| 3 | `for...else` | 循环正常跑完才执行else，被break打断就不执行 |
| 4 | break只能跳出一层 | 嵌套循环中，break只跳出它所在的最内层 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出运行结果**
```python
for i in range(1, 6):
    if i == 3:
        continue
    if i == 5:
        break
    print(i)
```

**题2：补全——查找列表中第一个大于100的数**
```python
numbers = [45, 78, 120, 56, 200, 88]
for num in numbers:
    if num ______ 100:
        print(f"找到了：{num}")
        ______
```

---

### 【进阶实操题】

**题3：质数判断器**
让用户输入一个正整数，判断它是不是质数。用for...else来实现。

**题4：筛选健康数据**
有一组体检数据：`[120, 85, 150, 78, 200, 95, 130, 88]`（收缩压mmHg），正常范围是90~140。写程序：
- 列出所有正常的血压值
- 找到第一个高血压（>140）的值
- 统计正常和异常各有多少个

---

### 【拓展思考题】

**题5：找出100以内的所有质数**
用嵌套循环 + break + for...else，找出1到100之间的所有质数。

---

> 🎉 break和continue让你的循环操控力提升一个档次！
