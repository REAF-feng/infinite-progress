# Day 11：条件判断进阶——嵌套与多条件组合

---

## 🎯 本节课学习目标

- 掌握if嵌套（if里面写if）的写法
- 理解多条件组合判断的技巧
- 写出复杂判断逻辑的程序

---

## 📖 知识点讲解

### 1. 什么是嵌套if？

**生活场景：** 去电影院看电影，要经过两道检查：
- 第一道：有票吗？→ 没票就去买票
- 第二道：有票了，几点的场次？→ 根据时间进不同的厅

这就是"嵌套"——**一个判断的结果会影响下一个判断**。

```python
if 外层条件:
    # 外层通过了，再判断内层
    if 内层条件:
        做事情A
    else:
        做事情B
else:
    # 外层没通过，根本不看内层
    做事情C
```

### 2. 嵌套 vs 多条件并列

什么时候用嵌套，什么时候用and连接？

```python
# 方式一：用 and 连接（两个条件地位平等时用）
if age >= 18 and has_ticket:
    print("可以进入")

# 方式二：嵌套（内层依赖外层结果时用）
if age >= 18:
    if has_ticket:
        print("可以进入")
    else:
        print("成年了但没票，请先买票")
else:
    print("未成年不能单独进入")
```

**选择原则：** 当你需要在外层条件不满足时给出不同的提示，就用嵌套。

---

## 💻 课堂演示代码

```python
# ========== 嵌套if示例：考试评级系统 ==========

score = int(input("请输入你的考试成绩（0~100）："))

if score >= 0 and score <= 100:          # 先判断分数是否合法
    # 分数合法，进入详细评级
    if score >= 90:
        grade = "A"
        comment = "太棒了！继续保持！"
    elif score >= 80:
        grade = "B"
        comment = "不错，再努力一点就能拿A了！"
    elif score >= 70:
        grade = "C"
        comment = "还需努力，找找薄弱环节。"
    elif score >= 60:
        grade = "D"
        comment = "刚刚及格，要加把劲了。"
    else:
        grade = "E"
        comment = "不及格，建议找老师辅导。"
    
    print(f"你的等级是：{grade}")
    print(f"评语：{comment}")
else:
    # 分数不合法
    print("⚠️ 请输入0到100之间的分数！")

# ========== 复杂条件：会员折扣计算 ==========

print()
print("=== 商场折扣计算 ===")
is_member = input("您是会员吗？（是/否）：") == "是"
amount = float(input("请输入消费金额："))

if is_member:
    # 会员的折扣规则更复杂
    if amount >= 1000:
        discount = 0.7      # 7折
    elif amount >= 500:
        discount = 0.8      # 8折
    elif amount >= 200:
        discount = 0.9      # 9折
    else:
        discount = 0.95     # 9.5折
else:
    # 非会员折扣简单
    if amount >= 1000:
        discount = 0.9
    elif amount >= 500:
        discount = 0.95
    else:
        discount = 1.0      # 没折扣

final_price = amount * discount
saved = amount - final_price
print(f"原价：{amount}元")
print(f"折扣：{discount*10}折")
print(f"实付：{final_price:.2f}元")
print(f"省了：{saved:.2f}元")
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | 嵌套if | if里面写if，先过外层再过内层 |
| 2 | and连接 vs 嵌套 | 需要不同错误提示时用嵌套 |
| 3 | 输入验证 | 先判断输入是否合法，再做处理 |
| 4 | 缩进对齐 | 同一层if的代码缩进必须对齐 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出运行结果**
```python
x = 10
if x > 5:
    if x > 8:
        print("A")
    else:
        print("B")
else:
    print("C")
```

**题2：补全代码——判断三角形类型**
```python
a = 5
b = 5
c = 8
if a + b > c and a + c > b and b + c > a:
    # 是三角形，进一步判断类型
    if a == b ______ b == c:
        print("等边三角形")
    elif a == b ______ b == c ______ a == c:
        print("等腰三角形")
    else:
        print("普通三角形")
else:
    print("不能构成三角形")
```

---

### 【进阶实操题】

**题3：智能门禁系统**
写一个门禁判断程序，规则如下：
- 先判断是否是本楼住户（是→直接通过）
- 如果不是住户，判断是否有访客码（有→通过，无→拒绝）
- 如果是住户且年龄>70岁，额外提醒"注意安全"

**题4：网约车计价器**
写一个网约车计价程序，规则：
- 起步价8元（3公里以内）
- 超过3公里，每公里1.5元
- 超过15公里，超出部分每公里加收0.8元远途费
- 等待时间每5分钟折算为1公里
让用户输入里程和等待时间，计算总费用。

---

> 🎉 嵌套判断让你的程序能处理更复杂的现实场景！
