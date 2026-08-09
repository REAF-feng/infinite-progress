# Day 32：函数参数详解——灵活的数据传递

---

## 🎯 本节课学习目标

- 理解形参和实参的区别
- 掌握默认参数、关键字参数
- 学会用 `*args` 和 `**kwargs` 处理不定数量的参数

---

## 📖 知识点讲解

### 1. 形参 vs 实参

```python
def greet(name):       # name 是形参（形式上的参数，占位用的）
    print(f"你好{name}")

greet("小明")          # "小明" 是实参（实际传进去的值）
```

**记忆：** 形参是定义时写在括号里的"占位符"，实参是调用时传进去的"真实值"。

### 2. 默认参数

给参数设置默认值，调用时如果不传就用默认值：

```python
def greet(name="同学"):    # 默认值是"同学"
    print(f"你好，{name}")

greet()               # 没传参，用默认值 → 你好，同学
greet("小明")         # 传了参，用传的 → 你好，小明
```

### 3. 关键字参数

调用函数时写出参数名，可以不按顺序传递：

```python
def introduce(name, age, city):
    print(f"{name}，{age}岁，来自{city}")

introduce(age=18, city="北京", name="小明")   # 顺序随便，指定名字就行
```

### 4. `*args` 和 `**kwargs`

- `*args`：接收任意数量的**位置参数**，打包成一个**元组**
- `**kwargs`：接收任意数量的**关键字参数**，打包成一个**字典**

```python
def func(*args):       # 能收0个、1个、100个参数
    print(args)

func(1, 2, 3)          # 输出：(1, 2, 3)

def func(**kwargs):    # 能收任意键值对
    print(kwargs)

func(name="小明", age=18)  # 输出：{'name':'小明', 'age':18}
```

---

## 💻 课堂演示代码

```python
# ========== 默认参数 ==========

def make_tea(tea_type="绿茶", sugar=True):
    """泡茶函数"""
    sweet = "加糖" if sugar else "不加糖"
    print(f"一杯{tea_type}，{sweet}")

make_tea()                          # 全用默认 → 一杯绿茶，加糖
make_tea("红茶")                    # 改茶种 → 一杯红茶，加糖
make_tea("乌龙茶", False)           # 两个都改 → 一杯乌龙茶，不加糖
make_tea(sugar=False)               # 只改糖 → 一杯绿茶，不加糖

# ========== 关键字参数 ==========

def book_ticket(from_city, to_city, date, seat="经济舱"):
    print(f"{date} {from_city}→{to_city} {seat}")

# 下面三种调用方式完全等价
book_ticket("北京", "上海", "2026-02-01")
book_ticket(from_city="北京", to_city="上海", date="2026-02-01")
book_ticket(date="2026-02-01", seat="商务舱", to_city="上海", from_city="北京")

# ========== *args 任意数量参数 ==========

def calculate_sum(*numbers):
    """可以计算任意个数的和"""
    total = sum(numbers)
    print(f"{' + '.join(str(n) for n in numbers)} = {total}")

calculate_sum(1, 2)              # 1 + 2 = 3
calculate_sum(1, 2, 3, 4, 5)    # 1 + 2 + 3 + 4 + 5 = 15
calculate_sum(100)               # 100 = 100

def get_best_student(class_name, *scores):
    """计算一个班级的最高分"""
    print(f"{class_name}班最高分：{max(scores)}分")

get_best_student("一班", 85, 92, 78, 95, 88)

# ========== **kwargs 任意关键字参数 ==========

def build_profile(**info):
    """构建个人资料，可以传任意信息"""
    print("个人资料卡：")
    print("-" * 20)
    for key, value in info.items():
        print(f"  {key}：{value}")

build_profile(name="小明", age=18, city="北京", hobby="编程")
# 可以传完全不同的字段！
build_profile(姓名="张三", 职位="工程师", 工龄=5, 部门="技术部")

# ========== 综合：灵活的函数 ==========

def create_report(title, *items, **options):
    """生成报告：标题 + 任意条目 + 任意选项"""
    print(f"\n{'='*30}")
    print(f"  {title}")
    print(f"{'='*30}")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    if options.get("show_total"):
        print(f"  总计：{len(items)}项")
    if options.get("author"):
        print(f"  作者：{options['author']}")

create_report("购物清单", "牛奶", "面包", "鸡蛋", 
              show_total=True, author="小明")
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | 默认参数 | 不传就用默认值，传了就用传的 |
| 2 | 关键字参数 | 写名字传参，可以不按顺序 |
| 3 | `*args` | 收任意个位置参数，打包成元组 |
| 4 | `**kwargs` | 收任意个关键字参数，打包成字典 |
| 5 | 参数顺序 | `普通 → *args → 默认 → **kwargs` |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出运行结果**
```python
def test(a, b=10, *args):
    print(a, b, args)

test(1)                 # ______
test(1, 2, 3, 4, 5)     # ______
```

**题2：补全函数**
```python
# 写一个函数，可以接收任意数量的成绩，返回平均分
def average(______):
    return sum(______) / len(______)

print(average(85, 90, 78, 92))   # 86.25
```

---

### 【进阶实操题】

**题3：智能打印函数**
写一个函数 `smart_print(*items, sep=", ", end="\n")`，功能类似print但能按自定义分隔符和结尾符输出。用到默认参数和*args。

**题4：学生信息录入系统**
写一个函数 `add_student(**info)`，接收任意学生信息，把它添加到全局的`students`列表中。然后再写一个`find_student(name)`函数按姓名查找。

---

### 【拓展思考题】

**题5：用*args和**kwargs写一个"数学计算器"函数**
`calculate(operation, *args, **options)`：operation可以是"sum"、"product"、"average"；options可以包含`precision=2`（保留几位小数）、`absolute=True`（是否取绝对值）等。根据参数灵活处理。

---

> 🎉 掌握了灵活的函数参数，你写出的代码会更优雅！
