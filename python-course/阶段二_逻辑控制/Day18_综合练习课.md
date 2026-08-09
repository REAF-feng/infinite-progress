# Day 18：阶段二综合练习课——用逻辑解决实际问题

---

## 🎯 本节课学习目标

- 综合运用if、while、for、break、continue解决实际问题
- 锻炼"把问题翻译成代码"的思维
- 为阶段二测评做准备

---

## 📖 今日是练习课

前17天学了很多知识，今天不做新知识讲解，而是通过**6道经典练习**帮你巩固。建议每题先自己思考5分钟，再看参考答案。

---

## 💻 练习题目

### 练习1：数字猜谜（综合while + if + break）

**需求：** 电脑随机生成1~100的数字，用户有**最多7次**猜测机会。每次猜完提示"大了/小了/猜对了"，7次用完还没猜对就显示正确答案。

```python
import random

answer = random.randint(1, 100)
max_chances = 7

print(f"猜数字游戏！你有{max_chances}次机会。")

for chance in range(1, max_chances + 1):
    guess = int(input(f"第{chance}次，请猜："))
    
    if guess == answer:
        print(f"🎉 猜对了！用了{chance}次")
        break     # 猜对了，结束游戏
    elif guess > answer:
        print("大了")
    else:
        print("小了")
else:
    # 这个else属于for，只有没用break（即没猜对）时才执行
    print(f"😢 机会用完！答案是{answer}")
```

---

### 练习2：成绩统计器（综合for + if + continue）

**需求：** 用户输入5个学生成绩，统计：平均分、最高分、最低分、及格人数。

```python
total = 0
max_score = 0
min_score = 100
pass_count = 0

for i in range(1, 6):
    score = float(input(f"请输入第{i}个学生的成绩："))
    
    total = total + score
    
    if score > max_score:
        max_score = score
    if score < min_score:
        min_score = score
    
    if score >= 60:
        pass_count = pass_count + 1

avg = total / 5
print(f"\n===== 成绩统计 =====")
print(f"平均分：{avg:.1f}")
print(f"最高分：{max_score}")
print(f"最低分：{min_score}")
print(f"及格人数：{pass_count}/5")
```

---

### 练习3：数字金字塔（嵌套for循环）

**需求：** 打印如下数字金字塔
```
   1
  121
 12321
1234321
```

```python
n = 4   # 总行数
for i in range(1, n + 1):
    # 先打印空格
    for space in range(n - i):
        print(" ", end="")
    # 打印左半边递增
    for j in range(1, i + 1):
        print(j, end="")
    # 打印右半边递减
    for j in range(i - 1, 0, -1):
        print(j, end="")
    print()
```

---

### 练习4：FizzBuzz经典问题

**需求：** 打印1~100，遇到3的倍数打印"Fizz"，5的倍数打印"Buzz"，同时是3和5的倍数打印"FizzBuzz"。

```python
for num in range(1, 101):
    if num % 3 == 0 and num % 5 == 0:
        print("FizzBuzz", end=" ")
    elif num % 3 == 0:
        print("Fizz", end=" ")
    elif num % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(num, end=" ")
```

---

### 练习5：最大公约数

**需求：** 输入两个正整数，求它们的最大公约数（辗转相除法）。

```python
a = int(input("输入第一个数："))
b = int(input("输入第二个数："))

# 欧几里得算法（辗转相除法）
while b != 0:
    remainder = a % b       # 求余数
    a = b                   # 把b变成新的a
    b = remainder           # 把余数变成新的b
    # 循环到余数为0，此时a就是最大公约数

print(f"最大公约数是：{a}")
```

---

### 练习6：简单加密解密

**需求：** 把用户输入的字符串每个字符向后移动3位（凯撒密码）。只处理字母。

```python
text = input("请输入要加密的文字：")
result = ""

for ch in text:
    if ch.isalpha():              # 如果是字母
        code = ord(ch) + 3        # ord()得到字符的编码数字
        new_ch = chr(code)        # chr()把数字变回字符
        result = result + new_ch
    else:
        result = result + ch      # 非字母原样保留

print(f"加密结果：{result}")
```

---

## ✅ 今日课后任务

1. 手打以上6个练习的代码，理解每一行
2. 尝试修改参数，观察不同效果
3. 选一道题，不看书自己默写出来
4. 去完成[阶段二测评卷](../阶段测评/阶段二测评卷.md)

---

> 🎉 恭喜完成阶段二全部内容！休息一下，迎接阶段三的挑战！
