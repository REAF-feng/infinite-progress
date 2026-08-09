# Day 17：random模块 + 列表初识——让程序有"随机性"

---

## 🎯 本节课学习目标

- 理解什么是"模块"（别人写好的现成工具）
- 用 `random` 模块生成随机数
- 初步认识列表（一组数据的容器，Day21会深入）

---

## 📖 知识点讲解

### 1. 什么是模块？

Python自带很多"工具箱"，每个工具箱里有很多现成的函数。**模块就是一个工具箱**。你用 `import` 命令把工具箱拿过来，就能用里面的工具了。

```python
import random          # 把random工具箱拿过来
random.randint(1,10)   # 用里面的"随机整数"工具
```

**生活类比：** 你要做饭，不需要自己造锅，去超市（import）买现成的锅（模块）就行了。

### 2. random常用功能

| 代码 | 功能 | 例子 |
|------|------|------|
| `random.randint(a, b)` | 生成a到b之间的随机整数（含a和b） | `random.randint(1,10)` |
| `random.random()` | 生成0到1之间的随机小数 | `0.3742...` |
| `random.choice(列表)` | 从列表中随机选一个 | `random.choice(["苹果","香蕉"])` |
| `random.shuffle(列表)` | 把列表顺序打乱 | 洗牌效果 |

### 3. 列表是什么？（预热）

列表是一对中括号 `[ ]`，里面可以放多个数据，用逗号分隔。就像一个"大篮子"，可以把很多东西装在一起。

```python
fruits = ["苹果", "香蕉", "橘子", "葡萄"]
numbers = [1, 2, 3, 4, 5]
```

---

## 💻 课堂演示代码

```python
import random

# ========== 随机整数 ==========

print("=== 随机整数 ===")
for i in range(5):
    num = random.randint(1, 100)     # 1~100的随机整数
    print(f"第{i+1}次：{num}")

# ========== 随机选择 ==========

print()
print("=== 随机点菜 ===")
menu = ["黄焖鸡", "麻辣烫", "兰州拉面", "沙县小吃", "肯德基"]
today = random.choice(menu)
print(f"今天吃：{today}")

# ========== 随机洗牌 ==========

print()
cards = ["A", "K", "Q", "J", "10"]
print("洗牌前：", cards)
random.shuffle(cards)
print("洗牌后：", cards)

# ========== 实战：猜数字游戏（完整版） ==========

print()
print("=" * 40)
print("    猜数字游戏（1~100）")
print("=" * 40)

answer = random.randint(1, 100)     # 电脑随机想一个数
guess_count = 0                      # 记录猜了几次

while True:
    try:
        guess = int(input("请猜一个数字（1~100）："))
        if guess < 1 or guess > 100:
            print("⚠️ 请输入1~100之间的数！")
            continue
    except ValueError:
        print("⚠️ 请输入整数！")
        continue

    guess_count = guess_count + 1

    if guess > answer:
        print("📈 猜大了，往小猜！")
    elif guess < answer:
        print("📉 猜小了，往大猜！")
    else:
        print(f"🎉 恭喜你猜对了！答案就是{answer}")
        print(f"你一共猜了{guess_count}次")
        # 评价
        if guess_count <= 5:
            print("评价：天才！")
        elif guess_count <= 10:
            print("评价：不错！")
        else:
            print("评价：还需练习！")
        break
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `import` | 导入别人写好的工具箱 |
| 2 | `random.randint(a,b)` | 生成a到b的随机整数 |
| 3 | `random.choice(列表)` | 从列表中随机挑一个 |
| 4 | `random.shuffle(列表)` | 把列表的顺序打乱 |
| 5 | 列表 `[ ]` | 中括号装多个数据，逗号分隔 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出以下代码的功能**
```python
import random
result = random.randint(1, 6)
```
这段代码模拟的是：____________

**题2：补全代码——随机抽奖**
```python
import ______
names = ["张三", "李四", "王五", "赵六"]
winner = random.______(names)
print(f"中奖者是：{______}")
```

---

### 【进阶实操题】

**题3：掷骰子模拟器**
模拟掷两个骰子，显示每个骰子的点数和总点数。让用户可以反复掷，输入q退出。

**题4：随机密码生成器**
生成一个8位随机密码，包含大写字母、小写字母和数字。提示：可以用 `random.choice()` 从字符列表中挑选。

---

### 【拓展思考题】

**题5：石头剪刀布**
实现一个石头剪刀布游戏，用户出拳，电脑随机出拳，判断输赢并显示结果。支持反复玩和统计胜率。

---

> 🎉 加上random，你的程序开始变得"不可预测"了！
