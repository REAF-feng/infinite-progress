# Day 29：容器综合练习——五道经典实战题

---

## 🎯 本节课学习目标

- 通过5道综合题巩固列表、字典、字符串操作
- 锻炼独立分析问题、写出完整代码的能力

---

## 💻 练习1：通讯录CRUD完整版

写一个通讯录管理系统，支持增删改查。

```python
contacts = []  # 列表套字典

def add_contact():
    name = input("姓名：")
    phone = input("电话：")
    email = input("邮箱：")
    contacts.append({"name": name, "phone": phone, "email": email})
    print("✅ 添加成功！")

def find_contact(name):
    for c in contacts:
        if c["name"] == name:
            return c
    return None

def delete_contact():
    name = input("输入要删除的联系人姓名：")
    c = find_contact(name)
    if c:
        contacts.remove(c)
        print("✅ 删除成功！")
    else:
        print("❌ 未找到该联系人")

def show_all():
    if not contacts:
        print("通讯录为空")
        return
    print(f"\n{'姓名':<8}{'电话':<15}{'邮箱':<20}")
    print("-" * 43)
    for c in contacts:
        print(f"{c['name']:<8}{c['phone']:<15}{c['email']:<20}")

# 主循环
while True:
    print("\n1.添加 2.删除 3.查找 4.显示全部 0.退出")
    choice = input("请选择：")
    if choice == "0": break
    elif choice == "1": add_contact()
    elif choice == "2": delete_contact()
    elif choice == "3":
        name = input("输入姓名：")
        c = find_contact(name)
        print(c if c else "未找到")
    elif choice == "4": show_all()
```

---

## 💻 练习2：英文词频统计器

```python
text = """The quick brown fox jumps over the lazy dog.
The dog was not happy about the fox jumping over him."""

# 全部小写，去掉标点，切词
for ch in ".,!?\n'\"":
    text = text.replace(ch, "")
words = text.lower().split()

# 统计
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1

# 按频率排序
sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
for word, count in sorted_words[:5]:  # 取前5
    print(f"{word}: {count}")
```

---

## 💻 练习3：按条件过滤和分组

```python
students = [
    {"name": "张三", "class": "A", "score": 85},
    {"name": "李四", "class": "B", "score": 92},
    {"name": "王五", "class": "A", "score": 78},
    {"name": "赵六", "class": "B", "score": 88},
    {"name": "孙七", "class": "A", "score": 95},
    {"name": "周八", "class": "C", "score": 70},
]

# 按班级分组
by_class = {}
for s in students:
    cls = s["class"]
    if cls not in by_class:
        by_class[cls] = []
    by_class[cls].append(s)

# 每个班按成绩排序并显示
for cls, stu_list in by_class.items():
    stu_list.sort(key=lambda s: s["score"], reverse=True)
    print(f"\n{cls}班排名：")
    for i, s in enumerate(stu_list, 1):
        print(f"  {i}. {s['name']} {s['score']}分")

# 找出每个班最高分
print("\n各班最高分：")
for cls, stu_list in by_class.items():
    best = max(stu_list, key=lambda s: s["score"])
    print(f"  {cls}班：{best['name']} ({best['score']}分)")
```

---

## 💻 练习4：两个列表合并去重排序

```python
list_a = [3, 1, 5, 7, 5, 3]
list_b = [2, 8, 1, 9, 2, 5]

# 方法：转集合去重，取并集，排序
result = sorted(set(list_a) | set(list_b))
print("合并去重排序：", result)

# 找出只在一边出现的元素
only_a = set(list_a) - set(list_b)
only_b = set(list_b) - set(list_a)
print("只在A中：", only_a)
print("只在B中：", only_b)
```

---

## 💻 练习5：银行账户管理系统

```python
accounts = {
    "1001": {"name": "张三", "balance": 10000, "pin": "1234"},
    "1002": {"name": "李四", "balance": 5000, "pin": "5678"},
}

# 登录
acc_id = input("账号：")
pin = input("密码：")

if acc_id not in accounts or accounts[acc_id]["pin"] != pin:
    print("账号或密码错误")
else:
    acc = accounts[acc_id]
    print(f"欢迎{acc['name']}，余额{acc['balance']}元")
    
    while True:
        print("\n1.存款 2.取款 3.查余额 0.退出")
        choice = input("请选择：")
        
        if choice == "0":
            print("再见！")
            break
        elif choice == "1":
            amount = float(input("存款金额："))
            if amount > 0:
                acc["balance"] += amount
                print(f"存款成功，余额{acc['balance']}元")
        elif choice == "2":
            amount = float(input("取款金额："))
            if 0 < amount <= acc["balance"]:
                acc["balance"] -= amount
                print(f"取款成功，余额{acc['balance']}元")
            else:
                print("余额不足或金额无效")
        elif choice == "3":
            print(f"当前余额：{acc['balance']}元")
```

---

## ✅ 今日课后习题

独立完成以上5道练习题，确保每道题都能默写出来。遇到卡壳的地方，就是你的薄弱点，回去复习对应章节。

---

> 🎉 这5道题覆盖了阶段三的核心知识点，搞定它们就去挑战测评吧！
