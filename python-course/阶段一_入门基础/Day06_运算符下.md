# Day 06：比较运算符和逻辑运算符

---

## 🎯 本节课学习目标

学完今天的内容，你能做到：
- 用比较运算符判断大小、相等
- 用逻辑运算符组合多个判断条件
- 让程序具备"判断对错"的能力

---

## 📖 知识点讲解

### 1. 比较运算符——"比大小"

就像生活中你总是在做判断："我的钱够不够买这个？""我比他高吗？"，程序也需要做判断。比较运算符就是用来"比大小"的，**比较的结果永远是 True 或 False**。

| 运算符 | 含义 | 例子 | 结果 |
|--------|------|------|------|
| `==` | 等于 | `5 == 5` | `True` |
| `!=` | 不等于 | `5 != 3` | `True` |
| `>` | 大于 | `10 > 5` | `True` |
| `<` | 小于 | `3 < 8` | `True` |
| `>=` | 大于等于 | `5 >= 5` | `True` |
| `<=` | 小于等于 | `4 <= 3` | `False` |

> ⚠️ **重点区分：`=` vs `==`**
> - `=` 是**赋值号**：把右边的东西装进左边变量（`age = 18`）
> - `==` 是**等于号**：判断左右两边是否相等（`age == 18` 问"age等于18吗？"）
> - 这是新手最容易搞混的地方！

### 2. 逻辑运算符——"组合判断"

现实生活中，判断往往不只有一个条件。比如"今天出门的条件是：不下雨**而且**温度高于15度"。Python用三个逻辑运算符来组合判断：

| 运算符 | 含义 | 说明 |
|--------|------|------|
| `and` | 并且（与） | 两个条件**都满足**，结果才是True |
| `or` | 或者（或） | 两个条件**只要有一个满足**，结果就是True |
| `not` | 取反（非） | True变False，False变True |

**生活类比：**
```
去游乐场玩的条件：
  身高 >= 120   and   年龄 >= 6     → 两个条件必须同时满足
  有会员卡      or    买全价票      → 满足一个就行
  not 下雨                         → 反过来，"不下雨"就是 not 下雨
```

---

## 💻 课堂演示代码

```python
# ========== 比较运算符 ==========

age = 18
print("age =", age)
print("age == 18 ?", age == 18)     # True，等于18吗？等于！
print("age != 18 ?", age != 18)     # False，不等于18吗？不，它等于
print("age > 16 ?", age > 16)       # True，大于16吗？大于！
print("age < 21 ?", age < 21)       # True，小于21吗？小于！
print("age >= 18 ?", age >= 18)     # True，大于等于18吗？等于！
print("age <= 17 ?", age <= 17)     # False，小于等于17吗？不，大于

# ========== 逻辑运算符 ==========

# and（并且）：两边都True才是True
print("True and True =", True and True)     # True
print("True and False =", True and False)   # False
print("False and False =", False and False) # False

# or（或者）：只要有一边True就是True
print("True or True =", True or True)       # True
print("True or False =", True or False)     # True
print("False or False =", False or False)   # False

# not（取反）：反着来
print("not True =", not True)               # False
print("not False =", not False)             # True

# ========== 实际应用场景 ==========

# 场景1：判断能否开车（年龄>=18 而且 有驾照）
user_age = 20
has_license = True
can_drive = user_age >= 18 and has_license
print("能开车吗？", can_drive)   # True

# 场景2：判断能否半价（学生 或者 老人）
is_student = False
age = 70
half_price = is_student or age >= 65
print("能半价吗？", half_price)   # True（因为是老人）

# 场景3：检查年龄是否在合理范围内（18到60岁之间）
age = 25
is_valid = age >= 18 and age <= 60
print("年龄在合理范围吗？", is_valid)  # True

# 场景4：判断用户名和密码是否都正确
username = "admin"
password = "123456"
input_user = input("请输入用户名：")
input_pwd = input("请输入密码：")
login_success = (input_user == username) and (input_pwd == password)
print("登录成功？", login_success)
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `==` 等于 | 两个等号是"判断相等"，一个等号是"赋值" |
| 2 | `!=` 不等于 | 感叹号+等号，问"不相等吗？" |
| 3 | `>` `<` `>=` `<=` | 数学里的大于小于号，一模一样 |
| 4 | `and` | 两边都True才True，"并且" |
| 5 | `or` | 有True就True，"或者" |
| 6 | `not` | 布尔值翻转，True↔False |
| 7 | 比较结果 | 永远是 `True` 或 `False` |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出结果**
```python
print(10 > 5)           # ______
print(3 == 3)           # ______
print(7 != 7)           # ______
print(5 >= 10)          # ______
```

**题2：写出逻辑运算结果**
```python
print(True and False)           # ______
print(True or False)            # ______
print(not True)                 # ______
print((5 > 3) and (8 < 10))     # ______
```

---

### 【进阶实操题】

**题3：年龄判断器**
让用户输入年龄，程序判断并显示：
- 是否成年（>=18）
- 是否是青少年（13到19岁）
- 是否是老年人（>=65）

**题4：简易登录系统**
预设用户名 `"python"` 和密码 `"123456"`，让用户输入用户名和密码，程序判断是否登录成功并显示结果。

---

### 【拓展思考题】

**题5：闰年判断器**
让用户输入一个年份，判断是否是闰年。
闰年规则：能被4整除但不能被100整除，或者能被400整除。
（比如2000年是闰年，1900年不是，2004年是闰年）

---

> 🎉 比较和逻辑运算是让程序"会思考"的基础！
