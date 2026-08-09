# Day 26：字符串进阶——格式化、切割与拼接

---

## 🎯 本节课学习目标

- 掌握字符串切割（split）和拼接（join）
- 学会多种字符串格式化方法
- 处理现实中的文本数据

---

## 📖 知识点讲解

### 1. 切割 split() —— 把字符串拆成列表

```python
"苹果,香蕉,橘子".split(",")       → ["苹果", "香蕉", "橘子"]
"Hello World Python".split()     → ["Hello", "World", "Python"]  默认按空格切
```

### 2. 拼接 join() —— 把列表合成字符串

```python
",".join(["苹果", "香蕉", "橘子"])     → "苹果,香蕉,橘子"
" ".join(["Hello", "World"])          → "Hello World"
```

### 3. 三种字符串格式化方法

```python
# 方法1：f-string（推荐！Python 3.6+）
name, age = "小明", 18
f"{name}今年{age}岁"

# 方法2：.format()
"{}今年{}岁".format(name, age)

# 方法3：% 格式化（老方法，了解即可）
"%s今年%d岁" % (name, age)
```

---

## 💻 课堂演示代码

```python
# ========== 切割 split() ==========

text = "北京,上海,广州,深圳"
cities = text.split(",")
print("按逗号切割：", cities)        # ["北京","上海","广州","深圳"]

sentence = "Python 是一门 优雅的 语言"
words = sentence.split()            # 默认按空白字符（空格、换行等）切割
print("按空格切割：", words)

data = "2024-01-15"
parts = data.split("-")             # 按"-"切割
print(f"年：{parts[0]}，月：{parts[1]}，日：{parts[2]}")

# ========== 拼接 join() ==========

words = ["我", "爱", "Python"]
result = "".join(words)             # 无分隔符拼接
print("直接拼：", result)            # 我爱Python

result = "❤".join(words)            # 用爱心连接
print("爱心拼：", result)            # 我❤爱❤Python

# 实用：把列表转成字符串显示
scores = [85, 92, 78, 95]
# str(85) 等需要先转成字符串
score_str = ", ".join(str(s) for s in scores)
print("成绩列表：", score_str)       # 85, 92, 78, 95

# ========== 格式化输出对比 ==========

name = "小明"
age = 18
score = 95.567

# f-string（最推荐）
print(f"姓名：{name}，年龄：{age}，成绩：{score:.1f}")

# format()
print("姓名：{}，年龄：{}，成绩：{:.1f}".format(name, age, score))

# 对齐和填充
print(f"|{'姓名':<6}|{'年龄':<6}|{'成绩':<6}|")   # 左对齐
print(f"|{name:<6}|{age:<6}|{score:<6.1f}|")

# 补零
num = 7
print(f"编号：{num:03d}")            # 输出：编号：007

# ========== 字符串替换与清理 ==========

text = "  Hello  World  \n"
print("原始：", repr(text))          # 显示原始字符（包括空格和换行）
print("去空格：", repr(text.strip()))

old_text = "我的电话是138-1234-5678"
new_text = old_text.replace("-", "")  # 去掉所有"-"
print("去横线：", new_text)

# 批量替换
dirty = "Python  is  SO  cool!!"
# 多余空格替换成单个空格
clean = " ".join(dirty.split())
print("清理后：", clean)
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | `.split("分隔符")` | 字符串→列表，按分隔符拆开 |
| 2 | `"分隔符".join(列表)` | 列表→字符串，用分隔符拼起来 |
| 3 | f-string | `f"文字{变量}文字"`，最推荐 |
| 4 | `:.1f` | 保留1位小数 |
| 5 | `:<6` | 左对齐，占6个字符宽度 |
| 6 | `:03d` | 整数补零到3位 |
| 7 | `.strip()` | 去掉头尾空格和换行 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：写出运行结果**
```python
s = "a,b,c,d,e"
print(s.split(","))          # ______
print("-".join(["1","2","3"]))  # ______
print(f"{100:.2f}")          # ______
```

**题2：填空——把句子每个单词首字母大写**
```python
sentence = "hello world python"
words = sentence.______()            # 切成单词列表
capitalized = [w.capitalize() for w in words]
result = " ".______(capitalized)     # 拼回句子
print(result)                        # Hello World Python
```

---

### 【进阶实操题】

**题3：CSV数据解析器**
CSV是一种用逗号分隔的数据格式。给一个字符串 `"张三,25,北京,工程师\n李四,30,上海,设计师"`，解析成结构化的列表，并格式化输出表格。提示：先按`\n`切行，再按`,`切列。

**题4：名字格式统一器**
用户输入一个包含多个名字的字符串（用逗号或空格分隔），程序自动去掉多余空格，每个名字的首字母大写，然后按字母顺序排列输出。

---

### 【拓展思考题】

**题5：简易Markdown表格生成器**
让用户输入表头和数据行（用逗号分隔），然后生成一个Markdown格式的表格。例如输入表头"姓名,年龄,城市"和数据行"张三,25,北京"，输出对齐的Markdown表格。

---

> 🎉 字符串处理是实际工作中使用频率最高的技能！
