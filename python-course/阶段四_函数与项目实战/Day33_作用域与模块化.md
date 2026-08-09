# Day 33：作用域与模块化——代码的"可见范围"

---

## 🎯 本节课学习目标

- 理解变量的"作用域"（在哪能访问、在哪不能）
- 区分全局变量和局部变量
- 学会把代码拆分成多个文件

---

## 📖 知识点讲解

### 1. 什么是作用域？

**作用域**就是一个变量"在哪能被看到"的范围。就像你在自己房间里说话，客厅的人不一定能听到。

```python
def my_func():
    x = 10        # x 只在my_func内部可见
    print(x)      # ✅ 能访问

my_func()
print(x)          # ❌ 报错！x 在函数外面"看不到"
```

### 2. 全局变量 vs 局部变量

| 类型 | 定义位置 | 可见范围 |
|------|----------|----------|
| 局部变量 | 函数内部 | 只在函数内部 |
| 全局变量 | 函数外部（文件顶层） | 整个文件都能读 |

```python
name = "小明"        # 全局变量

def say_hello():
    print(name)      # ✅ 可以读取全局变量

def change_name():
    global name      # 声明要修改全局变量
    name = "小红"     # 现在才能修改全局变量
```

### 3. 模块化——把代码拆分到多个文件

当一个文件太长，可以拆成多个文件：

```
项目/
├── main.py          # 主程序
├── utils.py         # 工具函数
└── models.py        # 数据模型
```

在 `main.py` 中这样引入：
```python
import utils          # 导入整个文件
from utils import add # 只导入某个函数
```

---

## 💻 课堂演示代码

```python
# ========== 局部变量 ==========

def calculate(x):
    y = x * 2       # y是局部变量
    print(f"函数内：x={x}, y={y}")
    return y

result = calculate(5)
# print(y)          # ❌ 报错！y在函数内定义的，外面看不到

# ========== 全局变量 ==========

APP_NAME = "我的记账本"      # 全局常量（约定全大写）
total_count = 0             # 全局变量

def increment():
    global total_count       # 声明要修改全局变量
    total_count = total_count + 1
    print(f"第{total_count}次调用")

increment()    # 第1次调用
increment()    # 第2次调用
increment()    # 第3次调用

def show_status():
    # 只读取全局变量不需要global声明
    print(f"程序：{APP_NAME}，已调用{total_count}次")

show_status()

# ========== 函数内函数（嵌套作用域）==========

def outer(x):
    y = x * 2                # y属于outer
    
    def inner(z):
        return y + z         # inner可以访问outer的y！
    
    return inner(10)         # 调用inner

print(outer(5))              # 5*2 + 10 = 20

# ========== 模块化示例 ==========

# 假设这是 utils.py 的内容（另一个文件）
"""
# utils.py
def is_even(n):
    return n % 2 == 0

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
"""

# 在主文件中导入使用
# import utils
# print(utils.is_even(10))     # True
# print(utils.is_prime(17))    # True

# 只导入需要的函数
# from utils import is_even, is_prime
# print(is_even(10))
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | 局部变量 | 函数内定义的变量，外面看不到 |
| 2 | 全局变量 | 文件顶层定义的变量，整个文件都可读 |
| 3 | `global` | 函数内修改全局变量前必须声明 |
| 4 | 嵌套作用域 | 内层函数可以访问外层函数的变量 |
| 5 | `import` | 把其他文件的功能引进来 |
| 6 | `from...import` | 只引入需要的部分 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：指出代码中的错误**
```python
count = 0
def add():
    count = count + 1    # 这行有什么问题？怎么修改？
```

**题2：写出运行结果**
```python
x = 10
def test():
    x = 5
    print(x)
test()
print(x)
```

---

### 【进阶实操题】

**题3：创建工具函数库**
新建一个 `mymath.py` 文件，里面写几个数学函数：`factorial(n)` 阶乘、`is_prime(n)` 判断质数、`gcd(a,b)` 最大公约数。然后在另一个文件中导入并使用。

**题4：计数器程序**
写一个程序，用全局变量记录用户的操作次数。提供几个函数：`do_something()`（计数+1）、`reset_count()`（归零）、`get_count()`（查看）。测试不同的调用顺序。

---

### 【拓展思考题】

**题5：自制简易日志系统**
用全局变量+函数做一个简易日志系统。`log(message)` 把消息追加到全局列表里，`show_logs()` 显示所有日志，`save_logs(filename)` 把日志写入文件，`clear_logs()` 清空日志。

---

> 🎉 理解作用域是写出无bug代码的关键！
