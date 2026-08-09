# Day 31：函数基础——把代码"打包"起来

---

## 🎯 本节课学习目标

- 理解为什么需要函数
- 学会定义函数和调用函数
- 把重复代码改造成函数

---

## 📖 知识点讲解

### 1. 为什么需要函数？

回想你写过的程序，是不是经常有重复的代码？比如每次都要写一遍输入验证。**函数就是把一段代码"打包"起来，给它起个名字，以后需要的时候直接叫它的名字就行了。**

**生活类比：**
- 你妈妈教你"炒鸡蛋"的做法（定义函数）
- 把做法写在小本子上
- 以后你想吃，翻开本子照着做就行（调用函数）
- 不用每次都重新想一遍怎么做

### 2. 函数的定义和调用

```python
# 定义函数（"打包"代码）
def 函数名():
    要打包的代码1
    要打包的代码2
    ...

# 调用函数（"使用"打包好的代码）
函数名()
```

### 3. 函数的基本结构

```python
def greet():               # def是define的缩写，意思是"定义"
    print("你好！")         # 这行属于函数，要缩进
    print("欢迎学习Python！")  # 这行也属于函数
```

---

## 💻 课堂演示代码

```python
# ========== 最简单的函数 ==========

def say_hello():
    """这是一个简单的打招呼函数"""    # 这是函数的说明文档
    print("=" * 20)
    print("你好，欢迎来到Python世界！")
    print("=" * 20)

# 调用函数（可以多次调用！）
say_hello()
print()                 # 空行
say_hello()             # 再调用一次
print()
say_hello()             # 想调多少次都行

# ========== 带参数的函数 ==========

def greet_person(name):
    """向指定的人打招呼"""
    print(f"你好，{name}！今天过得怎么样？")

greet_person("小明")      # 输出：你好，小明！今天过得怎么样？
greet_person("小红")      # 输出：你好，小红！今天过得怎么样？
greet_person("老师")      # 输出：你好，老师！今天过得怎么样？

# ========== 带返回值的函数 ==========

def add(a, b):
    """计算两个数的和并返回结果"""
    result = a + b
    return result        # return：把结果"送出去"

sum1 = add(3, 5)         # sum1 = 8
sum2 = add(10, 20)       # sum2 = 30
print(f"3+5={sum1}, 10+20={sum2}")

# 可以直接用返回值
print(f"100+200={add(100, 200)}")

# ========== 把常见操作封装成函数 ==========

def get_positive_number(prompt):
    """让用户输入一个正数，不合法就一直重来"""
    while True:
        try:
            num = float(input(prompt))
            if num > 0:
                return num     # 返回合法值并结束函数
            print("⚠️ 请输入正数！")
        except ValueError:
            print("⚠️ 请输入数字！")

# 现在可以很方便地获取多个输入了
# weight = get_positive_number("请输入体重(kg)：")
# height = get_positive_number("请输入身高(m)：")
# print(f"BMI = {weight / height**2:.1f}")

# ========== 函数间调用 ==========

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "偏瘦"
    elif bmi < 24:
        return "正常"
    elif bmi < 28:
        return "偏胖"
    else:
        return "肥胖"

def bmi_checker():
    """完整的BMI检测流程"""
    print("=== BMI计算器 ===")
    w = get_positive_number("体重(kg)：")
    h = get_positive_number("身高(m)：")
    bmi = calculate_bmi(w, h)
    category = get_bmi_category(bmi)
    print(f"你的BMI是：{bmi:.1f}，属于【{category}】")

# 试试运行完整流程
# bmi_checker()
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `def 函数名():` | 定义函数，给一段代码起名字 |
| 2 | 调用 `函数名()` | 使用已经定义好的函数 |
| 3 | 参数 | 括号里的变量，把数据传给函数 |
| 4 | `return` | 把计算结果送回给调用者 |
| 5 | 为什么要用函数 | 避免重复代码，一处修改处处生效 |
| 6 | 函数命名 | 用动词短语：`get_name`、`calculate_total` |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：填空——定义一个计算平方的函数**
```python
def square(num):
    ______ num * num      # 返回平方结果

result = square(5)        # result = ______
```

**题2：找出代码错误**
```python
def hello()
    print("你好")
```

**题3：写出运行结果**
```python
def double(x):
    return x * 2

print(double(3))          # ______
print(double(double(2)))  # ______
```

---

### 【进阶实操题】

**题4：把之前的代码改造成函数**
从Day10的计算器中，把加减乘除分别包装成4个函数，然后在主程序中调用它们。

**题5：温度转换函数包**
写三个函数：`c_to_f(摄氏)` 摄氏转华氏、`f_to_c(华氏)` 华氏转摄氏、`show_menu()` 显示转换菜单让用户选择方向。

---

### 【拓展思考题】

**题6：编写一个"判断质数"的函数**
函数接收一个整数参数，如果是质数返回`True`，不是返回`False`。然后用这个函数找出1~100中的所有质数。

---

> 🎉 函数是编程里最重要的抽象工具，写函数是写"好代码"的开始！
