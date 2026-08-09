# Day 38：Python标准库与第三方库入门

---

## 🎯 本节课学习目标

- 了解Python自带的有用模块（标准库）
- 学会用 `pip` 安装第三方库
- 用几个实用库提升程序品质

---

## 📖 知识点讲解

### 1. Python标准库——藏在宝库里的工具

Python安装时自带了很多模块，不需要额外安装。你已经用过：
- `random` —— 随机数
- `json` —— JSON处理
- `os` —— 操作系统相关
- `datetime` —— 日期时间

还有更多宝藏：

| 模块 | 功能 | 例子 |
|------|------|------|
| `csv` | 读写CSV表格文件 | 导出Excel能打开的表格 |
| `datetime` | 日期时间处理 | 计算两个日期差几天 |
| `collections` | 高级容器 | `Counter`一键统计 |
| `pathlib` | 路径处理 | 创建文件夹、遍历文件 |
| `argparse` | 命令行参数 | 给程序加启动选项 |

### 2. pip —— Python的应用商店

`pip` 是Python的包管理工具，能下载安装别人写好的库。

```bash
# 在终端（cmd）里运行
pip install 库名       # 安装
pip list               # 查看已安装的库
pip uninstall 库名     # 卸载
```

### 3. 推荐的入门第三方库

| 库 | 用途 | 安装命令 |
|------|------|----------|
| `rich` | 美化终端输出（彩色、表格、进度条） | `pip install rich` |
| `tabulate` | 把列表/字典变成漂亮表格 | `pip install tabulate` |
| `pyinstaller` | 把Python程序打包成exe | `pip install pyinstaller` |

---

## 💻 课堂演示代码

```python
# ========== datetime 时间处理 ==========
from datetime import datetime, timedelta

# 当前时间
now = datetime.now()
print("现在：", now.strftime("%Y年%m月%d日 %H:%M:%S"))

# 计算时间差
birthday = datetime(2000, 1, 1)
days_alive = (now - birthday).days
print(f"从2000年1月1日到现在已经过了{days_alive}天")

# 90天后是什么日期
future = now + timedelta(days=90)
print(f"90天后：{future.strftime('%Y-%m-%d')}")

# ========== csv 表格处理 ==========
import csv

# 写入CSV
data = [
    ["姓名", "年龄", "城市"],
    ["张三", "25", "北京"],
    ["李四", "30", "上海"],
    ["王五", "28", "广州"],
]
with open("output.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerows(data)
print("✅ CSV文件已生成（可用Excel打开）")

# 读取CSV
with open("output.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    for row in reader:
        print(" | ".join(row))

# ========== collections.Counter 计数器 ==========
from collections import Counter

words = ["apple", "banana", "apple", "orange", "banana", "apple"]
count = Counter(words)
print("\n词频统计：", count)
print("最多的是：", count.most_common(2))   # 前2名

# ========== pathlib 路径操作 ==========
from pathlib import Path

# 创建文件夹（不存在才创建）
data_dir = Path("./我的数据")
data_dir.mkdir(exist_ok=True)    # exist_ok=True 已存在也不报错

# 列出某文件夹下所有.txt文件
txt_files = list(Path(".").glob("*.py"))
print(f"\n当前目录有{len(txt_files)}个.py文件")

# ========== os 系统操作 ==========
import os

print(f"当前工作目录：{os.getcwd()}")
print(f"Python版本：{os.sys.version}")

# 检查文件是否存在
if os.path.exists("output.csv"):
    size = os.path.getsize("output.csv")
    print(f"output.csv 大小：{size}字节")
```

---

## 📝 本节课核心知识点总结

| 序号 | 知识点 | 一句话记忆 |
|------|--------|------------|
| 1 | 标准库 | Python自带的工具集，直接import用 |
| 2 | `pip install` | 在终端运行，安装第三方库 |
| 3 | `datetime` | 处理日期和时间 |
| 4 | `csv` | 读写Excel兼容的表格文件 |
| 5 | `Counter` | 一键统计元素出现次数 |
| 6 | `Path` | 现代化文件和路径操作 |

---

## ✅ 今日课后习题

### 【基础巩固题】

**题1：** 用 `datetime` 计算你出生到现在过了多少天。

**题2：** 用 `csv` 模块把通讯录数据导出为CSV格式。

---

### 【进阶实操题】

**题3：用Counter分析文本**
读取一个文本文件，用 `Counter` 统计所有单词的出现频率，输出前10个高频词。

**题4：文件整理器**
写一个程序，扫描当前目录的所有文件，按扩展名分类放入不同的文件夹。比如把所有 `.txt` 放入"文本文件"文件夹，`.jpg` 放入"图片文件夹"。（用 `pathlib` 和 `os`）

---

### 【拓展思考题】

**题5：把Python程序打包成exe**
用 `pyinstaller` 把你之前写的猜数字游戏打包成exe文件，发给朋友玩。命令：`pyinstaller --onefile your_game.py`

---

> 🎉 Python的海量库是你解决问题的弹药库！
