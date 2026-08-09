# Day 35：文件读写——让数据永久保存

---

## 🎯 本节课学习目标

- 理解为什么要读写文件
- 学会用 `open()` 打开、读取、写入文件
- 掌握 `with` 语句安全操作文件

---

## 📖 知识点讲解

### 1. 为什么需要文件读写？

之前写的所有程序，数据都存在内存里。关掉程序，数据就没了。**文件读写让数据可以"持久化"**——写到硬盘上的文件里，下次打开程序还能读到。

**生活类比：** 
- 程序内存 = 草稿纸（用完就扔）
- 文件读写 = 笔记本（写下来，明天还能看）

### 2. 文件操作三步走

```
① 打开文件  →  open("文件名", "模式")
② 读写操作  →  .read() / .write() / .readlines()
③ 关闭文件  →  .close()（或用with自动关闭）
```

### 3. 文件模式

| 模式 | 含义 | 说明 |
|------|------|------|
| `"r"` | 只读 | 文件必须存在，只能看不能写 |
| `"w"` | 写入 | 文件不存在就创建，**存在就清空再写！** |
| `"a"` | 追加 | 文件不存在就创建，存在就在末尾接着写 |
| `"r+"` | 读写 | 文件必须存在，可读可写 |

### 4. with语句 —— 最推荐的方式

```python
with open("文件.txt", "r", encoding="utf-8") as f:
    content = f.read()    # with代码块结束，自动关闭文件
# 不需要手动close！
```

---

## 💻 课堂演示代码

```python
# ========== 写入文件 ==========

# 写模式：会覆盖原有内容
with open("日记.txt", "w", encoding="utf-8") as f:
    f.write("今天是学Python的第35天\n")
    f.write("今天学习文件读写，很有意思！\n")
    f.write("坚持下去，加油！💪\n")

print("✅ 日记写入成功！")

# 追加模式：不会覆盖，加在末尾
with open("日记.txt", "a", encoding="utf-8") as f:
    f.write("晚上又复习了一遍，更熟练了。\n")

# ========== 读取文件 ==========

# 一次性读取全部内容
with open("日记.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("=== 文件内容 ===")
    print(content)

# 按行读取
print("=== 按行读取 ===")
with open("日记.txt", "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        print(f"第{line_num}行：{line.strip()}")

# 读取所有行到一个列表
with open("日记.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(f"总共{len(lines)}行")

# ========== 实用：把数据保存到文件 ==========

# 保存列表数据
shopping_list = ["牛奶", "面包", "鸡蛋", "苹果", "洗衣液"]
with open("购物清单.txt", "w", encoding="utf-8") as f:
    for item in shopping_list:
        f.write(item + "\n")       # 每行一个
print("✅ 购物清单已保存")

# 读回来
loaded_list = []
with open("购物清单.txt", "r", encoding="utf-8") as f:
    for line in f:
        loaded_list.append(line.strip())   # strip()去掉换行符
print("读取的清单：", loaded_list)

# ========== 保存字典数据（简易版）==========

contacts = [
    {"姓名": "张三", "电话": "13800001111"},
    {"姓名": "李四", "电话": "13800002222"},
]

# 保存为CSV格式
with open("通讯录.csv", "w", encoding="utf-8") as f:
    f.write("姓名,电话\n")           # 表头
    for c in contacts:
        f.write(f"{c['姓名']},{c['电话']}\n")

print("✅ 通讯录已保存为CSV文件")

# ========== 文件不存在的处理 ==========

try:
    with open("不存在的文件.txt", "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("⚠️ 文件不存在，创建新文件")
    with open("不存在的文件.txt", "w", encoding="utf-8") as f:
        f.write("这是新建的文件\n")
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `open("文件名","模式")` | 打开文件，r读w写a追加 |
| 2 | `with...as f:` | 自动关闭文件，最推荐的方式 |
| 3 | `encoding="utf-8"` | 指定编码，处理中文必须加 |
| 4 | `.read()` | 一次性读取全部内容 |
| 5 | `.write("内容")` | 把字符串写入文件 |
| 6 | `w` 模式 | 会覆盖原文件内容，慎用！ |
| 7 | `a` 模式 | 追加到文件末尾，不覆盖 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：填空——读取文件并打印**
```python
with ______("data.txt", "______", encoding="utf-8") as f:
    content = f.______()
    print(content)
```

**题2：判断对错**
- `"w"` 模式打开文件，如果文件已存在会报错（ ）
- `with` 语句结束后会自动关闭文件（ ）
- 读写中文文件时可以不写 `encoding="utf-8"`（ ）

---

### 【进阶实操题】

**题3：日记本程序**
写一个简易日记本程序：每次运行时让用户输入今天的日记内容，自动加上日期，追加保存到 `日记本.txt` 文件中。还要支持查看历史日记功能。

**题4：记账本数据持久化**
修改Day30的记账本程序，把账目记录保存到文件中。程序启动时从文件读取，添加记录后自动保存。提示：可以用CSV格式存储。

---

### 【拓展思考题】

**题5：简易数据库**
用文件模拟一个简易的键值数据库。支持 `set(key, value)` 存数据、`get(key)` 取数据、`delete(key)` 删数据、`list_keys()` 列出所有键。数据保存在一个文本文件中，每条记录一行。

---

> 🎉 学会文件操作，你的程序终于有了"记忆"！
