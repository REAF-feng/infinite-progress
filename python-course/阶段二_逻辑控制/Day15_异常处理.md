# Day 15：异常处理——程序不崩溃的秘诀

---

## 🎯 本节课学习目标

- 理解什么是"异常"（程序报错）
- 用 `try...except` 捕获错误，让程序不崩溃
- 处理常见的输入类型错误

---

## 📖 知识点讲解

### 1. 什么是异常？

你写程序时一定遇到过这种情况：运行得好好的，突然冒出一大堆红色英文，程序直接退出了——这就是"异常"（Exception），俗称"报错"。

**最常见的异常：** 用户让你输入数字，他偏要输入字母，程序就崩了。

```python
age = int(input("请输入年龄："))   # 用户输入"abc"
# 报错：ValueError: invalid literal for int() with base 10: 'abc'
```

### 2. try...except —— 给程序买保险

`try...except` 就像给代码买了保险。try里面的代码如果出错了，程序不会崩溃，而是跳到except里执行"备选方案"。

```python
try:
    # 尝试执行，可能有风险的代码
    可能出错的代码
except:
    # 如果出错，就执行这里的"备选方案"
    备选处理
```

**生活类比：** 你出门前看天气预报。try就是"尝试不带伞出门"，如果下雨了（异常），except就是"去便利店买把伞"（备用方案）。你不会因为下雨就原地崩溃。

---

## 💻 课堂演示代码

```python
# ========== 基础：捕获输入错误 ==========

print("=== 安全数字输入 ===")
while True:
    try:
        age = int(input("请输入年龄："))
        break                        # 转换成功，跳出循环
    except ValueError:               # 捕获"值错误"（输入不是数字）
        print("⚠️ 输入有误，请输入一个整数！")

print(f"你的年龄是：{age}")

# ========== 捕获多种异常 ==========

print()
print("=== 除法计算器（安全版）===")

try:
    a = float(input("被除数："))
    b = float(input("除数："))
    result = a / b
    print(f"结果：{result}")
except ValueError:
    print("⚠️ 请输入数字！")
except ZeroDivisionError:
    print("⚠️ 除数不能为0！")
except Exception as e:
    print(f"⚠️ 发生未知错误：{e}")

# ========== try...except...else...finally 完整结构 ==========

print()
print("=== 完整异常处理结构 ===")

try:
    num = int(input("请输入一个整数："))
    result = 100 / num
except ValueError:
    print("输入的不是整数！")
except ZeroDivisionError:
    print("不能输入0！")
else:
    # try里的代码没出错才执行这里
    print(f"100 ÷ {num} = {result}")
finally:
    # 不管出不出错，这里都会执行
    print("程序执行完毕。")

print()
print("即使上面出错了，这行话也能正常显示。")
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `try...except` | 尝试运行，出错就执行备用方案 |
| 2 | `ValueError` | 数据类型不对时的错误（比如字母转数字） |
| 3 | `ZeroDivisionError` | 除以0的错误 |
| 4 | `else`（在try中） | 不出错才执行 |
| 5 | `finally` | 不管出不出错都会执行 |
| 6 | 不要空except | 最好指定捕获哪种异常类型 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：常见的错误类型连线**
```
ValueError          →  除以0
ZeroDivisionError   →  变量没定义就使用
NameError           →  把字母转成数字
TypeError           →  字符串和数字相加
```

**题2：给下面的代码加上try...except保护**
```python
a = int(input("输入第一个数："))
b = int(input("输入第二个数："))
print(f"{a} ÷ {b} = {a / b}")
```

---

### 【进阶实操题】

**题3：万能数字输入器**
写一个函数式风格的循环，让用户反复输入直到输入的是合法数字。分别实现：输入整数版、输入正数版、输入1~100之间整数版。

**题4：健壮计算器升级**
改进Day10的计算器，所有用户输入的地方都加上try...except保护，确保输入非数字时程序不崩溃。

---

### 【拓展思考题】

**题5：文件读取保护（预习）**
尝试用 `open("不存在的文件.txt")` 打开一个不存在的文件，观察什么错误。然后用try...except捕获它。（提示：异常类型叫 `FileNotFoundError`）

---

> 🎉 会处理异常的程序才是真正"能用"的程序！
