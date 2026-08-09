# Day 27：综合应用——用容器解决真实数据处理问题

---

## 🎯 本节课学习目标

- 综合运用列表、字典、字符串处理实际数据
- 学会"获取数据→清洗→分析→输出结果"的完整流程
- 为阶段三项目做准备

---

## 💻 案例1：成绩分析系统

```python
# 原始数据：一行一个学生，格式"姓名,语文,数学,英语"
raw_data = """张三,85,92,78
李四,90,88,95
王五,76,82,70
赵六,95,91,89
孙七,68,75,72
周八,88,85,90"""

# === 第一步：解析数据 ===
students = []
lines = raw_data.strip().split("\n")    # 按换行符切成多行
for line in lines:
    parts = line.split(",")             # 每行按逗号切
    student = {
        "姓名": parts[0],
        "语文": int(parts[1]),
        "数学": int(parts[2]),
        "英语": int(parts[3]),
    }
    # 计算总分和平均分
    student["总分"] = student["语文"] + student["数学"] + student["英语"]
    student["平均分"] = round(student["总分"] / 3, 1)
    students.append(student)

# === 第二步：统计分析 ===
# 按总分排序
students.sort(key=lambda s: s["总分"], reverse=True)

# 各科平均分
avg_chinese = sum(s["语文"] for s in students) / len(students)
avg_math = sum(s["数学"] for s in students) / len(students)
avg_english = sum(s["英语"] for s in students) / len(students)

# 找出各科最高分
top_chinese = max(students, key=lambda s: s["语文"])
top_math = max(students, key=lambda s: s["数学"])
top_english = max(students, key=lambda s: s["英语"])

# === 第三步：输出结果 ===
print("=" * 50)
print("              成绩分析报告")
print("=" * 50)
print(f"{'排名':<4}{'姓名':<6}{'语文':<6}{'数学':<6}{'英语':<6}{'总分':<6}{'平均分'}")
print("-" * 50)
for i, s in enumerate(students):
    print(f"{i+1:<4}{s['姓名']:<6}{s['语文']:<6}{s['数学']:<6}{s['英语']:<6}{s['总分']:<6}{s['平均分']}")
print("-" * 50)
print(f"班级平均分——语文：{avg_chinese:.1f}  数学：{avg_math:.1f}  英语：{avg_english:.1f}")
print(f"单科最高——语文：{top_chinese['姓名']}({top_chinese['语文']})  "
      f"数学：{top_math['姓名']}({top_math['数学']})  "
      f"英语：{top_english['姓名']}({top_english['英语']})")

# 统计不及格情况（<60分）
print()
print("=== 不及格情况 ===")
for s in students:
    fail_subjects = []
    if s["语文"] < 60:
        fail_subjects.append("语文")
    if s["数学"] < 60:
        fail_subjects.append("数学")
    if s["英语"] < 60:
        fail_subjects.append("英语")
    if fail_subjects:
        print(f"{s['姓名']}：{', '.join(fail_subjects)}不及格")
```

---

## 💻 案例2：词频统计

```python
# 统计一段文字中每个词出现的次数
article = """
Python is an amazing programming language.
Python is easy to learn and powerful to use.
Many people love Python because of its simplicity.
"""

# 清洗并切词
words = article.lower()              # 全部转小写
# 去掉标点符号
for ch in ".,!?\n":
    words = words.replace(ch, " ")
word_list = words.split()            # 按空格切

# 统计词频
word_count = {}
for word in word_list:
    word_count[word] = word_count.get(word, 0) + 1

# 按频率排序输出
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
print("词频统计：")
for word, count in sorted_words:
    print(f"  {word:<15} {count}次")
```

---

## 💻 案例3：购物车结算系统

```python
# 商品库
products = {
    "A001": {"name": "Python入门书", "price": 59.0},
    "A002": {"name": "机械键盘", "price": 299.0},
    "A003": {"name": "鼠标", "price": 89.0},
    "A004": {"name": "显示器", "price": 1299.0},
    "A005": {"name": "U盘64G", "price": 49.0},
}

cart = []   # 购物车，列表里放{商品ID, 数量}

# 模拟购物流程
while True:
    print("\n=== 商品列表 ===")
    for pid, info in products.items():
        print(f"  {pid} - {info['name']} - ¥{info['price']}")
    print("  输入'结算'完成购物，输入'q'退出")

    choice = input("请输入商品编号：")
    if choice == "q":
        break
    if choice == "结算":
        if not cart:
            print("购物车是空的！")
            continue
        # 计算总价
        total = 0
        print("\n=== 您的购物小票 ===")
        print(f"{'商品':<15}{'单价':<8}{'数量':<6}{'小计'}")
        for item in cart:
            pid = item["id"]
            qty = item["qty"]
            info = products[pid]
            subtotal = info["price"] * qty
            total = total + subtotal
            print(f"{info['name']:<15}¥{info['price']:<7}{qty:<6}¥{subtotal:.1f}")
        print(f"{'':->40}")
        print(f"总价：¥{total:.2f}")
        break

    if choice in products:
        qty = int(input("请输入数量："))
        cart.append({"id": choice, "qty": qty})
        print(f"已添加 {products[choice]['name']} × {qty}")
    else:
        print("商品编号不存在！")
```

---

## 📝 数据处理通用流程

```
原始数据 → 解析（split/切分） → 结构化（存到列表/字典）
         → 清洗（去空格/转类型/去重）
         → 分析（统计/排序/筛选）
         → 展示（格式化输出/生成表格）
```

---

## ✅ 今日课后习题

### 【进阶实操题】

**题1：** 修改案例1的成绩分析系统，增加功能：找出进步最大的学生（假设有两次考试数据）。

**题2：** 独立完成一个"月度支出统计器"：用列表套字典记录每天的各项支出（日期、类别、金额、备注），然后按类别汇总、按日期汇总、计算总支出。

---

> 🎉 学到这里，你已经具备了用Python处理真实数据的能力！
