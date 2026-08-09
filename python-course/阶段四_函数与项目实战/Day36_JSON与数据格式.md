# Day 36：JSON与数据格式——让数据结构化的艺术

---

## 🎯 本节课学习目标

- 理解JSON是什么、为什么用它
- 学会用 `json` 模块保存和读取Python数据
- 为项目实战提供专业的存储方案

---

## 📖 知识点讲解

### 1. 什么是JSON？

JSON（念作"杰森"）是一种**数据交换格式**。它用文本表示结构化数据，人和机器都能轻松读懂。

```json
{
    "姓名": "小明",
    "年龄": 18,
    "爱好": ["编程", "篮球", "音乐"],
    "地址": {
        "城市": "北京",
        "区": "朝阳区"
    }
}
```

这看起来像Python字典？没错！JSON和Python的字典/列表几乎一一对应，所以非常好用。

### 2. 为什么用JSON而不是自己拼字符串？

- ✅ 有标准格式，不会出错
- ✅ Python自带 `json` 模块，一行代码保存，一行代码读取
- ✅ 支持嵌套结构（字典套列表套字典）
- ✅ 几乎所有编程语言都支持JSON

### 3. json模块核心操作

```python
import json

# Python对象 → JSON字符串
json.dumps(数据)              # 转成JSON字符串
json.dump(数据, 文件对象)     # 直接写入文件

# JSON字符串 → Python对象
json.loads(json字符串)        # 从字符串解析
json.load(文件对象)           # 从文件读取并解析
```

---

## 💻 课堂演示代码

```python
import json

# ========== Python对象 → JSON ==========

# 复杂数据结构
data = {
    "app_name": "记账本",
    "version": "1.0",
    "records": [
        {"type": "收入", "amount": 5000, "category": "工资", "date": "2026-01-15"},
        {"type": "支出", "amount": 35, "category": "餐饮", "date": "2026-01-15"},
        {"type": "支出", "amount": 200, "category": "购物", "date": "2026-01-16"},
    ],
    "settings": {
        "currency": "CNY",
        "theme": "dark"
    }
}

# 转成JSON字符串（美化格式）
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print("=== JSON字符串 ===")
print(json_str)

# ensure_ascii=False：保证中文正常显示，不变成\uXXX
# indent=2：缩进2格，让JSON好看

# ========== JSON字符串 → Python对象 ==========

json_text = '{"name": "张三", "age": 25, "skills": ["Python", "Java"]}'
person = json.loads(json_text)
print(f"\n解析后：{person['name']}，{person['age']}岁，会{person['skills']}")

# ========== 写入JSON文件 ==========

# 保存到文件
with open("记账数据.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("\n✅ 数据已保存到 记账数据.json")

# 从文件读取
with open("记账数据.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
print(f"✅ 读取成功！共{len(loaded_data['records'])}条记录")

# ========== 实战：用JSON改造通讯录 ==========

CONTACTS_FILE = "通讯录.json"

def load_contacts():
    """从JSON文件加载通讯录"""
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []    # 文件不存在，返回空列表

def save_contacts(contacts):
    """保存通讯录到JSON文件"""
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def add_contact():
    contacts = load_contacts()
    name = input("姓名：")
    phone = input("电话：")
    email = input("邮箱：")
    contacts.append({"姓名": name, "电话": phone, "邮箱": email})
    save_contacts(contacts)
    print("✅ 联系人已保存！")

def show_contacts():
    contacts = load_contacts()
    if not contacts:
        print("通讯录为空")
        return
    for i, c in enumerate(contacts, 1):
        print(f"{i}. {c['姓名']} - {c['电话']} - {c['邮箱']}")

# 测试
# add_contact()
# show_contacts()
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | JSON | 用文本表示结构化数据的标准格式 |
| 2 | `json.dump(obj, f)` | Python对象写入文件 |
| 3 | `json.load(f)` | 从文件读取并还原Python对象 |
| 4 | `ensure_ascii=False` | 保证中文正常显示 |
| 5 | `indent=2` | 美化输出，带缩进 |
| 6 | JSON ↔ Python | dict→`{}`, list→`[]`, str→`""`, int→数字 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：填空**
```python
import json
data = {"name": "test", "score": 95}

# 把data转成JSON字符串
text = json.______(data, ensure_ascii=False)

# 把JSON字符串还原
restored = json.______(text)
```

**题2：写出下面JSON对应的Python数据结构**
```json
[{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
```

---

### 【进阶实操题】

**题3：用JSON改造记账本**
将Day30/35的记账本程序改用JSON存储。程序启动时自动加载JSON文件，退出时自动保存。需要处理文件不存在的情况。

**题4：考试题库系统**
用JSON文件存储选择题题库（题干、选项A/B/C/D、正确答案）。程序随机出5道题，用户作答后打分并显示错题。

---

### 【拓展思考题】

**题5：配置管理系统**
写一个程序，用JSON文件存储软件配置（语言、主题、字体大小等）。支持：查看当前配置、修改某项配置、恢复默认配置。程序启动时自动加载配置。

---

> 🎉 JSON是程序间数据交换的通用语言，学会它如虎添翼！
